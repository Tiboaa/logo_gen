
import os
import requests
import random
import json
import sys


MODEL = "black-forest-labs/FLUX.1-schnell"
def main(api_key):
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {api_key}"}

    with open("prompts\input.json", "r") as f:
        payload = json.load(f)

    payload["parameters"]["seed"] = random.randint(0, 2**32 - 1)    

    resp = requests.post(url, headers=headers, json=payload)
    if not resp.ok:
        print("Error:", resp.status_code, resp.text)
        resp.raise_for_status()

    i = 0
    while True:
        filename = f"output_pics/logo_{i:04d}.png"
        if not os.path.exists(filename):
            break
        i += 1

    with open(filename, "wb") as f:
        f.write(resp.content)

    print(f"Saved image to {filename}")
    print(f"The seed is: {payload['parameters']['seed']}")