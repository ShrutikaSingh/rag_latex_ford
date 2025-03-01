import re
from typing import List, Dict, Any
import logging
from pathlib import Path
from utils import logs

class MathProcessor:
    """Handles LaTeX expressions and mathematical content processing"""
    
    def __init__(self):
        self.latex_patterns = {
            'inline': r'\$(.*?)\$',
            'display': r'\\\[(.*?)\\\]',
            'equation': r'\\begin\{equation\}(.*?)\\end\{equation\}',
            'align': r'\\begin\{align\}(.*?)\\end\{align\}'
        }
        logs.log.info("Math processor initialized")

    def extract_latex(self, text: str) -> List[Dict[str, Any]]:
        """Extract LaTeX expressions from text with metadata"""
        expressions = []
        
        for env_type, pattern in self.latex_patterns.items():
            matches = re.finditer(pattern, text, re.DOTALL)
            for match in matches:
                expressions.append({
                    'type': env_type,
                    'content': match.group(1),
                    'full_match': match.group(0),
                    'position': match.span(),
                    'normalized': self._normalize_latex(match.group(1))
                })
        
        return expressions

    def _normalize_latex(self, latex: str) -> str:
        """Normalize LaTeX expression for better matching"""
        latex = re.sub(r'\s+', ' ', latex.strip())
        replacements = {
            r'\\left\(': '(',
            r'\\right\)': ')',
            r'\\left\[': '[',
            r'\\right\]': ']',
            r'\\left\\{': '\\{',
            r'\\right\\}': '\\}',
        }
        for old, new in replacements.items():
            latex = re.sub(old, new, latex)
        return latex

    def enhance_document(self, text: str, metadata: Dict = None) -> Dict[str, Any]:
        """Enhance document with mathematical content analysis"""
        if metadata is None:
            metadata = {}
            
        expressions = self.extract_latex(text)
        metadata['math_expressions'] = expressions
        metadata['math_expression_count'] = len(expressions)
        
        searchable_text = text
        for expr in expressions:
            searchable_text += f"\n[MATH_EXPR_{expr['type']}]: {expr['normalized']}"
            
        return {
            'text': text,
            'searchable_text': searchable_text,
            'metadata': metadata
        }

    def format_latex_for_display(self, text: str) -> str:
        """Format LaTeX expressions for proper display"""
        text = re.sub(r'([^\s])\$\$', r'\1 $$', text)
        text = re.sub(r'\$\$([^\s])', r'$$ \1', text)
        text = re.sub(
            r'\\begin\{equation\}(.*?)\\end\{equation\}',
            r'$$\1$$',
            text,
            flags=re.DOTALL
        )
        return text