from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

PDF_PATH = "data/manual.pdf"
CHUNK_SIZE = 500  # carácteres por chunk
CHUNK_OVERLAP = 100  # cantidad de texto repetido en fragmentos


def load_pdf(path):
    """Extraer el texto de cada página."""
    reader = PdfReader(path)
    return [page.extract_text() or "" for page in reader.pages]


def split_into_chunks(pages):
    """Dividir cada página en overlapping chunks, manteniendo el número de la página."""
    chunks = []
    for page_num, text in enumerate(pages, start=1):
        text = text.strip()
        start = 0

        while start < len(text):
            piece = text[start : start + CHUNK_SIZE].strip()

            if len(piece) > 50:
                chunks.append({"text": piece, "page": page_num})
            start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def main():
    pages = load_pdf(PDF_PATH)
    chunks = split_into_chunks(pages)
    print(f"Páginas: {len(pages)}")
    print(f"Chunks generados: {len(chunks)}")
    print(f"Caracteres extraídos: {sum(len(p) for p in pages)}")

    if not chunks:
        raise ValueError(
            "No se generaron chunks. Comprueba que el PDF contiene "
            "texto extraíble y que la ruta es correcta"
        )

    # Embedding: text -> vector
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode([c["text"] for c in chunks]).tolist()

    print(f"Textos: {len(texts)}")
    print(f"Embeddings: {len(embeddings)}")

    assert len(texts) == len(embeddings) > 0

    # guardar vectores en ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")
    try:
        client.delete_collection("manual")
    except Exception:
        pass
    collection = client.create_collection("manual", metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[{"page": c["page"]} for c in chunks],
    )
    print("Ingestion completada")


if __name__ == "__main__":
    main()
