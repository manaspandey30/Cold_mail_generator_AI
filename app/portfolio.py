import pandas as pd
import chromadb
import uuid
import os


class Portfolio:
    def __init__(self, file_path=None):
        # Get the absolute path to my_portfolio.csv in the root directory
        if file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(current_dir)
            file_path = os.path.join(root_dir, "my_portfolio.csv")
        
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        
        # Create vectorstore directory if it doesn't exist
        vector_store_path = os.path.join(root_dir, "vectorstore")
        os.makedirs(vector_store_path, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(vector_store_path)
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills, custom_links=None):
        # If custom links are provided, use them instead of vector search
        if custom_links and len(custom_links) > 0:
            # Filter out empty links
            valid_links = [link.strip() for link in custom_links if link.strip()]
            if valid_links:
                return [{"links": link} for link in valid_links[:2]]  # Return max 2 links
        
        # Fallback to vector search if no custom links
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
