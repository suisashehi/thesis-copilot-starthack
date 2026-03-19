import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load Secrets & App Config
load_dotenv()
app = FastAPI(title="Thesis Copilot Backend")

# 2. Setup CORS (The Security Handshake)
# This allows your Frontend (Next.js) to talk to this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Setup the AI Brain Connection
CHROMA_PATH = "./chroma_db"

# Check if the database folder actually exists before trying to load it
if not os.path.exists(CHROMA_PATH):
    print("❌ ERROR: 'chroma_db' folder not found. Run ingest.py first!")
else:
    print("🧠 AI Brain connected successfully.")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

# 4. Endpoints
@app.get("/health")
async def health():
    return {"status": "Backend is live", "database": "Connected"}

@app.post("/find-matches")
async def find_matches(user_query: dict):
    try:
        # Get the query text from the frontend request
        query_text = user_query.get("text", "")
        
        if not query_text:
            raise HTTPException(status_code=400, detail="No search text provided")

        # Search the Vector DB (k=3 keeps usage/costs low)
        results = db.similarity_search(query_text, k=3)
        
        # Format the results into a clean list for the Frontend
        matches = []
        for doc in results:
            matches.append({
                "id": doc.metadata.get("topic_id"),
                "title": doc.metadata.get("title", "No Title"),
                "company": doc.metadata.get("company_name", "Industry Partner"),
                "expert": doc.metadata.get("expert_names", "TBD"),
                "snippet": doc.page_content[:200] + "..." # Useful for frontend cards
            })
            
        return matches

    except Exception as e:
        print(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail="Internal AI Error")