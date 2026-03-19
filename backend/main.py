import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI

# 1. Load Secrets & Config
load_dotenv()
app = FastAPI(title="Thesis Copilot Backend")
openai_client = OpenAI() 

# --- BLOCK 4: SESSION STATE ---
user_session = {}

# 2. Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Data Structures
class ProfileData(BaseModel):
    full_name: str
    skills: str
    interests: str

class SearchRequest(BaseModel):
    text: str

class PitchRequest(BaseModel):
    topic_id: str

# 4. AI Brain (Block 3)
CHROMA_PATH = "./chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

# --- ENDPOINTS ---

@app.get("/health")
async def health():
    return {"status": "online", "db_count": db._collection.count()}

@app.post("/save-profile")
async def save_profile(profile: ProfileData):
    user_session["current_user"] = profile.dict()
    return {"message": "Profile saved", "user": user_session["current_user"]}

@app.post("/find-matches")
async def find_matches(query: SearchRequest):
    try:
        # Step 3 logic: Find top 3
        results = db.similarity_search(query.text, k=3)
        matches = []
        for doc in results:
            matches.append({
                "id": doc.metadata.get("topic_id"),
                "title": doc.metadata.get("title"),
                "company": doc.metadata.get("company_name"),
                "expert": doc.metadata.get("expert_names"),
                "snippet": doc.page_content[:200]
            })
        return matches
    except Exception as e:
        print(f"Search Error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.post("/generate-pitch")
async def generate_pitch(request: PitchRequest):
    # --- MOCK MODE FOR DEMO SAFETY ---
    if request.topic_id == "test_id":
        return {"pitch": "Dear Expert, I'm interested in your project. I have the skills you need. Best, Student."}

    try:
        # 1. Get Topic from DB
        # Use a similarity search with k=1 to find the specific ID if .get() fails
        results = db.similarity_search(request.topic_id, k=1)
        if not results:
             raise HTTPException(status_code=404, detail="Topic not found")
        
        meta = results[0].metadata
        
        # 2. Get User from Session (Block 4)
        user = user_session.get("current_user", {"full_name": "Student", "skills": "research"})

        # 3. Generate Pitch
        prompt = f"""
        Write a professional 3-sentence cold email from {user['full_name']} 
        to {meta.get('expert_names')} at {meta.get('company_name')} 
        about the thesis: {meta.get('title')}.
        Mention these student skills: {user['skills']}.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {"pitch": response.choices[0].message.content}
    except Exception as e:
        print(f"Pitch Error: {e}")
        raise HTTPException(status_code=500, detail="Pitch generation failed")