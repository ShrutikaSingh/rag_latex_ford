from typing import List, Dict, Any
import logging
from pathlib import Path
import os
import json
from tenacity import retry, stop_after_attempt, wait_exponential
import httpx
from tqdm import tqdm
from llama_index.core import (
    VectorStoreIndex,
    Document,
    ServiceContext,
    Settings,
    StorageContext,
    load_index_from_storage
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from utils import logs
from utils.math_processor import MathProcessor
from utils.symbolic_processor import SymbolicProcessor
from utils.latex_symbols_processor import LatexSymbolsProcessor
from pypdf import PdfReader
from tenacity import retry, stop_after_attempt, wait_exponential


class RagPipeline:
   def __init__(self, math_processor: MathProcessor, symbolic_processor: SymbolicProcessor):
        self.math_processor = math_processor
        self.symbolic_processor = symbolic_processor
        self.latex_processor = LatexSymbolsProcessor()
        self.index = None
        self.llm = None
        self.embedding_model = None
        self.storage_dir = "data/index_storage"
        print("Initializing RAG Pipeline...")
        with tqdm(total=3, desc="Setup Progress") as pbar:
            self.setup_models()
            pbar.update(1)
            self.load_existing_index()
            pbar.update(1)
            logs.log.info("RAG pipeline initialized")
            pbar.update(1)

   def setup_models(self):
        """Initialize LLM and embedding models"""
        try:
            with tqdm(total=3, desc="Setting up models") as pbar:
                import warnings
                warnings.filterwarnings('ignore', category=UserWarning)
                pbar.update(1)
                
                # Increase timeout and add threading
                self.llm = Ollama(
                    model="llama2:7b",
                    base_url="http://localhost:11434",
                    request_timeout=60.0,  # 3 minutes
                    additional_kwargs={
                        "num_ctx": 2048,
                        "num_thread": 4
                    }
                )
                Settings.llm = self.llm
                pbar.update(1)
                
                self.embedding_model = HuggingFaceEmbedding(
                    model_name="BAAI/bge-large-en-v1.5",
                    cache_folder="./models",
                    max_length=512,
                    embed_batch_size=4
                )
                Settings.embed_model = self.embedding_model
                pbar.update(1)
                
                logs.log.info("Models initialized successfully")
        except Exception as e:
            logs.log.error(f"Model initialization failed: {e}")
            raise
 
   def process_pdf(self, file_path: str) -> List[Document]:
       """Process PDF with enhanced LaTeX handling"""
       try:
           reader = PdfReader(file_path)
           documents = []
          
           for page_num, page in enumerate(reader.pages):
               try:
                   text = page.extract_text()
                  
                   # Extract math environments
                   math_envs = self.latex_processor.extract_math_environments(text)
                  
                   # Process each math environment
                   for env in math_envs:
                       searchable_text = self.latex_processor.create_searchable_text(env)
                      
                       # Get symbols and ensure they're JSON serializable
                       symbols = self.latex_processor.categorize_symbols(env['content'])
                      
                       doc = Document(
                           text=env['full'],  # Original LaTeX
                           metadata={
                               'type': 'math',
                               'math_type': env['type'],
                               'page': page_num + 1,
                               'searchable_text': searchable_text,
                               'symbols': symbols  # Now contains lists instead of sets
                           }
                       )
                       documents.append(doc)
                  
                   # Process remaining text
                   remaining_text = text
                   for env in math_envs:
                       remaining_text = remaining_text.replace(env['full'], '')
                  
                   if remaining_text.strip():
                       doc = Document(
                           text=remaining_text.strip(),
                           metadata={
                               'type': 'text',
                               'page': page_num + 1
                           }
                       )
                       documents.append(doc)
                      
               except Exception as e:
                   logs.log.warning(f"Error processing page {page_num + 1}: {str(e)}")
                   continue
          
           return documents
          
       except Exception as e:
           logs.log.error(f"Error processing PDF {file_path}: {str(e)}")
           raise


   def load_existing_index(self):
           """Load existing index if available"""
           try:
               if os.path.exists(self.storage_dir):
                   storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
                   self.index = load_index_from_storage(storage_context)
                   logs.log.info("Loaded existing index")
           except Exception as e:
               logs.log.warning(f"Could not load existing index: {e}")
               self.index = None


   def _ensure_json_serializable(self, obj):
       """Ensure all nested structures are JSON serializable"""
       if isinstance(obj, (str, int, float, bool, type(None))):
           return obj
       elif isinstance(obj, (list, tuple)):
           return [self._ensure_json_serializable(item) for item in obj]
       elif isinstance(obj, dict):
           return {key: self._ensure_json_serializable(value) for key, value in obj.items()}
       elif isinstance(obj, set):
           return list(obj)
       else:
           return str(obj)
   def process_documents(self, files: List[Any]) -> None:
       """Process uploaded documents with enhanced math handling"""
       documents = []
      
       for file in files:
           try:
               # Create uploads directory if it doesn't exist
               os.makedirs("uploads", exist_ok=True)
              
               temp_path = Path("uploads") / file.name
               with open(temp_path, "wb") as f:
                   f.write(file.read())
              
               # Process PDF
               if file.name.lower().endswith('.pdf'):
                   docs = self.process_pdf(str(temp_path))
                   for doc in docs:
                       # Ensure metadata is JSON serializable
                       doc.metadata = self._ensure_json_serializable(doc.metadata)
                   documents.extend(docs)
               else:
                   # Handle other file types
                   with open(temp_path, "r", encoding='utf-8') as f:
                       content = f.read()
                  
                   enhanced_doc = self.math_processor.enhance_document(content)
                   doc = Document(
                       text=enhanced_doc['searchable_text'],
                       metadata=self._ensure_json_serializable({
                           **enhanced_doc['metadata'],
                           'file_name': file.name
                       })
                   )
                   documents.append(doc)
              
               os.remove(temp_path)
              
           except Exception as e:
               logs.log.error(f"Error processing file {file.name}: {e}")
               continue
      
       if documents:
           self.create_index(documents)


   def create_index(self, documents: List[Document]) -> None:
       """Create or update the vector store index"""
       try:
           service_context = ServiceContext.from_defaults(
               llm=self.llm,
               embed_model=self.embedding_model
           )
          
           os.makedirs(self.storage_dir, exist_ok=True)
          
           self.index = VectorStoreIndex.from_documents(
               documents,
               service_context=service_context
           )
          
           self.index.storage_context.persist(persist_dir=self.storage_dir)
          
           logs.log.info("Index created and persisted successfully")
       except Exception as e:
           logs.log.error(f"Index creation failed: {e}")
           raise
       
   @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: {"error": "Query timed out after multiple attempts"}
    )
   def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """Query with enhanced math understanding and timeout handling"""
        if not self.index:
            self.load_existing_index()
            if not self.index:
                raise ValueError("No index available. Please process documents first.")
            
        try:
            with tqdm(total=5, desc="Processing query") as pbar:
                print("\nStep 1: Extracting math expressions...")
                math_expressions = self.latex_processor.extract_math_environments(question)
                pbar.update(1)
                
                print("Step 2: Setting up query engine...")
                # Split long questions if necessary
                max_chunk_length = 1000
                if len(question) > max_chunk_length:
                    print("Long question detected, splitting into chunks...")
                    chunks = [question[i:i + max_chunk_length] 
                             for i in range(0, len(question), max_chunk_length)]
                    responses = []
                    
                    with tqdm(total=len(chunks), desc="Processing chunks") as chunk_pbar:
                        for chunk in chunks:
                            query_engine = self.index.as_query_engine(
                                similarity_top_k=top_k,
                                system_prompt="""You are a mathematical assistant specialized in LaTeX and mathematical concepts.
                                When responding:
                                1. Always use proper LaTeX notation for mathematical expressions
                                2. Provide step-by-step explanations for mathematical problems
                                3. Include relevant mathematical theorems or definitions
                                4. Format complex equations using display math mode ($$...$$)
                                5. Use appropriate mathematical symbols and notations""",
                                streaming=False
                            )
                            print(f"\nProcessing chunk {chunk_pbar.n + 1}/{len(chunks)}...")
                            try:
                                chunk_response = query_engine.query(chunk)
                                responses.append(chunk_response)
                            except Exception as e:
                                print(f"Error processing chunk: {e}")
                                raise
                            chunk_pbar.update(1)
                    
                    # Combine responses
                    print("\nStep 3: Combining chunk responses...")
                    combined_response = " ".join([str(r.response) for r in responses])
                    sources = []
                    for r in responses:
                        sources.extend([{
                            'text': node.node.text[:200] + "...",
                            'score': float(node.score) if node.score else 0.0,
                            'metadata': node.node.metadata
                        } for node in r.source_nodes])
                else:
                    print("\nStep 3: Processing single query...")
                    query_engine = self.index.as_query_engine(
                        similarity_top_k=top_k,
                        system_prompt="""You are a mathematical assistant specialized in LaTeX and mathematical concepts.
                        When responding:
                        1. Always use proper LaTeX notation for mathematical expressions
                        2. Provide step-by-step explanations for mathematical problems
                        3. Include relevant mathematical theorems or definitions
                        4. Format complex equations using display math mode ($$...$$)
                        5. Use appropriate mathematical symbols and notations""",
                        streaming=False
                    )
                    
                    try:
                        print("Querying LLM (this might take a while)...")
                        response = query_engine.query(question)
                        combined_response = str(response.response)
                        sources = [{
                            'text': node.node.text[:200] + "...",
                            'score': float(node.score) if node.score else 0.0,
                            'metadata': node.node.metadata
                        } for node in response.source_nodes]
                    except httpx.TimeoutException as e:
                        print(f"\nTimeout occurred during LLM query: {e}")
                        raise
                    except Exception as e:
                        print(f"\nError during LLM query: {e}")
                        raise
                
                pbar.update(2)  # Update for steps 2 and 3
                
                print("\nStep 4: Formatting response...")
                # Format response with enhanced LaTeX handling
                formatted_response = combined_response
                if math_expressions:
                    for expr in math_expressions:
                        if expr['type'] == 'inline':
                            formatted_response = formatted_response.replace(
                                expr['content'],
                                f"${expr['content']}$"
                            )
                        else:
                            formatted_response = formatted_response.replace(
                                expr['content'],
                                f"$${expr['content']}$$"
                            )
                pbar.update(1)
                
                print("\nStep 5: Preparing final response...")
                result = {
                    'answer': formatted_response,
                    'sources': sources[:top_k],
                    'math_expressions': [
                        {
                            'type': expr['type'],
                            'content': expr['content']
                        } for expr in math_expressions
                    ] if math_expressions else []
                }
                pbar.update(1)
                
                print("\nQuery processing completed successfully!")
                return result
            
        except httpx.TimeoutException as e:
            print(f"\n❌ Query timed out: {e}")
            logs.log.error(f"Query timed out: {e}")
            raise
        except Exception as e:
            print(f"\n❌ Query failed: {e}")
            logs.log.error(f"Query failed: {e}")
            raise