import replicate

input = {
    "prompt": "black forest gateau cake spelling out the words \"FLUX SCHNELL\", tasty, food photography, dynamic shot"
}

output = replicate.run(
    "black-forest-labs/flux-schnell",
    input=input
)

# To access the file URLs:
print(output[0].url())
#=> "https://replicate.delivery/.../output_0.webp"

# To write the files to disk:
for index, item in enumerate(output):
    with open(f"output_{index}.webp", "wb") as file:
        file.write(item.read())
#=> output_0.webp written to disk