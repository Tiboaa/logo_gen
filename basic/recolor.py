import os
import requests
import random
import json
from PIL import Image

ACCESS_TOKEN = "" # PLACE TOKEN HERE
MODEL = "black-forest-labs/FLUX.1-schnell"

url = f"https://api-inference.huggingface.co/models/{MODEL}"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Load payload
with open(r"basic\payload.json", "r") as f:
    payload = json.load(f)

# Set a random seed
payload["parameters"]["seed"] = random.randint(0, 2**32 - 1)

# Call API
resp = requests.post(url, headers=headers, json=payload)
if not resp.ok:
    print("Error:", resp.status_code, resp.text)
    resp.raise_for_status()

# Prepare output folder
os.makedirs("output_pics", exist_ok=True)

i = 0
while True:
    filename = os.path.join("output_pics", f"logo_{i:04d}.png")
    if not os.path.exists(filename):
        break
    i += 1

# Save raw image
with open(filename, "wb") as f:
    f.write(resp.content)

print(f"Saved image to {filename}")
print(f"The seed is: {payload['parameters']['seed']}")

# --- Recolor dark pixels to hex ---
hex_color = "#7434eb"  # desired color
r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
black_threshold = 100  # adjust for wider range of dark pixels

# Helper function
def is_dark(pixel, threshold=100):
    r_, g_, b_ = pixel[:3]
    luminance = 0.2126*r_ + 0.7152*g_ + 0.0722*b_  # perceptual luminance
    return luminance < threshold

# Open image
img = Image.open(filename).convert("RGBA")
datas = img.getdata()
new_data = []

for item in datas:
    if is_dark(item, black_threshold):
        new_data.append((r, g, b, item[3]))  # replace dark pixel with hex color
    else:
        new_data.append(item)

img.putdata(new_data)
recolor_filename = filename.replace(".png", "_colored.png")
img.save(recolor_filename)
print(f"Saved recolored image to {recolor_filename}")
