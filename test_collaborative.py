
import requests
import json
import sys
import uuid

BASE_URL = "http://localhost:8000"

def log(msg, success=True):
    icon = "✅" if success else "❌"
    print(f"{icon} {msg}")

def test_collaborative_flow():
    print("🚀 Starting Collaborative Feature Test...\n")
    
    try:
        print("1. Creating Users...")
        suffix = uuid.uuid4().hex[:6]
        email_a = f"user_a_{suffix}@sap.com"
        email_b = f"user_b_{suffix}@sap.com"
        
        # User A
        res_a = requests.post(f"{BASE_URL}/api/users", json={
            "name": "User A", "role": "Manager", "department": "Sales", "email": email_a, "password": "password123"
        })
        if res_a.status_code != 200:
            log(f"Failed to create User A: {res_a.text}", False)
            return
        user_a = res_a.json()["user"]
        
        # User B
        res_b = requests.post(f"{BASE_URL}/api/users", json={
            "name": "User B", "role": "Director", "department": "Sales", "email": email_b, "password": "password123"
        })
        if res_b.status_code != 200:
            log(f"Failed to create User B: {res_b.text}", False)
            return
        user_b = res_b.json()["user"]
        
        log(f"Created Users: {user_a['name']} ({user_a['user_id']}) & {user_b['name']} ({user_b['user_id']})")
        
        # 2. User A creates conversation
        print("\n2. User A creates conversation...")
        res_conv = requests.post(f"{BASE_URL}/api/conversations", json={
            "user_id": user_a["user_id"],
            "title": "Q4 Sales Forecast",
            "visibility": "department"
        })
        conv = res_conv.json()["conversation"]
        conv_id = conv["conversation_id"]
        log(f"Created Conversation: {conv['title']} ({conv_id})")
        
        # 3. User B views conversations
        print("\n3. User B views shared conversations...")
        res_list = requests.get(f"{BASE_URL}/api/conversations", params={
            "user_id": user_b["user_id"],
            "department": "Sales",
            "view": "all"
        })
        conversations = res_list.json()["conversations"]
        found = any(c["conversation_id"] == conv_id for c in conversations)
        
        if found:
            log("User B can see the conversation.")
        else:
            log("User B CANNOT see the conversation.", False)
            return

        # 4. User B adds a comment
        print("\n4. User B adds a comment...")
        res_comment = requests.post(f"{BASE_URL}/api/conversations/{conv_id}/comments", json={
            "user_id": user_b["user_id"],
            "content": "Looks promising, let's discuss."
        })
        comment = res_comment.json()["comment"]
        log(f"Comment added by User B: '{comment['content']}'")
        
        # 5. Verify comment is visible in details
        print("\n5. Verifying comment visibility...")
        res_details = requests.get(f"{BASE_URL}/api/conversations/{conv_id}")
        details = res_details.json()
        comments = details["comments"]
        
        comment_found = any(c["content"] == "Looks promising, let's discuss." and c["user_id"] == user_b["user_id"] for c in comments)
        
        if comment_found:
            log("Comment successfully retrieved in conversation details.")
        else:
            log("Comment NOT found in details.", False)
            return
            
        print("\n✅ ALL TESTS PASSED!")
        
    except Exception as e:
        log(f"Test Failed with Exception: {str(e)}", False)

if __name__ == "__main__":
    test_collaborative_flow()
