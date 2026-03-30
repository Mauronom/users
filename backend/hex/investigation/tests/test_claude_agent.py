import json
import pytest
from unittest.mock import patch, MagicMock
from hex.investigation.infra.claude_agent import ClaudeCliAgent
from hex.investigation.domain import RateLimitError

_VALID_CLASSIFY_OUTPUT = json.dumps({
    "structured_output": {
        "type": "scout",
        "new_clues": [],
    }
})

_VALID_EXTRACT_OUTPUT = json.dumps({
    "structured_output": {
        "nom": "Paupaterres",
        "mail": "info@paupaterres.cat",
        "new_clues": [],
    }
})


def _mock_result(stdout="", stderr="", returncode=0):
    r = MagicMock()
    r.stdout = stdout
    r.stderr = stderr
    r.returncode = returncode
    return r


def test_rate_limit_in_stdout_does_not_raise():
    """JSON response mentioning 'rate limit' in content should NOT trigger RateLimitError."""
    output = json.dumps({
        "structured_output": {
            "type": "entity",
            "notes": "This venue has a rate limit policy for ticket sales",
            "new_clues": [],
        }
    })
    with patch("subprocess.run", return_value=_mock_result(stdout=output)):
        agent = ClaudeCliAgent()
        # should not raise
        result = agent.classify("some clue", [])
        assert result.type == "entity"


def test_rate_limit_in_stderr_raises():
    """Rate limit signal in stderr should raise RateLimitError."""
    with patch("subprocess.run", return_value=_mock_result(
        stdout="", stderr="Error: rate limit exceeded", returncode=1
    )):
        agent = ClaudeCliAgent()
        with pytest.raises(RateLimitError):
            agent.classify("some clue", [])


def test_429_in_stderr_raises():
    """429 in stderr should raise RateLimitError."""
    with patch("subprocess.run", return_value=_mock_result(
        stdout="", stderr="HTTP 429 Too Many Requests", returncode=1
    )):
        agent = ClaudeCliAgent()
        with pytest.raises(RateLimitError):
            agent.classify("some clue", [])


def test_classify_result_includes_summary():
    output = json.dumps({
        "structured_output": {
            "type": "scout",
            "summary": "Banda indie barcelonina amb concerts a sala Apolo",
            "new_clues": [],
        }
    })
    with patch("subprocess.run", return_value=_mock_result(stdout=output)):
        agent = ClaudeCliAgent()
        result = agent.classify("some clue", [])
        assert result.summary == "Banda indie barcelonina amb concerts a sala Apolo"


def test_extract_uses_summary_and_web_in_prompt():
    with patch("subprocess.run", return_value=_mock_result(stdout=_VALID_EXTRACT_OUTPUT)) as mock_run:
        agent = ClaudeCliAgent()
        agent.extract("Paupaterres", summary="Festival de folk", web="paupaterres.cat")
        cmd = mock_run.call_args[0][0]
        prompt = cmd[2]  # claude -p <prompt> ...
        assert "Festival de folk" in prompt
        assert "paupaterres.cat" in prompt


def test_429_in_stdout_content_does_not_raise():
    """A URL or note containing '429' in the JSON response should NOT raise RateLimitError."""
    output = json.dumps({
        "structured_output": {
            "type": "entity",
            "web": "https://example.com/error/429",
            "new_clues": [],
        }
    })
    with patch("subprocess.run", return_value=_mock_result(stdout=output)):
        agent = ClaudeCliAgent()
        result = agent.classify("some clue", [])
        assert result.type == "entity"
