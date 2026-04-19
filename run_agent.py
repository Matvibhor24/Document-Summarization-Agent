import sys
from agent.graph import build_graph

def run():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "pdf_docs/test_pdf.pdf"
    print(f"Initializing complete Agent workflow on: {pdf_path}\n")
    
    graph = build_graph()
    
    initial_state = {"file_path": pdf_path}
    
    try:
        print("----------Running pipeline----------")
        result = graph.invoke(initial_state)
        
        print("\n" + "="*80)
        print("FINAL AGENTIC SUMMARY OUTPUT:")
        print("="*80)
        print("----- PIPELINE TRACE -----")
        print(f"1. Raw Chunks extracted: {len(result.get('raw_chunks', []))}")
        print(f"2. Normalized Chunks formed: {len(result.get('normalized_chunks', []))}")
        print(f"3. Summaries successfully collected: {len(result.get('chunk_summaries', []))}")
        print("--------------------------\n")

        print(result.get("final_output", "No output generated!"))
        
    except Exception as e:
        print(f"\nPipeline failed: {e}")

if __name__ == "__main__":
    run()
