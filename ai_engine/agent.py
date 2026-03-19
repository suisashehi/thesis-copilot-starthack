import json
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = "./chroma_db"

class StudentProfile(BaseModel):
    extracted_skills: List[str] = Field(description="Hard skills like programming languages or tools.")
    core_interests: List[str] = Field(description="Broad industries, topics, or academic fields.")
    excluded_topics: List[str] = Field(description="Anything the student explicitly says they do NOT want to do.")

# --- FUNCTION 1: EXTRACT & SEARCH (Returns Top 3) ---
def search_projects(user_message: str):
    print("LLM is extracting profile...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    extractor = llm.with_structured_output(StudentProfile)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert academic headhunter. Extract the student's skills, interests, and exclusions."),
        ("human", "{message}")
    ])
    
    profile: StudentProfile = (prompt | extractor).invoke({"message": user_message})
    
    print("Database is finding the top 3 matches...")
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
    )
    
    search_query = f"Skills: {', '.join(profile.extracted_skills)}. Interests: {', '.join(profile.core_interests)}"
    
    # CHANGE: Grab the top 3 matches instead of 1
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 
    docs = retriever.invoke(search_query)
    
    matches = [doc.metadata for doc in docs]
    
    return {
        "extracted_profile": profile.model_dump(),
        "top_matches": matches
    }

# --- FUNCTION 2: GENERATE THE PITCH (Runs only when the user clicks a project) ---
def generate_pitch(profile_dict: dict, selected_project: dict):
    print(f"Drafting email for {selected_project.get('company_name')}...")
    
    writer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    pitch_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert career advisor. Write a concise, professional cold email 
        for this student to apply for the provided thesis project. 
        Rules: Keep it under 150 words. Connect skills to the project. Sound academic."""),
        ("human", "Student Profile: {profile}\n\nThesis Project: {project}")
    ])
    
    pitch_chain = pitch_prompt | writer_llm
    pitch_response = pitch_chain.invoke({
        "profile": json.dumps(profile_dict),
        "project": json.dumps(selected_project)
    })
    
    return {"generated_pitch": pitch_response.content}