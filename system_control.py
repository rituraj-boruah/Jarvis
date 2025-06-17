import pyautogui
import os
import psutil
import shutil

# You can expand or customize this map
SOFTWARE_MAP = {
    "notepad": "notepad.exe",
    "command prompt": "C:\\Windows\\System32\\cmd.exe",
    "chrome": shutil.which("chrome") or "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vscode": shutil.which("code") or "C:\\Users\\<YourUsername>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "spotify": shutil.which("spotify") or "C:\\Users\\<YourUsername>\\AppData\\Roaming\\Spotify\\Spotify.exe"
}

def advanced_system_control(command):
    if "volume up" in command:
        pyautogui.press("volumeup")
    elif "volume down" in command:
        pyautogui.press("volumedown")
    elif "mute" in command:
        pyautogui.press("volumemute")
    elif "shutdown" in command:
        os.system("shutdown /s /t 60")
    elif "restart" in command:
        os.system("shutdown /r /t 60")
    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif "move mouse" in command:
        pyautogui.moveRel(100, 0, duration=0.5)
    elif "click mouse" in command:
        pyautogui.click()
    elif "scroll up" in command:
        pyautogui.scroll(300)
    elif "scroll down" in command:
        pyautogui.scroll(-300)
    elif "type" in command:
        text = command.replace("type", "").strip()
        pyautogui.typewrite(text)
    else:
        print("[WARN] Unknown system control command.")

def open_software(app_name):
    app_name = app_name.lower()
    try:
        if app_name in SOFTWARE_MAP:
            path = SOFTWARE_MAP[app_name]
            if path and os.path.exists(path):
                os.startfile(path)
            else:
                print(f"[ERROR] Path not found for '{app_name}'")
        else:
            os.startfile(app_name)  # attempt generic path
    except Exception as e:
        print(f"[ERROR] Could not open '{app_name}': {e}")

def close_software(app_name):
    app_name = app_name.lower()
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if app_name in proc.info['name'].lower():
                proc.kill()
                print(f"[SUCCESS] Killed {proc.info['name']}")
                return
        except Exception:
            pass
    print(f"[WARN] No running process found for '{app_name}'")
