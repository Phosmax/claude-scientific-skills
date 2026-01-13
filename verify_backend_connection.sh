#!/bin/bash

# Configuration
API_URL="http://localhost:8000"
ADMIN_EMAIL="admin@auramax.ai"
ADMIN_PASSWORD="admin" # Adjust if your local db has different pass

echo "=== Verifying AuraMax Backend Connectivity ==="

# 1. Check Health Endpoint
echo "1. Pinging /health..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health)
if [ "$HEALTH" == "200" ]; then
    echo "✅ Health Check Passed (200 OK)"
else
    echo "❌ Health Check Failed. Status Code: $HEALTH"
    echo "⚠️  Ensure backend is running: 'python -m auramax_api.main'"
    exit 1
fi

# 2. Login to get Token
echo -e "\n2. Logging in as Admin..."
TOKEN_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}")

# Extract token (simple grep/sed, assume successful json)
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ Login Failed. Response: $TOKEN_RESPONSE"
    exit 1
else
    echo "✅ Login Successful. Token obtained."
fi

# 3. Test Clinic Patients Endpoint
echo -e "\n3. Testing GET /api/v1/clinic/patients..."
PATIENTS_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_URL/api/v1/clinic/patients" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if [ "$PATIENTS_CODE" == "200" ]; then
    echo "✅ /api/v1/clinic/patients is reachable (200 OK)"
else
    echo "❌ /api/v1/clinic/patients Failed. Status Code: $PATIENTS_CODE"
    echo "👉 If this fails with 500, check backend logs."
fi

echo -e "\n=== Verification Complete ==="
