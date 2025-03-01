from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from utils.math_processor import MathProcessor
from utils.symbolic_processor import SymbolicProcessor
from utils.rag_pipeline import RagPipeline

app = FastAPI(
    title="Math-Enhanced Local RAG API",
    description="API for mathematical question answering using RAG",
    version="1.0.0"
)

# Initialize processors and pipeline
math_processor = MathProcessor()
symbolic_processor = SymbolicProcessor()
rag_pipeline = RagPipeline(math_processor, symbolic_processor)

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
    """
    try:
        rag_pipeline.process_documents(files)
        return {"message": "Files processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)