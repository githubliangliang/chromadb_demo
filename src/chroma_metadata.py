import chromadb

"""
This is a simple example of how to use Chroma to store and retrieve embeddings.
"""
chroma_client = chromadb.Client()

# 增加onnx.tar.gz文件路径
file_path = r"C:\Users\lzq\.cache\chroma\onnx_models\all-MiniLM-L6-v2\onnx.tar.gz"

#
metadata = {"hnsw:space": "cosine"}
# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="my_c2", metadata=metadata)

# switch `add` to `upsert` to avoid adding the same documents every time
collection.upsert(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    metadatas=[{"character": "20"}, {"character": "21"}],
    ids=["id1", "id2"],
    uris=[file_path, file_path]  # 添加文件路径
)

results = collection.query(
    where={
        "character": {
            "$eq": "20"
        }
    },
    query_texts=["This is a query document about florida"], # Chroma will embed this for you
    n_results=2  # how many results to return
)

print(results)
