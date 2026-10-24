import os
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-l6-v2")
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection("manual")


def search(query, top_k=5):
    embedding = model.encode(query).tolist()
    collection = get_collection()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    docs = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        docs.append({"text": doc, "page": meta["page"], "score": round(1 - dist, 3)})
    return docs


def ask(question, top_k=5):
    docs = search(question, top_k=top_k)
    context = "\n\n".join([f"[Page {d['page']}] {d['text']}" for d in docs])
    prompt = f"""You are an assistant that answers questions about the Keyestudio 4WD Robot v2.0 manual.
    Answer based strictly on the context below. If the answer is not the context, say so cleary

Context:
{context}

Question: {question}

Answer:"""

    response = client_groq.chat.completions.create(
        model=os.getenv("LLM_MODEL", "openai/gpt-oss-20b"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512,
    )
    return response.choices[0].message.content, docs


if __name__ == "__main__":
    question = "what sensors does the robot have?"
    answer, docs = ask(question)
    print(f"Q: {question}\n")
    print(f"A: {answer}\n")
    print("Sourcers:")
    for d in docs:
        print(f" Page {d['page']} (score {d['score']}): {d['text'][:80]}...")
