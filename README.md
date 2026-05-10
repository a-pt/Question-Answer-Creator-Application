# 🎓 Question-Answer Creator Application

An intelligent, AI-powered tool that automatically generates high-quality Exam Preparation Questions and Answers from PDF documents. This application leverages state-of-the-art LLMs via Groq and advanced RAG (Retrieval-Augmented Generation) pipelines to transform static study materials into interactive learning resources.

---

## 🚀 Key Features

- **Instant PDF Preview**: View your uploaded study material immediately while the AI works in the background.
- **Iterative Question Generation**: Produces a curated set of 10 comprehensive questions covering the entire document.
- **Automated Answering**: Uses a RAG pipeline to provide accurate answers based solely on the document's context.
- **CSV Export**: Download the generated Q&A pairs in a structured CSV format for offline study or integration into other tools (like Anki).
- **Modern UI**: Clean, responsive interface built with Bootstrap, FontAwesome, and SweetAlert2.

---

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **AI Orchestration**: [LangChain](https://www.langchain.com/) (LCEL)
- **LLM Hosting**: [Groq](https://groq.com/) (using high-speed inference)
- **Vector Database**: [FAISS](https://github.com/facebookresearch/faiss)
- **Embeddings**: [HuggingFace](https://huggingface.co/) (`sentence-transformers/all-MiniLM-L6-v2`)
- **Frontend**: HTML5, Vanilla JS, Bootstrap 5, jQuery

---

## 🧠 Advanced Approaches

### 1. Iterative Question Refinement
To ensure maximum coverage of long documents without exceeding model context limits, the application employs an **Iterative Refinement Strategy**:
- **Initial Chain**: The first chunk of the document is used to generate an initial set of questions.
- **Refinement Loop**: As the app processes subsequent chunks, it uses a specialized `refine_question_prompt`. This prompt asks the LLM to either update existing questions with more relevant information from the new context or add new ones, ensuring the final list represents the most important concepts of the entire file.

### 2. RAG Pipeline with Parallel Chains
For generating answers, we use a robust **Retrieval-Augmented Generation** architecture:
- **Vector Search**: The document is split into overlapping chunks and stored in a FAISS vector index using HuggingFace embeddings.
- **Parallel Retrieval**: Using LangChain Expression Language (LCEL), we implement a `RunnableParallel` chain. This chain simultaneously fetches the relevant context from the vector store and passes the user question to the prompt, optimizing performance.

### 3. Non-Blocking Event Loop Management
To maintain a "Premium" user experience:
- **Async File I/O**: PDF uploads use `aiofiles` to prevent blocking the server.
- **Threaded Execution**: Heavy AI processing is handled in a separate thread pool (FastAPI standard `def` endpoints), allowing the main event loop to remain responsive and serve the PDF file immediately after upload.

---

## 📋 Setup & Installation

### Prerequisites
- Python 3.11+
- [Groq API Key](https://console.groq.com/)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Question-Answer-Creator-Application.git
   cd Question-Answer-Creator-Application
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. **Install Dependencies**:
   ```bash
   conda create -n qanda python=3.11 -y
   conda activate qanda
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```
   Access the app at `http://localhost:8000`

---

## 📖 Usage
1. **Upload**: Drag and drop or select a PDF file (Max 5 pages recommended for best results).
2. **Preview**: The PDF will appear in the viewer instantly.
3. **Wait**: The "Generate" spinner indicates the AI is analyzing the text and refining questions.
4. **Download**: Once finished, click the yellow download button to get your `QA.csv` file.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
