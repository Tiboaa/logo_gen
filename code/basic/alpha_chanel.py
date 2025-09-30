from PIL import Image
import os

white = 240
black = 60
def main(input):

    input_file = input
    name = os.path.basename(input_file)
    output_file = f"arculatok/logos/{name}_transparent.png"

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
