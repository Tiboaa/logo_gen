import json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBold", "arialbd.ttf"))
pdfmetrics.registerFont(TTFont("MontserratBold", "Montserrat-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat", "Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans", "OpenSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("OpenSansBold", "OpenSans-Bold.ttf"))

page_width, page_height = 2560, 1440  
title_size = 64
text_size = 32
leading = text_size+8
start_x = 240
start_y = page_height-start_x
sub_tiltle_y = start_y-160

# BANNER ARÁNYOK
# 18 : 5
banner_wide_width = 1440
banner_wide_height = 400
# 15 : 11
banner_width = 720
banner_height = 528

logo_0 = "logo_0056_transparent.png"
logo_1 = "logo_0057_transparent.png"
logo_2 = ""
logo_3 = ""
logo_4 = ""
logo_on_merch = "logo_0056_transparent.png"
merch = "baseballcap_1.png"
banner = "banner.png"
banner_wide = "banner_wide.png"

logo_dict = {
    "number": 3, #number of images
    "placement": (12,23, 3,3, 5,5), #where to place them x,y
    "size": (512,512, 1024,1024, 512,512) #size of the images
    #IDK just use dict for logos it seems easier that way
}

def draw_squares(c, colors, square_size):
    steps = page_height / (len(colors) + 1)
    y = steps - square_size / 2

    for color in colors.keys():
        c.setFillColor(colors[color])
        c.setStrokeColor("#000000")
        c.rect(page_width/3 + 200, y, square_size, square_size, fill=1, stroke=1)

        r, g, b = hexToRgb(colors[color])
        cmyk = hexToCmyk(colors[color])

        text_x = page_width/3 + 200 + square_size + 60
        center_y = y + square_size/2

        c.setFont("ArialBold", text_size)
        c.setFillColor("#000000")
        c.drawString(text_x, center_y + square_size/7, color.upper())

        c.setFont("Arial", text_size)
        c.drawString(text_x, center_y - square_size/5, colors[color].upper())
        c.drawString(text_x + 200, center_y - square_size/5, f"CMYK: {cmyk[0]} / {cmyk[1]} / {cmyk[2]} / {cmyk[3]}     RGB: {r} / {g} / {b}")
                
        y += steps

def hexToRgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgbToCmyk(r: int, g: int, b: int):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 100

    r_prime, g_prime, b_prime = [x / 255.0 for x in (r, g, b)]

    k = 1 - max(r_prime, g_prime, b_prime)
    c = (1 - r_prime - k) / (1 - k) if k < 1 else 0
    m = (1 - g_prime - k) / (1 - k) if k < 1 else 0
    y = (1 - b_prime - k) / (1 - k) if k < 1 else 0

    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

def hexToCmyk(hex_color: str):
    r, g, b = hexToRgb(hex_color)
    return rgbToCmyk(r, g, b)

def drawBackground(c, page_width, page_height):
    c.setFillColor("#FFFFFF")
    c.rect(0, 0, page_width, page_height, stroke=0, fill=1)

    c.setFillColor("#1F1F1F")
    c.rect(0, 0, page_width / 3, page_height, stroke=0, fill=1)

def createPage(title, sub_title, text, c):
    drawBackground(c, page_width, page_height)
    c.setFillColor("#FFFFFF")
    c.setFont("ArialBold", title_size)
    c.drawString(start_x, start_y, title)
    c.setFontSize(text_size+2)
    c.drawString(start_x, sub_tiltle_y, sub_title)
    textobject =  c.beginText()
    textobject.setTextOrigin(start_x, sub_tiltle_y-leading-8)
    textobject.setFillColor("#FFFFFF")
    textobject.setFont("Arial", text_size)
    textobject.setLeading(leading) 
    for line in text:
        textobject.textLine("%s" % (line))
    c.drawText(textobject)
    logo_x = page_width/6 - 512/3
    logo_y = 0
    
    c.drawImage(logo_0, logo_x, logo_y, width=512/1.5, height=512/1.5, mask='auto')

def createPdf(filename):
    c = canvas.Canvas(filename, pagesize=(page_width, page_height))
    
    with open("basic/pdf_text.json", "r", encoding="utf-8") as f:
        pages = json.load(f)

    n = 0
    main_colors = pages[2]
    all_colors = pages[1]

    for page in pages[0]:
        createPage(page["title"], page["sub_title"], page["text"], c)

        if n == 0:
            c.drawImage(logo_0, page_width/1.5 - 512, page_height/2 - 512, width=1024, height=1024, mask='auto')

        if n == 1:
            c.drawImage(logo_1, page_width/3 - 100, page_height/2 - 512, width=1024, height=1024, mask='auto')
            c.drawImage(logo_0, page_width/1.5 - 100, page_height/2 - 512, width=1024, height=1024, mask='auto')

        if n == 2:
            c.drawImage(logo_1, page_width/3 - 100, page_height/2 - 512, width=1024, height=1024, mask='auto')
            c.drawImage(logo_0, page_width/1.5 - 100, page_height/2 - 512, width=1024, height=1024, mask='auto')
           
        if page["title"] == "LOGÓ SZÍNEI":
            hex_color = pages[1][page["sub_title"]]
            c.setFillColor(hex_color)
            c.rect(page_width / 3, 0, 2 * page_width / 3, page_height, stroke=0, fill=1)

        if page["sub_title"] == "LOGÓ SZÍNEI":       
            square_size = 140
            draw_squares(c, main_colors, square_size)

        if page["title"] == "SZÍNPALETTA":       
            square_size = 140    
            draw_squares(c, all_colors, square_size)

        if page["sub_title"] == "LOGÓ TIPOGRÁFIÁJA":
            font_name_on = "MONTSERRAT"
            abc = ("ABCDEFGHIJKLMNOPQRSTUVZXY",
                   "abcdefghijklmnopqrstuvzxy",
                   "0123456789") 
            c.setFont("MontserratBold", text_size)
            c.setFillColor("#000000")
            c.drawString(page_width/3 + 200, 2*page_height/3+80, "MONTSERRAT")
            textobject =  c.beginText()
            textobject.setFont("Montserrat", title_size)
            textobject.setTextOrigin(page_width/3 + 200, 2*page_height/3)
            textobject.setLeading(title_size) 
            for line in abc:
                textobject.textLine("%s" % (line))
            c.drawText(textobject)  

        if page["title"] == "TIPOGRÁFIA":
            font_name_on = "MONTSERRAT"
            font_name_off ="OPEN SANS"
            abc = ("ABCDEFGHIJKLMNOPQRSTUVZXY",
                   "abcdefghijklmnopqrstuvzxy",
                   "0123456789") 
            
            c.setFont("MontserratBold", text_size)
            c.setFillColor("#000000")
            c.drawString(page_width/3 + 200, 2*page_height/3+80, "MONTSERRAT")
            textobject =  c.beginText()
            textobject.setFont("Montserrat", title_size)
            textobject.setTextOrigin(page_width/3 + 200, 2*page_height/3)
            textobject.setLeading(title_size) 
            for line in abc:
                textobject.textLine("%s" % (line))
            c.drawText(textobject)

            c.setFont("OpenSansBold", text_size)
            c.setFillColor("#000000")
            c.drawString(page_width/3 + 200, page_height/3+80, "OPEN SANS")
            textobject =  c.beginText()
            textobject.setFont("OpenSans", title_size)
            textobject.setTextOrigin(page_width/3 + 200, page_height/3)
            textobject.setLeading(64) 
            for line in abc:
                textobject.textLine("%s" % (line))
            c.drawText(textobject)

        if page["title"] == "RUHÁZAT":
            c.setFillColor("#FCFCFC")
            c.rect(page_width / 3, 0, 2 * page_width / 3, page_height, stroke=0, fill=1)
            c.drawImage(merch, page_width/1.5 - 520, page_height/2 - 520, width=1040, height=1040)
            c.drawImage(logo_on_merch, page_width/1.5-256, page_height/2-180, mask='auto')

        if page["title"] == "ONLINE REKLÁM":
            width = 2*page_width/3 - banner_wide_width/2
            height = page_height/2 + banner_wide_height/4
            c.drawImage(banner_wide, width, height,
                        width=banner_wide_width, height=banner_wide_height)
            # --- Overlay logo (top-left on banner) ---
            logo_size = 200
            c.drawImage(logo_0, width+20, height+banner_wide_height-logo_size+20,
                        width=logo_size, height=logo_size, mask='auto')

            # --- White box for text (right side) ---
            box_w, box_h = 800, 180
            box_x = width + banner_wide_width - box_w
            box_y = height
            c.setFillColor("#FFFFFF")
            c.rect(box_x, box_y, box_w, box_h, fill=1, stroke=0)

            c.setFillColor("#000000")
            c.setFont("ArialBold", 40)
            c.drawString(box_x+30, box_y+box_h-60, "Lorem ipsum")

            c.setFont("Arial", 24)
            textobject = c.beginText()
            textobject.setTextOrigin(box_x+30, box_y+box_h-100)
            textobject.setLeading(28)
            textobject.textLine("Pellentesque habitant morbi tristique senectus et netus et malesuada") 
            textobject.textLine("fames ac turpis egestas. Vivamus cursus nibh fringilla arcu lobortis")
            c.drawText(textobject)

            width = 2*page_width/3 - banner_width
            height = page_height/2 - banner_height
            c.drawImage(banner, width, height, 
                        width=banner_width, height=banner_height)
            
            logo_size2 = 120
            c.drawImage(logo_0, width + 20, height+banner_height-logo_size2,
                width=logo_size2, height=logo_size2, mask='auto')

            box_w2, box_h2 = 400, 160
            box_x2 = width + banner_width - box_w2
            box_y2 = height
            c.setFillColor("#FFFFFF")
            c.rect(box_x2, box_y2, box_w2, box_h2, fill=1, stroke=0)

            c.setFillColor("#000000")
            c.setFont("ArialBold", 32)
            c.drawString(box_x2+20, box_y2+box_h2-50, "Lorem ipsum")

            c.setFont("Arial", 20)
            textobject = c.beginText()
            textobject.setTextOrigin(box_x2+20, box_y2+box_h2-80)
            textobject.setLeading(24)
            textobject.textLine("Pellentesque habitant morbi tristique")
            textobject.textLine("senectus et netus et malesuada.")
            c.drawText(textobject)

        n += 1
        
        c.showPage()
    c.save()
    
createPdf("example.pdf")
