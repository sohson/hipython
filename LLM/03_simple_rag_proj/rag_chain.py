import os
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

PDF_PATH = "data/samsung_manual.pdf"

PROMPT_TEMPLATE = """
너는 삼성전자 메모리카드 매뉴얼에 대한 전문 어시스턴트이다.
다음의 참고 문서를 바탕으로 질문에 정확하게 답하라.

[참고문서]
{context}

[질문]
{question}

한글로 간결하고 정확하게 답변하라.
"""


def build_rag_chain():
    """PDF를 로드하고 RAG 체인을 생성하여 반환한다."""

    # 1. 인덱싱: PDF 로드 및 청크 분할
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents(pages)

    # 2. 임베딩 및 벡터스토어 생성
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_documents(docs, embeddings)

    # 3. 검색기
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # 4. 프롬프트 및 LLM
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 5. RAG 체인 조립
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain