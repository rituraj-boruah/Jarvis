import tkinter as tk

root = None
text_display = None

def launch_display():
    global root, text_display
    root = tk.Tk()
    root.title("Jarvis Voice Assistant")
    root.geometry("600x400")
    root.configure(bg="#121212")
    root.attributes('-topmost', True)

    text_display = tk.Text(
        root,
        font=("Consolas", 14),
        bg="#121212",
        fg="#00FF00",
        wrap='word',
        state='normal'
    )
    text_display.pack(expand=True, fill='both')
    text_display.insert(tk.END, "Jarvis Ready...\n")
    text_display.see(tk.END)

    root.after(100, lambda: root.focus_force())

def run_display():
    global root
    if root:
        root.mainloop()

def update_display(message):
    global text_display
    if text_display:
        text_display.config(state='normal')
        text_display.insert(tk.END, f"{message}\n")
        text_display.see(tk.END)
        text_display.config(state='disabled')
