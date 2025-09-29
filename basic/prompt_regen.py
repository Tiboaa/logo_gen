import requests
import random
import os
import json
import re
import ast

def regenerate_prompt(change_text: str, api_key: str) -> str:
    """
    Regenerates an existing prompt based on `change_text` and saves it to prompts/input.json.
    Returns the path to the saved file.
    """
    delete_input_file()
    print("[DEBUG] Loading existing input.json...")
    input_file = "prompts/input.json"
    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            existing_prompt = json.load(f)
    else:
        existing_prompt = {"inputs": "", "parameters": {}}

    print(f"[DEBUG] Existing positive prompt: {existing_prompt.get('inputs', '')[:100]}...")

    # --- Setup HuggingFace API ---
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-120b:cerebras",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a prompt rewriter for the Flux image model. "
                    "Rewrite the positive prompt according to the user's instructions. "
                    "Keep the original prompt as much as possible, but emphasize the user's instructions. "
                    "Fix contradictions between positive and negative prompts. "
                    "Simplify negative prompts if too complex. "
                    "Always output valid JSON with 'positive_prompt' and 'negative_prompt'."
                )
            },
            {"role": "user", "content": f"Existing prompt:\n{existing_prompt.get('inputs','')}\n\nUpdate instructions:\n{change_text}"}
        ],
        "temperature": 0.4,
        "max_tokens": 600
    }

    print("[DEBUG] Sending request to HuggingFace API for regeneration...")
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    resp_json = response.json()
    print("[DEBUG] Response received from API.")

    # Extract text
    msg = ""
    if "choices" in resp_json and len(resp_json["choices"]) > 0:
        choice = resp_json["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            msg = choice["message"]["content"]
        elif "text" in choice:
            msg = choice["text"]
    elif "output_text" in resp_json:
        msg = resp_json["output_text"]
    elif "generated_text" in resp_json:
        msg = resp_json["generated_text"]

    print(f"[DEBUG] Raw model output (first 500 chars):\n{msg[:500]}...")

    # Extract JSON
    def extract_json(msg: str):
        fenced = re.search(r"```json\s*(\{.*?\})\s*```", msg, re.DOTALL)
        if fenced:
            json_str = fenced.group(1)
        else:
            braced = re.search(r"(\{.*\})", msg, re.DOTALL)
            json_str = braced.group(1) if braced else None
        if json_str:
            try:
                return ast.literal_eval(json_str)
            except Exception:
                cleaned = json_str.replace("\n", " ").replace("\r", "")
                return json.loads(cleaned)
        return {"positive_prompt": msg.strip(), "negative_prompt": ""}

    generated = extract_json(msg)

    # Prepare flux payload
    flux_payload = {
        "inputs": generated.get("positive_prompt", ""),
        "parameters": {
            "width": existing_prompt.get("parameters", {}).get("width", 512),
            "height": existing_prompt.get("parameters", {}).get("height", 512),
            "negative_prompt": generated.get("negative_prompt", ""),
            "num_inference_steps": existing_prompt.get("parameters", {}).get("num_inference_steps", 120),
            "guidance_scale": existing_prompt.get("parameters", {}).get("guidance_scale", 20),
            "seed": random.randint(0, 2**32 - 1)
        }
    }

    os.makedirs("prompts", exist_ok=True)
    filename = "prompts/input.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(flux_payload, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Saved regenerated Flux prompt to {filename} (JSON format)")
    return filename

def delete_input_file():
    file_path = "prompts/input.json"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[INFO] Deleted existing file: {file_path}")
    else:
        print(f"[INFO] No file to delete at {file_path}")    