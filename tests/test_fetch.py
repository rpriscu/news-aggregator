import subprocess
import sys
import json

def test_fetch_example():
    result = subprocess.run(
        [sys.executable, "-m", "src.fetch", "https://example.com"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    for key in ["id", "url", "title", "author", "published_at", "text"]:
        assert key in data