def compose_node(state: dict) -> dict:
    title = state.get("doc_metadata", {}).get("title", "Document")
    hierarchy = state.get("hierarchy",[])

    summaries = sorted(state.get("chunk_summaries", []), key=lambda x: x["chunk_id"])
    out = [f"# {title}\n"]

    visited_ids = set()
    
    for node in hierarchy:
        level_hashes = "#" * (node.get("level", 1) + 1)
        out.append(f"\n{level_hashes} {node['title']}")
        
        # Finding any summaries that belong to exactly this heading
        matched = [
            s for s in summaries 
            if s["chunk_id"] not in visited_ids and node["title"] in s["heading_path"]
        ]
        
        for s in matched:
            out.append(s["summary"])
            visited_ids.add(s["chunk_id"])

    leftovers = [s for s in summaries if s["chunk_id"] not in visited_ids]
    if leftovers:
        for s in leftovers:
            out.append(s["summary"])
    return {"final_output": "\n".join(out)}
