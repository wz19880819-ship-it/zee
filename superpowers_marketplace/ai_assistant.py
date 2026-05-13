"""Claude-powered assistant for the superpowers marketplace."""

from __future__ import annotations

import anthropic

from . import marketplace


def query_superpowers(prompt: str) -> str:
    """Search the catalog for relevant superpowers and ask Claude to explain them."""
    catalog_hits = marketplace.search(prompt)
    if not catalog_hits:
        catalog_hits = marketplace.get_all()

    catalog_text = "\n".join(
        f"- {sp['name']} v{sp['version']}: {sp['description']} (tags: {', '.join(sp.get('tags', []))})"
        for sp in catalog_hits
    )

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=1024,
        thinking={"type": "adaptive"},
        system=(
            "You are a helpful assistant for the Superpowers Marketplace. "
            "Use the catalog data provided to give accurate, specific recommendations."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Available superpowers from the marketplace:\n{catalog_text}\n\n"
                    f"User question: {prompt}"
                ),
            }
        ],
    ) as stream:
        return stream.get_final_message().content[0].text
