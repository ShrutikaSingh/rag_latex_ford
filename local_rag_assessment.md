**Assessment: Building a Local RAG System for Mathematical Question Answering**

---

## Objective

Demonstrate your ability to set up, extend, and document a **local Retrieval-Augmented Generation (RAG)** system using the [Local RAG](https://github.com/jonfairbanks/local-rag) repository. Your system should focus on answering **mathematical questions** and effectively handle **LaTeX** formulas, derivations, or proofs from locally stored reference materials (e.g., PDFs or text files containing math lecture notes, textbooks, or research papers).

Additionally, you are allowed to **switch out the default model** in Local RAG for **any [Ollama](https://github.com/jmorganca/ollama) model** (e.g., LLaMA, MPT, etc.) that can run **entirely offline on your local machine**.

---

## Task Overview

You have **3 hours** to complete the following tasks:

1. **Set Up the Environment**
   - Clone the [Local RAG repository](https://github.com/jonfairbanks/local-rag).
   - Follow the [setup documentation](https://github.com/jonfairbanks/local-rag/blob/develop/docs/setup.md) to configure your local environment, ensuring everything can run offline.
   - If desired, configure your chosen **Ollama-compatible model** (e.g., LLaMA variant) to be used by the RAG system in place of the default model.

2. **Enhance the RAG System**
   - Implement **one major feature or improvement** that benefits math-focused question answering. Examples of possible enhancements include (but are not limited to):
     - **LaTeX-Aware Retrieval**: Extend the retrieval pipeline to index math expressions, enabling more accurate searches for formulas or theorems.
     - **Advanced Text Processing**: Incorporate libraries or techniques (e.g., symbolic manipulation) to parse or interpret mathematical expressions.
     - **Improved UI**: Create a front-end feature that displays queries and answers with LaTeX formatting for a clear, math-friendly experience.
     - **Semantic Search Optimization**: Use vector embeddings or specialized algorithms (e.g., approximate nearest neighbor) to handle conceptually complex math questions.
     - **Step-by-Step Solutions**: Integrate a process that explains or derives the answer in multiple steps, helpful for math proofs or derivations.

3. **Expose an API Endpoint**
   - Develop and document an **API endpoint** (e.g., `/api/math-query`) that:
     - Accepts a math-related question (possibly containing LaTeX).
     - Returns a generated answer along with references to the relevant source documents.

---

## Submission Requirements

1. **Code Repository**
   - Provide a **public GitHub repository** link containing your solution.
   - Include:
     - **Commit History**: Showing each step of your development.
     - **Documentation**: A clear README or docs covering:
       - Installation and setup instructions, including how to configure any **Ollama models** you used.
       - A description of your math-focused enhancements.
       - Usage details for your new API endpoint (e.g., sample requests, responses, and how to handle LaTeX-based queries).

2. **Demonstration Video (5–10 minutes)**
   - Record a short video that covers:
     1. **Environment Setup**: Show how you install dependencies, configure any local Ollama models, and start the RAG environment.
     2. **Code Walkthrough**: Highlight the structure of the codebase, focusing on the enhancements you introduced for math retrieval or LaTeX handling.
     3. **System Demo**: 
        - Perform a live query with a math question (e.g., containing LaTeX or referencing a specific theorem).
        - Show how the system retrieves relevant information and generates an answer.
        - Demonstrate the **API endpoint** in action (e.g., using a tool like cURL or Postman to send requests).

---

## Evaluation Criteria

1. **Technical Implementation**
   - Correctly set up and run the base **Local RAG** environment.
   - Successful integration (if chosen) of an **Ollama-based model** into the pipeline, ensuring local inference.
   - Quality and relevance of the enhancement for math question answering (e.g., improved retrieval for LaTeX formulas, step-by-step derivations, or specialized indexing).
   - Proper implementation and thorough documentation of the API endpoint.

2. **Code Quality**
   - Clarity, organization, and readability of your code.
   - Use of best practices and coding standards.

3. **Documentation**
   - Adequacy of instructions for replicating your setup.
   - Accuracy and thoroughness when explaining your enhancements and how to use the new features.
   - Clear guidance on how to configure and run your chosen Ollama model locally (if you opt to switch the default model).

4. **Presentation**
   - Effectiveness of the video in demonstrating installation, feature explanations, and usage.
   - Clarity and coherence in showing how math queries are processed and answered.

---

## Notes

- Your entire solution must run **locally** without relying on cloud services.
- You may incorporate any additional libraries or tools that facilitate math parsing or LaTeX handling, as long as they operate offline.
- Feel free to replace the default model in Local RAG with **any Ollama-compatible model** (LLaMA, MPT, etc.) that you can run on your machine.
- Aim to deliver a **functional prototype** demonstrating your chosen features within the time limit.
- Focus on showcasing how your system handles **mathematical questions** and **LaTeX** content effectively.

---

Good luck! This assessment tests your capability to work with an existing codebase, innovate around mathematical queries, and provide a well-documented local environment—ensuring a clear, robust prototype that can handle technical, formula-based questions.