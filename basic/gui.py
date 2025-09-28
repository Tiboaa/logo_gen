from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess
import sys
import json
import unicodedata

current_logo_path = ""
logo_0 = ""
logos = []
logo_on_merch = ""

root = Tk()
root.title("Logo Generator")
root.geometry("620x440")
root.minsize(300, 200)

json_path = "basic/logo_data.json"

api_key_var = StringVar()

# --- global variables for inputs ---
'''l_subject = None
l_shape = None
subject_style = None
shape_style = None
subject_clr = None
shape_clr = None
xtra_inf = None
change_prompt = None
inputs_display = None'''

#subject_clr_0, subject_clr_1, letter, shape, shape_ular, shape_2, shape_2_ular, text_clr_0, text_clr_1, text_0, text_1, font



canvas = Canvas(root)
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

current_frame = Frame(canvas)
canvas.create_window((0, 0), window=current_frame, anchor="nw")


# ---------------- OLDALAK ----------------

def create_from_preset(preset):
    clear_widgets()
    canvas.yview_moveto(0)
    print("hi mom")
    global subject_clr_0, subject_clr_1, letter, shape, shape_ular, shape_2, shape_2_ular, text_clr_0, text_clr_1, text_0, text_1, font
 
    grid_index = 0

    if preset in ["a1", "a3", "a5", "b1", "c1", "d1"]:
        Label(current_frame, text="Letter").grid(row=grid_index)
        letter = Entry(current_frame)
        letter.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a4","a5","b1","b2","b3","b5","c1","c2","c4","d1","d2","d4","d5"]:
        Label(current_frame, text="Shape 1").grid(row=grid_index)
        shape = Entry(current_frame)
        shape.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a3","a5","b1","b2","b3","d1","d2"]:
        Label(current_frame, text="Shape (adjective) 1").grid(row=grid_index)
        shape_ular = Entry(current_frame)
        shape_ular.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["b1","b2","b3","b5","c1","c2"]:
        Label(current_frame, text="Shape 2").grid(row=grid_index)
        shape_2 = Entry(current_frame)
        shape_2.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["b1","b3"]:
        Label(current_frame, text="Shape (adjective) 2").grid(row=grid_index)
        shape_2_ular = Entry(current_frame)
        shape_2_ular.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a4","a5","b1","b2","b3","b5","c1","c2","c3","c4","c5","d1","d2","d3","d4","d5"]:
        Label(current_frame, text="Color 1").grid(row=grid_index)
        subject_clr_0 = Entry(current_frame)
        subject_clr_0.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a4","a5","b1","b2","b3","b5","c1","c4","c5","d3","d4"]:
        Label(current_frame, text="Color 2").grid(row=grid_index)
        subject_clr_1 = Entry(current_frame)
        subject_clr_1.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a4","a5","b1","b2","b3","b5","c1","c2","c3","c4","c5","d1","d2","d3","d4","d5"]:
        Label(current_frame, text="Company name").grid(row=grid_index)
        text_0 = Entry(current_frame)
        text_0.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a5","b1","b3","b5","c1","c3","c4","c5","d2"]:
        Label(current_frame, text="Slogan").grid(row=grid_index)
        text_1 = Entry(current_frame) 
        text_1.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a4","a5","b1","b2","b3","b4","b5","c1","c2","c3","c4","c5","d1","d2","d5"]:
        Label(current_frame, text="Text color 1").grid(row=grid_index)        
        text_clr_0 = Entry(current_frame)    
        text_clr_0.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a5","b1","b4","b5","c1","d2"]:
        Label(current_frame, text="Text color 2").grid(row=grid_index)
        text_clr_1 = Entry(current_frame)
        text_clr_1.grid(row=grid_index, column=1)
        grid_index += 1

    if preset in ["a1","a2","a3","a4","a5","b1","b2","b3","b4","b5","c1","c2","c3","c4","c5","d1","d2","d3","d4","d5"]:
        Label(current_frame, text="Font").grid(row=grid_index)
        font = Entry(current_frame)
        font.grid(row=grid_index, column=1)
        grid_index += 1

    Button(current_frame, text="Clear all", width=20, command=lambda: clear_all(preset)).grid(row=0, column=2, columnspan=2)
    Button(current_frame, text="Generate Logo", width=20, command=lambda: run_preset(1, grid_index, preset)).grid(row=0, column=4, columnspan=2)
    Button(current_frame, text="Generate Logo x2", width=20, command=lambda: run_preset(2, grid_index, preset)).grid(row=2, column=4, columnspan=2)
    Button(current_frame, text="Generate Logo x4", width=20, command=lambda: run_preset(4, grid_index, preset)).grid(row=4, column=4, columnspan=2)

    Button(current_frame, text="Stop the program", width=25, command=exit_app).grid(row=grid_index, column=0, columnspan=2)

    for widget in current_frame.winfo_children():
        if not isinstance(widget, Menu):
            widget.grid_configure(padx=10, pady=5)    

def create_new():
    clear_widgets()
    canvas.yview_moveto(0)
    global l_subject, l_shape, subject_style, shape_style, subject_clr, shape_clr, xtra_inf, change_prompt, inputs_display

    l_subject = Entry(current_frame)
    l_shape = Entry(current_frame)
    subject_style = Entry(current_frame)
    shape_style = Entry(current_frame)
    subject_clr = Entry(current_frame)
    shape_clr = Entry(current_frame)
    xtra_inf = Entry(current_frame)
    change_prompt = Entry(current_frame)

    Label(current_frame, text="Logo subject").grid(row=0)
    Label(current_frame, text="Logo shape").grid(row=1)

    Button(current_frame, text="Clear all", width=20, command=lambda: clear_all("create_new")).grid(row=0, column=1, columnspan=2)
    

    Label(current_frame, text="Subject style").grid(row=2)
    Label(current_frame, text="Shape style").grid(row=3)
    Label(current_frame, text="Subject color").grid(row=4)
    Label(current_frame, text="Shape color").grid(row=5)
    Label(current_frame, text="Extra info").grid(row=6)

    l_subject.grid(row=0, column=1)
    l_shape.grid(row=1, column=1)
    subject_style.grid(row=2, column=1)
    shape_style.grid(row=3, column=1)
    subject_clr.grid(row=4, column=1)
    shape_clr.grid(row=5, column=1)
    xtra_inf.grid(row=6, column=1)

    Button(current_frame, text="Generate prompt", width=25, command=generate_prompt).grid(row=7, column=0, columnspan=2)
    Label(current_frame, text="What to change").grid(row=8)
    change_prompt.grid(row=8, column=1)
    Button(current_frame, text="Regenerate prompt", width=25, command=regenerate_prompt).grid(row=9, column=0, columnspan=2)
    Label(current_frame, text="Current prompt:").grid(row=9, column=1, columnspan=2)
    Button(current_frame, text="Generate image based\non current prompt", width=25, command=generate_img).grid(row=10, column=0, columnspan=2)
    Button(current_frame, text="Stop the program", width=25, command=exit_app).grid(row=11, column=0, columnspan=2)

    inputs_display = Text(current_frame, height=5, width=40, wrap=WORD)
    inputs_display.grid(row=10, column=2, rowspan=5, padx=10, pady=5)

    for widget in current_frame.winfo_children():
        if not isinstance(widget, Menu):
            widget.grid_configure(padx=10, pady=5)

    load_logo_data()
    load_current_inputs()

def create_json():
    clear_widgets()
    canvas.yview_moveto(0)
    global pdf_main_color_entry, pdf_main_hex_entry, pdf_secondary_color_entry, pdf_secondary_hex_entry, pdf_display_main, pdf_display_secondary

    ensure_pdf_json()

    # MAIN COLORS
    Label(current_frame, text="Main Colors").grid(row=0, column=0, columnspan=2)
    Label(current_frame, text="Color Name").grid(row=1, column=0, sticky=W)
    pdf_main_color_entry = Entry(current_frame)
    pdf_main_color_entry.grid(row=1, column=1)

    Label(current_frame, text="HEX Color").grid(row=2, column=0, sticky=W)
    pdf_main_hex_entry = Entry(current_frame)
    pdf_main_hex_entry.grid(row=2, column=1)

    Button(current_frame, text="Append to PDF_TEXT JSON", width=25, command=lambda: append_pdf_json(2)).grid(row=3, column=0, columnspan=2, pady=5)
    Button(current_frame, text="Delete given color (via key)", width=25, command=lambda: delete_from_pdf(False, 2, pdf_main_color_entry)).grid(row=4, column=0, columnspan=2, pady=5)
    Button(current_frame, text="Delete main colors", width=25, command=lambda: delete_from_pdf(False, 2, "")).grid(row=5, column=0, columnspan=2, pady=5)
    
    Label(current_frame, text="Main colors in pdf_text.json").grid(row=0, column=2, padx=10, sticky=W)
    pdf_display_main = Text(current_frame, height=10, width=40)
    pdf_display_main.grid(row=1, column=2, rowspan=5, padx=10, pady=5)

    # SECONDARY COLORS
    Label(current_frame, text="Secondary Colors").grid(row=6, column=0, columnspan=2)
    Label(current_frame, text="Color Name").grid(row=7, column=0, sticky=W)
    pdf_secondary_color_entry = Entry(current_frame)
    pdf_secondary_color_entry.grid(row=7, column=1)

    Label(current_frame, text="HEX Color").grid(row=8, column=0, sticky=W)
    pdf_secondary_hex_entry = Entry(current_frame)
    pdf_secondary_hex_entry.grid(row=8, column=1)    
    
    Button(current_frame, text="Append to PDF_TEXT JSON", width=25, command=lambda: append_pdf_json(1)).grid(row=9, column=0, columnspan=2, pady=5)
    Button(current_frame, text="Delete given color (via key)", width=25, command=lambda: delete_from_pdf(False, 1, pdf_secondary_color_entry)).grid(row=10, column=0, columnspan=2, pady=5)
    Button(current_frame, text="Delete secondary colors", width=25, command=lambda: delete_from_pdf(False, 1, "")).grid(row=11, column=0, columnspan=2, pady=5)
    
    Label(current_frame, text="Secondary colors in pdf_text.json").grid(row=6, column=2, padx=10, sticky=W)
    pdf_display_secondary = Text(current_frame, height=10, width=40)
    pdf_display_secondary.grid(row=7, column=2, rowspan=5, padx=10, pady=5)

    # PAGES
    Button(current_frame, text="Create pages with Main colors", width=25, command=lambda: create_color_pages("main")).grid(row=12, column=1, columnspan=2, pady=5)
    Button(current_frame, text="Create pages with Secondary colors", width=30, command=lambda: create_color_pages("secondary")).grid(row=13, column=1, columnspan=2, pady=5)

    # MAKE PDF
    

    # MISCELLANEOUS
    Button(current_frame, text="Delete everything from the JSON", width=25, command=lambda: delete_from_pdf(True, 0, "")).grid(row=16, column=1, columnspan=2, pady=5) 
    Button(current_frame, text="Stop the program", width=25, command=exit_app).grid(row=17, column=1, columnspan=2, pady=5)

    load_pdf_display()

def arculat_from_json():
    canvas.yview_moveto(0)
    clear_widgets()
    global logo_0, logo_on_merch, logos

    logos = []
    folder_path = "arculatok/json"
    try:
        json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    except FileNotFoundError:
        json_files = []

    grid_index = 1
    Label(current_frame, text="Choose a json to continue").grid(row=0, column=0, padx=220, pady=4)
    for i, filename in enumerate(json_files):
        Button(current_frame, text=filename.replace(".json", ""), width=25, command=lambda f=filename: arculat_chosen(f) ).grid(row=1+i, column=0, padx=220, pady=1)
        grid_index += 1
    Label(current_frame).grid(row=grid_index, column=0)
    Button(current_frame, text="Stop the program", width=25, command=exit_app).grid(row=grid_index+1, column=0, columnspan=2)

    def arculat_chosen(file):
        clear_widgets()
        canvas.yview_moveto(0)

        add_image_selector()

        Label(current_frame, text="Edit "+file+":").grid(row=0, column=0, padx=4, pady=4)

        with open("arculatok/json/"+file, "r", encoding="utf-8") as f:
            data = json.load(f)

        text_widgets = []

        for i in range(len(data[0])):
            Label(current_frame, text=f"Page {i+1}").grid(row=1+10*i, column=0, padx=4, pady=4)
            Label(current_frame, text=f"{data[0][i]['sub_title']}").grid(row=2+10*i, column=0, padx=4, pady=4)
            json_text = Text(current_frame, height=5, width=40, wrap=WORD)
            json_text.grid(row=3+10*i, column=0, rowspan=5, padx=10, pady=5)
            text_lines = data[0][i]["text"]

            for line in text_lines:
                json_text.insert("end", line + "\n")
        
            text_widgets.append(json_text)


        def save_changes():
                for i, text_widget in enumerate(text_widgets):
                    new_text = text_widget.get("1.0", "end").strip().split("\n")
                    data[0][i]["text"] = new_text

                with open("arculatok/json/" + file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                print("✅ Changes saved to", file)

        def go_back_and_save():
            save_changes()
            arculat_from_json()

        def go_back_without_save():
            arculat_from_json()

        def create_arculat():
            save_changes()
            print(f"main: {logo_0}")
            print(f"merch: {logo_on_merch}")
            print(f"secondary: {logos}")
            # THIS SHOULD CALL basic\arculat.py
            

        Button(current_frame, text="Save and generate arculat", width=25, command=create_arculat).grid(row=1000, column=0)
        Button(current_frame, text="Go back (and save)", width=25, command=go_back_and_save).grid(row=1001, column=0)
        Button(current_frame, text="Go back (without save)", width=25, command=go_back_without_save).grid(row=1002, column=0)
        Button(current_frame, text="Stop the program", width=25, command=exit_app).grid(row=1003, column=0)

    def add_image_selector():
        frame = Frame(current_frame)
        frame.grid(row=0, column=1, rowspan=1000, sticky="n")
        folder = "output_pics"
        png_files = [f for f in os.listdir(folder) if f.endswith(".png")]

        search_var = StringVar()
        

        def choose_image(where):
            global logo_0, logos, logo_on_merch
            if not current_logo_path:
                return
            
            logo_name = os.path.basename(current_logo_path)
            if where == "main":
                logo_0 = logo_name
                update_main_listbox()
                print(where)
                print(logo_0)
                return
            if where == "merch":
                logo_on_merch = logo_name
                update_merch_listbox()
                print(where)
                print(logo_on_merch)
                return
            if where == "secondary":
                print(where)
                if logo_name not in logos:
                    if len(logos) >= 4:
                        messagebox.showwarning("Limit reached", "Cannot add more than 4 logos. Please delete one first.")
                        print("cannot add more than 4 delete one")
                    else:
                        logos.append(logo_name)
                print(logos)
                update_secondary_listbox()
                return   


        def delete_selected_secondary_logo():
            global logos
            selection = secondary_listbox.curselection()
            if not selection:
                return 
            for index in reversed(selection):
                logo = secondary_listbox.get(index)
                if logo in logos:
                    logos.remove(logo)
            update_secondary_listbox()

        def update_list(*args):
            search_term = search_var.get().lower()
            listbox.delete(0, END)
            for f in png_files:
                if search_term in f.lower():
                    listbox.insert(END, f)
        def update_main_listbox():
            main_listbox.config(state=NORMAL)
            main_listbox.delete(0, END)
            if logo_0:
                main_listbox.insert(END, logo_0)
            main_listbox.config(state=DISABLED)

        def update_secondary_listbox():
            secondary_listbox.config(state=NORMAL)
            secondary_listbox.delete(0, END)
            for logo in logos:
                secondary_listbox.insert(END, logo)
            #secondary_listbox.config(state=DISABLED)

        def update_merch_listbox():
            on_merch_listbox.config(state=NORMAL)
            on_merch_listbox.delete(0, END)
            if logo_on_merch:
                on_merch_listbox.insert(END, logo_on_merch)
            on_merch_listbox.config(state=DISABLED)


        def show_image(event):
            selection = listbox.curselection()
            if not selection:
                return
            filename = listbox.get(selection[0])
            path = os.path.join(folder, filename)
            global current_logo_path
            current_logo_path = path
            img = Image.open(path)
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)

            if hasattr(frame, "current_img_label"):
                frame.current_img_label.config(image=img_tk)
                frame.current_img_label.image = img_tk
            else:
                frame.current_img_label = Label(frame, image=img_tk)
                frame.current_img_label.image = img_tk
                frame.current_img_label.grid(row=2, column=1, columnspan=5, pady=10)

        Entry(frame, textvariable=search_var).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        search_var.trace_add("write", update_list)

        listbox = Listbox(frame, width=40, height=10)
        listbox.grid(row=1, column=1, columnspan=5, padx=5, pady=5)
        listbox.bind("<<ListboxSelect>>", show_image)

        Button(frame, width=25, text="Choose image as main logo", command=lambda : choose_image("main")).grid(row=3, column=1)
        Button(frame, width=25, text="Add image as logo", command=lambda : choose_image("secondary")).grid(row=4, column=1)
        Button(frame, width=25, text="Choose as logo on merch", command=lambda : choose_image("merch")).grid(row=5, column=1)

        Label(frame, text="Main logo:").grid(row=6, column=1, sticky='w')
        main_listbox = Listbox(frame, width=40, height=2)
        main_listbox.grid(row=7, column=1, pady=2)
        Label(frame, text="Logo variants:").grid(row=8, column=1, sticky='w')
        secondary_listbox = Listbox(frame, width=40, height=4)
        secondary_listbox.grid(row=9, column=1, pady=2)
        Button(frame, width=25, text="Delete selected logo", command=delete_selected_secondary_logo).grid(row=10, column=1, padx=5, sticky='w')

        Label(frame, text="Logo on merch:").grid(row=11, column=1, sticky='w')
        on_merch_listbox = Listbox(frame, width=40, height=2)
        on_merch_listbox.grid(row=12, column=1, pady=2)

        update_list()
        update_main_listbox()
        update_secondary_listbox()
        update_merch_listbox()
       
def open_api_key_window():
    win = Toplevel(root)
    win.title("Enter API Key")
    win.geometry("400x180")
    win.transient(root)
    win.grab_set()

    Label(win, text="Hugging Face API Key:").pack(pady=(20, 5))

    entry = Entry(win, textvariable=api_key_var, width=40, show="*")
    entry.pack(pady=(0, 5))
    entry.focus()

    warning_label = Label(win, text="", fg="red")
    warning_label.pack()
    key = api_key_var.get().strip()

    def save_and_close():
        key = api_key_var.get().strip()
        if not (key.startswith("hf_") and len(key) == 37):
            warning_label.config(text="Invalid API Key (must start with 'hf_' and be 37 chars long)")
            return
        api_key_required(key)
        win.destroy()

    api_key_required(key)
    Button(win, text="Save", command=save_and_close).pack(pady=10)
    
# ---------------- MENU ----------------

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Presets", menu=filemenu)
filemenu.add_command(label="New", command=create_new) 
presetsmenu = Menu(filemenu, tearoff=0)
filemenu.add_cascade(label="Open...", menu=presetsmenu)
presetsmenu.add_command(label="A 1", command=lambda: create_from_preset("a1"))
presetsmenu.add_command(label="A 2", command=lambda: create_from_preset("a2"))
presetsmenu.add_command(label="A 3", command=lambda: create_from_preset("a3"))
presetsmenu.add_command(label="A 4", command=lambda: create_from_preset("a4"))
presetsmenu.add_command(label="A 5", command=lambda: create_from_preset("a5"))
presetsmenu.add_command(label="B 1", command=lambda: create_from_preset("b1"))
presetsmenu.add_command(label="B 2", command=lambda: create_from_preset("b2"))
presetsmenu.add_command(label="B 3", command=lambda: create_from_preset("b3"))
presetsmenu.add_command(label="B 4", command=lambda: create_from_preset("b4"))
presetsmenu.add_command(label="B 5", command=lambda: create_from_preset("b5"))
presetsmenu.add_command(label="C 1", command=lambda: create_from_preset("c1"))
presetsmenu.add_command(label="C 2", command=lambda: create_from_preset("c2"))
presetsmenu.add_command(label="C 3", command=lambda: create_from_preset("c3"))
presetsmenu.add_command(label="C 4", command=lambda: create_from_preset("c4"))
presetsmenu.add_command(label="C 5", command=lambda: create_from_preset("c5"))
presetsmenu.add_command(label="D 1", command=lambda: create_from_preset("d1"))
presetsmenu.add_command(label="D 2", command=lambda: create_from_preset("d2"))
presetsmenu.add_command(label="D 3", command=lambda: create_from_preset("d3"))
presetsmenu.add_command(label="D 4", command=lambda: create_from_preset("d4"))
presetsmenu.add_command(label="D 5", command=lambda: create_from_preset("d5"))

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About")

arculat = Menu(menu, tearoff=0)
menu.add_cascade(label="Arculat", menu=arculat)  
arculat.add_command(label="Create JSON", command=create_json)
arculat.add_command(label="Arculat from PDF", command=arculat_from_json)  
menu.add_command(label="API Key", command=open_api_key_window)



# ---------------- KISEBB FÜGGVÉNYEK ----------------

def create_color_pages(colors):
    api_key = api_key_var.get().strip()
    if not api_key.startswith("hf_") or len(api_key) != 37:
        messagebox.showerror("Invalid API Key", "Please enter a valid Hugging Face API key.")
        return
    
    if colors in ("main", "secondary"):
        try:
            subprocess.run(
                ["python", "basic/create_page_text.py", colors, api_key],
                check=True
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Execution Error", f"Failed to run create_page_text.py:\n{e}")
        return
    
    print("Error: This shouldn't happen, there might be a typo.")
    return

def api_key_required(key):
    if not (key.startswith("hf_") and len(key) == 37):
        info_label = Label(root, text="API Key Required", fg="red", bg="lightgray")
        info_label.place(x=0, y=0, anchor="nw")
    else:
        for widget in root.place_slaves():
            if isinstance(widget, Label) and widget.cget("text") == "API Key Required":
                widget.destroy()

def delete_from_pdf(del_json, del_from_list, del_dict_from):
    json_file = "basic/pdf_text.json"
    
    if del_json:
        if os.path.exists(json_file):
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the entire JSON?")
            if confirm:
                os.remove(json_file)
                messagebox.showinfo("Deleted", "✅ JSON file deleted.")
        else:
            messagebox.showwarning("Not found", "JSON file does not exist.")
        load_pdf_display()
        return

    if not os.path.exists(json_file):
        messagebox.showwarning("Not found", "JSON file does not exist.")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Could not read JSON file.")
            return

    if del_dict_from and del_from_list is not None:
        try:
            key_to_delete = del_dict_from.get().strip().upper()
            if key_to_delete in data[del_from_list]:
                confirm = messagebox.askyesno(
                    "Confirm Key Deletion",
                    f"Are you sure you want to delete the key '{key_to_delete}' from entry {del_from_list}?"
                )
                if confirm:
                    del data[del_from_list][key_to_delete]
                    messagebox.showinfo("Deleted", f"✅ Key '{key_to_delete}' deleted from entry {del_from_list}.")
            else:
                messagebox.showwarning("Not found", f"Key '{key_to_delete}' not found in entry {del_from_list}.")
        except IndexError:
            messagebox.showerror("Error", "Invalid index.")

    elif del_from_list is not None:
        try:
            confirm = messagebox.askyesno(
                "Confirm Entry Deletion",
                f"Are you sure you want to clear all colors in entry {del_from_list}?"
            )
            if confirm:
                data[del_from_list].clear()
                messagebox.showinfo("Deleted", f"✅ All colors in entry {del_from_list} cleared.")
        except IndexError:
            messagebox.showerror("Error", "Invalid index.")
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    load_pdf_display()
       
def append_pdf_json(where):
    if where == 1:
        color_entry = pdf_secondary_color_entry
        hex_entry = pdf_secondary_hex_entry
    elif where == 2:
        color_entry = pdf_main_color_entry
        hex_entry = pdf_main_hex_entry
    else:
        messagebox.showerror("Error", f"Invalid target: {where}")
        return

    color = color_entry.get().strip().upper()
    hex_code = hex_entry.get().strip().upper()

    if not color or not hex_code:
        messagebox.showwarning("Missing data", "Please fill in both fields!")
        return

    confirm = messagebox.askyesno("Confirm", f"Add {color} : {hex_code}?")
    if not confirm:
        return

    color = unicodedata.normalize('NFC', color)
    hex_code = unicodedata.normalize('NFC', hex_code)
    json_file = "basic/pdf_text.json"
    data = ensure_pdf_json()

    if where == 1:
        target_dict = data[1]  # secondary colors
    else:
        target_dict = data[2]  # main colors

    if color in target_dict:
        messagebox.showerror("Duplicate Key", f"The key '{color}' already exists!")
        return

    target_dict[color] = hex_code

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    if where == 2:
        pdf_display_main.config(state=NORMAL)
        pdf_display_main.delete("1.0", END)
        pdf_display_main.insert(END, json.dumps(target_dict, indent=4, ensure_ascii=False))
        pdf_display_main.config(state=DISABLED)
    if where == 1:
        pdf_display_secondary.config(state=NORMAL)
        pdf_display_secondary.delete("1.0", END)
        pdf_display_secondary.insert(END, json.dumps(target_dict, indent=4, ensure_ascii=False))
        pdf_display_secondary.config(state=DISABLED)

def load_pdf_display():
    json_file = "basic/pdf_text.json"
    data = ensure_pdf_json()

    # Main colors
    pdf_display_main.config(state=NORMAL)
    pdf_display_main.delete("1.0", END)
    pdf_display_main.insert(END, json.dumps(data[2], indent=4, ensure_ascii=False))
    pdf_display_main.config(state=DISABLED)

    # Secondary colors
    pdf_display_secondary.config(state=NORMAL)
    pdf_display_secondary.delete("1.0", END)
    pdf_display_secondary.insert(END, json.dumps(data[1], indent=4, ensure_ascii=False))
    pdf_display_secondary.config(state=DISABLED)

def ensure_pdf_json():
    json_file = "basic/pdf_text.json"
    os.makedirs("basic", exist_ok=True)
    default_structure = [[], {}, {}]

    if os.path.exists(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                data = default_structure
            else:

                while len(data) < 3:
                    if len(data) == 0:
                        data.append([])
                    else:
                        data.append({})

                if not isinstance(data[0], list):
                    data[0] = []

                for i in [1, 2]:
                    if not isinstance(data[i], dict):
                        data[i] = {}
        except (json.JSONDecodeError, ValueError):
            data = default_structure
    else:
        data = default_structure

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data

def run_preset(num, grid_index, preset):
    api_key = api_key_var.get().strip()
    if not api_key.startswith("hf_") or len(api_key) != 37:
        messagebox.showerror("Invalid API Key", "Please enter a valid Hugging Face API key.")
        return


    variables = {
        "subject_clr_0": subject_clr_0.get() if subject_clr_0 else "",
        "subject_clr_1": subject_clr_1.get() if subject_clr_1 else "",
        "letter": letter.get() if letter else "",
        "shape": shape.get() if shape else "",
        "shape_ular": shape_ular.get() if shape_ular else "",
        "shape_2": shape_2.get() if shape_2 else "",
        "shape_2_ular": shape_2_ular.get() if shape_2_ular else "",
        "text_clr_0": text_clr_0.get() if text_clr_0 else "",
        "text_clr_1": text_clr_1.get() if text_clr_1 else "",
        "text_0": text_0.get() if text_0 else "",
        "text_1": text_1.get() if text_1 else "",
        "font": font.get() if font else ""
    }

    filled_vars = sum(1 for v in variables.values() if v.strip() != "")

    if filled_vars < grid_index:
        messagebox.showwarning("Missing data", "Please fill in all fields before running!")
        return

    if filled_vars > grid_index:
        messagebox.showwarning("ERROR: Too many fields are filled?")
        return
    
    confirm = messagebox.askyesno("Creating logo...", "Are you sure about creating the logo?")
    if not confirm:
        return

    for i in range(1): #range(num) <= CHANGE LATER TO COMMENT !!!
        try:
            script_path = ("basic/presets.py")
            result = subprocess.run(
                [sys.executable, script_path, json.dumps(variables), preset, api_key],
                capture_output=True,
                text=True,
                check=True
            )
            print("[DEBUG] Script stdout:\n", result.stdout)
            print("[DEBUG] Script stderr:\n", result.stderr)
            messagebox.showinfo("Image Generated", f"✅ Generated {num} logos using preset {preset}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Subprocess failed: {e}")
            print("[ERROR] stdout:\n", e.stdout)
            print("[ERROR] stderr:\n", e.stderr)
            messagebox.showerror("Error", "❌ Could not run main.py\nCheck console for details.")

def load_current_inputs():
    global inputs_display
    if not inputs_display:
        return
    input_file = "prompts/input.json"
    if not os.path.exists(input_file):
        print("[DEBUG] No prompts/input.json found.")
        inputs_display.config(state=NORMAL)
        inputs_display.delete("1.0", END)
        inputs_display.insert(END, "[No inputs generated yet]")
        inputs_display.config(state=DISABLED)
        return
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        current_inputs = data.get("inputs", "[No 'inputs' key found]")
    except Exception as e:
        print(f"[ERROR] Could not read {input_file}: {e}")
        current_inputs = f"[Error reading input.json: {e}]"
    inputs_display.config(state=NORMAL)
    inputs_display.delete("1.0", END)
    inputs_display.insert(END, current_inputs)
    inputs_display.config(state=DISABLED)

def load_logo_data():
    if not os.path.exists(json_path):
        print("[DEBUG] No existing logo_data.json found.")
        return
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            logo_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load JSON: {e}")
        return
    if l_subject:
        l_subject.delete(0, END)
        l_subject.insert(0, logo_data.get("subject", ""))
    if l_shape:
        l_shape.delete(0, END)
        l_shape.insert(0, logo_data.get("logo_shape", ""))
    if subject_style:
        subject_style.delete(0, END)
        subject_style.insert(0, logo_data.get("subject_style", ""))
    if shape_style:
        shape_style.delete(0, END)
        shape_style.insert(0, logo_data.get("shape_style", ""))
    if subject_clr:
        subject_clr.delete(0, END)
        subject_clr.insert(0, logo_data.get("color_of_subject", ""))
    if shape_clr:
        shape_clr.delete(0, END)
        shape_clr.insert(0, logo_data.get("color_of_shape", ""))
    if xtra_inf:
        xtra_inf.delete(0, END)
        xtra_inf.insert(0, logo_data.get("extra_instructions", ""))

def generate_prompt():
    api_key = api_key_var.get().strip()
    if not api_key.startswith("hf_") or len(api_key) != 37:
        messagebox.showerror("Invalid API Key", "Please enter a valid Hugging Face API key.")
        return

    subject = l_subject.get().strip()
    logo_shape = l_shape.get().strip()
    subj_style = subject_style.get().strip()
    sh_style = shape_style.get().strip()
    subj_clr = subject_clr.get().strip()
    sh_clr = shape_clr.get().strip()
    extra = xtra_inf.get().strip()

    if not all([subject, logo_shape, subj_style, sh_style, subj_clr, sh_clr, extra]):
        messagebox.showwarning("Missing data", "Please fill in all fields before saving!")
        return
    confirm = messagebox.askyesno("Save Prompt", "Do you want to save the .json file?")
    if not confirm:
        return
    
    logo_data = {
        "subject": subject,
        "subject_style": subj_style,
        "logo_shape": logo_shape,
        "shape_style": sh_style,
        "color_of_subject": subj_clr,
        "color_of_shape": sh_clr,
        "background": "white",
        "extra_instructions": extra
    }
    os.makedirs("basic", exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(logo_data, f, indent=4)

    try:
        script_path = os.path.join("basic", "prompt_gen_2.py")
        
        result = subprocess.run(
            [sys.executable, script_path, api_key],
            capture_output=True,
            text=True,
            check=True
        )
        print("[DEBUG] Script stdout:\n", result.stdout)
        print("[DEBUG] Script stderr:\n", result.stderr)
        messagebox.showinfo("Prompt Generated", "✅ Prompt file created in /prompts folder")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Subprocess failed: {e}")
        print("[ERROR] stdout:\n", e.stdout)
        print("[ERROR] stderr:\n", e.stderr)
        messagebox.showerror("Error", f"❌ Could not run prompt_gen_2.py\nCheck console for details.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        messagebox.showerror("Error", f"❌ Could not run prompt_gen_2.py\n{e}")
    load_current_inputs()

def regenerate_prompt():
    api_key = api_key_var.get().strip()
    if not api_key.startswith("hf_") or len(api_key) != 37:
        messagebox.showerror("Invalid API Key", "Please enter a valid Hugging Face API key.")
        return
    
    if not change_prompt:
        return
    change_text = change_prompt.get().strip()
    if not change_text:
        messagebox.showwarning("No instruction", "Please fill in the 'What to change' field.")
        return
    confirm = messagebox.askyesno("Regenerate Prompt", f"Regenerate with:\n\n{change_text}")
    if not confirm:
        return
    print(f"[DEBUG] User confirmation for regenerate: {confirm}")
    if not confirm:
        return

    try:
        print("[DEBUG] Running prompt_regen.py with stdin...")
        script_path = os.path.join("basic", "prompt_regen.py")
        result = subprocess.run(
            [sys.executable, script_path, change_text, api_key],
            capture_output=True,
            text=True,
            check=True
        )
        print("[DEBUG] Script stdout:\n", result.stdout)
        print("[DEBUG] Script stderr:\n", result.stderr)
        messagebox.showinfo("Prompt Regenerated", "✅ Prompt has been regenerated in /prompts/input.json")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Subprocess failed: {e}")
        print("[ERROR] stdout:\n", e.stdout)
        print("[ERROR] stderr:\n", e.stderr)
        messagebox.showerror("Error", f"❌ Could not run prompt_regen.py\nCheck console for details.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        messagebox.showerror("Error", f"❌ Could not run prompt_regen.py\n{e}")
    load_current_inputs()

def generate_img():
    confirm = messagebox.askyesno(
        "Generate Image",
        "Would you like to create the logo based on the current prompt?"
    )
    if not confirm:
        print("[DEBUG] User canceled image generation.")
        return

    api_key = api_key_var.get().strip() 
    if not api_key.startswith("hf_") or len(api_key) != 37:
        messagebox.showerror("Invalid API Key", "Please enter a valid Hugging Face API key.")
        return

    try:
        print("[DEBUG] Running basic/main.py...")
        script_path = os.path.join("basic", "main.py")
        result = subprocess.run(
            [sys.executable, script_path, api_key],
            capture_output=True,
            text=True,
            check=True
        )
        print("[DEBUG] Script stdout:\n", result.stdout)
        print("[DEBUG] Script stderr:\n", result.stderr)
        messagebox.showinfo("Image Generated", "✅ Logo image created successfully")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Subprocess failed: {e}")
        print("[ERROR] stdout:\n", e.stdout)
        print("[ERROR] stderr:\n", e.stderr)
        messagebox.showerror("Error", "❌ Could not run main.py\nCheck console for details.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        messagebox.showerror("Error", f"❌ Could not run main.py\n{e}")

def clear_all(button):
    if button == "create_new":
        l_subject.delete(0, END)
        l_shape.delete(0, END)
        subject_style.delete(0, END)
        shape_style.delete(0, END)
        subject_clr.delete(0, END)
        shape_clr.delete(0, END)
        xtra_inf.delete(0, END)
        change_prompt.delete(0, END)
        print(button)
        return
    if button != "create_new" and button != "":
        print(button)
        return
    else:
        print("clear_all failed")
        return

def clear_widgets():
    global subject_clr_0, subject_clr_1, letter, shape, shape_ular, shape_2, shape_2_ular
    global text_clr_0, text_clr_1, text_0, text_1, font
    global logo_0, logos, logo_merch, banner, banner_wide
    global inputs_display

    for widget in current_frame.winfo_children():
        if not isinstance(widget, Menu):
            widget.destroy()

    subject_clr_0 = subject_clr_1 = letter = shape = shape_ular = None
    shape_2 = shape_2_ular = text_clr_0 = text_clr_1 = text_0 = text_1 = font = None

def exit_app():
    confirm = messagebox.askyesno("Exit", "Are you sure you want to quit?")
    if not confirm:
        return
    root.destroy()

# ---------------- GÖRGETÉS ----------------
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

current_frame.bind("<Configure>", on_frame_configure)

def _on_mousewheel(event):
    if os.name == 'nt':  # Windows
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    elif os.name == 'posix':  # Linux
        canvas.yview_scroll(-1 * int(event.delta), "units")

    # Windows and Linux
canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # MacOS
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

root.after(100, open_api_key_window)
root.mainloop()