import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI(title="AI CRM Suite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI CRM Suite Backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the AI CRM backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


class AIInsightsRequest(BaseModel):
    text: str

@app.post("/api/ai/insights")
def generate_insights(payload: AIInsightsRequest) -> Dict[str, Any]:
    """
    Lightweight, deterministic insights generator.
    In a real setup you'd call an LLM. Here we return structured suggestions
    so the frontend can show "AI-powered" behavior without external deps.
    """
    text = payload.text.strip()
    summary = text[:160] + ("..." if len(text) > 160 else "") if text else "No input provided"

    action_items = []
    if any(k in text.lower() for k in ["meeting", "call", "sync", "demo"]):
        action_items.append("Schedule a follow-up meeting")
    if any(k in text.lower() for k in ["price", "budget", "quote", "discount"]):
        action_items.append("Send pricing proposal")
    if any(k in text.lower() for k in ["integration", "api", "trial", "pilot"]):
        action_items.append("Share technical integration guide")
    if not action_items:
        action_items = [
            "Send a thank-you email",
            "Log the conversation in the CRM",
            "Set a reminder to follow up in 3 days",
        ]

    sentiment = "positive" if any(w in text.lower() for w in ["great", "good", "excited", "love"]) else (
        "negative" if any(w in text.lower() for w in ["concern", "issue", "problem", "delay"]) else "neutral"
    )

    return {
        "summary": summary,
        "sentiment": sentiment,
        "action_items": action_items,
        "confidence": 0.72 if sentiment != "neutral" else 0.55,
    }


@app.get("/schema")
def get_schema():
    """Expose Pydantic schemas for the database viewer/UI builder."""
    from schemas import Company, Contact, Deal, Activity, User, Product
    return {
        "company": Company.model_json_schema(),
        "contact": Contact.model_json_schema(),
        "deal": Deal.model_json_schema(),
        "activity": Activity.model_json_schema(),
        "user": User.model_json_schema(),
        "product": Product.model_json_schema(),
    }

# ---------------------------------------------
# Minimal CRM endpoints using MongoDB
# ---------------------------------------------
from schemas import Contact
from database import create_document, get_documents

@app.post("/api/contacts")
def create_contact(contact: Contact) -> Dict[str, Any]:
    try:
        new_id = create_document("contact", contact)
        return {"id": new_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/contacts")
def list_contacts(limit: Optional[int] = 20) -> List[Dict[str, Any]]:
    try:
        docs = get_documents("contact", limit=limit)
        # Convert ObjectId to string if present
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
