import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq

# Load API key
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Load PDF
loader = PyMuPDFLoader("google_privacy_policy.pdf")
docs = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

print(f"Total chunks: {len(chunks)}")

# MAP STEP
chunk_summaries = []

for i, chunk in enumerate(chunks):
    print(f"Summarizing chunk {i+1}/{len(chunks)}...")
    
    response = llm.invoke(
        f"Summarize the following text clearly:\n{chunk.page_content}"
    )
    
    chunk_summaries.append(response.content)

# REDUCE STEP
print("\nCombining summaries...\n")

final_summary = llm.invoke(
    "Combine the following summaries into a final coherent summary:\n" +
    "\n".join(chunk_summaries)
)

print("\n===== FINAL SUMMARY =====\n")
print(final_summary.content)