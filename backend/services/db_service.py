from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from ..models import Base, User, Conversation, Query, Insight, Comment, Reaction
from passlib.context import CryptContext

# Create tables
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- User Management ---

def create_user(name: str, role: str, department: str, email: str, password: str = "password123") -> dict:
    db = SessionLocal()
    try:
        hashed_password = pwd_context.hash(password)
        db_user = User(
            name=name,
            role=role,
            department=department,
            email=email,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "user_id": db_user.user_id,
            "name": db_user.name,
            "role": db_user.role,
            "department": db_user.department,
            "email": db_user.email,
            "password": db_user.password, # Return hash for internal use/verification
            "created_at": db_user.created_at.isoformat()
        }
    finally:
        db.close()

def validate_user(email: str, password: str) -> Optional[dict]:
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user or not pwd_context.verify(password, db_user.password):
            return None
        return {
            "user_id": db_user.user_id,
            "name": db_user.name,
            "role": db_user.role,
            "department": db_user.department,
            "email": db_user.email
        }
    finally:
        db.close()

def get_user(user_id: str) -> Optional[dict]:
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if not db_user:
            return None
        return {
            "user_id": db_user.user_id,
            "name": db_user.name,
            "role": db_user.role,
            "department": db_user.department,
            "email": db_user.email
        }
    finally:
        db.close()

# --- Conversation Management ---

def create_conversation(user_id: str, title: str, visibility: str = "department") -> dict:
    db = SessionLocal()
    try:
        db_conv = Conversation(
            user_id=user_id,
            title=title,
            visibility=visibility
        )
        db.add(db_conv)
        db.commit()
        db.refresh(db_conv)
        return {
            "conversation_id": db_conv.conversation_id,
            "user_id": db_conv.user_id,
            "title": db_conv.title,
            "visibility": db_conv.visibility,
            "status": db_conv.status,
            "created_at": db_conv.created_at.isoformat()
        }
    finally:
        db.close()

def get_conversation(conversation_id: str) -> Optional[dict]:
    db = SessionLocal()
    try:
        db_conv = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        if not db_conv:
            return None
        return {
            "conversation_id": db_conv.conversation_id,
            "user_id": db_conv.user_id,
            "title": db_conv.title,
            "visibility": db_conv.visibility,
            "status": db_conv.status,
            "created_at": db_conv.created_at.isoformat()
        }
    finally:
        db.close()

def get_user_conversations(user_id: str) -> List[dict]:
    db = SessionLocal()
    try:
        conversations = db.query(Conversation, User.name).join(User, Conversation.user_id == User.user_id).filter(Conversation.user_id == user_id).all()
        return [{
            "conversation_id": c.Conversation.conversation_id,
            "user_id": c.Conversation.user_id,
            "creator_name": c.name,
            "title": c.Conversation.title,
            "visibility": c.Conversation.visibility,
            "status": c.Conversation.status,
            "created_at": c.Conversation.created_at.isoformat()
        } for c in conversations]
    finally:
        db.close()

def get_shared_conversations(user_id: str, department: Optional[str] = None) -> List[dict]:
    db = SessionLocal()
    try:
        # Visibility logic:
        # public: everyone
        # department: same department as creator
        # private/active: creator only
        query = db.query(Conversation, User.name).join(User, Conversation.user_id == User.user_id).filter(
            (Conversation.visibility == "public") | 
            (Conversation.user_id == user_id) |
            ((Conversation.visibility == "department") & (User.department == department))
        )
        conversations = query.all()
        return [{
            "conversation_id": c.Conversation.conversation_id,
            "user_id": c.Conversation.user_id,
            "creator_name": c.name,
            "title": c.Conversation.title,
            "visibility": c.Conversation.visibility,
            "status": c.Conversation.status,
            "created_at": c.Conversation.created_at.isoformat()
        } for c in conversations]
    finally:
        db.close()

def update_conversation_status(conversation_id: str, status: str) -> Optional[dict]:
    db = SessionLocal()
    try:
        db_conv = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        if not db_conv:
            return None
        db_conv.status = status
        db.commit()
        db.refresh(db_conv)
        return {
            "conversation_id": db_conv.conversation_id,
            "status": db_conv.status
        }
    finally:
        db.close()

# --- Query & Insight Operations ---

def create_query(conversation_id: str, user_id: str, question: str) -> dict:
    db = SessionLocal()
    try:
        db_query = Query(
            conversation_id=conversation_id,
            user_id=user_id,
            question=question
        )
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        return {
            "query_id": db_query.query_id,
            "conversation_id": db_query.conversation_id,
            "user_id": db_query.user_id,
            "question": db_query.question,
            "created_at": db_query.created_at.isoformat()
        }
    finally:
        db.close()

def get_conversation_queries(conversation_id: str) -> List[dict]:
    db = SessionLocal()
    try:
        queries = db.query(Query).filter(Query.conversation_id == conversation_id).all()
        return [{
            "query_id": q.query_id,
            "conversation_id": q.conversation_id,
            "user_id": q.user_id,
            "question": q.question,
            "created_at": q.created_at.isoformat()
        } for q in queries]
    finally:
        db.close()

def create_insight(query_id: str, response: str) -> dict:
    db = SessionLocal()
    try:
        db_insight = Insight(
            query_id=query_id,
            response=response
        )
        db.add(db_insight)
        db.commit()
        db.refresh(db_insight)
        return {
            "insight_id": db_insight.insight_id,
            "query_id": db_insight.query_id,
            "response": db_insight.response,
            "created_at": db_insight.created_at.isoformat()
        }
    finally:
        db.close()

def get_query_insight(query_id: str) -> Optional[dict]:
    db = SessionLocal()
    try:
        db_insight = db.query(Insight).filter(Insight.query_id == query_id).first()
        if not db_insight:
            return None
        return {
            "insight_id": db_insight.insight_id,
            "query_id": db_insight.query_id,
            "response": db_insight.response,
            "created_at": db_insight.created_at.isoformat()
        }
    finally:
        db.close()

# --- Comment Operations ---

def create_comment(conversation_id: str, user_id: str, content: str) -> dict:
    db = SessionLocal()
    try:
        db_comment = Comment(
            conversation_id=conversation_id,
            user_id=user_id,
            content=content
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return {
            "comment_id": db_comment.comment_id,
            "conversation_id": db_comment.conversation_id,
            "user_id": db_comment.user_id,
            "content": db_comment.content,
            "created_at": db_comment.created_at.isoformat()
        }
    finally:
        db.close()

def get_conversation_comments(conversation_id: str) -> List[dict]:
    db = SessionLocal()
    try:
        comments = db.query(Comment).filter(Comment.conversation_id == conversation_id).all()
        return [{
            "comment_id": c.comment_id,
            "conversation_id": c.conversation_id,
            "user_id": c.user_id,
            "content": c.content,
            "created_at": c.created_at.isoformat()
        } for c in comments]
    finally:
        db.close()

def delete_comment(comment_id: str, user_id: str) -> bool:
    db = SessionLocal()
    try:
        db_comment = db.query(Comment).filter(Comment.comment_id == comment_id, Comment.user_id == user_id).first()
        if not db_comment:
            return False
        db.delete(db_comment)
        db.commit()
        return True
    finally:
        db.close()

# --- Reaction Operations ---

def add_reaction(conversation_id: str, user_id: str, reaction_type: str) -> dict:
    db = SessionLocal()
    try:
        # Check if reaction already exists
        db_reaction = db.query(Reaction).filter(
            Reaction.conversation_id == conversation_id,
            Reaction.user_id == user_id
        ).first()
        
        if db_reaction:
            db_reaction.reaction_type = reaction_type
        else:
            db_reaction = Reaction(
                conversation_id=conversation_id,
                user_id=user_id,
                reaction_type=reaction_type
            )
            db.add(db_reaction)
        
        db.commit()
        db.refresh(db_reaction)
        return {
            "reaction_id": db_reaction.reaction_id,
            "conversation_id": db_reaction.conversation_id,
            "user_id": db_reaction.user_id,
            "reaction_type": db_reaction.reaction_type
        }
    finally:
        db.close()

def remove_reaction(conversation_id: str, user_id: str) -> bool:
    db = SessionLocal()
    try:
        db_reaction = db.query(Reaction).filter(
            Reaction.conversation_id == conversation_id,
            Reaction.user_id == user_id
        ).first()
        
        if not db_reaction:
            return False
        
        db.delete(db_reaction)
        db.commit()
        return True
    finally:
        db.close()

def get_conversation_reactions(conversation_id: str) -> List[dict]:
    db = SessionLocal()
    try:
        reactions = db.query(Reaction).filter(Reaction.conversation_id == conversation_id).all()
        return [{
            "reaction_id": r.reaction_id,
            "conversation_id": r.conversation_id,
            "user_id": r.user_id,
            "reaction_type": r.reaction_type
        } for r in reactions]
    finally:
        db.close()
