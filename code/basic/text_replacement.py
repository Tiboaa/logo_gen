from PIL import Image, ImageDraw, ImageFont
import os

# Paths
logo_path = "inwb_logo_001.png"   # your existing logo
output_dir = "outputs"

# Make sure output folder exists
os.makedirs(output_dir, exist_ok=True)

# Open logo
logo = Image.open(logo_path)

# Create a new canvas to fit logo + text
width, height = logo.size
new_width = width + 400  # extra space for text
canvas = Image.new("RGB", (new_width, height), "white")

# Paste logo onto canvas
canvas.paste(logo, (0, 0))

# Draw text
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype("arialbd.ttf", 50)  # Arial Bold
text = "Arial Bold Test"
text_x = width + 20
text_y = (height - 50) // 2
draw.text((text_x, text_y), text, fill="black", font=font)

# Save output
i = 0
while True:
    filename = os.path.join(output_dir, f"logo_text_{i:04d}.png")
    if not os.path.exists(filename):
        break
    i += 1

canvas.save(filename)
print(f"Saved image to {filename}")
