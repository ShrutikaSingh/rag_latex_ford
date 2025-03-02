# Math-Enhanced Local RAG System Documentation

## Overview
A local Retrieval-Augmented Generation (RAG) system specialized for mathematical question answering, featuring LaTeX support, symbolic mathematics processing, and advanced document handling capabilities.

![rag_latex](https://github.com/user-attachments/assets/a295f6b4-2587-40df-92ef-df30b03671e7)

## Core Features I implemented

### 1. Mathematical Processing
- **LaTeX Support**: Full LaTeX expression parsing and rendering
- **Symbolic Math**: Built-in symbolic computation using SymPy
- **Step-by-Step Solutions**: Detailed mathematical problem solving

### 2. User Interface
<img width="1680" alt="Screenshot 2025-02-27 at 11 30 06 PM" src="https://github.com/user-attachments/assets/137d92ad-1641-4302-b1f7-94adec51f8ce" />

- **LaTeX Rendering**: Beautiful display of mathematical formulas in both queries and responses
- **Source Attribution**: Clear presentation of reference sources with relevance scores
- **Progressive Feedback**: Step-by-step visibility into query processing stages
- **Improved UI**: Math-friendly interface that correctly formats and displays LaTeX expressions for clear, readable mathematical content
- **Expandable Sources**: Collapsible sections showing reference materials used to generate answers
- **Sliding Sidebar**: Navigation panel that provides easy access to configuration options, file uploads, and system settings
- **Chunking Slider**: Interactive slider control for fine-tuning document chunking size, allowing users to balance between retrieval precision and processing efficiency

### 3. Document Handling
- **PDF & Other file Processing**: Extraction of mathematical content in from pdfs & files
- **LaTeX-Aware Indexing**: Specialized indexing for mathematical expressions
- **Context Preservation**: Maintains mathematical relationships
- **Optimized Storage**: Organized storage with separate directories for PDFs and indexes

### 4. RAG Capabilities
- **Local Inference**: Uses Ollama models for offline operation
- **Semantic Search**: Advanced mathematical concept matching
- **Context-Aware Responses**: Mathematically accurate answers
- **Vector Store Indexing**: Efficient retrieval of relevant mathematical information

## Quick Installation
```bash
# Clone repository
git clone [https://github.com/yourusername/math-enhanced-rag](https://github.com/ShrutikaSingh/rag_latex_ford)
cd rag_latex_ford

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
- `pip install pipenv && pipenv install`
- `pipenv shell && streamlit run main.py`

# Start Ollama in other termina
ollama serve
ollama pull llama2:7b

# Run application
streamlit run main.py

# In separate terminal you can run the api
python api.py
```



## Technical Implementation Details

### 1. PDF Processing Workflow
1. **Upload Detection**: System detects and validates uploaded PDF files
2. **File Storage**: PDFs are stored in the `pdfs/` directory
3. **Duplicate Check**: Hash-based verification prevents reprocessing identical files
4. **Content Extraction**: Mathematical content is extracted with structure preservation
5. **LaTeX Identification**: LaTeX expressions are identified and parsed
6. **Indexing**: Vector embeddings are created and stored in the `indexes/` directory

### 2. Query Processing Workflow
1. **Query Analysis**: Input is analyzed for mathematical expressions
2. **Embedding Generation**: Query is converted to vector embeddings
3. **Cache Check**: System checks if similar query exists in cache
4. **Retrieval**: Relevant document chunks are retrieved using vector similarity
5. **LLM Integration**: Ollama model generates comprehensive response
6. **Result Formatting**: Response is enhanced with proper LaTeX formatting


## System Architecture
```plaintext
math-enhanced-rag/
├── main.py              # Streamlit UI
├── api.py              # FastAPI endpoints
├── utils/
│   ├── math_processor.py    # LaTeX handling
│   ├── symbolic_processor.py # Math operations
│   ├── rag_pipeline.py      # Core RAG logic
│   ├── pdf_processor.py     # Document processing
│   └── ollama.py           # Model integration
└── components/             # UI elements 
```

## Configuration

### Environment Variables
```plaintext
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama2:7b
DEBUG=False
```

### Model Settings
```yaml
model:
  name: "llama2:7b"
  request_timeout: 60
  context_window: 2048

indexing:
  chunk_size: 512
  overlap: 50
  top_k: 3

math:
  latex_support: true
  symbolic_processing: true
```

## API Endpoints

### 1. Query Endpoint
```plaintext
POST /query
```
#### Request
```json
{
    "question": "Solve x^2 + 2x + 1 = 0",
    "top_k": 3
}
```
#### Response
```json
{
    "answer": "Step-by-step solution...",
    "sources": [...],
    "math_expressions": [...]
}
```

### 2. Math Analysis
```plaintext
POST /analyze-math
```
#### Request
```json
{
    "latex": "\\frac{d}{dx}x^2"
}
```
#### Response
```json
{
    "simplified": "2x",
    "steps": [...]
}
```

### 3. Document Upload
```plaintext
POST /upload
```
- Accepts PDF, TXT, TEX files
- Returns processing status and index information


## API Usage Examples

### 1. Basic Query
```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "question": "What is the derivative of x^2?"
    }
)
print(response.json())
```

### 2. Document Processing
```python
files = {
    'file': open('math_document.pdf', 'rb')
}
response = requests.post(
    "http://localhost:8000/upload",
    files=files
)
```

### 3. Math Analysis
```python
response = requests.post(
    "http://localhost:8000/analyze-math",
    json={
        "latex": "\\int x^2 dx"
    }
)
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Ollama Connection
```shell
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart if needed
ollama serve
```