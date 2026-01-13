import requests
import os
import uuid
import time

def verify_phase42():
    print("--- Verifying Phase 42: Medical Imaging & Digital Twin Integration ---")
    API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
    
    # 1. Auth & Setup
    user_payload = {
        "email": "imaging_pro@example.com",
        "password": "password123",
        "full_name": "Imaging Pro"
    }
    requests.post(f"{API_URL}/auth/register", json=user_payload)
    login_res = requests.post(f"{API_URL}/auth/login", json={"email": user_payload["email"], "password": user_payload["password"]})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Authenticated")

    # 2. Upload and Segment (Triggers persistence and Twin update)
    # Using a dummy PNG for the test
    with open("test_scan.png", "wb") as f:
        f.write(b"fake png content")
    
    files = {"file": ("liver_scan_ct.png", open("test_scan.png", "rb"), "image/png")}
    data = {"model": "vista-3d"}
    
    print("Running VISTA-3D Segmentation...")
    seg_res = requests.post(f"{API_URL}/imaging/segment", headers=headers, files=files, data=data)
    seg_res.raise_for_status()
    print("✅ Segmentation successful")
    
    # 3. Verify Scan History
    history_res = requests.get(f"{API_URL}/imaging/scans", headers=headers)
    history_res.raise_for_status()
    scans = history_res.json()
    assert len(scans) > 0
    assert scans[0]["filename"] == "liver_scan_ct.png"
    assert "liver" in scans[0]["volumetric_data"]
    print(f"✅ Scan history verified: {len(scans)} records found")

    # 4. Verify Digital Twin Impact
    # The volunteer Liver Volume in mock is 1500.5cc (Normal)
    # If the score is > 80, it's stable.
    twin_res = requests.get(f"{API_URL}/twin/status", headers=headers)
    twin_res.raise_for_status()
    twin_data = twin_res.json()
    
    liver_resilience = twin_data["liver"]["resilience"]
    print(f"📊 Liver Resilience Score: {liver_resilience}%")
    assert liver_resilience > 80
    assert "1500.5 cc" in twin_data["liver"]["latest_metric"]
    print("✅ Digital Twin integration verified")

    # Cleanup
    os.remove("test_scan.png")
    print("--- Phase 42 Verification Complete ---")

if __name__ == "__main__":
    verify_phase42()
