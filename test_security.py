from backend.services import db_service
import uuid

def test_password_hashing():
    print("Testing Password Hashing...")
    
    # 1. Create a user
    email = f"test_{uuid.uuid4()}@example.com"
    password = "securePassword123"
    print(f"Creating user: {email} / {password}")
    
    user = db_service.create_user("Test User", "Tester", "QA", email, password)
    
    # 2. Check if password is hashed
    stored_password = user["password"]
    print(f"Stored Password (First 20 chars): {stored_password[:20]}...")
    
    if stored_password == password:
        print("❌ FAIL: Password is stored in plain text!")
        return
    
    if not stored_password.startswith("$argon2"):
        print("⚠️ WARNING: Password doesn't look like a standard argon2 hash (may depend on config).")
    else:
        print("✅ PASS: Password appears to be hashed.")

    # 3. Validate correct password
    print("Validating with CORRECT password...")
    valid_user = db_service.validate_user(email, password)
    if valid_user:
        print("✅ PASS: Login successful.")
    else:
        print("❌ FAIL: Login failed with correct password.")

    # 4. Validate incorrect password
    print("Validating with WRONG password...")
    invalid_user = db_service.validate_user(email, "wrongpassword")
    if not invalid_user:
        print("✅ PASS: Login failed as expected.")
    else:
        print("❌ FAIL: Login SUCCEEDED with wrong password!")

if __name__ == "__main__":
    test_password_hashing()
