import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from capture.screen_capture import capture_screen
from capture.ocr_reader import extract_text_from_image
from capture.window_monitor import get_active_window_title
from capture.clipboard_monitor import get_clipboard_text
from core.logger import log_event
import requests
import time
import os
import threading
import json
import sys
import shutil
import winshell
from win32com.client import Dispatch

SAVE_PATH = "./data/screenshots/"
SETTINGS_PATH = "./data/settings.json"
permissions = {"screen_capture": False}
monitoring_active = threading.Event()

faq_list = {
    "What does this app do?": "It captures your screen, extracts text, and monitors clipboard activity locally.",
    "Is my data safe?": "Yes, everything stays on your computer. Nothing is sent online.",
    "How often does it capture?": "Every 10 seconds by default.",
    "Can I select an image manually?": "Yes, use the '📷 Attach Photo' button."
}

root = tk.Tk()
root.title("Local Passive Assistant - Powered by Ollama")
root.geometry("620x740")

style = ttk.Style()

# Load theme from settings or default to light
def load_theme():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                return json.load(f).get("theme", "light")
        except:
            return "light"
    return "light"

def save_theme(theme):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({"theme": theme}, f)

current_theme = load_theme()

# Create desktop shortcut if not exists
def create_shortcut():
    shortcut_path = os.path.join(winshell.desktop(), "Local Assistant.lnk")
    if not os.path.exists(shortcut_path):
        target = sys.executable
        script = os.path.abspath(__file__)
        work_dir = os.path.dirname(script)
        icon = target

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.Arguments = f'"{script}"'
        shortcut.WorkingDirectory = work_dir
        shortcut.IconLocation = icon
        shortcut.save()

create_shortcut()

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=70, state='disabled')
chat_display.pack(pady=10)

def apply_theme(theme):
    global current_theme
    current_theme = theme
    save_theme(theme)
    if theme == "dark":
        root.configure(bg="#2e2e2e")
        style.theme_use("clam")
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TButton", background="#444", foreground="white")
        style.configure("TLabel", background="#2e2e2e", foreground="white")
        chat_display.configure(bg="#1e1e1e", fg="white")
    else:
        root.configure(bg="#f0f0f0")
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", background="#fff", foreground="black")
        style.configure("TLabel", background="#f0f0f0", foreground="black")
        chat_display.configure(bg="white", fg="black")

apply_theme(current_theme)

def toggle_theme():
    apply_theme("dark" if current_theme == "light" else "light")

def attach_photo():
    file_path = filedialog.askopenfilename()
    if file_path:
        extracted_text = extract_text_from_image(file_path)
        messagebox.showinfo("Extracted Text", extracted_text)

def grant_screen_capture():
    permissions["screen_capture"] = True
    messagebox.showinfo("Permission Granted", "Screen capture permission granted!")

def start_monitoring():
    if not permissions["screen_capture"]:
        messagebox.showerror("Permission Needed", "Please grant screen capture permission first.")
        return

    if monitoring_active.is_set():
        monitoring_active.clear()
        start_btn.config(text="▶ Start Monitoring")
        messagebox.showinfo("Monitoring Stopped", "Screen monitoring has been stopped.")
        return

    def monitor_loop():
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)

        monitoring_active.set()
        while monitoring_active.is_set():
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{SAVE_PATH}screenshot_{timestamp}.png"

            capture_screen(screenshot_path)
            screen_text = extract_text_from_image(screenshot_path)
            active_window = get_active_window_title()
            clipboard_content = get_clipboard_text()

            event = {
                "timestamp": timestamp,
                "window": active_window,
                "screen_text": screen_text,
                "clipboard": clipboard_content
            }

            log_event(event)
            print(f"[{timestamp}] Data captured.")
            time.sleep(10)

    threading.Thread(target=monitor_loop, daemon=True).start()
    start_btn.config(text="⏹ Stop Monitoring")
    messagebox.showinfo("Monitoring Started", "Screen monitoring has started in background.")

def stream_response_to_chatbox(answer):
    def stream(index=0):
        if index < len(answer):
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, answer[index])
            chat_display.see(tk.END)
            chat_display.configure(state='disabled')
            root.after(30, stream, index + 1)
        else:
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, "\n\n")
            chat_display.configure(state='disabled')
            chat_display.see(tk.END)

    stream()

def generate_bot_reply(user_input):
    try:
        with open("./data/events.log", "r") as f:
            context = f.read()[-1000:]
    except:
        context = "This assistant monitors screen and clipboard for useful context."

    full_prompt = f"Context: {context}\n\nQuestion: {user_input}\nAnswer:"

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False
        }, timeout=60)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Sorry, no answer was generated.")
        else:
            return "Error communicating with Ollama."
    except Exception as e:
        return f"Error: {str(e)}"

def send_chat_message():
    user_input = chat_entry.get().strip()
    if not user_input:
        return

    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"You: {user_input}\n")
    chat_display.see(tk.END)
    chat_display.configure(state='disabled')
    chat_display.update()
    chat_entry.delete(0, tk.END)

    progress_bar.pack(side=tk.LEFT, padx=5)
    progress_bar.start(10)

    def process():
        response = generate_bot_reply(user_input)
        progress_bar.stop()
        progress_bar.pack_forget()
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, "Bot: ")
        chat_display.configure(state='disabled')
        stream_response_to_chatbox(response)

    threading.Thread(target=process, daemon=True).start()

def open_faq():
    faq_text = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in faq_list.items()])
    messagebox.showinfo("Frequently Asked Questions", faq_text)

def export_logs():
    log_file_path = "./data/events.log"
    if os.path.exists(log_file_path):
        os.startfile(log_file_path)
    else:
        messagebox.showinfo("No Logs", "No logs found yet.")

frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

attach_btn = ttk.Button(frame_buttons, text="📷 Attach Photo", command=attach_photo, width=18)
attach_btn.grid(row=0, column=0, padx=5)

grant_btn = ttk.Button(frame_buttons, text="✅ Grant Permission", command=grant_screen_capture, width=18)
grant_btn.grid(row=0, column=1, padx=5)

start_btn = ttk.Button(frame_buttons, text="▶ Start Monitoring", command=start_monitoring, width=18)
start_btn.grid(row=0, column=2, padx=5)

frame_chat = ttk.Frame(root)
frame_chat.pack(pady=5)

chat_entry = ttk.Entry(frame_chat, width=50)
chat_entry.pack(side=tk.LEFT, padx=5)

send_btn = ttk.Button(frame_chat, text="💬 Send", command=send_chat_message)
send_btn.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(frame_chat, mode='indeterminate', length=100)

theme_btn = ttk.Button(root, text="🌓 Toggle Theme", command=toggle_theme, width=25)
theme_btn.pack(pady=5)

faq_btn = ttk.Button(root, text="❓ Help / FAQ", command=open_faq, width=25)
faq_btn.pack(pady=5)

log_btn = ttk.Button(root, text="📄 View Logs", command=export_logs, width=25)
log_btn.pack(pady=5)

root.mainloop()
