import os
import requests
import random
import json
import sys

hardcoded_vars = {
    "subject_clr_0": "blue, yellow and green",
    "subject_clr_1" : "black",
    "letter": "",
    "shape": "",
    "shape_ular": "",
    "shape_2": "",
    "shape_2_ular": "",
    "text_clr_0": "",
    "text_clr_1": "",
    "text_0": "CEG KFT",
    "text_1": "",
    "font": ""
}

import sys
import json
global variables_json, preset_name, api_key, variables

'''if len(sys.argv) > 1:
    variables_json = sys.argv[1]          # first argument is JSON
    preset_name = sys.argv[2] if len(sys.argv) > 2 else "a1"
    api_key = sys.argv[3] if len(sys.argv) > 3 else ""
    variables = json.loads(variables_json)
else:
    variables = hardcoded_vars.copy()
    preset_name = "a1"
    api_key = ""'''


# --- API setup ---
#ACCESS_TOKEN = api_key
MODEL = "black-forest-labs/FLUX.1-schnell"
URL = f"https://api-inference.huggingface.co/models/{MODEL}"

def generate_image(variables_json, preset_name, api_key):
    variables_json
    if variables_json is None:
        variables_json = hardcoded_vars.copy()

    headers = {"Authorization": f"Bearer {api_key}"}

    premade_propmt = os.path.join("premade_prompts", f"{preset_name}.json")

    with open(premade_propmt, "r", encoding="utf-8") as f:
        premade_data = json.load(f)

    payload = premade_data.copy()
    inputs_template = payload["inputs"]
    payload["inputs"] = inputs_template.format(**variables_json)

    if "variables" in payload:
        del payload["variables"]

    payload["parameters"]["seed"] = random.randint(0, 2**32 - 1)

    # --- DEBUG ---

    print(f"\nRandom seed used: {payload['parameters']['seed']}")
    print("IMAGE GENERATION IS COMMENTED OUT")
# --- UNCOMMENT BELOW TO SEND TO API !!! ---

'''resp = requests.post(url, headers=headers, json=payload)
if not resp.ok:
    print("Error:", resp.status_code, resp.text)
    resp.raise_for_status()
 
os.makedirs("output_pics", exist_ok=True)
i = 0
while True:
    filename = f"output_pics/logo_{i:04d}.png"
    if not os.path.exists(filename):
        break
    i += 1

with open(filename, "wb") as f:
    f.write(resp.content)

print(f"Saved image to {filename}")'''
