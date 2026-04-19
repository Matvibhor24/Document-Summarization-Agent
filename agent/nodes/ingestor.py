from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

def ingest_node(state: dict) -> dict:
    pipeline_opts = PdfPipelineOptions()
    pipeline_opts.do_ocr = True
    converter = DocumentConverter(
        format_options={InputFormat.PDF:PdfFormatOption(pipeline_options=pipeline_opts)}
    )
    
    result = converter.convert(state["file_path"])
    doc = result.document
    hierarchy = []
    raw_chunks = []
    current_path = ["Document Start"]

    for item, level in doc.iterate_items():
        text_content = item.text.strip() if hasattr(item, "text") and item.text else ""
        if item.label.name in ["title", "section_header"]:
            title=text_content
            lvl = level if level>0 else 1
            hierarchy.append({"level": lvl, "title": title})

            current_path = current_path[:lvl-1] + [title]
            continue
        
        if item.label.name=="table":
            text_content=item.export_to_markdown()
            
        if text_content:
            raw_chunks.append({
                "chunk_id":len(raw_chunks),
                "heading_path": list(current_path),
                "content": text_content,
                "token_count": len(text_content.split())
            })
    
    return {
        "doc_metadata": {"title": doc.name or "Parsed Document"},
        "hierarchy": hierarchy,
        "raw_chunks": raw_chunks
    }
    