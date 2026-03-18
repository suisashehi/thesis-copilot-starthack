from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "./chroma_db"

def inspect_database():
    print("Connecting to local ChromaDB...")
    
    # Connect to the existing database
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
    )
    
    # Grab the underlying data collection
    data = vectorstore.get()
    total_items = len(data['ids'])
    
    print(f"\nFound {total_items} items in the database.")
    
    if total_items == 0:
        print("The database is empty! Something went wrong with ingest.py.")
        return

    print("\n--- RAW DATABASE CONTENTS ---")
    
    # Loop through and print the contents (limiting to 3 so it doesn't flood your terminal)
    for i in range(min(3, total_items)):
        print(f"\nItem [{i+1}]:")
        print(f"ID:       {data['ids'][i]}")
        print(f"Metadata: {data['metadatas'][i]}")
        print("Text Embedded:")
        print("-" * 20)
        print(data['documents'][i].strip())
        print("-" * 20)

if __name__ == "__main__":
    inspect_database()