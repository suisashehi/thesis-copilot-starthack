import json
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = "./chroma_db"

# --- MOMENT 1: THE EXTRACTOR (Pydantic Schema) ---
class StudentProfile(BaseModel):
    extracted_skills: List[str] = Field(description="Hard skills like programming languages or tools.")
    core_interests: List[str] = Field(description="Broad industries, topics, or academic fields.")
    excluded_topics: List[str] = Field(description="Anything the student explicitly says they do NOT want to do.")

def run_copilot(user_message: str):
    print(f"\nSTUDENT TYPED: '{user_message}'\n")
    print("LLM is translating human text into strict data...")
    
    # Set up the fast LLM to act as a strict data parser
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    extractor = llm.with_structured_output(StudentProfile)
    
    # Extract the profile
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert academic headhunter. Extract the student's skills, interests, and exclusions."),
        ("human", "{message}")
    ])
    
    profile: StudentProfile = (prompt | extractor).invoke({"message": user_message})
    print(f"EXTRACTED PROFILE:\n   Skills: {profile.extracted_skills}\n   Interests: {profile.core_interests}\n")
    
    # --- MOMENT 2 & 3: THE SEARCH (Zero LLM, Pure Math) ---
    print("Database is calculating mathematical distance to find a match...")
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
    )
    
    search_query = f"Skills: {', '.join(profile.extracted_skills)}. Interests: {', '.join(profile.core_interests)}"
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1}) 
    docs = retriever.invoke(search_query)
    
    match_metadata = docs[0].metadata if docs else None

    # --- MOMENT 4: THE PITCH ENGINE (The Magic Button) ---
    email_draft = "No match found to generate a pitch."
    
    if match_metadata:
        print("LLM is drafting the personalized outreach email...")
        
        # We use a slightly higher temperature (0.7) here so the email sounds human and natural
        writer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        
        pitch_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert career advisor. Write a concise, professional cold email 
            for this student to apply for the provided thesis project. 
            Rules:
            1. Keep it under 150 words.
            2. Explicitly connect the student's skills to the project.
            3. Do not use generic placeholders like [Insert Name] if you have the data.
            4. Make it sound enthusiastic but academic."""),
            ("human", "Student Profile: {profile}\n\nThesis Project: {project}")
        ])
        
        pitch_chain = pitch_prompt | writer_llm
        pitch_response = pitch_chain.invoke({
            "profile": json.dumps(profile.model_dump()),
            "project": json.dumps(match_metadata)
        })
        
        email_draft = pitch_response.content
    
    # --- THE HANDOFF (Packaging data for your Backend/Frontend) ---
    final_output = {
        "extracted_profile": profile.model_dump(),
        "top_match_found": match_metadata or "No match found.",
        "generated_pitch": email_draft # <-- We added the newly generated email to the payload!
    }
    
    return final_output

if __name__ == "__main__":
    # We are simulating a messy message from the frontend UI
    test_message = "I'm a massive data nerd but I really want to work outside, maybe with climate or food stuff. I know Python and a bit of ML."
    
    # Run the engine
    result = run_copilot(test_message)
    
    # Print the exact JSON your backend will send to the frontend UI
    print("\nFINAL JSON PAYLOAD FOR THE FRONTEND:")
    print(json.dumps(result, indent=2))