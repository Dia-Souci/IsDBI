import argparse
import os
from rich.console import Console
from rich.table import Table
from server import AIServer
from model_manager import ModelManager

def main():
    """Main function to start the server with all AI components"""
    console = Console()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Start AI server with selected model")
    parser.add_argument(
        "--model", 
        type=str, 
        choices=["bloom", "llama2"], 
        default="bloom",
        help="Model to use: 'bloom' for local BLOOM 560M or 'llama2' for Ollama Llama 2"
    )
    parser.add_argument(
        "--model-path", 
        type=str, 
        default="./local_models/bloom-560m",
        help="Path to the local model (for BLOOM)"
    )
    parser.add_argument(
        "--ollama-url", 
        type=str, 
        default="http://localhost:11434",
        help="Ollama API base URL (for Llama 2)"
    )
    parser.add_argument(
        "--data-path", 
        type=str, 
        default=os.path.join(os.path.expanduser("~"), "Desktop", "IsDBI", "Data.json"),
        help="Path to the data JSON file"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8080,
        help="Server port (default: 8080)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Display available models in a table
    available_models = ModelManager.list_available_models()
    table = Table(title="Available Models")
    table.add_column("Model ID", style="cyan")
    table.add_column("Description", style="green")
    for model_id, model_desc in available_models.items():
        table.add_row(model_id, model_desc)
    console.print(table)
    
    console.print(f"[bold cyan]Using model:[/] [bold green]{args.model}[/]")
    
    # Initialize and start server
    server = AIServer(port=args.port)
    server.initialize_components(
        model_type=args.model,
        model_path=args.model_path,
        ollama_base_url=args.ollama_url,
        data_path=args.data_path
    )
    
    try:
        server.start()
    except KeyboardInterrupt:
        console.print("[bold yellow]Server stopped by user")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}")

if __name__ == "__main__":
    main()