from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Lets the Frontend talk to this code
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "Backend is live"}

@app.post("/extract-profile")
async def extract_profile(data: dict):
    return {"skills": ["AI", "Python"], "interests": ["Theses"]}

@app.post("/find-matches")
async def find_matches():
    return [{"id": 1, "title": "AI Thesis @ OST", "company": "Studyond"}]