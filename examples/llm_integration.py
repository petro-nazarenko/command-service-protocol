"""examples/llm_integration.py — Process LLM-generated CSP commands"""
from csprotocol import handle

def process_llm_output(raw: str) -> str:
    return handle(raw.strip())

llm_outputs = [
    'g "Improve onboarding"',
    "up dry",
    "m force",
    "sync",    # Not in MVP — returns ERROR
]

for output in llm_outputs:
    result = process_llm_output(output)
    status = "OK " if not result.startswith("ERROR") else "ERR"
    print(f"[{status}] {output!r:35} -> {result}")
