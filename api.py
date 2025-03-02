from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from pathlib import Path
from utils.math_processor import MathProcessor
from utils.symbolic_processor import SymbolicProcessor
from utils.rag_pipeline import RagPipeline
from utils import rag

app = FastAPI(
    title="Math-Enhanced Local RAG API",
    description="API for mathematical question answering using RAG",
    version="1.0.0"
)

# Initialize processors and pipeline
math_processor = MathProcessor()
symbolic_processor = SymbolicProcessor()
rag_pipeline = RagPipeline(math_processor, symbolic_processor)
# Set storage directory to indexes
rag_pipeline.storage_dir = "indexes"

# Create necessary directories
os.makedirs("pdfs", exist_ok=True)
os.makedirs("indexes", exist_ok=True)

class Query(BaseModel):
    question: str
    top_k: Optional[int] = 3

class MathAnalysis(BaseModel):
    latex: str

@app.post("/query")
async def query_endpoint(query: Query):
    """
    Process a mathematical query and return the answer with sources
    """
    try:
        response = rag_pipeline.query(
            question=query.question,
            top_k=query.top_k
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-math")
async def analyze_math(analysis: MathAnalysis):
    """
    Analyze a LaTeX expression
    """
    try:
        expr = symbolic_processor.parse_expression(analysis.latex)
        if expr is None:
            raise HTTPException(status_code=400, detail="Failed to parse LaTeX")
            
        result = symbolic_processor.analyze_expression(expr)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload and process mathematical documents
    
    Files will be saved to:
    - PDFs: saved in 'pdfs' folder
    - Vector indexes: created and stored in 'indexes' folder
    """
    try:
        # Save PDFs to the pdfs folder first
        for file in files:
            if file.name.lower().endswith('.pdf'):
                pdf_path = Path("pdfs") / file.name
                file_content = await file.read()
                with open(pdf_path, "wb") as f:
                    f.write(file_content)
                
                # Reset the file pointer to the beginning
                await file.seek(0)
        
        # Process documents using the RAG pipeline
        error = rag.rag_pipeline(files)
        if error is not None:
            raise HTTPException(status_code=500, detail=str(error))
            
        return {
            "message": "Files processed successfully",
            "pdfs_location": "pdfs/",
            "indexes_location": "indexes/"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)