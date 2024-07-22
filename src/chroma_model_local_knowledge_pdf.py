import os

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFium2Loader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import TokenTextSplitter

import api_key



# 加载文档
def load_documents(directory):
    # loader = DirectoryLoader(directory, glob="**/*.pdf")
    # docs = loader.load()
    docs = []
    for doc in os.listdir(directory):
        doc_path = f'{directory}/{doc}'
        if doc_path.endswith('.pdf'):
            loader = PyPDFium2Loader(file_path=doc_path)
            docs.extend(loader.load())
    return docs


# 分割文档 pdf:PyMuPDFLoader ;  markdown:UnstructuredMarkdownLoader
def split_documents(docs):
    # 创建TokenTextSplitter对象，用于分割文档
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_texts = text_splitter.split_documents(docs)  # 分割加载的文本
    return docs_texts  # 返回分割后的文本


# 创建Chroma对象
def create_chroma(docs, persist_directory, collection_name, dashscope_ef):
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=dashscope_ef,
        persist_directory=persist_directory,
        collection_name=collection_name)
    return vectordb


# 创建embeddings,用于构建向量
def create_embeddings():
    return DashScopeEmbeddings(dashscope_api_key=api_key.dashscope_api_key)


# 创建openai,用于对话
def create_openai(chroma):
    openai_ojb = ChatOpenAI(
        openai_api_key=api_key.dashscope_api_key,
        temperature=0,
        model="qwen-max",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        # https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope?spm=a2c4g.11186623.0.0.65fe46c1CllXqx#414defd168byq
    )
    # 从模型和向量检索器创建ConversationalRetrievalChain对象
    chain = ConversationalRetrievalChain.from_llm(openai_ojb, chroma.as_retriever())
    return chain


# 对话结果
def get_ans(chain, question):
    chat_history = []  # 初始化聊天历史为空列表
    """
    以下写法将会失效,须用invoke
    The method `Chain.__call__` was deprecated in langchain 0.1.0 and will be removed in 0.3.0
    
    result = chain({  # 调用chain对象获取聊天结果
         'chat_history': chat_history,  # 传入聊天历史
         'question': question,  # 传入问题
    })
    """

    result = chain.invoke(
        input={
            'chat_history': chat_history,
            'question': question,
        }
    )
    return result['answer']


if __name__ == '__main__':
    collection_name = "langchain5"
    directory = "data"
    persist_directory = "../db_data"

    dashscope_ef = create_embeddings()
    docs = load_documents(directory)
    docs_texts = split_documents(docs)

    chroma = create_chroma(docs_texts, persist_directory, collection_name, dashscope_ef)

    chain = create_openai(chroma)

    while True:
        question = input('please input:')
        if question == 'exit':  # 如果用户输入的是'exit',就退出循环
            break
        ans = get_ans(chain, question)
        print(ans)
