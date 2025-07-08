import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VECTORSTORE_DIR = "./chroma_db"
DOCUMENTS_DIR = "./documents"
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = OllamaLLM(model="llama3.2:latest")
vectorstore = None

def load_or_create_vectorstore():
    global vectorstore
    if os.path.exists(VECTORSTORE_DIR) and os.listdir(VECTORSTORE_DIR):
        print("Loading existing vectorstore...")
        vectorstore = Chroma(
            persist_directory=VECTORSTORE_DIR,
            embedding_function=embeddings
        )
    else:
        vectorstore = None

load_or_create_vectorstore()

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    file_path = f"{DOCUMENTS_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    global vectorstore
    vectorstore = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )

    return {"message": f"{file.filename} uploaded and processed."}

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    global vectorstore
    if not vectorstore:
        return JSONResponse(status_code=400, content={"error": "No vectorstore loaded. Upload a PDF first."})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    answer = qa_chain.invoke(query)
    return {"question": query, "answer": answer}
