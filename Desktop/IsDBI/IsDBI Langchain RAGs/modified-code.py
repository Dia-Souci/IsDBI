from langchain.llms import HuggingFacePipeline, Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import cgi
from rich.console import Console
from rich.panel import Panel
from rich import box
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document


# First, let's modify the AAOIFIAgentChain class to add methods for the new endpoints
class AAOIFIAgentChain:
    """Class to manage the AAOIFI agent chains with RAG capabilities"""
    
    def __init__(self, llm, retriever=None):
        """
        Initialize with an LLM and optional retriever
        
        Args:
            llm: The language model to use
            retriever: Document retriever for RAG functionality
        """
        self.llm = llm
        self.retriever = retriever
        self.console = Console()
        self.review_chain = None
        self.enhancement_chain = None
        self.validation_chain = None
        self.multi_agent_chain = None
        self.custom_qa_chain = None  # New chain for challenge_1
        self._setup_chains()
        
    def _setup_chains(self):
        """Set up all the necessary chains"""
        # Define prompts with RAG integration
        review_prompt = PromptTemplate(
            input_variables=["input_text", "retrieved_context"],
            template="""
You are a specialized agent for reviewing AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions) standards.
            
Your task is to carefully analyze the provided standard text and extract key elements including:
1. Main principles and requirements
2. Key definitions and concepts
3. Compliance requirements
4. Areas that might need clarification or enhancement
5. Current limitations or ambiguities
6. The specific Islamic finance principles and Shariah considerations involved

Please organize your analysis in a structured format focusing on these key elements.

Here is relevant contextual information from our knowledge base that may help your analysis:
{retrieved_context}

Standard text to analyze:
{input_text}
"""
        )

        enhancement_prompt = PromptTemplate(
            input_variables=["summary", "retrieved_context"],
            template="""
You are a specialized agent for proposing AI-driven enhancements to AAOIFI standards.
            
Based on the analysis of the standard provided and current trends in Islamic finance, propose specific modifications or enhancements that would:
1. Improve clarity and reduce ambiguity
2. Enhance practical applicability
3. Address any identified gaps or limitations
4. Incorporate modern financial practices while maintaining Shariah compliance
5. Improve standardization and consistency

For each proposed enhancement, explain:
- The specific section or concept being enhanced
- The proposed modification
- The rationale behind the enhancement
- The expected impact on standard implementation
- How it aligns with Shariah principles

Here is relevant contextual information from our knowledge base that may help inform your enhancement suggestions:
{retrieved_context}

Standard analysis:
{summary}
"""
        )

        validation_prompt = PromptTemplate(
            input_variables=["input_text", "suggestion", "retrieved_context"],
            template="""
You are a specialized agent for validating proposed enhancements to AAOIFI standards.
            
Your task is to rigorously evaluate the proposed enhancements based on:
1. Compliance with Shariah principles and Islamic finance fundamentals
2. Consistency with the original intent and purpose of the standard
3. Practical applicability in Islamic financial institutions
4. Potential impacts on transparency, governance, and stakeholder interests
5. Technical accuracy and clarity

For each proposed enhancement:
- Determine if it aligns with core Islamic finance principles (e.g., prohibition of riba, gharar, and maysir)
- Evaluate if it maintains or improves the standard's effectiveness
- Identify any potential unintended consequences
- Provide a final recommendation: Approve, Approve with modifications, or Reject
- For any modifications or rejections, provide clear reasoning based on Shariah principles

Here is relevant contextual information from our knowledge base that may help in your validation:
{retrieved_context}

Original standard information:
{input_text}

Proposed enhancements:
{suggestion}
"""
        )
        
        # New prompt for challenge_1 - Direct Q&A
        qa_prompt = PromptTemplate(
            input_variables=["context", "question", "retrieved_context"],
            template="""
You are an expert in Islamic finance and AAOIFI standards. A user has asked a question related to 
Islamic finance or AAOIFI standards. Please provide a detailed, accurate, and helpful response based 
on the provided context and your knowledge of Islamic finance principles.

Here is the context provided by the user:
{context}

Here is relevant contextual information from our knowledge base that may help:
{retrieved_context}

User's question:
{question}

Please provide a comprehensive and accurate answer to the question based on the context provided.
"""
        )

        # Define LLMChains
        self.review_chain = LLMChain(llm=self.llm, prompt=review_prompt, output_key="summary")
        self.enhancement_chain = LLMChain(llm=self.llm, prompt=enhancement_prompt, output_key="suggestion")
        self.validation_chain = LLMChain(llm=self.llm, prompt=validation_prompt, output_key="validation")
        self.custom_qa_chain = LLMChain(llm=self.llm, prompt=qa_prompt, output_key="answer")  # New chain for challenge_1

        # Define Sequential Chain
        self.multi_agent_chain = SequentialChain(
            chains=[self.review_chain, self.enhancement_chain, self.validation_chain],
            input_variables=["input_text", "retrieved_context"],
            output_variables=["summary", "suggestion", "validation"],
            verbose=False
        )
        
    def _retrieve_relevant_documents(self, query, max_docs=3):
        """
        Retrieve relevant documents based on query
        
        Args:
            query: The query to search for
            max_docs: Maximum number of documents to retrieve
            
        Returns:
            String containing relevant context or message if retriever not available
        """
        if not self.retriever:
            return "No document retriever available. Proceeding without additional context."
            
        try:
            docs = self.retriever.get_relevant_documents(query, k=max_docs)
            if not docs:
                return "No relevant documents found in knowledge base."
                
            context_parts = []
            for i, doc in enumerate(docs):
                source = doc.metadata.get("source", "Unknown source")
                page = doc.metadata.get("page", "Unknown page")
                context_parts.append(f"Document {i+1} (Source: {source}, Page: {page}):\n{doc.page_content}\n")
                
            return "\n".join(context_parts)
        except Exception as e:
            self.console.print(f"[bold red]Error retrieving documents: {str(e)}")
            return "Error retrieving documents from knowledge base."
    
    def _retrieve_top_fas_rules(self, query, max_docs=3):
        """
        Retrieve top FAS rules with similarity percentages
        
        Args:
            query: The query to search for
            max_docs: Maximum number of documents to retrieve
            
        Returns:
            List of tuples with (document, score) or empty list if retriever not available
        """
        if not self.retriever or not hasattr(self.retriever, 'vectorstore'):
            return []
            
        try:
            # Use similarity search with scores if available
            if hasattr(self.retriever.vectorstore, 'similarity_search_with_score'):
                docs_and_scores = self.retriever.vectorstore.similarity_search_with_score(query, k=max_docs)
                return docs_and_scores
            else:
                # Fallback if similarity_search_with_score is not available
                docs = self.retriever.get_relevant_documents(query, k=max_docs)
                # Return docs with a placeholder score since actual scores aren't available
                return [(doc, 0.0) for doc in docs]
        except Exception as e:
            self.console.print(f"[bold red]Error retrieving FAS rules: {str(e)}")
            return []
            
    def process_standard(self, input_text):
        """
        Process a standard through the multi-agent chain with RAG integration
        
        Args:
            input_text: The standard text to analyze
            
        Returns:
            Dictionary with results from each step
        """
        self.console.print("[bold]Processing standard through agent chain with RAG integration...")
        
        # Create a shorter version for retrieval query
        query_text = input_text[:1000] if len(input_text) > 1000 else input_text
        
        # Step 1: Review
        self.console.print("[bold cyan]Step 1: Retrieving context for review phase...")
        review_context = self._retrieve_relevant_documents(query_text)
        self.console.print("[bold cyan]Running review analysis...")
        summary = self.review_chain.invoke({"input_text": input_text, "retrieved_context": review_context})["summary"]
        
        # Step 2: Enhancement
        self.console.print("[bold cyan]Step 2: Retrieving context for enhancement phase...")
        enhancement_context = self._retrieve_relevant_documents(summary)
        self.console.print("[bold cyan]Generating enhancement suggestions...")
        suggestion = self.enhancement_chain.invoke({"summary": summary, "retrieved_context": enhancement_context})["suggestion"]
        
        # Step 3: Validation
        self.console.print("[bold cyan]Step 3: Retrieving context for validation phase...")
        validation_context = self._retrieve_relevant_documents(suggestion)
        self.console.print("[bold cyan]Validating enhancement suggestions...")
        validation = self.validation_chain.invoke({
            "input_text": input_text, 
            "suggestion": suggestion, 
            "retrieved_context": validation_context
        })["validation"]
        
        # Combine results
        output = {
            "summary": summary,
            "suggestion": suggestion,
            "validation": validation
        }
        
        return output
    
    # New method for challenge_1
    def answer_question(self, context, question):
        """
        Answer a question based on context through the custom QA chain
        
        Args:
            context: The context provided by the user
            question: The question to answer
            
        Returns:
            Dictionary with answer
        """
        self.console.print("[bold]Processing question through QA chain with RAG integration...")
        
        # Create a query combining context and question for better retrieval
        query_text = f"{context} {question}"
        if len(query_text) > 1000:
            query_text = query_text[:1000]
        
        # Retrieve relevant context
        self.console.print("[bold cyan]Retrieving context for question...")
        retrieved_context = self._retrieve_relevant_documents(query_text)
        
        # Process through QA chain
        self.console.print("[bold cyan]Generating answer...")
        answer = self.custom_qa_chain.invoke({
            "context": context,
            "question": question,
            "retrieved_context": retrieved_context
        })["answer"]
        
        # Return result
        return {"answer": answer}
    
    # New method for challenge_2
    def find_relevant_fas_rules(self, context, question):
        """
        Find top 3 relevant FAS rules with similarity percentages
        
        Args:
            context: The context provided by the user
            question: The question to answer
            
        Returns:
            Dictionary with results including top rules and percentages
        """
        self.console.print("[bold]Finding relevant FAS rules with percentages...")
        
        # Create a query combining context and question for better retrieval
        query_text = f"{context} {question}"
        if len(query_text) > 1000:
            query_text = query_text[:1000]
        
        # Retrieve top FAS rules with scores
        docs_and_scores = self._retrieve_top_fas_rules(query_text, max_docs=3)
        
        if not docs_and_scores:
            return {
                "message": "No relevant FAS rules found or retriever not available.",
                "rules": []
            }
        
        # Process results
        rules = []
        # Find max score for normalization if needed
        max_score = max([score for _, score in docs_and_scores]) if docs_and_scores else 1.0
        
        for doc, score in docs_and_scores:
            # Normalize score to percentage (assuming higher score is better)
            # Convert to percentage and invert if needed (depends on the scoring system)
            # Some similarity scores are distance-based (lower is better), some are cosine (higher is better)
            # Adjust this calculation based on your specific embedding model
            percentage = (score / max_score) * 100
            
            rules.append({
                "source": doc.metadata.get("source", "Unknown source"),
                "page": doc.metadata.get("page", "Unknown page"),
                "content_snippet": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "relevance_percentage": round(percentage, 2)
            })
        
        # Return results
        return {
            "message": f"Found {len(rules)} relevant FAS rules.",
            "rules": rules
        }
        
    def display_results(self, output):
        """Display the results using rich formatting"""
        self.console.rule("[bold green]Step 1: Review Output")
        self.console.print(Panel(output['summary'], title="🧠 Extracted Summary", style="white", box=box.ROUNDED))

        self.console.rule("[bold yellow]Step 2: Enhancement Suggestion")
        self.console.print(Panel(output['suggestion'], title="🛠️ Suggested Enhancement", style="white", box=box.ROUNDED))

        self.console.rule("[bold blue]Step 3: Validation Result")
        self.console.print(Panel(output['validation'], title="✅ Validation", style="white", box=box.ROUNDED))
        
        return output
        
    def set_retriever(self, retriever):
        """Set or update the document retriever"""
        self.retriever = retriever
        self.console.print("[bold green]Document retriever updated successfully")


# Now, let's modify the AIRequestHandler in the AIServer class to handle the modified endpoints
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

# Keep the rest of the code (main function, ModelManager, DocumentManager) as is
