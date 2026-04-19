import operator
from typing import Annotated
from typing_extensions import TypedDict

class DocumentState(TypedDict):
    file_path: str
    doc_metadata: dict
    hierarchy: list[dict]
    raw_chunks: list[dict]
    normalized_chunks: list[dict]
    chunk_summaries: Annotated[list[dict], operator.add]
    final_output: str
