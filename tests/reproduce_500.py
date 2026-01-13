import requests
import json

def test_endpoint(name, url, token):
    headers = {"Authorization": f"Bearer {token}"}
    print(f"--- Testing {name}: {url} ---")
    try:
        resp = requests.get(url, headers=headers)
        print(f"Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Body: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def reproduce():
    # Admin credentials
    login_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {"email": "admin@auramax.ai", "password": "admin"}
    
    r = requests.post(login_url, json=login_data)
    if r.status_code != 200:
        print(f"Login failed: {r.status_code} - {r.text}")
        return
    
    token = r.json()["access_token"]
    
    test_endpoint("Clinic Patients", "http://localhost:8000/api/v1/clinic/patients", token)
    test_endpoint("Daily Advice", "http://localhost:8000/api/v1/coach/daily-advice", token)

if __name__ == "__main__":
    reproduce()
