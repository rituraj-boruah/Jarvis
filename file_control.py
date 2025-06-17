import os
import shutil

def open_folder(folder_name):
    try:
        os.startfile(folder_name)
    except Exception as e:
        print(f"[ERROR] Couldn't open folder '{folder_name}': {e}")

def search_file(file_name):
    print(f"[INFO] Searching for '{file_name}' on C:\\ drive")
    for root, dirs, files in os.walk("C:\\"):
        if file_name in files:
            path = os.path.join(root, file_name)
            try:
                os.startfile(path)
                print(f"[SUCCESS] Opened file at {path}")
                return
            except Exception as e:
                print(f"[ERROR] Found but couldn't open '{file_name}': {e}")
                return
    print("[WARN] File not found.")

def delete_file(file_name):
    try:
        os.remove(file_name)
        print(f"[SUCCESS] File '{file_name}' deleted.")
    except Exception as e:
        print(f"[ERROR] Couldn't delete '{file_name}': {e}")

def move_file(file_name, destination):
    try:
        shutil.move(file_name, destination)
        print(f"[SUCCESS] File moved to '{destination}'.")
    except Exception as e:
        print(f"[ERROR] Couldn't move file: {e}")

def create_folder(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"[SUCCESS] Folder '{folder_name}' created or already exists.")
    except Exception as e:
        print(f"[ERROR] Couldn't create folder '{folder_name}': {e}")
