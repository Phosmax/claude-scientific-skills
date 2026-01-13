import requests
import json
import os

API_URL = "http://localhost:8000/api/v1"

def test_phase43():
    print("🚀 Starting Phase 43 Verification...")

    # 1. Login
    login_url = f"{API_URL}/auth/login"
    login_data = {"email": "test@example.com", "password": "password123"}
    resp = requests.post(login_url, json=login_data)
    
    if resp.status_code != 200:
        # Register if not exists
        print("Registering test user...")
        reg_url = f"{API_URL}/auth/register"
        reg_data = {"email": "test@example.com", "password": "password123", "full_name": "Test User"}
        requests.post(reg_url, json=reg_data)
        resp = requests.post(login_url, json=login_data)
    
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Authentication successful.")

    # 2. Check Twin Status (incorporating genomic risk)
    twin_url = f"{API_URL}/twin/status"
    print(f"Fetching: {twin_url}")
    resp = requests.get(twin_url, headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Error Body: {resp.text}")
    assert resp.status_code == 200
    data = resp.json()
    print("✅ Twin Status retrieved.")
    print(f"   Brain Risk: {data['brain']['risk']} (Genomic Boost: {data['brain'].get('genomic_boost')}%)")
    print(f"   Heart Risk: {data['heart']['risk']} (Genomic Boost: {data['heart'].get('genomic_boost')}%)")

    # 3. Check Clinical Trial Matches
    trials_url = f"{API_URL}/trials/matches"
    resp = requests.get(trials_url, headers=headers)
    assert resp.status_code == 200
    trials_data = resp.json()
    print(f"✅ Found {trials_data['total']} matching clinical trials.")
    for trial in trials_data['matches'][:2]:
        print(f"   - {trial['title']} ({trial['organ']})")

    print("\n🎉 Phase 43 Verification Complete!")

if __name__ == "__main__":
    test_phase43()
