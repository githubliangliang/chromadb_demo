from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import api_key
import chroma_model_document as cm_document

dashscope_ef = DashScopeEmbeddings(dashscope_api_key=api_key.dashscope_api_key)

"""
通过文档创建向量存储
"""
vectorstore = Chroma.from_documents(
    cm_document.documents,
    embedding=dashscope_ef
)
"""
查询向量存储
k:返回文档数,默认4
"""

# 返回文档
# result = vectorstore.similarity_search("fruit",k=3)

# 返回文档和分数
# result = vectorstore.similarity_search_with_score("fruit", k=3)

# 查询向量存储,返回文档
query_ef = dashscope_ef.embed_query("fruit")
result = vectorstore.similarity_search_by_vector(query_ef, k=3)

print(result)
