from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import json
import os

class DocumentManager:
    """Class to manage document loading and vector store creation"""
    
    def __init__(self, embedding_model):
        """Initialize with an embedding model"""
        self.embedding_model = embedding_model
        self.documents = []
        self.vectorstore = None
        self.retriever = None
        
    def load_documents(self, file_path=None):
        """Load documents from a JSON file"""
        if not file_path:
            # Default path
            base_dir = os.path.expanduser("~")
            file_path = os.path.join(base_dir, "Desktop", "IsDBI", "Data.json")
        
        print(f"Loading documents from {file_path}...")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.documents = []
            for item in data:
                file_name = item["file_name"]
                for page in item["content"]:
                    text = page.get("text", "").strip()
                    if text:
                        self.documents.append(Document(
                            page_content=text,
                            metadata={"source": file_name, "page": page.get("page")}
                        ))
            print(f"Loaded {len(self.documents)} document chunks successfully")
            return True
        except Exception as e:
            print(f"Error loading documents: {str(e)}")
            return False
            
    def build_vectorstore(self):
        """Build vector store from loaded documents"""
        if not self.documents:
            print("No documents loaded. Load documents first.")
            return False
            
        print("Building vector store...")
        self.vectorstore = FAISS.from_documents(self.documents, self.embedding_model)
        self.retriever = self.vectorstore.as_retriever()
        print("Vector store built successfully")
        return True
        
    def get_retriever(self):
        """Return the document retriever"""
        return self.retriever
