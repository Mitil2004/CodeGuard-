import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import motor.motor_asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="CodeGuard API")

# Enable CORS for the React frontend (Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from Environment Variables
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URL = os.getenv("MONGODB_URL")

# Initialize Gemini AI
if GEMINI_KEY:
    try:
        genai.configure(api_key=GEMINI_KEY)
        print("✅ SUCCESS: Gemini AI Engine Initialized.")
    except Exception as e:
        print(f"❌ ERROR: Gemini Config Failed: {e}")
else:
    print("⚠️ WARNING: GEMINI_API_KEY is missing.")

# Initialize MongoDB Cloud Archive
db_client = None
collection = None
if MONGO_URL:
    try:
        db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        db = db_client.codeguard_db
        collection = db.audits
        print("✅ SUCCESS: MongoDB Cloud Archive Linked.")
    except Exception as e:
        print(f"❌ ERROR: MongoDB Link Failed: {e}")

class CodeRequest(BaseModel):
    code: str

@app.get("/")
async def root():
    return {
        "status": "online", 
        "message": "CodeGuard SEC-OPS API is active",
        "engine": "Gemini 1.5 Flash"
    }

@app.post("/analyze")
async def analyze(request: CodeRequest):
    if not GEMINI_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key is not configured on the server.")
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = (
            "Act as a Senior Security Research Engineer. Perform a deep security audit on the following source code. "
            "Identify vulnerabilities, rate their severity (Low/Medium/High/Critical), and provide fix recommendations. "
            "Format the entire response in clean Markdown:\n\n"
            f"{request.code}"
        )
        
        response = model.generate_content(prompt)
        report_text = response.text

        # Log to Database if connected
        if collection is not None:
            await collection.insert_one({
                "code": request.code,
                "report": report_text,
                "timestamp": datetime.utcnow()
            })

        return {
            "audit_report": report_text, 
            "db_status": "Logged to Cloud Archive" if collection is not None else "DB Offline (Local Session Only)"
        }
    except Exception as e:
        print(f"Audit Exception: {e}")
        return {"error": str(e)}

@app.get("/history")
async def history():
    if collection is None:
        return {"history": []}
    try:
        # Fetch last 10 audits
        cursor = collection.find().sort("timestamp", -1).limit(10)
        logs = []
        async for doc in cursor:
            logs.append({
                "id": str(doc["_id"]),
                "code": doc.get("code", ""),
                "report": doc.get("report", ""),
                "time": doc.get("timestamp").isoformat() if doc.get("timestamp") else None
            })
        return {"history": logs}
    except Exception as e:
        return {"error": str(e)}