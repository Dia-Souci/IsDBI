# Ollama Setup Instructions

## Installing Ollama

If you plan to use the Llama2 model option in this application, you need to install Ollama separately, as it's not a Python package but a standalone application.

### Installation Steps

1. **Install Ollama**:
   - **For macOS**: Download from [ollama.ai](https://ollama.ai/)
   - **For Linux**:
     ```bash
     curl -fsSL https://ollama.ai/install.sh | sh
     ```
   - **For Windows**: Ollama is available via WSL2 (Windows Subsystem for Linux)

2. **Start Ollama**:
   After installation, make sure Ollama is running:
   ```bash
   ollama serve
   ```
   This will start the Ollama server on port 11434 by default.

3. **Pull the Llama2 model**:
   ```bash
   ollama pull llama2
   ```
   This may take some time depending on your internet connection as it downloads the model (~3.8GB).

## Verifying the Installation

To verify Ollama is working properly:

```bash
ollama list
```

You should see `llama2` in the list of available models.

## Using Llama2 with the Application

When running the application, specify the `llama2` model:

```bash
python main_py.py --model llama2
```

By default, the application will look for Ollama at `http://localhost:11434`. If you're running Ollama on a different host or port, use:

```bash
python main_py.py --model llama2 --ollama-url http://your-host:your-port
```

## Troubleshooting

- If you get connection errors, make sure Ollama is running with `ollama serve`
- Check that the model was downloaded properly with `ollama list`
- Ensure there are no firewall rules blocking access to port 11434
- For more help, visit [Ollama GitHub repository](https://github.com/ollama/ollama)
