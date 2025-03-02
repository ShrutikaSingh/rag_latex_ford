import os
from pathlib import Path
from typing import List, Any, Optional
import shutil

from utils import logs
from utils.math_processor import MathProcessor
from utils.symbolic_processor import SymbolicProcessor
from utils.rag_pipeline import RagPipeline

def rag_pipeline(uploaded_files=None):
    """
    Process uploaded files or documents in data directory through the RAG pipeline.
    
    Args:
        uploaded_files (list, optional): List of uploaded files to process.
        
    Returns:
        error: Any error that occurred during processing, or None if successful.
    """
    try:
        # Initialize processors and pipeline
        math_processor = MathProcessor()
        symbolic_processor = SymbolicProcessor()
        rag_pipeline = RagPipeline(math_processor, symbolic_processor)
        
        # Create necessary directories
        os.makedirs("pdfs", exist_ok=True)
        os.makedirs("indexes", exist_ok=True)
        
        # Update storage directory to use indexes folder
        rag_pipeline.storage_dir = "indexes"
        
        # If files were provided, process them
        if uploaded_files:
            # Copy uploaded files to pdfs directory first
            for file in uploaded_files:
                if file.name.lower().endswith('.pdf'):
                    pdf_path = Path("pdfs") / file.name
                    with open(pdf_path, "wb") as f:
                        # Reset file pointer to beginning
                        file.seek(0)
                        file_content = file.read()
                        f.write(file_content)
                        logs.log.info(f"Saved PDF {file.name} to pdfs directory")
                        
                    # Reset file pointer again for processing
                    file.seek(0)
                
            # Process the documents to create indexes
            rag_pipeline.process_documents(uploaded_files)
            logs.log.info("Documents processed successfully")
            
        return None  # No errors
    except Exception as e:
        logs.log.error(f"Error in RAG pipeline: {e}")
        return e  # Return the error 