from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma

import os


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
collection_name = "diploma"


def _load_pdf() -> list:
    pdf_path = "diploma.pdf"
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    pdf_loader = PyPDFLoader(pdf_path)
    try:
        pages = pdf_loader.load()
        print(f"PDF has been loaded and has {len(pages)} pages")
        return pages
    except Exception as e:
        print(f"Error loading PDF: {e}")
        raise


def _create_persist_dir() -> str:
    persist_directory = "tmp/vector_dbs"

    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    return persist_directory


def _create_chroma_db():
    pages = _load_pdf()
    pages_split = text_splitter.split_documents(pages)
    persist_directory = _create_persist_dir()
    try:
        # Here, we actually create the chroma database using our embeddigns model
        vectorstore = Chroma.from_documents(
            documents=pages_split,
            embedding=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        print(f"Created ChromaDB vector store!")
        return vectorstore
        
    except Exception as e:
        print(f"Error setting up ChromaDB: {str(e)}")
        raise


vector_store = _create_chroma_db()
rag_diploma_retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5} # K is the amount of chunks to return
)
