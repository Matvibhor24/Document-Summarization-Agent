# 📄 Agentic Document Summarizer

An agentic, UI-driven document summarization pipeline built using **LangGraph**, **Groq (Meta Llama 3)**, and **IBM Docling**. 

Unlike traditional AI parsing scripts that randomly chop text into disconnected character chunks, this pipeline utilizes **Hierarchical Context Chunking**. It natively extracts structural boundaries (chapters, section headers, tables) out of a PDF and deploys parallel, concurrent LLM agents to map and summarize discrete sections without ever losing structural context. 

## ⚙️ Tech Stack
- **Agent Orchestration**: **[LangGraph](https://python.langchain.com/v0.1/docs/langgraph/)** — Provides deterministic control flow and explicit typed-state handling for orchestrating parallel Map-Reduce architectures.
- **AI Inference Engine**: **[Groq API](https://wow.groq.com/) (Llama-3.3-70b-versatile)** — Chosen for its ultra-low latency LPU architecture, empowering dozens of simultaneous sub-agents to summarize chunks flawlessly in parallel.
- **PDF Layout Analysis**: **[IBM Docling](https://github.com/DS4SD/docling)** — Utilizes Machine Learning models to interpret deep document hierarchies rather than arbitrarily scraping raw text.
- **Frontend App**: **[Streamlit](https://streamlit.io/)** — Provides a cleanly wrapped, reactive web interface. 

---

## 🚀 The Architecture (Map-Reduce Workflow)

1. **Document Ingestion (`ingestor.py`)** 
   Docling reads the PDF like a human, identifying all main chapters, titles, and paragraphs, and tagging every single paragraph with a structural "breadcrumb trail".
2. **Chunk Merging (`normalizer.py`)** 
   Dynamically glues tiny scattered paragraphs together to optimize token limits, specifically merging chunks *only if* they belong under the exact same section header sequence.
3. **Parallel Summarization (`chunk_summarizer.py`)** 
   LangGraph spins up a targeted AI sub-agent for every single normalized chunk simultaneously (Map Phase), passing the exact structural context alongside the chunk text.
4. **Final Assembly (`composer.py`)** 
   Rebuilds a master Table of Contents, gracefully maps the finished AI summaries back underneath their original Markdown headings, and outputs a highly readable document via the UI.

---

## 🛠️ Getting Started

### 1. Prerequisites 
You will need Python 3.10+ and a free [Groq API Key](https://console.groq.com/keys).

### 2. Environment Setup
Install the necessary package requirements:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the root of the project and add your Groq key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Running the App
Run the Streamlit server directly from your terminal:
```bash
streamlit run app.py --logger.level=error
```
Upload any complex PDF and watch the Agent orchestrate the output!
