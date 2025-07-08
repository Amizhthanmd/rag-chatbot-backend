from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
import os

VECTORSTORE_DIR = "./chroma_db"
vectorstore = Chroma
# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists(VECTORSTORE_DIR):
    print("Loading existing vectorstore...")
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings
    )
else:
    # Load data
    loader = PyPDFLoader("documents/amizhthan-resume-2025.pdf")
    documents = loader.load()

    # Split data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    # Store in vector DB
    vectorstore = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )

# Retrieval with Ollama
llm = OllamaLLM(model="llama3.2:latest")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

query = "Does he knows python?"
response = qa_chain.invoke(query)

print("\nAnswer:", response)
