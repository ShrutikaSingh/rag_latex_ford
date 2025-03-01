from typing import Dict, List, Set
import re

class LatexSymbolsProcessor:
    def __init__(self):
        # Common LaTeX math environments
        self.math_environments = [
            'equation', 'equation*', 'align', 'align*', 'gather', 'gather*',
            'multline', 'multline*', 'array', 'matrix', 'cases'
        ]
        
        # Initialize symbol mappings
        self.symbol_categories = {
            'greek': r'\\(?:alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega)',
            'operators': r'\\(?:sum|prod|int|oint|bigcup|bigcap|bigoplus|bigotimes|biguplus|bigsqcup)',
            'relations': r'\\(?:eq|neq|leq|geq|approx|sim|simeq|cong|equiv|prec|succ|subset|supset|subseteq|supseteq|in|ni|notin)',
            'delimiters': r'\\(?:left|right|langle|rangle|lfloor|rfloor|lceil|rceil|lbrace|rbrace|lbrack|rbrack|vert|Vert)',
            'functions': r'\\(?:sin|cos|tan|cot|sec|csc|arcsin|arccos|arctan|sinh|cosh|tanh|log|ln|exp|lim|sup|inf|max|min)'
        }

    def extract_math_environments(self, text: str) -> List[Dict[str, str]]:
        """Extract mathematical environments and their contents"""
        environments = []
        
        # Pattern for all math environments
        for env in self.math_environments:
            pattern = rf"\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}"
            matches = re.finditer(pattern, text, re.DOTALL)
            for match in matches:
                environments.append({
                    'type': env,
                    'content': match.group(1),
                    'full': match.group(0)
                })
        
        # Extract inline math $...$ and display math $$...$$
        inline_pattern = r'\$(.*?)\$'
        display_pattern = r'\$\$(.*?)\$\$'
        
        for match in re.finditer(inline_pattern, text):
            if not text[match.start()-2:match.start()].endswith('$$'):
                environments.append({
                    'type': 'inline',
                    'content': match.group(1),
                    'full': match.group(0)
                })
                
        for match in re.finditer(display_pattern, text):
            environments.append({
                'type': 'display',
                'content': match.group(1),
                'full': match.group(0)
            })
        
        return environments
    def categorize_symbols(self, latex: str) -> Dict[str, list]:
        """Categorize LaTeX symbols in the text"""
        # Initialize with lists instead of sets
        categories = {cat: [] for cat in self.symbol_categories.keys()}
        
        for category, pattern in self.symbol_categories.items():
            matches = re.finditer(pattern, latex)
            # Convert to list and remove duplicates while preserving order
            symbols = []
            seen = set()
            for match in matches:
                symbol = match.group(0)
                if symbol not in seen:
                    symbols.append(symbol)
                    seen.add(symbol)
            categories[category] = symbols
        
        return categories

    def normalize_math_expression(self, expr: str) -> str:
        """Normalize mathematical expressions for consistent processing"""
        # Remove extra whitespace
        expr = re.sub(r'\s+', ' ', expr.strip())
        
        # Standardize spacing around operators
        expr = re.sub(r'([=<>+\-*/])', r' \1 ', expr)
        
        # Normalize fractions
        expr = re.sub(r'\\frac\s*{([^}]*)}\s*{([^}]*)}', r'(\1)/(\2)', expr)
        
        # Normalize subscripts and superscripts
        expr = re.sub(r'_\{([^}]*)\}', r'_\1', expr)
        expr = re.sub(r'\^\{([^}]*)\}', r'^\1', expr)
        
        return expr.strip()

    def create_searchable_text(self, math_content: Dict[str, str]) -> str:
        """Create searchable text representation of mathematical content"""
        content_type = math_content['type']
        content = math_content['content']
        
        # Normalize the content
        normalized = self.normalize_math_expression(content)
        
        # Get symbol categories
        categories = self.categorize_symbols(content)
        
        # Create searchable description
        searchable_parts = [f"Math {content_type}:"]
        
        for category, symbols in categories.items():
            if symbols:
                searchable_parts.append(f"{category}: {' '.join(symbols)}")
        
        searchable_parts.append(f"Expression: {normalized}")
        
        return " ".join(searchable_parts)