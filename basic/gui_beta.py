from tkinter import *
from tkinter import messagebox
import os
import subprocess
import sys
import json

root = Tk()
root.title("Logo Generator")
root.geometry("600x440")
root.minsize(300, 200)
json_path = "basic/logo_data.json"



# ---  ---
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="Presets", menu=filemenu)
filemenu.add_command(label="New")
presetsmenu = Menu(menu)
filemenu.add_cascade(label="Open...", menu=presetsmenu)
presetsmenu.add_command(label="A 1")
#filemenu.add_separator()
#filemenu.add_command(label="Exit", command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About")
menu.add_command(label="Create PDF")

l_subject = Entry(root)
l_shape = Entry(root)
subject_style = Entry(root)
shape_style = Entry(root)
subject_clr = Entry(root)
shape_clr = Entry(root)
xtra_inf = Entry(root)
change_prompt = Entry(root)


def load_current_inputs():
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
    print("[DEBUG] Loaded current inputs into preview box.")

def load_logo_data():
    if not os.path.exists(json_path):
        print("[DEBUG] No existing logo_data.json found.")
        return

    print(f"[DEBUG] Loading data from {json_path}")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            logo_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load JSON: {e}")
        return

    # Fill entries if data exists
    l_subject.delete(0, END)
    l_subject.insert(0, logo_data.get("subject", ""))

    l_shape.delete(0, END)
    l_shape.insert(0, logo_data.get("logo_shape", ""))

    subject_style.delete(0, END)
    subject_style.insert(0, logo_data.get("subject_style", ""))

    shape_style.delete(0, END)
    shape_style.insert(0, logo_data.get("shape_style", ""))

    subject_clr.delete(0, END)
    subject_clr.insert(0, logo_data.get("color_of_subject", ""))

    shape_clr.delete(0, END)
    shape_clr.insert(0, logo_data.get("color_of_shape", ""))

    xtra_inf.delete(0, END)
    xtra_inf.insert(0, logo_data.get("extra_instructions", ""))

    print("[DEBUG] Logo data loaded into entry fields.")

def generate_prompt():
    print("[DEBUG] Collecting input values...")
    # Collect values
    subject = l_subject.get().strip()
    logo_shape = l_shape.get().strip()
    subj_style = subject_style.get().strip()
    sh_style = shape_style.get().strip()
    subj_clr = subject_clr.get().strip()
    sh_clr = shape_clr.get().strip()
    extra = xtra_inf.get().strip()
    
    print(f"[DEBUG] Values -> subject={subject}, logo_shape={logo_shape}, "
          f"subject_style={subj_style}, shape_style={sh_style}, "
          f"color_of_subject={subj_clr}, color_of_shape={sh_clr}, extra={extra}")

    # Check for empty fields
    if not all([subject, logo_shape, subj_style, sh_style, subj_clr, sh_clr, extra]):
        print("[DEBUG] Missing data detected, aborting save.")  # debug
        messagebox.showwarning("Missing data", "Please fill in all fields before saving!")
        return

    # Ask for confirmation
    confirm = messagebox.askyesno("Save Prompt", "Do you want to save the .json file?")
    print(f"[DEBUG] User confirmation: {confirm}")  # debug
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
    print(f"[DEBUG] Saving logo data to {json_path}")  # debug

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(logo_data, f, indent=4)
        

    try:
        print("[DEBUG] Running prompt_gen_2.py...")  # debug
        script_path = os.path.join("basic", "prompt_gen_2.py")
        print(f"[DEBUG] Script path: {script_path}")  # debug
        print(f"[DEBUG] Python executable: {sys.executable}")  # debug
        
        result = subprocess.run(
            [sys.executable, script_path],
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
    change_text = change_prompt.get().strip()
    if not change_text:
        messagebox.showwarning("No instruction", "Please fill in the 'What to change' field before regenerating!")
        return

    confirm = messagebox.askyesno("Regenerate Prompt", f"Do you want to regenerate the prompt with:\n\n{change_text}")
    print(f"[DEBUG] User confirmation for regenerate: {confirm}")
    if not confirm:
        return

    try:
        print("[DEBUG] Running prompt_regen.py with stdin...")
        script_path = os.path.join("basic", "prompt_regen.py")
        result = subprocess.run(
            [sys.executable, script_path, change_text],
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
    """Ask if user wants to generate image from current prompt and run main.py"""
    confirm = messagebox.askyesno(
        "Generate Image",
        "Would you like to create the logo based on the current prompt?"
    )
    if not confirm:
        print("[DEBUG] User canceled image generation.")
        return

    try:
        print("[DEBUG] Running basic/main.py...")
        script_path = os.path.join("basic", "main.py")
        result = subprocess.run(
            [sys.executable, script_path],
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

def clear_all():
    l_subject.delete(0, END)
    l_shape.delete(0, END)
    subject_style.delete(0, END)
    shape_style.delete(0, END)
    subject_clr.delete(0, END)
    shape_clr.delete(0, END)
    xtra_inf.delete(0, END)
    change_prompt.delete(0, END)
    print("[DEBUG] Cleared all input fields.")


# --- Labels ---
#window = Toplevel(root)
#window.title("New Logo")
#window.geometry("600x440")


Label(root, text="Logo subject").grid(row=0)
Label(root, text="Logo shape").grid(row=1)

Button(root, text="Clear all", width=20, command=clear_all).grid(row=0, column=1, columnspan=2)

Label(root, text="Subject style").grid(row=2)
Label(root, text="Shape style").grid(row=3)
Label(root, text="Subject color").grid(row=4)
Label(root, text="Shape color").grid(row=5)
Label(root, text="Extra info").grid(row=6)


l_subject.grid(row=0, column=1)
l_shape.grid(row=1, column=1)
subject_style.grid(row=2, column=1)
shape_style.grid(row=3, column=1)
subject_clr.grid(row=4, column=1)
shape_clr.grid(row=5, column=1)
xtra_inf.grid(row=6, column=1)

# --- Buttons ---
Button(root, text="Generate prompt", width=25, command=generate_prompt).grid(row=7, column=0, columnspan=2)
Label(root, text="What to change").grid(row=8)
change_prompt.grid(row=8, column=1)
Button(root, text="Regenerate prompt", width=25, command=regenerate_prompt).grid(row=9, column=0, columnspan=2)
Label(root, text="Current prompt:").grid(row=9, column=1, columnspan=2)
Button(root, text="Generate image based\non current prompt", width=25, command=generate_img).grid(row=10, column=0, columnspan=2)
Button(root, text="Stop the program", width=25, command=root.destroy).grid(row=11, column=0, columnspan=2)

inputs_display = Text(root, height=5, width=40, wrap=WORD)
inputs_display.grid(row=10, column=2, rowspan=5, padx=10, pady=5)

# --- Padding ---
for widget in root.winfo_children():
    if not isinstance(widget, Menu):
        widget.grid_configure(padx=10, pady=5)

load_logo_data()
load_current_inputs()
root.mainloop()
