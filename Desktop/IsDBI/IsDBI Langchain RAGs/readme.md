# AAOIFI Standards AI Analysis Tool

An AI-powered tool for analyzing, enhancing, and validating AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions) standards.

## Project Structure

This project has been refactored into multiple files for better organization:

- `model_manager.py`: Manages AI model loading and configuration
- `document_manager.py`: Handles document loading and vector store creation
- `agent_chain.py`: Implements the AAOIFI agent chains with RAG capabilities
- `server.py`: Manages the HTTP server for API endpoints
- `main.py`: Entry point for starting the application

## Features

1. **Challenge 1**: Direct Q&A based on user context and questions
2. **Challenge 2**: Find relevant FAS rules with similarity percentages
3. **Challenge 3**: Process AAOIFI standards through multi-agent chain
4. **Challenge 4**: Process uploaded file content with multi-agent chain

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Install dependencies:
   ```
   pip install langchain transformers rich
   ```

3. For local BLOOM model:
   - Download the model to `./local_models/bloom-560m`
   
4. For Llama 2 model:
   - Install Ollama: https://ollama.ai/
   - Pull the Llama 2 model: `ollama pull llama2`

## Usage

Start the server with default settings:
```
python main.py
```

Start with custom settings:
```
python main.py --model llama2 --port 8080 --data-path /path/to/your/data.json
```

### Available Arguments

- `--model`: Model to use - 'bloom' (local) or 'llama2' (via Ollama)
- `--model-path`: Path to the local model (for BLOOM)
- `--ollama-url`: Ollama API base URL (for Llama 2)
- `--data-path`: Path to the data JSON file
- `--port`: Server port (default: 8080)

## API Endpoints

### Challenge 1: Direct Q&A
```
POST /challenge_1
{
    "context": "Your context here...",
    "question": "Your question here..."
}
```

### Challenge 2: Find Relevant FAS Rules
```
POST /challenge_2
{
    "context": "Your context here...",
    "question": "Your question here..."
}
```

### Challenge 3: Process AAOIFI Standard
```
POST /challenge_3
{
    "context": "AAOIFI standard text here...",
    "question": "Your question here..."
}
```

### Challenge 4: Process Uploaded File
```
POST /challenge_4
Content-Type: multipart/form-data
Form fields:
- file: The file to process
- question: Your question about the file
```

## Cross-Origin Resource Sharing (CORS)

All endpoints support CORS, allowing requests from any origin.

## Error Handling

Errors are returned in JSON format:
```json
{
    "error": "An Error Sample."
}
```