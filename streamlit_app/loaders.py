import json
from pathlib import Path

def load_registry(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)["projects"]