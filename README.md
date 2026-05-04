#  AI Question Paper Generator (RAG-based EdTech System)

An AI-powered system that generates **custom question papers from uploaded books/documents** using **Retrieval-Augmented Generation (RAG)**.

Upload content → process & chunk → store in vector DB → generate **user-defined question papers** → export/download.

---

## 🚀 Features

### 📥 Upload & Processing

* Upload books/documents (stored in `/data/uploads`)
* Automatic **text extraction & chunking**
* Efficient preprocessing via `document_processor.py`

### 🧠 RAG Pipeline

* Embeddings stored in **ChromaDB** (`/data/chromadb`)
* Semantic retrieval using `vector_store.py`
* Context-aware generation

### 📝 Question Paper Generation

Generate fully customized papers based on:

* Number of questions
* Question types:

  * ✅ MCQs
  * ✅ Short Answer
  * ✅ Long Answer
  * ✅ Case-based

Handled via:

* `generator.py`
* Prompt templates (`core/prompts.py`)

### 📄 Export System

* Structured paper formatting
* Export/download supported via `exporter.py`
* Files saved in `/data/exports`

### 🌐 Simple Frontend

* Basic UI using:

  * `index.html`
  * `style.css`
  * `app.js`

---

## 🔁 Workflow

```text
Upload File → Process & Chunk → Store Embeddings → Retrieve Context → Generate Questions → Export Paper
```

---

## 📂 Project Structure

```bash
AI_QGEN_EDTECH/
│
├── aiqgen/                  # (Main module / future expansion)
│
├── core/                    # Core configs & prompts
│   ├── config.py
│   ├── models.py
│   └── prompts.py
│
├── services/                # Business logic
│   ├── document_processor.py   # File parsing & chunking
│   ├── vector_store.py         # Embeddings + retrieval
│   ├── generator.py            # Question generation
│   └── exporter.py             # Export question paper
│
├── data/
│   ├── uploads/               # Uploaded files
│   ├── chromadb/              # Vector DB storage
│   └── exports/               # Generated papers
│
├── Designs/                  # DB diagrams
│   ├── postgre_db.mermaid
│   └── postgre_db.svg
│
├── static/                   # Frontend
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── main.py                   # Entry point
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repo

```bash
git clone https://github.com/HarshitWaldia/Ai_Qgen_RAG.git
cd Ai_Qgen_RAG
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

---

## ▶️ Run the Project

### 🚀 Run Backend (Uvicorn) + Frontend

#### 1. Start the Backend Server

From your project root directory:

```bash
uvicorn main:app --reload
```

#### What this does:

* `main:app` → looks for `app` inside `main.py`
* `--reload` → auto-restarts on code changes

---

### 🌐 2. Open the Frontend

Once the server starts, open your browser:

```
http://127.0.0.1:8000
```

👉 Since we have:

```
static/
 ├── index.html
 ├── style.css
 └── app.js
```

Our backend (likely FastAPI) should be serving this HTML.

---

## ⚠️ If frontend doesn’t load

Then `main.py` might be missing static file mounting.

### ✅ Add this to `main.py` (FastAPI)

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

---

## 📂 Expected Flow

```text
User opens browser → index.html loads → JS (app.js) → calls backend APIs → backend processes RAG → returns questions
```

---

## 🧪 Example Full Run

```bash
# 1. Activate env (optional)
source venv/bin/activate   # or .\venv\Scripts\activate (Windows)

# 2. Run server
uvicorn main:app --reload

# 3. Open browser
http://127.0.0.1:8000
```

---

## 🧪 Example Usage

### Input:

* Upload: Biology textbook
* User selects:

  * 20 questions
  * 10 MCQs
  * 5 Short
  * 3 Long
  * 2 Case-based

### Output:

```text
Section A: MCQs (10)
Section B: Short Answer (5)
Section C: Long Answer (3)
Section D: Case Study (2)
```

📥 Download available from `/data/exports`

---

## 🧠 Core Components

| File                    | Responsibility            |
| ----------------------- | ------------------------- |
| `document_processor.py` | Extracts & chunks text    |
| `vector_store.py`       | Embeddings + retrieval    |
| `generator.py`          | Question generation logic |
| `exporter.py`           | Formats & exports paper   |
| `prompts.py`            | LLM prompt templates      |

---

## 📌 Use Cases

* 🎓 Teachers creating exam papers
* 🏫 Schools & universities
* 📚 Self-assessment tools
* 🤖 EdTech platforms

---

## 🧪 Future Enhancements

* ✅ Answer key generation
* 🎯 Difficulty-level control
* 📊 Topic-wise filtering
* 🌐 Advanced UI (React / Streamlit)
* 📚 Multi-document querying
* 🧠 Fine-tuned models

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch
3. Commit changes
4. Open a PR

---

## 👨‍💻 Author

**Harshit Waldia**

---

## ⭐ Support

If this project helps you, consider giving it a ⭐ on GitHub!
