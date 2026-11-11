"""Prompt templates and prompt construction. No network access."""
import string
from pathlib import Path
from typing import Dict, Iterable, List

from rag.config import CONFIGURATIONS

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"
INPUT_VARIABLE = "user_query"


def load_template(configuration: str) -> str:
    """Return the prompt template of a RAG configuration.

    The baseline (0_BL) is rejected: it was run by hand in ChatGPT, so this pipeline
    has no code path for it. Its prompt text is kept in rag/prompts/0_BL.md for reference.
    """
    if configuration not in CONFIGURATIONS:
        raise ValueError(
            f"unknown configuration: {configuration!r} (choose from {', '.join(CONFIGURATIONS)})"
        )
    return (PROMPT_DIR / f"{configuration}.md").read_text(encoding="utf-8")


def template_variables(template: str) -> List[str]:
    return [name for _, name, _, _ in string.Formatter().parse(template) if name is not None]


def index_name(database: str) -> str:
    """Pinecone index names cannot contain underscores."""
    return database.replace("_", "-")


def format_nodes(nodes: Iterable) -> str:
    """Render retrieved chunks the way they appear in the prompt.

    Each node needs a `score` and a `text` attribute.
    """
    return "\n\n".join(
        f"【Context No.{number}】\n[similarity: {node.score}]\n{node.text}"
        for number, node in enumerate(nodes, 1)
    )


def build_prompt(template: str, values: Dict[str, str]) -> str:
    missing = [name for name in template_variables(template) if name not in values]
    if missing:
        raise KeyError(f"values missing for template variables: {missing}")
    return template.format(**values)


def split_prompt(template: str, prompt: str) -> Dict[str, str]:
    """Inverse of build_prompt: recover the value of each variable from a built prompt.

    Used to read the retrieved chunks back out of a stored result file.
    """
    values: Dict[str, str] = {}
    parts = list(string.Formatter().parse(template))
    position = 0
    pending = None
    for number, (literal, name, _, _) in enumerate(parts):
        is_last = number == len(parts) - 1
        if pending is None:
            if not prompt.startswith(literal, position):
                raise ValueError("prompt does not start with the template text")
            start = position
        elif is_last and name is None:
            # The closing text is matched from the end so that the same words
            # inside a retrieved chunk cannot be mistaken for it.
            if not prompt.endswith(literal):
                raise ValueError("prompt does not end with the template text")
            start = len(prompt) - len(literal)
        else:
            start = prompt.find(literal, position)
            if start == -1:
                raise ValueError(f"template text not found in prompt: {literal[:40]!r}")
        if pending is not None:
            values[pending] = prompt[position:start]
        position = start + len(literal)
        pending = name
    if pending is not None:
        values[pending] = prompt[position:]
    return values
