from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import search_projects, generate_pitch

app = FastAPI(title="Studyond AI Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data structures expected from the frontend
class ChatRequest(BaseModel):
    message: str

class DraftRequest(BaseModel):
    profile: dict
    selected_project: dict

# ENDPOINT 1: The Search
@app.post("/api/search")
async def handle_search(request: ChatRequest):
    print("🌐 API Received a search request.")
    return search_projects(request.message)

# ENDPOINT 2: The Email Drafter
@app.post("/api/draft")
async def handle_draft(request: DraftRequest):
    print("🌐 API Received a draft request.")
    return generate_pitch(request.profile, request.selected_project)