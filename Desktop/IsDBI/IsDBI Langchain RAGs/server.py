from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
from rich.console import Console
from rich.panel import Panel
from rich import box

class AIServer:
    """Class to manage the AI server with RAG integration"""
    
    def __init__(self, port=8000):
        """Initialize the server with the specified port"""
        self.port = port
        self.model_manager = None
        self.document_manager = None
        self.agent_chain = None
        self.console = Console()
        
    def initialize_components(self, model_type="bloom", model_path="./local_models/bloom-560m", 
                             ollama_base_url="http://localhost:11434", data_path=None):
        """
        Initialize all AI components
        
        Args:
            model_type (str): Type of model to use - 'bloom' or 'llama2'
            model_path (str): Path to local model (for BLOOM)
            ollama_base_url (str): Base URL for Ollama API (for Llama 2)
            data_path (str): Path to data JSON file
        """
        # Import here to avoid circular imports
        from model_manager import ModelManager
        from document_manager import DocumentManager
        from agent_chain import AAOIFIAgentChain
        
        self.console.print(Panel(
            "Initializing AI components...",
            title="[bold]System Startup",
            style="blue",
            box=box.ROUNDED
        ))
        
        # Initialize model manager and load models
        self.console.print(f"[bold]Setting up {model_type.upper()} model...")
        self.model_manager = ModelManager(
            model_type=model_type,
            model_path=model_path,
            ollama_base_url=ollama_base_url
        )
        self.model_manager.load_models()
        
        # Initialize document manager and load documents
        self.console.print("[bold]Setting up document manager...")
        self.document_manager = DocumentManager(self.model_manager.get_embedding_model())
        
        # Load documents if path provided
        if data_path:
            success = self.document_manager.load_documents(file_path=data_path)
            if success:
                self.console.print(f"[bold green]Successfully loaded documents from {data_path}")
                success = self.document_manager.build_vectorstore()
                if success:
                    self.console.print("[bold green]Successfully built vector store")
                else:
                    self.console.print("[bold red]Failed to build vector store")
            else:
                self.console.print(f"[bold red]Failed to load documents from {data_path}")
        else:
            self.console.print("[bold yellow]Warning: No data path provided. Document processing skipped.")
        
        # Initialize agent chain with retriever if available
        self.console.print("[bold]Initializing agent chain...")
        retriever = self.document_manager.get_retriever() if hasattr(self.document_manager, 'retriever') and self.document_manager.retriever else None
        self.agent_chain = AAOIFIAgentChain(self.model_manager.get_llm(), retriever)
        
        self.console.print(Panel(
            "All AI components initialized successfully",
            title="[bold green]Initialization Complete",
            style="green",
            box=box.ROUNDED
        ))
        
    def start(self):
        """Start the server"""
        server_address = ("", self.port)
        
        # Create a request handler with access to AI components
        ai_server = self
        
        class AIRequestHandler(BaseHTTPRequestHandler):
            def _set_headers(self, content_type="application/json", code=200):
                self.send_response(code)
                self.send_header("Content-type", content_type)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
            def do_OPTIONS(self):
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def do_POST(self):
                # Normalize path to lowercase for case-insensitive matching
                normalized_path = self.path.lower()
                
                # Handle challenge_1 endpoint - Answer a question based on context
                if normalized_path == "/challenge_1" or self.path == "/Challenge_1":
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length)
                    try:
                        data = json.loads(body)
                        context = data.get("context")
                        question = data.get("question")
                        if not context or not question:
                            raise ValueError("Missing context or question.")
                        
                        # Use the agent chain's new method to answer the question
                        ai_server.console.print(f"[bold blue]Processing question from {self.client_address[0]} to {self.path}")
                        output = ai_server.agent_chain.answer_question(context, question)
                        
                        response = {
                            "answer": output["answer"]
                        }
                        
                        self._set_headers()
                        self.wfile.write(json.dumps(response).encode())
                        ai_server.console.print(f"[bold green]Successfully processed question from {self.client_address[0]}")
                    except Exception as e:
                        ai_server.console.print(f"[bold red]Error processing request: {str(e)}")
                        self._set_headers(code=400)
                        self.wfile.write(json.dumps({"error": str(e)}).encode())
                
                # Handle challenge_2 endpoint - Find relevant FAS rules with percentages
                elif normalized_path == "/challenge_2" or self.path == "/Challenge_2":
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length)
                    try:
                        data = json.loads(body)
                        context = data.get("context")
                        question = data.get("question")
                        if not context or not question:
                            raise ValueError("Missing context or question.")
                        
                        # Use the agent chain's new method to find relevant FAS rules with percentages
                        ai_server.console.print(f"[bold blue]Finding relevant FAS rules from {self.client_address[0]} to {self.path}")
                        output = ai_server.agent_chain.find_relevant_fas_rules(context, question)
                        
                        response = output  # The output is already formatted correctly
                        
                        self._set_headers()
                        self.wfile.write(json.dumps(response).encode())
                        ai_server.console.print(f"[bold green]Successfully found relevant FAS rules for {self.client_address[0]}")
                    except Exception as e:
                        ai_server.console.print(f"[bold red]Error processing request: {str(e)}")
                        self._set_headers(code=400)
                        self.wfile.write(json.dumps({"error": str(e)}).encode())

                # Keep the existing endpoints
                elif normalized_path == "/challenge_3" or self.path == "/Challenge_3":
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length)
                    try:
                        data = json.loads(body)
                        context = data.get("context")
                        question = data.get("question")
                        if not context or not question:
                            raise ValueError("Missing context or question.")
                        
                        # Use the agent chain to process the input
                        ai_server.console.print(f"[bold blue]Processing request from {self.client_address[0]} to {self.path}")
                        output = ai_server.agent_chain.process_standard(context)
                        
                        response = {
                            "Analysis": output["summary"],
                            "suggestion": output["suggestion"],
                            "validation": output["validation"]
                        }
                        
                        self._set_headers()
                        self.wfile.write(json.dumps(response).encode())
                        ai_server.console.print(f"[bold green]Successfully processed request from {self.client_address[0]}")
                    except Exception as e:
                        ai_server.console.print(f"[bold red]Error processing request: {str(e)}")
                        self._set_headers(code=400)
                        self.wfile.write(json.dumps({"error": str(e)}).encode())

                elif normalized_path == "/challenge_4" or self.path == "/Challenge_4":
                    content_type = self.headers.get("Content-Type", "")
                    if "multipart/form-data" in content_type:
                        fs = cgi.FieldStorage(
                            fp=self.rfile,
                            headers=self.headers,
                            environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type},
                        )
                        file_item = fs["file"] if "file" in fs else None
                        question = fs.getvalue("question")

                        if file_item and file_item.file and question:
                            ai_server.console.print(f"[bold blue]Processing file upload from {self.client_address[0]}")
                            file_content = file_item.file.read().decode()
                            
                            # Process the file content with agent chain
                            output = ai_server.agent_chain.process_standard(file_content)
                            
                            response = {
                                "Analysis": output["summary"],
                                "suggestion": output["suggestion"],
                                "validation": output["validation"]
                            }
                            
                            self._set_headers()
                            self.wfile.write(json.dumps(response).encode())
                            ai_server.console.print(f"[bold green]Successfully processed file upload from {self.client_address[0]}")
                        else:
                            ai_server.console.print(f"[bold red]Missing file or question in request from {self.client_address[0]}")
                            self._set_headers(code=400)
                            self.wfile.write(json.dumps({"error": "Missing file or question."}).encode())
                    else:
                        ai_server.console.print(f"[bold red]Invalid content type in request from {self.client_address[0]}")
                        self._set_headers(code=400)
                        self.wfile.write(json.dumps({"error": "Expected multipart/form-data"}).encode())
                else:
                    ai_server.console.print(f"[bold red]Endpoint not found: {self.path} from {self.client_address[0]}")
                    self._set_headers(code=404)
                    self.wfile.write(json.dumps({"error": "Endpoint not found."}).encode())
                    
            def log_message(self, format, *args):
                # Override to prevent default logging
                return
        
        httpd = HTTPServer(server_address, AIRequestHandler)
        # Use rich for better formatting of the server startup message
        self.console.print(Panel(
            f"Server running at http://localhost:{self.port}",
            title="[bold green]Server Started Successfully",
            subtitle="[italic]Press Ctrl+C to stop",
            style="green",
            box=box.ROUNDED
        ))
        httpd.serve_forever()