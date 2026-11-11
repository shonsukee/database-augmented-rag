"""Repair generation with the OpenAI API."""
from openai import OpenAI

from rag.config import GENERATION_MODEL, SYSTEM_PROMPT


def generate(client: OpenAI, service: str, prompt: str) -> str:
    # No sampling parameters are passed, so the API defaults apply.
    completion = client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(service=service)},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content or ""
