from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_copilot

# 1. Initialize the API
app = FastAPI(title="Studyond AI Copilot API")

# 2. Prevent CORS errors
# This allows your web app (running on a different port) to talk to this Python server without the browser blocking it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the incoming data structure
class ChatRequest(BaseModel):
    message: str

# 4. Create the URL endpoint
@app.post("/api/chat")
async def chat_with_copilot(request: ChatRequest):
    print(f"API Received a message: {request.message}")
    
    # Run your exact agent pipeline
    result = run_copilot(request.message)
    
    # Send the JSON payload back to the web app
    return result