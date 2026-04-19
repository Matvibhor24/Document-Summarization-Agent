CHUNK_SUMMARY_PROMPT = """
Document: {title}
Section path: {heading_path}

Section content:
{content}

Summarize this specific section in 2-4 sentences.
- Preserve all numbers, dates, names, and key findings exactly.

Respond in this exact JSON format:
{{
  "summary": "<your summary>"
}}

STRICTLY output ONLY valid JSON, no explanation.
"""
