import chromadb
import os

print("Test ChromaDB")

try:
    # Create directory
    os.makedirs("test_vectorstore", exist_ok=True)
    
    # Initialize client
    client = chromadb.PersistentClient("test_vectorstore")
    
    # Create a collection
    collection = client.create_collection(name="test_collection")
    
    # Add some documents
    collection.add(
        documents=["This is a test document"],
        metadatas=[{"source": "test"}],
        ids=["id1"]
    )
    
    # Query
    results = collection.query(
        query_texts=["test document"],
        n_results=1
    )
    
    print("Success! Query results:", results)
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}") 