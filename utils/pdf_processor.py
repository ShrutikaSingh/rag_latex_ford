

from pypdf import PdfReader
import re
from typing import List, Dict, Tuple
import logging


class PDFProcessor:
   def __init__(self):
       self.latex_patterns = {
           'inline': r'\$(.*?)\$',
           'display': r'\$\$(.*?)\$\$',
           'equation': r'\\begin\{equation\}(.*?)\\end\{equation\}',
           'align': r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}'
       }
       logging.info("PDF processor initialized")


   def extract_content_with_latex(self, pdf_path: str) -> List[Dict]:
       """
       Extract text and LaTeX formulas from PDF while preserving structure
       """
       try:
           reader = PdfReader(pdf_path)
           content_blocks = []
          
           for page_num, page in enumerate(reader.pages):
               text = page.extract_text()
              
               # Split text into blocks based on paragraphs
               paragraphs = text.split('\n\n')
              
               for paragraph in paragraphs:
                   if not paragraph.strip():
                       continue
                      
                   # Check for LaTeX content
                   latex_blocks = self._extract_latex_blocks(paragraph)
                  
                   if latex_blocks:
                       # Process blocks with LaTeX
                       current_pos = 0
                       for start, end, latex in latex_blocks:
                           # Add text before LaTeX if exists
                           if start > current_pos:
                               text_content = paragraph[current_pos:start].strip()
                               if text_content:
                                   content_blocks.append({
                                       'type': 'text',
                                       'content': text_content,
                                       'page': page_num + 1
                                   })
                          
                           # Add LaTeX block
                           content_blocks.append({
                               'type': 'latex',
                               'content': latex,
                               'page': page_num + 1
                           })
                           current_pos = end
                      
                       # Add remaining text if exists
                       if current_pos < len(paragraph):
                           text_content = paragraph[current_pos:].strip()
                           if text_content:
                               content_blocks.append({
                                   'type': 'text',
                                   'content': text_content,
                                   'page': page_num + 1
                               })
                   else:
                       # Add as regular text block
                       content_blocks.append({
                           'type': 'text',
                           'content': paragraph.strip(),
                           'page': page_num + 1
                       })
          
           return content_blocks
          
       except Exception as e:
           logging.error(f"Error processing PDF {pdf_path}: {str(e)}")
           raise


   def _extract_latex_blocks(self, text: str) -> List[Tuple[int, int, str]]:
       """
       Extract LaTeX blocks with their positions in text
       """
       blocks = []
       for pattern_name, pattern in self.latex_patterns.items():
           for match in re.finditer(pattern, text, re.DOTALL):
               blocks.append((match.start(), match.end(), match.group(0)))
      
       # Sort blocks by start position
       return sorted(blocks, key=lambda x: x[0])


   def _is_likely_latex(self, text: str) -> bool:
       """
       Check if text is likely to be a LaTeX formula
       """
       latex_indicators = [
           r'\$.*\$',
           r'\\begin\{.*?\}',
           r'\\end\{.*?\}',
           r'\\frac',
           r'\\sum',
           r'\\int',
           r'\\lim',
           r'\\mathbb',
           r'\\alpha|\\beta|\\gamma|\\delta'
       ]
      
       return any(re.search(pattern, text) for pattern in latex_indicators)


   def extract_latex_expressions(self, text: str) -> List[Tuple[str, str]]:
       """
       Extract LaTeX expressions and their types from text
       """
       expressions = []
       for expr_type, pattern in self.latex_patterns.items():
           matches = re.finditer(pattern, text, re.DOTALL)
           for match in matches:
               expressions.append((expr_type, match.group(1)))
       return expressions


   def normalize_latex(self, latex: str) -> str:
       """
       Normalize LaTeX expressions for consistent processing
       """
       # Remove extra whitespace
       latex = re.sub(r'\s+', ' ', latex.strip())
      
       # Standardize delimiters
       latex = re.sub(r'\\left\s*[\[(]', '\\left(', latex)
       latex = re.sub(r'\\right\s*[\])]', '\\right)', latex)
      
       # Standardize mathematical operators
       operator_map = {
           r'\\times': '*',
           r'\\cdot': '·',
           r'\\div': '÷'
       }
       for tex, symbol in operator_map.items():
           latex = latex.replace(tex, symbol)
          
       return latex