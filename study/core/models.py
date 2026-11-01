"""Stand-in for the private model-access layer used to run this study.

The study's models were called through cloud APIs; the access layer itself isn't published. To re-run the study,
implement Models.call() with your own provider's client, returning the same fields. Model names and IDs below are
the ones used (IDs are the providers' identifiers on the run dates; see each design's run notes).
"""

MODELS = {  # the frozen v1.0 sample: seven models from three vendors
    "claude-opus-5.5":   ("anthropic", "claude-opus-5-5", "Anthropic"),
    "claude-sonnet-5.5": ("anthropic", "claude-sonnet-5-5", "Anthropic"),
    "claude-haiku-5.5":  ("anthropic", "claude-haiku-5-5", "Anthropic"),
    "claude-sonnet-4.6": ("anthropic", "claude-sonnet-4-6", "Anthropic"),
    "nova-pro":          ("converse", "amazon.nova-pro-v1:0", "Amazon"),
    "nova-lite":         ("converse", "amazon.nova-lite-v1:0", "Amazon"),
    "qwen3-32b":         ("converse", "qwen.qwen3-32b-v1:0", "Alibaba"),
}
EXTRA_MODELS = {  # E1 and E2 (named explicitly when run)
    "gpt-4o-mini": ("openai", "gpt-4o-mini-2024-07-18", "OpenAI"),
    "gpt-4o":      ("openai", "gpt-4o-2024-11-20", "OpenAI"),
    "gpt-5.5":     ("openai", "gpt-5.5-2026-04-24", "OpenAI"),
    "gpt-6-sol":   ("openai", "gpt-6-sol-2026-09-22", "OpenAI"),
}


class Models:
    def call(self, key: str, prompt: str, max_tokens: int = 700) -> dict:
        """Return {"text", "model_id", "vendor", "input_tokens", "output_tokens", "stop_reason", "seconds", "ok"}."""
        raise NotImplementedError("Plug in your own API client here (see the module docstring).")
