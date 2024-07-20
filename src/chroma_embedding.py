import chromadb
from chromadb.utils import embedding_functions
"""
@File    :   chroma_embedding.py
@Time    :   2023/07/06 15:08:08
@Version :   1.0
@Desc    :   None
"""
chroma_client = chromadb.Client()
default_ef = embedding_functions.DefaultEmbeddingFunction()

# 增加onnx.tar.gz文件路径
file_path = r"C:\Users\lzq\.cache\chroma\onnx_models\all-MiniLM-L6-v2\onnx.tar.gz"

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="my_c", embedding_function=default_ef)

# switch `add` to `upsert` to avoid adding the same documents every time
doc_ef = default_ef(['pineapple', 'oranges'])
collection.upsert(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"],
    uris=[file_path, file_path],  # 添加文件路径
    embeddings=doc_ef  # 转换成向量
)
print("doc_ef :", doc_ef)
query_ef = default_ef(['This is a query document about florida'])
print("query_ef :", query_ef)
results = collection.query(
    query_embeddings=query_ef,  # Chroma will embed this for you
    n_results=2  # how many results to return
)

print(results)
