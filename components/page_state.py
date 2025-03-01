import streamlit as st

import utils.logs as logs

from utils.ollama import get_models


def set_initial_state():

    ###########
    # General #
    ###########

    if "sidebar_state" not in st.session_state:
        st.session_state["sidebar_state"] = "expanded"

    if "ollama_endpoint" not in st.session_state:
        st.session_state["ollama_endpoint"] = "http://localhost:11434"

    if "embedding_model" not in st.session_state:
        st.session_state["embedding_model"] = "Default (bge-large-en-v1.5)"

    if "ollama_models" not in st.session_state:
        try:
            models = get_models()
            st.session_state["ollama_models"] = models
        except Exception:
            st.session_state["ollama_models"] = []
            pass

    if "selected_model" not in st.session_state:
        try:
            if "llama3:8b" in st.session_state["ollama_models"]:
                st.session_state["selected_model"] = (
                    "llama3:8b"  # Default to llama3:8b on initial load
                )
            elif "llama2:7b" in st.session_state["ollama_models"]:
                st.session_state["selected_model"] = (
                    "llama2:7b"  # Default to llama2:7b on initial load
                )
            else:
                st.session_state["selected_model"] = st.session_state["ollama_models"][
                    0
                ]  # If llama2:7b is not present, select the first model available
        except Exception:
            st.session_state["selected_model"] = None
            pass

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "Welcome to Local RAG! To begin, please either import some files or ingest a GitHub repo. Once you've completed those steps, we can continue the conversation and explore how I can assist you further.",
            }
        ]

    ################################
    #  Files, Documents & Websites #
    ################################

    if "file_list" not in st.session_state:
        st.session_state["file_list"] = []

    if "github_repo" not in st.session_state:
        st.session_state["github_repo"] = None

    if "websites" not in st.session_state:
        st.session_state["websites"] = []

    ###############
    # Llama-Index #
    ###############

    if "llm" not in st.session_state:
        st.session_state["llm"] = None

    if "documents" not in st.session_state:
        st.session_state["documents"] = None

    if "query_engine" not in st.session_state:
        st.session_state["query_engine"] = None

    if "chat_mode" not in st.session_state:
        st.session_state["chat_mode"] = "compact"

    #####################
    # Advanced Settings #
    #####################

    if "advanced" not in st.session_state:
        st.session_state["advanced"] = False

    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = """You are a knowledgeable mathematics assistant. Your primary role is to help users understand mathematical concepts, solve problems, and work through mathematical proofs and derivations.

        Key responsibilities:
        1. Interpret and explain mathematical concepts clearly and precisely
        2. Process LaTeX mathematical notation accurately
        3. Provide step-by-step solutions and derivations
        4. Reference relevant theorems and definitions from the provided materials
        5. Format mathematical expressions properly using LaTeX notation

        When responding:
        - Use LaTeX notation for mathematical expressions (e.g., $x^2 + y^2 = z^2$ for inline math)
        - For complex equations, use display math mode (e.g., $$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$)
        - Break down complex proofs into clear, logical steps
        - Cite specific theorems or definitions from the reference materials when applicable
        - Ensure all mathematical notation is precise and unambiguous

        Remember to maintain mathematical rigor while keeping explanations accessible."""

    if "top_k" not in st.session_state:
        st.session_state["top_k"] = 3

    if "embedding_model" not in st.session_state:
        st.session_state["embedding_model"] = None

    if "other_embedding_model" not in st.session_state:
        st.session_state["other_embedding_model"] = None

    if "chunk_size" not in st.session_state:
        st.session_state["chunk_size"] = 1024

    if "chunk_overlap" not in st.session_state:
        st.session_state["chunk_overlap"] = 200
