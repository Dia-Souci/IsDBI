from langchain.llms import HuggingFacePipeline, Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os

class ModelManager:
    """Class to manage AI model loading and configuration"""
    
    def __init__(self, model_type="bloom", model_path="./local_models/bloom-560m", device=0, ollama_base_url="http://localhost:11434"):
        """
        Initialize the model manager with specified parameters
        
        Args:
            model_type (str): Type of model to use - 'bloom' or 'llama2'
            model_path (str): Path to the local model (for BLOOM)
            device (int): Device ID for model computation
            ollama_base_url (str): Base URL for Ollama API
        """
        self.model_type = model_type.lower()
        self.model_path = model_path
        self.device = device
        self.ollama_base_url = ollama_base_url
        
        # Model components
        self.tokenizer = None
        self.model = None
        self.llm = None
        self.embedding_model = None
        
    def load_models(self):
        """Load all required models"""
        self._load_llm()
        self._load_embedding_model()
        
    def _load_llm(self):
        """Load the LLM model based on selected type"""
        if self.model_type == "bloom":
            self._load_bloom_model()
        elif self.model_type == "llama2":
            self._load_llama2_model()
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}. Choose 'bloom' or 'llama2'.")
    
    def _load_bloom_model(self):
        """Load the BLOOM model from local path"""
        print(f"Loading BLOOM model from {self.model_path}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            
            llm_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
            )
            self.llm = HuggingFacePipeline(pipeline=llm_pipeline)
            print("BLOOM model loaded successfully")
        except Exception as e:
            print(f"Error loading BLOOM model: {str(e)}")
            raise
        
    def _load_llama2_model(self):
        """Load the Llama2 model from Ollama"""
        print("Loading Llama2 model via Ollama API...")
        try:
            self.llm = Ollama(
                base_url=self.ollama_base_url,
                model="llama2",
                temperature=0.7,
                num_predict=512,
            )
            print("Llama2 model connected successfully via Ollama")
        except Exception as e:
            print(f"Error connecting to Ollama API: {str(e)}")
            print("Make sure Ollama is running with Llama2 model installed.")
            print("Install Llama2 in Ollama using: 'ollama pull llama2'")
            raise
        
    def _load_embedding_model(self):
        """Load the embedding model"""
        print("Loading embedding model...")
        self.embedding_model = HuggingFaceEmbeddings()
        print("Embedding model loaded successfully")
        
    def get_llm(self):
        """Return the loaded LLM"""
        if not self.llm:
            self._load_llm()
        return self.llm
        
    def get_embedding_model(self):
        """Return the loaded embedding model"""
        if not self.embedding_model:
            self._load_embedding_model()
        return self.embedding_model
        
    @staticmethod
    def list_available_models():
        """List available model options"""
        models = {
            "bloom": "BLOOM 560M (Local)",
            "llama2": "Llama 2 (via Ollama)"
        }
        return models
