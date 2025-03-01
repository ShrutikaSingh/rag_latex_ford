import streamlit as st
from utils.math_processor import MathProcessor
import utils.llama_index as llama_index

def format_message(message):
    """Format message with proper math rendering."""
    return MathProcessor.format_math_response(message)

def process_query(query):
    """Process query with math-aware handling."""
    # Preprocess the query for mathematical content
    processed_query = MathProcessor.preprocess_math_query(query)
    
    # Get response from query engine
    response = llama_index.query_engine.query(processed_query['original_query'])
    
    # Format the response for proper math rendering
    formatted_response = format_message(str(response))
    
    return formatted_response

def chatbox():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if prompt := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = process_query(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)