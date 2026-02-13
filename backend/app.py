from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import settings
from backend.services.model_service import run_model_test
from backend.services import db_service
from typing import Optional
import os

app = FastAPI(title="SAP Enterprise AI Assistant", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    """Seed the database with test data if empty"""
    # Check if we have any users
    db = db_service.SessionLocal()
    try:
        user_count = db.query(db_service.User).count()
        if user_count == 0:
            # Create users
            alice = db_service.create_user("Alice Smith", "Sales Manager", "Sales", "alice@sap.com", "password123")
            bob = db_service.create_user("Bob Jones", "Regional Director", "Sales", "bob@sap.com", "password123")
            charlie = db_service.create_user("Charlie Day", "Data Analyst", "IT", "charlie@sap.com", "password123")
            abby = db_service.create_user("Abby Nayaraj", "Data Analyst", "IT", "abbynayaraj@gmail.com", "password123")
            
            # Create a public conversation
            conv = db_service.create_conversation(alice["user_id"], "Q4 Sales Analysis", "public")
            
            # Add queries
            q1 = db_service.create_query(conv["conversation_id"], alice["user_id"], "What are the Q4 sales trends?")
            db_service.create_insight(q1["query_id"], "📊 **Q4 Sales Analysis**\n\nSales increased by 15% compared to Q3. The North region led with 25% growth.")
            
            # Add comment
            db_service.create_comment(conv["conversation_id"], bob["user_id"], "Great insights! Let's focus on the North region strategy for next year.")
            
            print(f"Seeded database. Alice ID: {alice['user_id']}")
    finally:
        db.close()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
def serve_frontend():
    """Serve the frontend HTML"""
    frontend_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend not found"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "environment": settings.app_env}


@app.get("/api/model-test")
def model_test() -> dict:
    return run_model_test()


@app.post("/api/analyze")
def analyze(request: dict) -> dict:
    """Analyze a business query using AI"""
    query = request.get("query", "").strip()
    
    if not query:
        return {
            "status": "error",
            "analysis": "Please provide a query to analyze.",
            "query": ""
        }
    
    from backend.services.model_service import analyze_business_query
    return analyze_business_query(query)


# ============================================
# USER MANAGEMENT ENDPOINTS
# ============================================

@app.post("/api/users")
def create_user(request: dict) -> dict:
    """Create a new user"""
    try:
        user = db_service.create_user(
            name=request["name"],
            role=request["role"],
            department=request.get("department", "General"),
            email=request["email"]
        )
        return {"status": "success", "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/login")
def login(request: dict) -> dict:
    """Login a user"""
    email = request.get("email")
    password = request.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
        
    user = db_service.validate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {"status": "success", "user": user}


@app.get("/api/users/{user_id}")
def get_user(user_id: str) -> dict:
    """Get user by ID"""
    user = db_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "user": user}


# ============================================
# CONVERSATION MANAGEMENT ENDPOINTS
# ============================================

@app.post("/api/conversations/quick-analyze")
def quick_analyze(request: dict) -> dict:
    """Consolidated endpoint for faster analysis (Atomic: Create Conv -> Create Query -> Get Insight)"""
    try:
        user_id = request["user_id"]
        question = request["question"]
        title = request.get("title", question[:30] + "...")
        visibility = request.get("visibility", "department")
        
        # 1. Create Conversation
        conversation = db_service.create_conversation(user_id, title, visibility)
        conv_id = conversation["conversation_id"]
        
        # 2. Create Query
        query = db_service.create_query(conv_id, user_id, question)
        
        # 3. Get AI Insight
        from backend.services.model_service import analyze_business_query
        ai_response = analyze_business_query(question)
        
        # 4. Store Insight
        db_service.create_insight(query["query_id"], ai_response.get("analysis", ""))
        
        # 5. Return full detail (simulating GET /api/conversations/{id} but faster)
        # We fetch fresh to ensure all relationships/counts are correct
        full_data = get_conversation(conv_id)
        return full_data
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/conversations")
def create_conversation(request: dict) -> dict:
    """Create a new conversation"""
    try:
        conversation = db_service.create_conversation(
            user_id=request["user_id"],
            title=request.get("title", "Untitled Conversation"),
            visibility=request.get("visibility", "department")
        )
        return {"status": "success", "conversation": conversation}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/conversations/{conversation_id}")
def get_conversation(conversation_id: str) -> dict:
    """Get conversation details with queries and insights"""
    conversation = db_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get related data
    queries = db_service.get_conversation_queries(conversation_id)
    
    # Enrich queries with insights
    for query in queries:
        insight = db_service.get_query_insight(query["query_id"])
        query["insight"] = insight
    
    comments = db_service.get_conversation_comments(conversation_id)
    reactions = db_service.get_conversation_reactions(conversation_id)
    
    # Enrich comments with user info
    for comment in comments:
        user = db_service.get_user(comment["user_id"])
        comment["user"] = user
    
    return {
        "status": "success",
        "conversation": conversation,
        "queries": queries,
        "comments": comments,
        "reactions": reactions
    }


@app.get("/api/conversations")
def get_conversations(
    user_id: str = Query(..., description="Current user ID"),
    department: Optional[str] = Query(None, description="User's department"),
    view: str = Query("all", description="'my' or 'all' conversations")
) -> dict:
    """Get conversations visible to the user"""
    if view == "my":
        conversations = db_service.get_user_conversations(user_id)
    else:
        conversations = db_service.get_shared_conversations(user_id, department)
    
    # Enrich with counts
    for conv in conversations:
        conv["comment_count"] = len(db_service.get_conversation_comments(conv["conversation_id"]))
        conv["query_count"] = len(db_service.get_conversation_queries(conv["conversation_id"]))
    
    return {"status": "success", "conversations": conversations}


@app.patch("/api/conversations/{conversation_id}")
def update_conversation(conversation_id: str, request: dict) -> dict:
    """Update conversation status"""
    try:
        status = request.get("status")
        if status:
            conversation = db_service.update_conversation_status(conversation_id, status)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            return {"status": "success", "conversation": conversation}
        return {"status": "error", "message": "No updates provided"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# QUERY & INSIGHT ENDPOINTS
# ============================================

@app.post("/api/conversations/{conversation_id}/queries")
def create_query(conversation_id: str, request: dict) -> dict:
    """Create a query and get AI insight"""
    try:
        # Create the query
        query = db_service.create_query(
            conversation_id=conversation_id,
            user_id=request["user_id"],
            question=request["question"]
        )
        
        # Get AI analysis
        from backend.services.model_service import analyze_business_query
        ai_response = analyze_business_query(request["question"])
        
        # Store the insight
        insight = db_service.create_insight(
            query_id=query["query_id"],
            response=ai_response.get("analysis", "")
        )
        
        query["insight"] = insight
        return {"status": "success", "query": query}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# COMMENT ENDPOINTS
# ============================================

@app.post("/api/conversations/{conversation_id}/comments")
def add_comment(conversation_id: str, request: dict) -> dict:
    """Add a comment to a conversation"""
    try:
        comment = db_service.create_comment(
            conversation_id=conversation_id,
            user_id=request["user_id"],
            content=request["content"]
        )
        
        # Enrich with user info
        user = db_service.get_user(comment["user_id"])
        comment["user"] = user
        
        return {"status": "success", "comment": comment}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/comments/{comment_id}")
def delete_comment(comment_id: str, user_id: str = Query(...)) -> dict:
    """Delete a comment"""
    success = db_service.delete_comment(comment_id, user_id)
    if not success:
        raise HTTPException(status_code=403, detail="Cannot delete comment")
    return {"status": "success", "message": "Comment deleted"}


# ============================================
# REACTION ENDPOINTS
# ============================================

@app.post("/api/conversations/{conversation_id}/reactions")
def add_reaction(conversation_id: str, request: dict) -> dict:
    """Add or update a reaction to a conversation"""
    try:
        reaction = db_service.add_reaction(
            conversation_id=conversation_id,
            user_id=request["user_id"],
            reaction_type=request["reaction_type"]
        )
        return {"status": "success", "reaction": reaction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/conversations/{conversation_id}/reactions")
def remove_reaction(conversation_id: str, user_id: str = Query(...)) -> dict:
    """Remove a reaction from a conversation"""
    success = db_service.remove_reaction(conversation_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reaction not found")
    return {"status": "success", "message": "Reaction removed"}


@app.get("/api/conversations/{conversation_id}/reactions")
def get_reactions(conversation_id: str) -> dict:
    """Get all reactions for a conversation"""
    reactions = db_service.get_conversation_reactions(conversation_id)
    
    # Count by type
    reaction_counts = {}
    for reaction in reactions:
        rtype = reaction["reaction_type"]
        reaction_counts[rtype] = reaction_counts.get(rtype, 0) + 1
    
    return {
        "status": "success",
        "reactions": reactions,
        "counts": reaction_counts
    }


# ============================================
# SHARE ENDPOINTS
# ============================================

@app.post("/api/conversations/{conversation_id}/share")
def share_conversation(conversation_id: str, request: dict) -> dict:
    """Share a conversation with another user"""
    try:
        share = db_service.share_conversation(
            conversation_id=conversation_id,
            shared_with_user_id=request["shared_with_user_id"],
            permission_level=request.get("permission_level", "view")
        )
        return {"status": "success", "share": share}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/conversations/{conversation_id}/share/{user_id}")
def unshare_conversation(conversation_id: str, user_id: str) -> dict:
    """Remove a share"""
    success = db_service.unshare_conversation(conversation_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Share not found")
    return {"status": "success", "message": "Share removed"}
