# DocuMind — PDF Question Answering with RAG

DocuMind is a terminal-based document question-answering application built using
Retrieval-Augmented Generation (RAG).

It allows users to ask questions about PDF documents and generates answers
using relevant information retrieved from the documents rather than relying
entirely on the language model's internal knowledge.

The project demonstrates the implementation of a basic RAG pipeline using
LangChain, Google's Gemini models, and ChromaDB.

## Features

- PDF text extraction using PyPDF.
- Text chunking using LangChain's RecursiveCharacterTextSplitter.
- Text embedding generation using Google's embedding model.
- Persistent vector storage using ChromaDB.
- Semantic similarity search to retrieve relevant document chunks.
- Context-based answer generation using a Gemini language model.
- Source-page references for retrieved document content.
- Persistent storage to avoid regenerating embeddings when the existing
  vector database is populated.
- Terminal-based interaction without requiring a frontend.

## Tech Stack

- Python
- LangChain
- Google Gemini API
- Google Generative AI Embeddings
- ChromaDB
- PyPDF
- python-dotenv

## How It Works

DocuMind follows a Retrieval-Augmented Generation (RAG) pipeline.

1. **Document Loading:** Extracts text from a PDF file using PyPDF.
2. **Text Chunking:** Splits the extracted text into smaller chunks using
   RecursiveCharacterTextSplitter.
3. **Embedding Generation:** Converts document chunks into vector embeddings
   using Google's embedding model.
4. **Vector Storage:** Stores document chunks and their embeddings in
   ChromaDB for persistent retrieval.
5. **Semantic Retrieval:** Converts a question into an embedding and retrieves
   the most relevant document chunks using similarity search.
6. **Prompt Construction:** Combines the retrieved context with instructions
   and the user's question.
7. **Answer Generation:** Sends the prompt to a Gemini language model to
   generate a context-based answer.
8. **Source References:** Displays the page numbers associated with the
   retrieved chunks.

## Project Structure

    documind/
    ├── documents/
    │   └── dsaimpquestion.pdf
    ├── main.py
    ├── requirements.txt
    ├── .gitignore
    ├── .env
    └── chroma_db/

Note: `.env`, `.venv/`, and `chroma_db/` are local files or directories
and should not be committed to GitHub. The PDF shown above is an example;
include it in your repository only if you have permission to redistribute it.

## Prerequisites

- Python 3.12 or a compatible Python version.
- A Google Gemini API key.
- Git.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd documind
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your repository's Git URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows, use:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Replace the placeholder with your own Google Gemini API key.

Do not commit your `.env` file or share your API key publicly.

### 5. Add a PDF document

Place the PDF you want to query inside the `documents/` directory.

Update the `pdf_path` variable in `main.py` to point to your PDF:

```python
pdf_path = "documents/your_document.pdf"
```

### 6. Run the application

```bash
python main.py
```

The first run processes the PDF, creates chunks, generates embeddings, and
stores them in ChromaDB.

Subsequent runs reuse the existing vector database when it already contains
document chunks.

## Example

Example question:

What is the time complexity of the Two Sum problem?

Example answer:

The time complexity of the Two Sum approach described in the document is O(n).

The application also displays the page numbers of the retrieved document
chunks used to construct the answer.

The exact answer and retrieved pages depend on the PDF and the question.

## Key Concepts Demonstrated

- Retrieval-Augmented Generation (RAG)
- Document loading and preprocessing
- Text chunking and chunk overlap
- Vector embeddings
- Vector databases
- Semantic similarity search
- Prompt engineering and context grounding
- Persistent storage and caching
- Integration with a hosted language model API

## Current Limitations

- The current question is hardcoded in `main.py`.
- The application uses an existing vector database when it is populated;
  it does not yet automatically detect changes to the source PDF.
- Answer quality depends on document extraction, chunking, retrieval, and
  the language model's response.
- The application is currently designed for terminal usage.

## Future Improvements

- Add interactive question input.
- Detect changes to source documents and rebuild the vector store when needed.
- Support multiple PDF documents.
- Improve retrieval quality and evaluate different chunking strategies.
- Add automated tests for document processing and retrieval.
- Improve error handling and logging.

## Learning Objectives

This project was built to understand the practical implementation of a
RAG pipeline, including document processing, embeddings, vector storage,
retrieval, prompt construction, and LLM-based answer generation.

## License

Choose a license before distributing this project publicly. Ensure that any
documents included in the repository can legally be redistributed.