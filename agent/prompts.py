CHUNK_SUMMARY_PROMPT = """
Document: {title}
Section path: {heading_path}

Section content:
{content}

Summarize this specific section in 2-4 sentences.
- Preserve all numbers, dates, names, and key findings exactly.
- Rate your confidence from 0.0 to 1.0 that this summary is accurate and complete.

Respond in this exact JSON format:
{{
  "summary": "<your summary>",
  "confidence": <0.0-1.0>
}}

STRICTLY output ONLY valid JSON, no explanation.
"""
