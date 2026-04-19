import json
import re
from langchain_groq import ChatGroq
from agent.prompts import CHUNK_SUMMARY_PROMPT

llm = ChatGroq(model="llama3-8b-8192", temperature=0)

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
        confidence = float(data.get("confidence", 0.7))
    except Exception as e:
        summary = chunk["content"][:300] + "..."
        confidence = 0.0
    
    return {
        "chunk_summaries": [{
            "chunk_id": chunk["chunk_id"],
            "heading_path": chunk["heading_path"],
            "summary": summary,
            "confidence": confidence,
        }]
    }