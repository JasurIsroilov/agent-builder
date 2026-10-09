"""
rag tools for the RAGDiplomaAgent

These tools provide retrieving of the information
"""

from langchain.tools import tool

from embeddings.rag_diploma_embeddings import rag_diploma_retriever

from utils.tool_permissions_decorator import tool_permission
from utils.permissions_enum import UserPermissions


@tool
@tool_permission(UserPermissions.READ_DIPLOMA_INFORMATION)
def retrieve_diploma_information(query: str) -> str:
    """
    This tool searches and returns the information from the diploma document.

    This tool uses embeddings and ChromaDB to retrieve information about the diploma project
    """

    docs = rag_diploma_retriever.invoke(query)

    if not docs:
        return "I found no relevant information in the Stock Market Performance 2024 document."
    
    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")
    
    return "\n\n".join(results)
