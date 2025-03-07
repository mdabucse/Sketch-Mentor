import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class RAGSystem:
    def __init__(self, json_path: str, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG system with a JSON file and embedding model.
        
        Args:
            json_path: Path to the JSON file containing the text data.
            model_name: Name of the sentence-transformer model to use.
        """
        self.json_path = json_path
        self.encoder = SentenceTransformer(model_name)
        self.documents = []
        self.document_embeddings = None
        self.index = None
        
        # Load and process the JSON data
        self.load_data()
        self.build_index()
        
    def load_data(self) -> None:
        """Load and process the JSON data."""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.documents = []  # Reset documents list

            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        content = item.get("text") or item.get("content") or item.get("body") or None
                        if content:  
                            self.documents.append({"content": content, "metadata": item})
                    elif isinstance(item, str):
                        self.documents.append({"content": item, "metadata": {}})

            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, str):
                        self.documents.append({"content": value, "metadata": {"id": key}})
                    elif isinstance(value, dict):
                        content = value.get("text") or value.get("content") or value.get("body") or None
                        if content:
                            self.documents.append({"content": content, "metadata": value})

            print(f"Loaded {len(self.documents)} documents from {self.json_path}")

        except Exception as e:
            print(f"Error loading data: {e}")
            self.documents = []
    
    def build_index(self) -> None:
        """Create FAISS index from document embeddings."""
        if not self.documents:
            print("No documents to index")
            return
        
        # Extract texts for encoding
        texts = [doc["content"] for doc in self.documents]
        
        # Generate embeddings
        self.document_embeddings = self.encoder.encode(texts, show_progress_bar=True)
        
        # Convert to float32 (required by FAISS)
        self.document_embeddings = np.array(self.document_embeddings).astype('float32')
        
        # Create and train the FAISS index
        dimension = self.document_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)  # Using L2 distance
        faiss.normalize_L2(self.document_embeddings)  # Normalize vectors
        self.index.add(self.document_embeddings)
        
        print(f"Created FAISS index with {self.index.ntotal} vectors of dimension {dimension}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for documents similar to the query.
        
        Args:
            query: The search query.
            top_k: Number of results to return.
            
        Returns:
            List of documents with similarity scores.
        """
        if not self.index:
            return []
        
        # Encode the query
        query_embedding = self.encoder.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search the index
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid index
                results.append({
                    "id": self.documents[idx]["metadata"].get("id", f"doc_{idx}"),
                    "content": self.documents[idx]["content"],
                    "metadata": self.documents[idx]["metadata"],
                    "score": float(1 - distances[0][i])  # Convert distance to similarity score
                })
        
        return results

def rag_main(query: str) -> str:
    """
    Main function to initialize RAG and perform search.

    Args:
        query: The input query string.

    Returns:
        A formatted string of search results.
    """
    # Path to your JSON file
    json_path = r"A:\Projects\Edu_Pro\backend\data\single.json"
    
    # Initialize the RAG system
    rag = RAGSystem(json_path)
    
    # Get results
    results = rag.search(query, top_k=3)
    
    # Display results
    if not results:
        return "No relevant documents found."

    return "\n\n".join([
        f"Result {i+1} (Score: {r['score']:.4f})\n{r['content']}"
        for i, r in enumerate(results)
    ])

# Uncomment to test
# if __name__ == "__main__":
#     query = input("Enter your query: ")
#     print(rag_main(query))
