import sympy
from sympy.parsing.latex import parse_latex
from typing import Dict, Any, Optional
from utils import logs

class SymbolicProcessor:
    """Handles symbolic mathematical processing and analysis"""
    
    def __init__(self):
        self.x, self.y, self.z = sympy.symbols('x y z')
        self.common_symbols = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            't': sympy.Symbol('t'),
            'n': sympy.Symbol('n'),
        }
        logs.log.info("Symbolic processor initialized")

    def parse_expression(self, latex: str) -> Optional[sympy.Expr]:
        """Parse LaTeX expression into SymPy expression"""
        try:
            return parse_latex(latex)
        except Exception as e:
            logs.log.warning(f"Failed to parse LaTeX: {e}")
            return None

    def analyze_expression(self, expr: sympy.Expr) -> Dict[str, Any]:
        """Analyze a mathematical expression"""
        analysis = {}
        
        try:
            analysis['variables'] = [str(s) for s in expr.free_symbols]
            analysis['is_polynomial'] = expr.is_polynomial()
            analysis['simplified'] = str(sympy.simplify(expr))
            analysis['expanded'] = str(sympy.expand(expr))
            
            try:
                analysis['factored'] = str(sympy.factor(expr))
            except:
                analysis['factored'] = "Could not factor"

            if len(expr.free_symbols) == 1:
                var = list(expr.free_symbols)[0]
                try:
                    analysis['derivative'] = str(sympy.diff(expr, var))
                    analysis['integral'] = str(sympy.integrate(expr, var))
                except Exception as e:
                    logs.log.warning(f"Calculus operations failed: {e}")

        except Exception as e:
            logs.log.error(f"Expression analysis failed: {e}")
            analysis['error'] = str(e)

        return analysis