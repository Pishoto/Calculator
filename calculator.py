import tkinter as tk
import math
import re

root = tk.Tk()
root.title("Calculator")
num_rows = root.grid_size()[0]
num_cols = root.grid_size()[1]
entry = tk.Entry(root, font=("Arial", 18), justify="right")
entry.grid(row=0, column=0, columnspan=5, sticky="nsew")

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("⌫", 1, 3), ("C", 1, 4),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3), ("/", 2, 4),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3), ("-", 3, 4),
    ("0", 4, 0), (".", 4, 1), ("π", 4, 2), (":-)", 4, 3), ("=", 4, 4),
    ("(", 5, 0), (")", 5, 1), ("^", 5, 2), ("x²", 5, 3), ("x³", 5, 4),
    ("√", 6, 0), ("∛", 6, 1), ("sin", 6, 2), ("cos", 6, 3), ("tan", 6, 4),
    ("e", 7, 0), ("ln", 7, 1), ("!", 7, 2), ("%", 7, 3), ("Deg", 7, 4)
]

light_theme = {
    "bg": "white", "entry_bg": "white", "entry_fg": "black",
    "button_bg": "SystemButtonFace", "button_fg": "black",
    "button_active_bg": "gray", "button_active_fg": "white"
}
dark_theme = {
    "bg": "#222", "entry_bg": "#333", "entry_fg": "white",
    "button_bg": "#444", "button_fg": "white",
    "button_active_bg": "#666", "button_active_fg": "black"
}

dark_mode = False

def write_to_entry(text):
    if text == "√":
        text = "√("
    elif text == "∛":
        text = "∛("
    elif text == "sin":
        text = "sin("
    elif text == "cos":
        text = "cos("
    elif text == "tan":
        text = "tan("
    elif text == "ln":
        text = "ln("
    entry.insert(tk.END, text)

degree_mode = True

def evaluate():
    try:
        expression = entry.get()
        expression = expression.replace("^", "**")
        expression = expression.replace("√", "math.sqrt")
        expression = expression.replace("∛", "math.pow")
        expression = re.sub(r'math.pow\(([^()]+)\)', r'math.pow(\1, 1/3)', expression)
        expression = expression.replace("π", "math.pi")
        expression = expression.replace("e", "math.e")
        expression = expression.replace("ln", "math.log")
        expression = expression.replace("²", "**2")
        expression = expression.replace("³", "**3")
        expression = re.sub(r'(\d+)!', r'math.factorial(\1)', expression)
        def replace_trig(match):
            func, arg = match.groups()
            if degree_mode:
                return f"math.{func}(math.radians({arg}))"
            else:
                return f"math.{func}({arg})"
        expression = re.sub(r'\b(sin|cos|tan)\(([^()]+)\)', replace_trig, expression)

        result = eval(expression, {"math": math})
        result = round(result, 10)
        if result == int(result):
            result = int(result)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def clear():
    entry.delete(0, tk.END)

def backspace():
    entry.delete(len(entry.get())-1, tk.END)

def handle_keypress(event):
    if event.char in "0123456789.+-*/()e!%":
        write_to_entry(event.char)
    elif event.char == "\r":
        evaluate()
    elif event.char == "\x08":
        backspace()
    elif event.char == "c":
        clear()
    elif event.char == "^":
        write_to_entry("^")
    elif event.char == "%":
        write_to_entry("%")
    elif event.char == "e":
        write_to_entry("e")
    elif event.char == "!":
        write_to_entry("!")

def create_button(text, row, col, command=None):
    if command is None:
        command = lambda t=text: write_to_entry(t)
    btn = tk.Button(root, text=text, width=5, height=2, font=("Arial", 14), command=command)
    btn.grid(row=row, column=col, sticky="nsew")
    buttons_obj.append((text, btn))

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    colors = dark_theme if dark_mode else light_theme
    
    root.configure(bg=colors["bg"])
    entry.configure(bg=colors["entry_bg"], fg=colors["entry_fg"])

    for button in buttons_obj:
        button[1].configure(bg=colors["button_bg"], fg=colors["button_fg"], 
                         activebackground=colors["button_active_bg"], activeforeground=colors["button_active_fg"])

def toggle_mode():
    global degree_mode
    degree_mode = not degree_mode
    for button in buttons_obj:
        if button[0] == "Deg":
            button[1].configure(text="Deg" if degree_mode else "Rad")

# List to store button objects
buttons_obj = []

for (text, row, col) in buttons:
    if text == "=":
        create_button(text, row, col, evaluate)
    elif text == "C":
        create_button(text, row, col, clear)
    elif text == "⌫":
        create_button(text, row, col, backspace)
    elif text == ":-)":
        create_button(text, row, col, toggle_dark_mode)
    elif text == "Deg":
        create_button(text, row, col, toggle_mode)
    elif text == "x²":
        create_button(text, row, col, lambda: write_to_entry("²"))
    elif text == "x³":
        create_button(text, row, col, lambda: write_to_entry("³"))
    else:
        create_button(text, row, col)

for i in range(root.grid_size()[0]):
    root.grid_rowconfigure(i, weight=1)
for i in range(root.grid_size()[1]):
    root.grid_columnconfigure(i, weight=1)

# Keyboard support
root.bind("<Key>", handle_keypress)

root.mainloop()
