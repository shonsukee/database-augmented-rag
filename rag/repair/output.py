"""Layout of the result files under results/."""
from pathlib import Path

RESPONSE_HEADER = "# LLM Response\n"
QUERY_HEADER = "\n\n# User Query\n"


def wrap_response(response: str, language: str) -> str:
    """Fence a response that came back as bare code, using the input file extension."""
    if "```" in response:
        return response
    return f"```{language}\n{response}\n```"


def result_dir(output_dir, configuration: str, service: str, source_type: str, input_name: str) -> Path:
    return Path(output_dir) / configuration / service / source_type / Path(input_name).stem


def save_result(directory, trial: int, prompt: str, response: str) -> Path:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{trial}.md"
    path.write_text(f"{RESPONSE_HEADER}{response or 'None'}{QUERY_HEADER}{prompt}", encoding="utf-8")
    return path
