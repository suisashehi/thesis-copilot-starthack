from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 1. Setup the Database Connection
CHROMA_PATH = "./chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Connect to the "Brain" your partner built
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "Backend is live and connected to AI Brain"}

@app.post("/find-matches")
async def find_matches(user_query: dict):
    # This takes the user's interests and finds the top 3 thesis topics
    query_text = user_query.get("text", "AI and Sustainability")
    
    # 2. Search the Vector DB
    results = db.similarity_search(query_text, k=3)
    
    # 3. Format the results for the Frontend
    matches = []
    for doc in results:
        matches.append({
            "id": doc.metadata.get("topic_id"),
            "title": doc.metadata.get("title"),
            "company": doc.metadata.get("company_name"),
            "expert": doc.metadata.get("expert_names")
        })
        
    return matches