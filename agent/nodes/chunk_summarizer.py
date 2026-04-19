import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from agent.prompts import CHUNK_SUMMARY_PROMPT

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def chunk_summarizer_node(state: dict) -> dict:
    chunk = state["chunk"]
    prompt = CHUNK_SUMMARY_PROMPT.format(
        title=state.get("doc_title", "Document"),
        heading_path=" > ".join(chunk["heading_path"]),
        content=chunk["content"][:6000],
    )
    try:
        resp = llm.invoke(prompt)
        raw = resp.content.strip()
        match=re.search(r"\{.*\}", raw, re.DOTALL)
        data = json.loads(match.group()) if match else {}
        summary = data.get("summary", raw[:400])
    except Exception as e:
        summary = chunk["content"][:300] + "..."
    
    return {
        "chunk_summaries": [{
            "chunk_id": chunk["chunk_id"],
            "heading_path": chunk["heading_path"],
            "summary": summary,
        }]
    }