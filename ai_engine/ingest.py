import json
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# The database folder will be created in your main project folder
CHROMA_PATH = "./chroma_db"

def load_json(filepath):
    # If the file doesn't exist, just return an empty list
    if not os.path.exists(filepath):
        print(f"⚠️ Warning: {filepath} not found. Check your folder structure!")
        return []
        
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def build_vector_database():
    print("🚀 Loading Studyond relational data...")
    
    # We load what we can. If a file is missing, it just returns an empty list []
    topics = load_json("ai_engine/data/topics.json")
    companies = load_json("ai_engine/data/companies.json")
    supervisors = load_json("ai_engine/data/supervisors.json")
    experts = load_json("ai_engine/data/experts.json")

    if not topics:
        print("❌ Error: Still can't find topics.json. The brain is empty!")
        return

    # Create lookup dictionaries (Using .get to prevent crashes if IDs are missing)
    company_dict = {c.get("id"): c for c in companies if "id" in c}
    expert_dict = {e.get("id"): e for e in experts if "id" in e}

    documents = []
    print("🧠 Merging data and creating embeddings... (almost done!)")
    
    for topic in topics:
        # Basic check to ensure we only process 'topic' types
        if topic.get("type") != "topic":
            continue

        title = topic.get("title", "Unknown Title")
        desc = topic.get("description", "No description provided.")
        
        company_id = topic.get("companyId")
        company_info = company_dict.get(company_id, {})
        company_name = company_info.get("name", "Industry Partner")

        # Build the text for the AI
        page_content = f"Title: {title}\nCompany: {company_name}\nDescription: {desc}"

        metadata = {
            "topic_id": str(topic.get("id", "0")),
            "title": title,
            "company_name": company_name,
        }

        documents.append(Document(page_content=page_content, metadata=metadata))

    # This is the line that takes a few seconds to finish
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory=CHROMA_PATH
    )
    
    print(f"✅ Success! Embedded {len(documents)} topics into the AI Brain.")

if __name__ == "__main__":
    build_vector_database()