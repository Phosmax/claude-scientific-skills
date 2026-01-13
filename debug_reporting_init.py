
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

try:
    print("Importing ReportingService...")
    from auramax_api.services.reporting_service import ReportingService
    print("Instantiating ReportingService...")
    service = ReportingService()
    print("SUCCESS: Service initialized.")
except Exception as e:
    print(f"CRITICAL FAILURE: {e}")
    import traceback
    traceback.print_exc()
