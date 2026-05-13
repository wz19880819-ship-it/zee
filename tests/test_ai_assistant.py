"""Tests for the Claude-powered AI assistant."""

from unittest.mock import MagicMock, patch

import superpowers_marketplace.ai_assistant  # ensure module is loaded before patching
from superpowers_marketplace.ai_assistant import query_superpowers


def _mock_stream(text: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=text)]
    stream = MagicMock()
    stream.get_final_message.return_value = msg
    stream.__enter__ = MagicMock(return_value=stream)
    stream.__exit__ = MagicMock(return_value=False)
    return stream


@patch("superpowers_marketplace.ai_assistant.anthropic.Anthropic")
def test_query_returns_text(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client
    mock_client.messages.stream.return_value = _mock_stream("Use the healing superpower.")

    result = query_superpowers("retry on failure")
    assert isinstance(result, str)
    assert len(result) > 0


@patch("superpowers_marketplace.ai_assistant.anthropic.Anthropic")
def test_query_passes_catalog_to_claude(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client
    mock_client.messages.stream.return_value = _mock_stream("recommendation text")

    query_superpowers("async tasks")

    call_kwargs = mock_client.messages.stream.call_args.kwargs
    user_content = call_kwargs["messages"][0]["content"]
    assert "flight" in user_content  # async superpower should appear in catalog hit
    assert "async tasks" in user_content


@patch("superpowers_marketplace.ai_assistant.anthropic.Anthropic")
def test_query_uses_correct_model(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client
    mock_client.messages.stream.return_value = _mock_stream("ok")

    query_superpowers("anything")

    call_kwargs = mock_client.messages.stream.call_args.kwargs
    assert call_kwargs["model"] == "claude-opus-4-7"
    assert call_kwargs["thinking"] == {"type": "adaptive"}
