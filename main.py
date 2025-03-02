import streamlit as st
import os
from pathlib import Path

from utils.math_processor import MathProcessor
from utils.symbolic_processor import SymbolicProcessor
from utils.rag_pipeline import RagPipeline
from components.ui_components import MathUI

def setup_environment():
    """Initialize the application environment"""
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("uploads").mkdir(exist_ok=True)
    Path("pdfs").mkdir(exist_ok=True)  # Directory for storing PDF documents
    Path("indexes").mkdir(exist_ok=True)  # Directory for storing vector indexes
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "math_mode" not in st.session_state:
        st.session_state.math_mode = True

def main():
    st.set_page_config(
        page_title="Math-Enhanced Local RAG",
        page_icon="📐",
        layout="wide"
    )

    setup_environment()

    st.title("Math-Enhanced Local RAG System")
    st.sidebar.title("Configuration")

    # Initialize components
    math_processor = MathProcessor()
    symbolic_processor = SymbolicProcessor()
    rag_pipeline = RagPipeline(math_processor, symbolic_processor)
    # Set storage directory to indexes
    rag_pipeline.storage_dir = "indexes"
    ui = MathUI(rag_pipeline)

    # Sidebar controls
    with st.sidebar:
        st.header("Settings")
        model_name = st.selectbox(
            "Select Model",
            ["llama2:7b", "llama2:13b", "mistral:7b"],
            index=0
        )
        
        top_k = st.slider(
            "Number of relevant chunks (top-k)",
            min_value=1,
            max_value=10,
            value=3
        )

        st.header("Document Upload")
        uploaded_files = st.file_uploader(
            "Upload mathematical documents",
            accept_multiple_files=True,
            type=["pdf", "txt", "tex"]
        )

        if uploaded_files:
            if st.button("Process Document"):
                with st.spinner("Processing documents..."):
                    # Save PDFs to the pdfs folder first
                    for file in uploaded_files:
                        if file.name.lower().endswith('.pdf'):
                            pdf_path = Path("pdfs") / file.name
                            with open(pdf_path, "wb") as f:
                                # Reset file pointer first
                                file.seek(0)
                                f.write(file.read())
                                
                            # Reset file pointer again for processing
                            file.seek(0)
                    
                    # Process the documents
                    rag_pipeline.process_documents(uploaded_files)
                st.success("Documents processed successfully! PDFs saved to 'pdfs' folder and indexes created in 'indexes' folder.")

    # Main chat interface
    ui.render_chat_interface()

    # Footer
    st.markdown("---")
    st.markdown(
        "Math-Enhanced Local RAG System - Powered by LlamaIndex and Ollama"
    )

if __name__ == "__main__":
    main()