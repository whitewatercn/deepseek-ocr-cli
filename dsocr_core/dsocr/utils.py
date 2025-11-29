import base64
import os
from pathlib import Path


def image_file_to_base64(image_path: str) -> str:
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    with p.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ensure_output_dir(dir_path: str) -> str:
    p = Path(dir_path)
    p.mkdir(parents=True, exist_ok=True)
    return str(p.resolve())


def default_output_path(input_path: str, output_dir: str, suffix: str = "-ocr-cli-output", ext: str = ".md") -> str:
    stem = Path(input_path).stem
    return os.path.join(output_dir, f"{stem}{suffix}{ext}")


def save_text_to_file(text: str, output_path: str) -> None:
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        f.write(text)
