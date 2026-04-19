from langchain_text_splitters import RecursiveCharacterTextSplitter

def normalizer_node(state: dict) -> dict:
    raw_chunks = state.get("raw_chunks", [])
    merged = []

    curr = None
    for chunk in raw_chunks:
        if chunk.get("token_count", 0) == 0:
            continue
            
        if not curr:
            curr = chunk.copy()
        # Increased threshold to 1200 words (~1600 tokens) to minimize total chunks
        elif curr["token_count"] < 1500 and curr["heading_path"]==chunk["heading_path"]:
            curr["content"] += "\n\n" + chunk["content"]
            curr["token_count"] += chunk["token_count"]
        else:
            merged.append(curr)
            curr = chunk.copy()
    
    if curr:
        merged.append(curr)
    
    # Using 6000 chars mapping closely to ~1200-1500 words
    splitter = RecursiveCharacterTextSplitter(chunk_size=6000, chunk_overlap=300)
    final_chunks = []
    for chunk in merged:
        if chunk["token_count"] > 1500:
            splits = splitter.split_text(chunk["content"])
            for text_split in splits:
                final_chunks.append({
                    "chunk_id": len(final_chunks),
                    "heading_path": chunk["heading_path"],
                    "content": text_split,
                })
        else:
            chunk["chunk_id"]=len(final_chunks)
            final_chunks.append(chunk)
    
    return {
        "normalized_chunks": final_chunks
    }
    