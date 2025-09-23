import os
import requests
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Hugging Face API setup
ACCESS_TOKEN = "" # PLACE TOKEN HERE
MODEL = "black-forest-labs/FLUX.1-schnell"
PROMPT = "A logo of a happy golden retriever, that looks up. Looking at it's tail, we can tell the dog is happy." \
    "Only the black stylized outline of the dog silhouette is visible. " \
    "The logo has a circle around it with the top open so it forms a tilted C shape." \
    "The logo should be abstract, stylized, black, monocrome and simple but nice"


url = f"https://api-inference.huggingface.co/models/{MODEL}"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Random seed for variation
seed = random.randint(0, 2**32 - 1)

payload = {
    "inputs": PROMPT,
    "parameters": {
        "width": 512,
        "height": 512,
        "num_inference_steps": 120,
        "guidance_scale": 30,
        "seed": seed
    }
}

# Request logo from Hugging Face
resp = requests.post(url, headers=headers, json=payload)
resp.raise_for_status()

# Convert response to PIL image
logo = Image.open(BytesIO(resp.content))

# Prepare canvas for logo + text
width, height = logo.size
new_width = width + 800  # extra space for text
canvas = Image.new("RGB", (new_width, height), "white")

# Paste logo onto canvas
canvas.paste(logo, (0, 0))

# Draw text
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("arialbd.ttf", 50)  # Arial Bold if available
except OSError:
    font = ImageFont.load_default()  # fallback if font not found

text = "Arial Bold Test"
text_x = width + 20
text_y = (height - 50) // 2
draw.text((text_x, text_y), text, fill="black", font=font)

# Save output incrementally
os.makedirs("outputs", exist_ok=True)
i = 0
while True:
    filename = os.path.join("outputs", f"logo_text_{i:04d}.png")
    if not os.path.exists(filename):
        break
    i += 1

canvas.save(filename)
print(f"Saved image to {filename}")
