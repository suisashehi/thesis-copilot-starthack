import json
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "./chroma_db"

def load_json(filepath):
    # If the file doesn't exist, just return an empty list so the code doesn't crash
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Skipping for now.")
        return []
        
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def build_vector_database():
    print("Loading Studyond relational data...")
    
    # 1. Load all the different mock datasets
    # (Assuming you save them in a folder called 'data')
    topics = load_json("data/topics.json")
    companies = load_json("data/companies.json")
    supervisors = load_json("data/supervisors.json")
    experts = load_json("data/experts.json")

    # 2. Create lookup dictionaries for instant matching
    company_dict = {c["id"]: c for c in companies}
    supervisor_dict = {s["id"]: s for s in supervisors}
    expert_dict = {e["id"]: e for e in experts}

    documents = []

    print("Merging relational data and embedding...")
    
    # 3. Build the rich text for the AI
    for topic in topics:
        # Skip jobs, we only want thesis topics for the Copilot right now
        if topic.get("type") != "topic":
            continue

        title = topic.get("title", "Unknown Title")
        desc = topic.get("description", "")
        
        # Look up the Company Name and their 'About' info
        company_id = topic.get("companyId")
        company_info = company_dict.get(company_id, {}) if company_id else {}
        company_name = company_info.get("name", "University Project")
        company_about = company_info.get("about", "")

        # Look up the Expert (Industry Mentor)
        expert_names = []
        for e_id in topic.get("expertIds", []):
            exp = expert_dict.get(e_id)
            if exp: expert_names.append(f"{exp['firstName']} {exp['lastName']} ({exp.get('title', '')})")
        expert_str = ", ".join(expert_names)

        # Build the mega-string that the AI will read and search against
        page_content = f"""
        Thesis Title: {title}
        Company/Institution: {company_name}
        Company Details: {company_about}
        Topic Description: {desc}
        Industry Experts Available: {expert_str}
        Degrees Accepted: {', '.join(topic.get('degrees', []))}
        """

        # Build the pristine metadata for the Frontend UI Cards
        metadata = {
            "topic_id": topic["id"],
            "title": title,
            "company_name": company_name,
            "expert_names": expert_str
        }

        documents.append(Document(page_content=page_content, metadata=metadata))

    # 4. Save to ChromaDB
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory=CHROMA_PATH
    )
    
    print(f"Success! Embedded {len(documents)} thesis topics into the AI Brain.")

if __name__ == "__main__":
    build_vector_database()