import requests
import random
import os
import json
import re
import ast
import sys
import io

# --- Force UTF-8 stdout for Windows ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("[DEBUG] Starting prompt_regen.py")

# --- Get rewrite instruction from argv ---
if len(sys.argv) < 2:
    print("[ERROR] No rewrite instruction provided.")
    sys.exit(1)

rewrite_instruction = sys.argv[1].strip()
print(f"[DEBUG] Rewrite instruction: {rewrite_instruction}")

# --- Load existing prompt (input.json) ---
input_file = "prompts/input.json"
if not os.path.exists(input_file):
    print(f"[ERROR] {input_file} not found.")
    sys.exit(1)

with open(input_file, "r", encoding="utf-8") as f:
    flux_payload = json.load(f)

current_positive = flux_payload.get("inputs", "")
current_negative = flux_payload.get("parameters", {}).get("negative_prompt", "")

print(f"[DEBUG] Current positive prompt (first 200 chars):\n{current_positive[:200]}...")
print(f"[DEBUG] Current negative prompt (first 200 chars):\n{current_negative[:200]}...")

# --- Setup HuggingFace API ---
ACCESS_TOKEN = sys.argv[-1] 
API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

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
        {
            "role": "user",
            "content": (
                f"Current positive prompt:\n{current_positive}\n\n"
                f"Current negative prompt:\n{current_negative}\n\n"
                f"Instruction:\n{rewrite_instruction}"
            )
        }
    ],
    "temperature": 0.4,
    "max_tokens": 400
}

# --- Send request ---
try:
    print("[DEBUG] Sending request to HuggingFace API...")
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    resp_json = response.json()
    print("[DEBUG] Response received from API")
    print(f"[DEBUG] Raw response keys: {list(resp_json.keys())}")
except requests.RequestException as e:
    print(f"[ERROR] API request failed: {e}")
    sys.exit(1)

# --- Extract model output robustly ---
msg = ""
try:
    if "choices" in resp_json and len(resp_json["choices"]) > 0:
        choice = resp_json["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            msg = choice["message"]["content"]
            print("[DEBUG] Extracted message.content from choices[0]")
        elif "text" in choice:
            msg = choice["text"]
            print("[DEBUG] Extracted text from choices[0]")
    elif "output_text" in resp_json:
        msg = resp_json["output_text"]
        print("[DEBUG] Extracted output_text from response")
    elif "generated_text" in resp_json:
        msg = resp_json["generated_text"]
        print("[DEBUG] Extracted generated_text from response")

    if not msg:
        print("[ERROR] No valid text output found from API")
        print(json.dumps(resp_json, indent=2, ensure_ascii=False))
        raise ValueError("No valid text output")
except Exception as e:
    print(f"[ERROR] Failed to extract model output: {e}")
    sys.exit(1)

print(f"[DEBUG] Raw model output (first 500 chars):\n{msg[:500]}...")

# --- Extract JSON safely ---
def extract_json(msg: str):
    print("[DEBUG] Extracting JSON from model output")
    
    # Try fenced JSON first
    fenced = re.search(r"```json\s*(\{.*\})\s*```", msg, re.DOTALL)
    if fenced:
        json_str = fenced.group(1)
        print("[DEBUG] Found fenced JSON")
    else:
        braced = re.search(r"(\{.*\})", msg, re.DOTALL)
        json_str = braced.group(1) if braced else msg
        print("[DEBUG] Using braced or raw string as JSON")

    try:
        parsed = json.loads(json_str)
        print("[DEBUG] Successfully parsed JSON with json.loads")
        return parsed
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        print(f"[ERROR] Raw string:\n{json_str[:1000]}...")  # print first 1000 chars for debugging
        raise


try:
    rewritten = extract_json(msg)
except Exception as e:
    print(f"[ERROR] Failed to parse JSON from model output: {e}")
    sys.exit(1)

print(f"[DEBUG] Rewritten positive prompt (first 300 chars):\n{rewritten.get('positive_prompt', '')[:300]}...")
print(f"[DEBUG] Rewritten negative prompt (first 300 chars):\n{rewritten.get('negative_prompt', '')[:300]}...")

# --- Merge rewritten prompt safely ---
flux_payload["inputs"] = rewritten.get("positive_prompt", current_positive)
flux_payload["parameters"]["negative_prompt"] = rewritten.get("negative_prompt", current_negative)
print("[DEBUG] Merged rewritten prompts into flux_payload")

# --- Save rewritten prompt ---
os.makedirs("prompts", exist_ok=True)
with open(input_file, "w", encoding="utf-8") as f:
    json.dump(flux_payload, f, indent=2, ensure_ascii=False)
print(f"✅ Saved rewritten Flux prompt to {input_file}")
