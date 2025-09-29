# MIGHT BE BUGGY

import os
import sys
import json
import requests

def main(the_colors, key, savefile):
    colors_arg = the_colors  # "main" or "secondary"
    api_key = key

    where = lambda colors: 2 if colors == "main" else 1 if colors == "secondary" else None

    savefile_path = f"arculatok/json/{savefile}"

    os.makedirs(os.path.dirname(savefile_path), exist_ok=True)
    if not os.path.exists(savefile_path):
        with open(savefile_path, "w", encoding="utf-8") as f:
            json.dump([[], {}, {}], f, ensure_ascii=False, indent=2)

    with open(savefile_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open("basic/pdf_text_original.json", "r", encoding="utf-8") as f:
        original_data = json.load(f)

    color_dict = data[where(colors_arg)]

    ACCESS_TOKEN = api_key
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are a professional brand text generator. DO NOT do anything else.\n"
        "Create a JSON array of Hungarian text lines describing a color.\n\n"
        "Requirements:\n"
        "• Around 8 to 14 lines per color.\n"
        "• A line should be short no more than 6 words or 40 letters\n"
        "• The sentences can and should be broken up into the next line when neccesary for length\n"
        "• The text should be a whole description, well worded and it should generaly make sense as a whole.\n"
        "• It should be like this example format:\n"
        "\n"
        "  \"A sárga az optimizmus, az\",\n"
        "  \"életenergia és a kreativitás\",\n"
        "  \"színe. Ez az árnyalat a napfény\",\n"
        "  \"melegségét és a pozitív\",\n"
        "  \"hangulatot idézi, miközben\",\n"
        "  \"figyelemfelkeltő és inspiráló\",\n"
        "  \"hatást kelt. A sárga dinamizmust\",\n"
        "  \"ad a megjelenésnek, és kiemelit\",\n"
        "  \"a márka innovatív, barátságos\",\n"
        "  \"oldalát.\"\n"

        "• Describe emotional, symbolic, visual meaning and brand importance.\n"
        "• The description shouldn't reffer to any specific area that the color can be used talk about it generally (what kind of vibe it has).\n"
        "• Clear, positive, professional tone.\n"
        "• The sentences and the whole text should make sense in hungarian, avoid structural and grammatical errors.\n"
        "• Output ONLY valid JSON array for the color."
    )

    final_data = original_data[0][:3]

    for i in data[where(colors_arg)].keys():

        user_prompt = (
            f'Generate ONLY a JSON array of Hungarian text lines for this color: "{i}". '
            'Do not add any explanations, reasoning, or extra text. '
            'Each array should have 8-14 lines. '
            'Each line short (<=6 words, <=40 letters).'
        )

        payload = {
            "model": "openai/gpt-oss-120b:cerebras",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 2000
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Error from API: {response.status_code}")
            continue 

        try:
            result = response.json()
            #print(f"RESULT: {result}")
            message = result["choices"][0]["message"]
            #print(f"MESSAGE: {message}")
            color_lines = message.get("content", message.get("reasoning", ""))
            #print(f"COLOR LINES :{color_lines}")
            color_lines = json.loads(color_lines)
            #print(f"COLOR LINES :{color_lines}")
            final_data.append({
                "title": "LOGÓ SZÍNEI",
                "sub_title": i,
                "text": color_lines
            })
            #print(f"FINAL DATA :{final_data}")

        except Exception as e:
            print(f"Failed to parse API response for {i}: {e}")

    final_data.extend(original_data[0][3:])
    data[0] = final_data 
    # ✅ Save back to pdf_text.json
    with open(savefile_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
'''
  {
    "title": "LOGÓ SZÍNEI",
    "sub_title": "VILÁGOSKÉK",
    "text": [
      "A világoskék a nyitottság, a",
      "tisztaság és a megbízhatóság",
      "színe. Ez az árnyalat a szabadság",
      "és a frissesség érzetét kelti,",
      "miközben modern és technológiai",
      "szemléletet tükröz. A világoskék",
      "segít kiemelni a márka innovatív",
      "és barátságos karakterét."
    ]
  },
'''