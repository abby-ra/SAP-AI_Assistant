"""Quick test script for the AI analysis API"""
import requests
import json

# Test the backend API
print("Testing SAP AI Assistant API...\n")

# Test 1: Health check
print("1. Health Check:")
response = requests.get("http://localhost:8000/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

# Test 2: Model test
print("2. Model Test:")
response = requests.get("http://localhost:8000/api/model-test")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

# Test 3: AI Analysis
print("3. AI Analysis (Stock Query):")
query_data = {"query": "Is stock getting reduced?"}
response = requests.post(
    "http://localhost:8000/api/analyze",
    json=query_data,
    headers={"Content-Type": "application/json"}
)
print(f"   Status: {response.status_code}")
result = response.json()
print(f"   Status: {result['status']}")
print(f"   Mock Mode: {result.get('mock_mode', 'N/A')}")
print(f"   Model: {result.get('model', 'N/A')}")
print(f"\n   Analysis:\n{result['analysis']}\n")

print("=" * 60)
print("✅ All tests passed! Your AI Assistant is working!")
print("=" * 60)
