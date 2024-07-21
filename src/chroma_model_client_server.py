from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import api_key
import chroma_model_document as cm_document

dashscope_ef = DashScopeEmbeddings(dashscope_api_key=api_key.dashscope_api_key)
collection_name = "langchain3"

"""
知识库存储
存储完可注释掉,验证documents是否入库
"""
# vectordb = Chroma.from_documents(cm_document.documents, dashscope_ef, persist_directory="../db_data",collection_name=collection_name)

"""
知识库搜索
"""
chroma = Chroma(
    persist_directory="../db_data",
    embedding_function=dashscope_ef,
    collection_name=collection_name
)

result = chroma.similarity_search("animal", k=3)
print(result)
