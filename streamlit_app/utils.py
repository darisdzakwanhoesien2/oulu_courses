from pathlib import Path

def resolve_path(root: Path, relative: str) -> Path:
    p = root / relative
    if not p.exists():
        raise FileNotFoundError(f"{p} not found")
    return p