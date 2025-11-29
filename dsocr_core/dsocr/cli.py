import argparse
from pathlib import Path
from typing import Optional

from dsocr.api import ocr_image_with_deepseek
from dsocr.utils import image_file_to_base64, ensure_output_dir, default_output_path, save_text_to_file

DEFAULT_PROMPT = "你是一个 OCR 识别助手，提取文本并将任何表格转换为 Markdown。"
DEFAULT_OUTPUT_DIR = "ocr-cli-output"


def parse_args():
    parser = argparse.ArgumentParser(description="OCR CLI: recognize text from an image using DeepSeek-OCR")
    parser.add_argument("--input", help="Path to the input image file to recognize")
    parser.add_argument("--api-key", "-k", dest="api_key", required=True, help="SiliconFlow API key (required)")
    parser.add_argument("--prompt", "-p", dest="prompt", default=DEFAULT_PROMPT, help="Prompt to the OCR model")
    parser.add_argument("--output", "-o", dest="output", default=None, help="Output file path (optional)")
    parser.add_argument("--output-dir", dest="output_dir", default=None, help="Output directory (optional)")
    parser.add_argument("--ext", dest="ext", default=".md", help="Output file extension")
    parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debug output")
    return parser.parse_args()


def run_cli(input_path: str, api_key: str, prompt: str = DEFAULT_PROMPT, output: Optional[str] = None, output_dir: Optional[str] = None, ext: str = ".md", debug: bool = False):
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output:
        out_path = Path(output)
        ensure_output_dir(str(out_path.parent))
        final_output = str(out_path.resolve())
    else:
        out_dir = output_dir if output_dir else DEFAULT_OUTPUT_DIR
        ensure_output_dir(out_dir)
        final_output = default_output_path(str(p), out_dir, ext=ext)

    if debug:
        print(f"Input: {input_path}")
        print(f"Output: {final_output}")
        print(f"Prompt: {prompt}")

    image_b64 = image_file_to_base64(str(p))
    result = ocr_image_with_deepseek(image_b64, api_key, prompt)
    if not result.get("success"):
        raise RuntimeError(f"OCR failed: {result.get('error')}")

    # Prefer cleaned content, fallback to raw content if cleaned is empty
    content = result.get("clean_content") or result.get("raw_content") or ""

    if debug:
        print("--- OCR Result Debug ---")
        print("success:", result.get("success"))
        print("raw_content:", repr(result.get("raw_content")))
        print("clean_content:", repr(result.get("clean_content")))
        # print full JSON if available
        if result.get("raw_json"):
            import json
            print("raw_json:", json.dumps(result.get("raw_json"), ensure_ascii=False)[:2000])
        print("------------------------")

    if not content:
        # No content was returned; prepare a diagnostic message and write that to file
        print("Warning: OCR returned empty content. Writing diagnostic information to the output file.")
        diag_lines = []
        diag_lines.append("# OCR Diagnostic Report\n")
        diag_lines.append("- Input file: {}\n".format(input_path))
        diag_lines.append("- API key present: {}\n".format(bool(api_key)))
        if result.get("raw_json"):
            import json
            diag_lines.append("\n## Raw JSON (truncated)\n")
            diag_lines.append(json.dumps(result.get("raw_json"), ensure_ascii=False)[:20000])
        else:
            diag_lines.append("No raw JSON available. Result object: {}\n".format(result))
        content = "\n".join(diag_lines)

    save_text_to_file(content, final_output)
    return final_output


if __name__ == "__main__":
    args = parse_args()
    out = run_cli(args.input, args.api_key, args.prompt, args.output, args.output_dir, args.ext, args.debug)
    print(f"Saved OCR result to: {out}")
