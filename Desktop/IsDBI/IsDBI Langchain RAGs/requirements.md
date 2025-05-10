# Core dependencies
langchain==0.0.267
transformers==4.31.0
faiss-cpu==1.7.4
torch==2.0.1
rich==13.5.2

# For the API and server
httpx==0.24.1

# For document processing
json5==0.9.14

# For embeddings
sentence-transformers==2.2.2

# For Ollama integration
ollama==0.1.0

# For HuggingFace models
huggingface-hub==0.16.4
accelerate==0.21.0

# Optional dependencies for better performance
nvidia-cuda-runtime-cu11==11.7.99  # Only if using NVIDIA GPU
nvidia-cudnn-cu11==8.5.0.96  # Only if using NVIDIA GPU
