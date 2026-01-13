import requests
import os
import json

def test_twin_api():
    print("--- Verifying Phase 41: Digital Twin API ---")
    
    # Configuration
    API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
    
    # 1. Register or Login to get token
    user_payload = {
        "email": "twin_tester@example.com",
        "password": "password123",
        "full_name": "Twin Tester"
    }
    
    try:
        # Try register first
        requests.post(f"{API_URL}/auth/register", json=user_payload)
        # Then login
        login_res = requests.post(f"{API_URL}/auth/login", json={"email": user_payload["email"], "password": user_payload["password"]})
        login_res.raise_for_status()
        token = login_res.json()["access_token"]
        print("✅ Authentication successful")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return

    # 2. Add some health metrics for the user to ensure non-default scores
    headers = {"Authorization": f"Bearer {token}"}
    sync_payload = {
        "source": "verification_script",
        "metrics": [
            {
                "type": "heart_rate_resting",
                "value": 58, # Ideal RHR
                "unit": "bpm",
                "recorded_at": "2026-01-07T10:00:00Z",
                "device_name": "VerifyBot"
            },
            {
                "type": "sleep_duration",
                "value": 510, # 8.5 hours (Ideal)
                "unit": "min",
                "recorded_at": "2026-01-07T08:00:00Z",
                "device_name": "VerifyBot"
            }
        ]
    }
    
    try:
        # Use full path for wearables
        sync_res = requests.post(f"{API_URL}/wearables/sync", headers=headers, json=sync_payload)
        sync_res.raise_for_status()
        print("✅ Mock metrics synced")
    except Exception as e:
        print(f"❌ Metric sync failed: {e}")

    # 3. Fetch Twin Status
    try:
        # Use full path for twin
        res = requests.get(f"{API_URL}/twin/status", headers=headers)
        res.raise_for_status()
        data = res.json()
        
        print(f"✅ Twin Status Response: {json.dumps(data, indent=2)}")
        
        # Verify specific scoring logic
        assert data["heart"]["resilience"] == 95, f"Expected 95 for 58bpm, got {data['heart']['resilience']}"
        assert data["brain"]["resilience"] == 98, f"Expected 98 for 8.5h sleep, got {data['brain']['resilience']}"
        print("✅ Scoring logic verified: Ideal metrics yield high resilience scores.")
        
    except Exception as e:
        print(f"❌ Twin Status verification failed: {e}")

if __name__ == "__main__":
    test_twin_api()
