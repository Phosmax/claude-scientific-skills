
import sys
import os
import asyncio

# Add src to path
sys.path.append(os.path.abspath("src"))

async def run_test():
    try:
        print("Importing ReportingService...")
        from auramax_api.services.reporting_service import ReportingService
        print("Instantiating ReportingService...")
        service = ReportingService()
        
        print("Running generate_insight_report...")
        payload = {
            "user_name": "Debug User",
            "age": 50,
            "medications": ["Warfarin"],
            "genotypes": {"CYP2C9": "*3/*3"},
            "recent_rri": [800.0] * 20
        }
        
        report = await service.generate_insight_report(**payload)
        print("SUCCESS: Report Generated")
        print(report["executive_summary"])
        
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
