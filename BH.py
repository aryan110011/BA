import requests
import json
import os
import time

# === COLORS ===
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

# === CONFIG ===
SERVER_URL = "http://fi11.bot-hosting.net:20295"
GITHUB_APPROVAL_URL = "https://raw.githubusercontent.com/aryan110011/fb-approvals/main/approval.json"
GLOBAL_PASSWORD = "aryan123"  # Change this password

# === GET UNIQUE DEVICE KEY ===
def get_device_key():
    try:
        import uuid
        return str(uuid.getnode())
    except:
        return "unknown-device"

# === CHECK APPROVAL FROM GITHUB ===
def check_approval():
    key = get_device_key()
    try:
        r = requests.get(GITHUB_APPROVAL_URL)
        if r.status_code != 200:
            print(f"{RED}[❌] Failed to fetch approval list from GitHub.{RESET}")
            return False

        data = r.json()
        if key in data:
            print(f"{GREEN}[✅] Approval found for this device ({data[key]}).{RESET}")
            return True
        else:
            print(f"{RED}[⛔] This device is not approved yet.{RESET}")
            print(f"{YELLOW}🔑 Your device key: {key}{RESET}")
            print(f"{CYAN}📩 Send this key to the tool owner for approval.{RESET}")
            return False
    except Exception as e:
        print(f"{RED}[❌] Error fetching approval: {e}{RESET}")
        return False

# === ASK FOR PASSWORD ===
def ask_password():
    print(f"{GREEN}🔐 Please enter your password to access the tool:{RESET}")
    password = input("Password: ")
    if password == GLOBAL_PASSWORD:
        print(f"{GREEN}✅ Access Granted!{RESET}")
        return True
    else:
        print(f"{RED}❌ Incorrect Password. Access Denied.{RESET}")
        return False

# === LOGO WITH ANIMATION ===
def print_logo():
    logo_lines = [
        "███████╗██╗██╗     ██╗     ",
        "██╔════╝██║██║     ██║     ",
        "███████╗██║██║     ██║     ",
        "╚════██║██║██║     ██║     ",
        "███████║██║███████╗███████╗",
        "╚══════╝╚═╝╚══════╝╚══════╝",
    ]
    for line in logo_lines:
        print(f"{RED}{line}{RESET}")
        time.sleep(0.1)

# === LOGIN TIME ===
def show_login_time():
    login_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{YELLOW}🔓 Login Time: {login_time}{RESET}\n")

# === NOTE ===
def print_note():
    note_lines = [
        f"{CYAN}⚠️ Note:{RESET}",
        f"{CYAN}If any user tries to access another user's account, their approval will be revoked.{RESET}",
        f"{CYAN}Using bad language will result in removal from the tool.{RESET}",
        f"{CYAN}This tool is strictly for LEGENDS only!{RESET}",
        f"{YELLOW}Made by ArYan.x3{RESET}\n"
    ]
    for line in note_lines:
        print(line)
        time.sleep(0.3)

# === INPUT PATH VALIDATOR ===
def input_path(label):
    path = input(f"{CYAN}[📂] {label} path: {RESET}").strip()
    if not os.path.exists(path):
        print(f"{RED}[❌] File not found: {path}{RESET}")
        return None
    return os.path.abspath(path)

# === START TASK ===
def start_task():
    user = input(f"{YELLOW}[👤] Enter your username: {RESET}").strip()
    task_name = input(f"{YELLOW}[📌] Enter a task name: {RESET}").strip()
    post_id = input(f"{YELLOW}[🎯] Enter target post ID: {RESET}").strip()
    resume_post_id = input(f"{YELLOW}[🔁] Enter resume post ID: {RESET}").strip()
    header_name = input(f"{YELLOW}[💬] Enter header name (e.g. HATER): {RESET}").strip()
    delay = input(f"{YELLOW}[⏱️] Delay between comments (in seconds): {RESET}").strip()

    cookie_file = input_path("Cookie file")
    comments_file = input_path("Comments file")

    if not cookie_file or not comments_file:
        return

    with open(cookie_file, 'r') as f:
        cookie_data = f.read()
    with open(comments_file, 'r') as f:
        comments_data = f.read()

    config = {
        "user": user,
        "task_name": task_name,
        "target_post_id": post_id,
        "resume_post_id": resume_post_id,
        "headers_name": header_name,
        "delay": delay,
        "cookie_data": cookie_data,
        "comments_data": comments_data
    }

    print(f"\n{GREEN}[🚀] Sending task to server...{RESET}")
    try:
        r = requests.post(f"{SERVER_URL}/start", json=config)
        print(f"{GREEN}[✅] Server Response: {r.json()}{RESET}")
    except Exception as e:
        print(f"{RED}[❌] Error: {e}{RESET}")

# === STOP TASK ===
def stop_task():
    user = input(f"{YELLOW}[👤] Enter your username: {RESET}").strip()
    task_name = input(f"{YELLOW}[📌] Enter task name to stop: {RESET}").strip()
    payload = {"user": user, "task_name": task_name}

    print(f"\n{GREEN}[🛑] Sending stop command to server...{RESET}")
    try:
        r = requests.post(f"{SERVER_URL}/stop", json=payload)
        print(f"{GREEN}[✅] Server Response: {r.json()}{RESET}")
    except Exception as e:
        print(f"{RED}[❌] Error: {e}{RESET}")

# === MAIN MENU ===
def menu():
    while True:
        print_logo()
        show_login_time()
        print_note()
        print(f"{CYAN}"
              "[1] Start a comment task\n"
              "[2] Stop a task\n"
              "[0] Exit"
              f"{RESET}")
        choice = input("Select option: ").strip()
        if choice == "1":
            start_task()
        elif choice == "2":
            stop_task()
        elif choice == "0":
            print(f"{YELLOW}👋 Goodbye!{RESET}")
            break
        else:
            print(f"{RED}[❌] Invalid option.{RESET}")
        input(f"\n{CYAN}Press Enter to return to menu...{RESET}")

# === START ===
if __name__ == "__main__":
    print_logo()
    if check_approval():
        if ask_password():
            menu()
