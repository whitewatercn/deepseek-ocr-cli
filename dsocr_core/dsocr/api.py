import requests
import re
from typing import Dict

API_URL = "https://api.siliconflow.cn/v1/chat/completions"


def ocr_image_with_deepseek(image_b64: str, api_key: str, prompt: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-ai/DeepSeek-OCR",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}, "type": "image_url"},
                    {"type": "text", "text": f"<image>\n<|grounding|>{prompt}"},
                ],
            }
        ],
        "stream": False,
        "response_format": {"type": "text"},
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        raw_content = data.get("choices", [])[0].get("message", {}).get("content", "")
        # Remove marker tags but preserve inner content if any (avoid deleting text)
        clean_content = re.sub(r"<\|/?ref\|>", "", raw_content)
        clean_content = re.sub(r"<\|/?det\|>", "", clean_content)
        clean_content = clean_content.strip()

        # Also include raw_json to help debug unexpected responses
        return {"raw_content": raw_content, "clean_content": clean_content, "success": True, "raw_json": data}
    except Exception as e:
        return {"raw_content": "", "clean_content": "", "success": False, "error": str(e)}
