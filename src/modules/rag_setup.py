# src/modules/rag_setup.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Configuration paths
BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "../../data/rag_docs")
DB_PATH = os.path.join(BASE_DIR, "../../data/chroma_db")

os.makedirs(DB_PATH, exist_ok=True)

# RAG Module
class RagModule2:
    def __init__(
        self,
        docs_dir=DOCS_DIR,
        db_path=DB_PATH,
        model_name="all-MiniLM-L6-v2"
    ):
        self.docs_dir = docs_dir
        self.model = SentenceTransformer(model_name)

        # ChromaDB persistent client
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="oracle_knowledge"
        )

    # Load markdown documents
    def load_documents(self):
        documents = []

        for file in os.listdir(self.docs_dir):
            if file.endswith(".md"):
                path = os.path.join(self.docs_dir, file)
                with open(path, "r", encoding="utf-8") as f:
                    documents.append({
                        "id": file,
                        "text": f.read(),
                        "source": file
                    })

        return documents

    # Embed texts
    def embed(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)

    # Index documents with metadata
    def index_documents(self):
        docs = self.load_documents()

        if not docs:
            print("[WARN] No documents found to index.")
            return

        texts = [d["text"] for d in docs]
        ids = [d["id"] for d in docs]
        metadatas = [
            {
                "source": d["source"],
                "doc_type": "oracle_rag_doc"
            }
            for d in docs
        ]

        embeddings = self.embed(texts)

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        print(f"[INFO] Indexed {len(docs)} documents with metadata.")

    # Retrieve context + sources
    def retrieve_context(self, query, top_k=5):
        query_embedding = self.embed([query])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        chunks = []
        sources = set()

        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            chunk = {
                "source": meta.get("source", "unknown"),
                "text": doc,
                "score": float(dist)
            }
            chunks.append(chunk)
            sources.add(chunk["source"])

        merged_context = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}"
            for c in chunks
        )

        return {
            "query": query,
            "context": merged_context,
            "sources": list(sources),
            "chunks": chunks
        }

# Quick test
if __name__ == "__main__":
    rag = RagModule2()

    # Note: this one needs to be run only once !!!
    # rag.index_documents()

    query = "index lent"
    result = rag.retrieve_context(query)

    print("\n==============================")
    print("QUERY:", result["query"])
    print("==============================\n")

    print("SOURCES USED:")
    for src in result["sources"]:
        print(" -", src)

    print("\nCONTEXT PREVIEW:\n")
    print(result["context"][:1000], "...")
