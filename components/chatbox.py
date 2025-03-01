import streamlit as st
from utils.math_processor import MathProcessor
import utils.llama_index as llama_index

def format_message(message):
    """Format message with proper math rendering."""
    return MathProcessor.format_math_response(message)

def process_query(query):
    """Process query with math-aware handling."""
    # Get the query engine
    query_engine = llama_index.get_query_engine()
    if not query_engine:
        st.error("Please upload some documents first and configure the settings.")
        return "I need some documents to work with. Please upload files or configure a data source in the settings."
    
    # Preprocess the query for mathematical content
    processed_query = MathProcessor.preprocess_math_query(query)
    
    try:
        # Get response from query engine
        response = query_engine.query(processed_query['original_query'])
        
        # Format the response for proper math rendering
        formatted_response = format_message(str(response))
        
        return formatted_response
    except Exception as e:
        st.error(f"Error processing query: {str(e)}")
        return "I encountered an error while processing your query. Please try again or check the settings."

def chatbox():
    """Display and handle the chat interface."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display existing messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Handle new user input
    if prompt := st.chat_input("How can I help you?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Process query and get response
        with st.spinner("Thinking..."):
            response = process_query(prompt)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)