import sys
import json
from agent.nodes.ingestor import ingest_node

def run_test():
    # If a path was passed via CLI, use it, otherwise use the privacy policy
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "google_privacy_policy.pdf"
    
    state = {"file_path": pdf_path}
    
    print(f"Running Docling ingestion on {pdf_path}...")
    print("Note: On the very first run, Docling will download its layout models (this takes a minute).")
    
    try:
        result = ingest_node(state)
    except Exception as e:
        print(f"\nIngestion failed: {e}")
        return
    
    hierarchy = result.get("hierarchy", [])
    raw_chunks = result.get("raw_chunks", [])
    
    print("\n" + "="*60)
    print("DOCUMENT HIERARCHY (Outline Extracted Built-in):")
    print("="*60)
    for node in hierarchy:
        indent = "  " * (node["level"] - 1)
        print(f"{indent}L- [H{node['level']}] {node['title']}")
        
    print("\n" + "="*60)
    print(f"TOTAL STRUCTURAL CHUNKS: {len(raw_chunks)}")
    print("="*60)
    
    if len(raw_chunks) > 0:
        print("\nHere is a preview of the first 3 chunks natively mapped:\n")
        for chunk in raw_chunks[:3]:
            path_str = " > ".join(chunk["heading_path"])
            print(f"- Chunk ID: {chunk['chunk_id']} | Tokens: {chunk['token_count']}")
            print(f"  Context Path: {path_str}")
            print(f"  Text Snippet: {chunk['content'][:200]}...\n")
            print("-" * 50)

if __name__ == "__main__":
    run_test()
