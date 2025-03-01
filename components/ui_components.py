import streamlit as st
from typing import List, Dict, Any
from utils.rag_pipeline import RagPipeline

class MathUI:
    """Handles the user interface components"""
    
    def __init__(self, rag_pipeline: RagPipeline):
        self.rag_pipeline = rag_pipeline

    def render_chat_interface(self):
        """Render the main chat interface"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a mathematical question..."):
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = self.rag_pipeline.query(prompt)
                        
                        st.markdown(response['answer'])
                        
                        if response['sources']:
                            with st.expander("Sources"):
                                for source in response['sources']:
                                    st.markdown(f"**Relevance:** {source['score']:.2f}")
                                    st.markdown(f"**Content:** {source['text']}")
                                    st.markdown("---")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['answer']
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

    def render_latex_preview(self, latex: str):
        """Render LaTeX preview"""
        st.latex(latex)

    def render_analysis_view(self, analysis: Dict[str, Any]):
        """Render mathematical analysis results"""
        if 'error' in analysis:
            st.error(f"Analysis failed: {analysis['error']}")
            return

        st.subheader("Mathematical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Basic Properties**")
            if 'variables' in analysis:
                st.write("Variables:", ", ".join(analysis['variables']))
            if 'is_polynomial' in analysis:
                st.write("Is polynomial:", analysis['is_polynomial'])

        with col2:
            st.markdown("**Transformations**")
            if 'simplified' in analysis:
                st.latex(f"Simplified: {analysis['simplified']}")
            if 'expanded' in analysis:
                st.latex(f"Expanded: {analysis['expanded']}")
            if 'factored' in analysis:
                st.latex(f"Factored: {analysis['factored']}")

        if 'derivative' in analysis or 'integral' in analysis:
            st.markdown("**Calculus**")
            if 'derivative' in analysis:
                st.latex(f"Derivative: {analysis['derivative']}")
            if 'integral' in analysis:
                st.latex(f"Integral: {analysis['integral']}")