import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from agent.graph import build_graph

os.makedirs("pdf_docs", exist_ok=True)

st.set_page_config(page_title="Semantic Document Summarizer", page_icon="📄", layout="centered")

st.title("📄 Semantic Document Summarizer")
st.markdown("Upload a complex PDF document to summarize it.")

uploaded_file = st.file_uploader("Upload your PDF here", type=["pdf"])

if uploaded_file is not None:
    temp_path = os.path.join("pdf_docs", "streamlit_temp.pdf")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    if st.button("Start Agentic Summarization"):
        with st.spinner("⏳ Orchestrating LangGraph Map-Reduce Pipeline... Please wait."):
            try:
                graph = build_graph()
                initial_state = {"file_path": temp_path}
                result = graph.invoke(initial_state)
                
                raw = len(result.get("raw_chunks", []))
                norm = len(result.get("normalized_chunks", []))
                sums = len(result.get("chunk_summaries", []))
                
                st.subheader("📊 Pipeline Trace")
                col1, col2, col3 = st.columns(3)
                col1.metric("Raw Chunks Extracted", raw)
                col2.metric("Normalized Chunks", norm)
                col3.metric("Summaries Completed", sums)
                
                st.divider()
                
                st.subheader("🎯 Final Agentic Summary")
                
                final_text = result.get("final_output", "No output generated!")
                st.markdown(final_text)
                
                st.download_button(
                    label="Download Summary (.md)",
                    data=final_text,
                    file_name=f"Summary_{uploaded_file.name}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ Pipeline failed: {e}")
