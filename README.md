# Minimal RAG

This project implements a minimal Retrieval-Augmented Generation (RAG) system.<br>
It loads .txt documents, splits them into chunks, stores embeddings in a local vector database (ChromaDB), 
and uses an LLM to answer user queries based on retrieved context.<br>
You can run it entirely locally using an open-source LLM (e.g. Llama 3 via Ollama), no API key or internet connection required.<br>

# Tools / Models Used
**LangChain**: document loading, chunking, and RAG orchestration.<br>
**ChromaDB**: local vector storage.<br>
**Ollama + Llama3:8b**: local LLM runtime for text generation.<br>
**nomic-embed-text**: via Ollama, for local embeddings.

# Setup Instructions (macOS/Linux)
## 1. Clone the repository
```
git clone https://github.com/mayhemph/minimal-rag-v1.git
cd minimal-rag-v1
```
## 2. Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate     # macOS / Linux
```

## 3. Install dependencies
```
pip install -U pip -r requirements.txt
```
### Install Ollama and pull models

Download, install and run Ollama: https://ollama.com/download

In a terminal:<br>
```
ollama pull llama3:8b           # LLM for answering
ollama pull nomic-embed-text    # embeddings model (fast, local)
```

# How to Run the RAG Bot

## Add text documents
```
mkdir -p data
```
Place your .txt files in the data/ folder<br>

## Run the CLI interface
```
python src/rag_cli.py
```

## Then ask questions interactively and wait for the answer, e.g.:
**You**: What is this project about?<br>

Type "exit" or "quit" to quit.<br>

## Example interaction 

**You**: Is it true that KEYTRUDA may be used in adults in combination with the medicine trastuzumab along with fluoropyrimidine and platinum chemotherapy as your first treatment when your stomach cancer?<br>

**Answer**: According to the provided context, yes, it is true that KEYTRUDA may be used in adults in combination with the medicine trastuzumab along with fluoropyrimidine and platinum chemotherapy as your first treatment when your stomach cancer is HER2-positive and tests positive for "PD-L1" and has spread or cannot be removed by surgery (advanced gastric cancer). <br>

**You**: Are you aware about “Mom Effect"?<br>

**Answer**: Yes, I am aware of the "Mom Effect" as mentioned in the context provided. According to the text, the "Mom Effect" refers to how mothers make valuable contributions to their communities and health systems, making them stronger. <br>

**You**: How important is the approval of BRAVECTO QUANTUM?   <br>

**Answer**: According to the context, the approval of BRAVECTO QUANTUM is very important because it sets a new standard in pet care by providing veterinarians and pet parents with a safe and effective option for flea and tick protection for dogs. It also provides continuous protection for up to 12 months, simplifying care for both pet owners and veterinarians, and promoting compliance. <br>

## Estimated Time Spent
~3 hours