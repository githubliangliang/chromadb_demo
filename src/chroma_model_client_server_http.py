import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import api_key
import chroma_model_document as cm_document

dashscope_ef = DashScopeEmbeddings(dashscope_api_key=api_key.dashscope_api_key)
collection_name = "langchain4"

client = chromadb.HttpClient(port=8000, host="localhost")
"""
知识库存储 - http 
"""
# Chroma.from_documents(cm_document.documents, dashscope_ef, collection_name=collection_name,client=client)
"""
知识库搜索
"""
chroma = Chroma(
    client=client,
    embedding_function=dashscope_ef,
    collection_name=collection_name
)

result = chroma.similarity_search("animal", k=3)
print(result)
