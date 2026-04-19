from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from agent.state import DocumentState
from agent.nodes.ingestor import ingest_node
from agent.nodes.normalizer import normalizer_node
from agent.nodes.chunk_summarizer import chunk_summarizer_node
from agent.nodes.composer import compose_node

def fan_out_summaries(state: dict):
    title = state.get("doc_metadata", {}).get("title", "Document")
    return [
        Send("chunk_summarizer", {"chunk": c, "doc_title": title})
        for c in state.get("normalized_chunks", [])
    ]

def build_graph():
    g = StateGraph(DocumentState)
    g.add_node("ingest", ingest_node)
    g.add_node("normalizer", normalizer_node)
    g.add_node("chunk_summarizer", chunk_summarizer_node)
    g.add_node("compose", compose_node)
    g.add_edge(START, "ingest")
    g.add_edge("ingest", "normalizer")
    
    # 1 (normalizer) --> N (summarizers)
    g.add_conditional_edges("normalizer", fan_out_summaries, ["chunk_summarizer"])
    
    # N (summarizers) --> 1 (compose)
    g.add_edge("chunk_summarizer", "compose")
    g.add_edge("compose", END)
    return g.compile()