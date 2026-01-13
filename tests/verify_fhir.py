import asyncio
import logging
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "auramax-core/src"))

from auramax_api.fhir.client import FHIRClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting FHIR Verification...")
    
    # Use Public Sandbox
    client = FHIRClient(base_url="http://hapi.fhir.org/baseR4")
    
    # 1. Search Patient
    # We'll search for a common name 'Smith' or just get first few patients
    logger.info("1. Testing Search Patient...")
    try:
        # Searching for 'Smith' usually yields results in sandbox
        patients = await client.search_patient(name="Smith")
        logger.info(f"Found {len(patients)} patients")
        
        if patients:
            p = patients[0]
            p_id = p.get("id")
            name = p.get("name", [{}])[0].get("family", "Unknown")
            logger.info(f"First Patient: ID={p_id}, Name={name}")
            
            # 2. Test DocumentReference
            if p_id:
                logger.info("2. Testing Create DocumentReference...")
                doc_ref = client.create_document_reference_resource(
                    _id="test-doc-ref", # Client usually lets server assign ID, or we generate UUID
                    patient_id=p_id,
                    url="https://example.com/report.pdf",
                    title="AuraMax Test Report",
                    created=datetime.utcnow()
                )
                
                # In real scenario we might not want to spam the sandbox, 
                # but sending one resource is fine for verification.
                # However, client.create_document_reference_resource returns a Pydantic model (or dict).
                # We need to send it.
                # Note: send_resource does PUT by default with ID.
                # If we use a random ID, it's a creates-as-update.
                
                # Let's generate a random ID to avoid collision
                import uuid
                doc_doc_id = str(uuid.uuid4())
                if hasattr(doc_ref, "id"):
                     doc_ref.id = doc_doc_id
                else:
                     doc_ref["id"] = doc_doc_id
                
                success = await client.send_resource(doc_ref)
                logger.info(f"Send DocumentReference result: {success}")

    except Exception as e:
        logger.error(f"Verification Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
