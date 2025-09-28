import sys
from PIL import Image
import os

white = 240
black = 60

if len(sys.argv) < 2:
    print("Usage: python alpha_chanel.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
name, ext = os.path.splitext(input_file)
output_file = f"{name}_transparent.png"

img = Image.open(input_file).convert("RGBA")
datas = img.getdata()

new_data = []
for item in datas:
    r, g, b, a = item
    if r >= white and g >= white and b >= white:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)

img.putdata(new_data)
img.save(output_file)
print(output_file) 
