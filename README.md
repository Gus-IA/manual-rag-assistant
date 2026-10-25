# 🤖 Keyestudio 4WD Robot Assistant

A simple RAG assistant that answers questions about the Keyestudio 4WD Robot V2.0 manual.
Built to understand and explain the core RAG pipeline: PDF ingestion, embeddings, vector search and LLM response.

---

## 🏗️ Architecture

```
PDF Manual
    → Extract text (pypdf)
    → Split into chunks (500 chars, 100 overlap)
    → Generate embeddings (all-MiniLM-L6-v2, local)
    → Store in ChromaDB (local vector database)
    → User asks a question
    → Question → embedding → vector search → top 5 chunks
    → Chunks + question → LLM (Groq)
    → Answer with sources
```


## 📊 Dataset

- **Manual:** Keyestudio 4WD Robot V2.0 (KS0559F) — included in `data/manual.pdf`
- **Pages:** 383
- **Chunks indexed:** 659

---

## 🛠️ Stack

- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (local, no API needed)
- **Vector DB:** ChromaDB (local, no Docker needed)
- **LLM:** Groq API (`openai/gpt-oss-20b`)
- **UI:** Streamlit

---

## 🚀 How to run

### 1. Clone the repository
```bash
git clone https://github.com/Gus-IA/manual-rag-assistant.git
cd manual-rag-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 4. Run ingestion (PDF → ChromaDB)
```bash
python src/ingest.py
```

### 5. Start the app
```bash
streamlit run src/app.py
```

### 6. Open in browser
http://localhost:8501


---

## 📁 Project Structure

```
manual-rag-assistant/
├── data/
│   └── manual.pdf           # Keyestudio 4WD Robot V2.0 manual
├── src/
│   ├── ingest.py            # PDF → chunks → embeddings → ChromaDB
│   ├── rag.py               # Vector search + LLM integration
│   └── app.py               # Streamlit UI
├── chroma_db/               # Local vector database (auto-generated)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔑 Environment Variables

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=openai/gpt-oss-20b
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

---

## 💡 Example Questions

- `What sensors does the robot have?`
- `How do I connect the ultrasonic sensor?`
- `How does line tracking work?`
- `What is the voltage of the motors?`
- `How do I control the robot via Bluetooth?`