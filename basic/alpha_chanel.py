from PIL import Image

white = 240
black = 60
# File to process
input_file = "logo_0056.png"
output_file = "logo_0056_transparent.png"

# Open the image and convert to RGBA (to support transparency)
img = Image.open(input_file).convert("RGBA")
datas = img.getdata()

new_data = []


# Loop through all pixels

for item in datas:
    r, g, b, a = item
    # If pixel is fully white, make it transparent
    if r <= black and g <= black and b <= black:
        new_data.append((255, 255, 255, 0))  # Transparent
    else:
        new_data.append(item)
'''
for item in datas:
    r, g, b, a = item
    # If pixel is fully white, make it transparent
    if r >= white and g >= white and b >= white:
        new_data.append((255, 255, 255, 0))  # Transparent
    else:
        new_data.append(item)
'''
# Update image data
img.putdata(new_data)

# Save the result
img.save(output_file)
print(f"Saved image with transparent background to {output_file}")
