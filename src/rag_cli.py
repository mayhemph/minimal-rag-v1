# src/rag_cli.py
# Minimal RAG (local): Ollama embeddings + Ollama LLM 

from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


load_dotenv()

# --- paths ---
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / ".chroma_db"


def load_and_split_docs(path: Path):
   #Loading text files and split to chunks with source metadata
    if not path.exists():
        raise SystemExit(f"[error] Data folder not found: {path}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = []
    for p in sorted(path.glob("*.txt")):
        parts = splitter.split_documents(TextLoader(str(p), encoding="utf-8").load())
        for d in parts:
            d.metadata["source"] = p.name
        docs.extend(parts)

    if not docs:
        raise SystemExit(f"[error] No .txt files found in {path}.")
    return docs


def build_vectorstore(docs):
    
    # Creating a Chroma vector store using local Ollama embeddings

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vs = Chroma.from_documents(docs, embedding=embeddings, persist_directory=str(DB_DIR))
    return vs


def build_rag_chain(retriever):

    # Building the Retrieval-Augmented Generation (RAG) chain and instructing the model to answer questions based strictly on the retrieved context

    llm = ChatOllama(model="llama3:8b", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Use ONLY the provided context to answer."),
            ("human", "Question: {input}\n\nContext:\n{context}"),
        ]
    )
    doc_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, doc_chain)
    return rag_chain


def main():
    print("Loading & chunking documents...")
    docs = load_and_split_docs(DATA_DIR)
    print(f"  -> {len(docs)} chunks from {len(list(DATA_DIR.glob('*.txt')))} files")

    print("Creating / loading vector store...")
    vs = build_vectorstore(docs)
    retriever = vs.as_retriever(search_kwargs={"k": 3})

    print("Wiring RAG chain...")
    rag = build_rag_chain(retriever)

    print("\n RAG CLI ready (local). Type 'exit' to quit.\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        if not q:
            continue
        try:
            result = rag.invoke({"input": q})
            print("\nAnswer:", result.get("answer", "").strip(), "\n")
        except Exception as e:
            print(f"[error] {e}\n"
                    f"Check if Ollama and a model is running and models are pulled"
                    f"  - `ollama pull nomic-embed-text`\n"
                    f"  - `ollama pull llama3:8b`")

if __name__ == "__main__":
    main()
