import requests
import random
import os
import json
import re
import ast
import io
import sys

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def generate_prompt_file(api_key: str) -> str:
    delete_input_file()
    print("[DEBUG] Loading logo_data.json...")
    logo_data = {}
    with open("basic/logo_data.json", "r", encoding="utf-8") as f:
        for line in f:
            if ": " in line:
                key, value = line.strip().split(": ", 1)
                logo_data[key] = value
    print(f"[DEBUG] Loaded logo_data: {logo_data}")

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
                    "You are a prompt generator for the Flux image model. "
                    "Use the logo data to produce a detailed positive prompt describing the logo. "
                    "Also produce a negative prompt describing things to avoid. "
                    "Always output valid JSON with 'positive_prompt' and 'negative_prompt' keys."
                )
            },
            {"role": "user", "content": f"Here is the logo data:\n{logo_data}"}
        ],
        "temperature": 0.4,
        "max_tokens": 600
    }

    print("[DEBUG] Sending request to HuggingFace API...")
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    resp_json = response.json()
    print("[DEBUG] Response received from API.")

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


    flux_payload = {
        "inputs": generated.get("positive_prompt", ""),
        "parameters": {
            "width": 512,
            "height": 512,
            "negative_prompt": generated.get("negative_prompt", ""),
            "num_inference_steps": 120,
            "guidance_scale": 20,
            "seed": random.randint(0, 2**32 - 1)
        }
    }

    

    os.makedirs("prompts", exist_ok=True)
    filename = "prompts/input.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(flux_payload, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Saved Flux prompt to {filename} (JSON format)")
    return filename

def delete_input_file():
    file_path = "prompts/input.json"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[INFO] Deleted existing file: {file_path}")
    else:
        print(f"[INFO] No file to delete at {file_path}")