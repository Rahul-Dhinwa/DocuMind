from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

def extract_text(pdf_path):
    path = Path(pdf_path)  # path object

    if not path.exists():
        raise FileNotFoundError(f"PDF not fount: {path}")

    reader = PdfReader(str(path))
    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip(): # removes white space
            extracted_pages.append({
                "page": page_number,
                "text": text
            })
    return extracted_pages



def create_chunks(pages):

    """Split extracted PDF pages into smaller text chunks."""

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,
        chunk_overlap=100,
        add_start_index=True
    )

    chunks = []

    for page in pages:

        page_chunks = splitter.create_documents(

            texts=[page["text"]],
            metadatas=[{"page": page["page"]}]
        )

        chunks.extend(page_chunks) # adds each object into chunk object

    return chunks

def create_vector_store(chunks):
    """Create or load the persistent ChromaDB vector store."""

    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Check your .env file."
        )

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )

    vector_store = Chroma(
        collection_name="documind_documents",
        embedding_function=embedding_model,
        persist_directory="./chroma_db"
    )

    existing_count = vector_store._collection.count()

    if existing_count == 0:
        vector_store.add_documents(chunks)
        print("Documents and embeddings saved to ChromaDB.")
    else:
        print(f"ChromaDB already contains {existing_count} chunks.")

    return vector_store


def retrieve_chunks(vector_store, question, k=3):
    """Retrieve the most relevant chunks for a question."""

    results = vector_store.similarity_search(
        query=question,
        k=k
    )

    return results



def generate_answer(question, retrieved_chunks):
    """Generate an answer using retrieved document context."""

    context = "\n\n".join(
        document.page_content
        for document in retrieved_chunks
    )

    prompt = f"""
    You are DocuMind, a document question-answering assistant.

    Your task is to answer the user's question using the retrieved document context.

    Instructions:
    1. Use only the information provided in the context.
    2. Do not use your own knowledge or make up information.
    3. If the context does not contain enough information to answer
    the question, respond with:
    "The document does not provide enough information to answer this question."
    4. Give a clear, concise, and accurate answer.
    5. When relevant, explain the reasoning behind the answer.

    Retrieved Context:
    {context}

    User Question:
    {question}

    Answer:
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0
    )

    response = llm.invoke(prompt)

    return response.text





if __name__ == "__main__":
    pdf_path = "documents/dsaimpquestion.pdf"

    pages = extract_text(pdf_path)

    print("\nPDF processed successfully!")
    print(f"Total pages with text: {len(pages)}")

    chunks = create_chunks(pages)

    print(f"Total chunks created: {len(chunks)}")

    vector_store = create_vector_store(chunks)

    print("Vector store is ready!")

    question = "What is the time complexity of the Two Sum problem?"

    results = retrieve_chunks(vector_store, question)

    answer = generate_answer(question, results)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    for document in results:
        page = document.metadata.get("page", "Unknown")
        print(f"- Page {page}")



    




