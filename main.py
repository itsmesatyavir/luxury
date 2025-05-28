
import requests
import json
import os
import time
import random
from colorama import init, Fore

init(autoreset=True)

print("""
╔═════════════════════════════════════════════╗
║ Luxury Auto Refferal http://t.me/forestarmy ║
╚═════════════════════════════════════════════╝
""")

REGISTER_URL = "https://luxury-airdrop.onrender.com/api/create-username"
TASK_URL = "https://luxury-airdrop.onrender.com/api/complete-task"
JSON_FILE = "username.json"
PROXY_FILE = "proxy.txt"

TASK_TYPES = [
    "telegramGroup", "telegramChannel", "twitter", "twitterRepost6", "twitterRepost5",
    "twitterRepost4", "twitterRepost3", "twitterRepost2", "twitterRepost1",
    "twitterRetweet", "twitterLike"
]

CUSTOM_NAMES = [
    "alex", "bella", "charlie", "diana", "ethan", "fiona", "george", "hannah",
    "ian", "julia", "kyle", "luna", "mike", "nina", "oliver", "paula",
    "quentin", "rose", "sam", "tina", "victor", "wade", "xena", "yuri", "zara"
]

def get_random_username():
    base = random.choice(CUSTOM_NAMES)
    suffix = random.choice(['fa', 'farmy', 'hello', 'sandy', 'satya', 'ragini', 'jake', str(random.randint(1000, 9999))])
    return base + suffix

def load_proxies():
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def get_proxy():
    proxies = load_proxies()
    if proxies:
        proxy = random.choice(proxies)
        return {"http": proxy, "https": proxy}
    return None

def load_usernames():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_username(username, ref_code):
    usernames = load_usernames()
    usernames.append({"username": username, "ref": ref_code})
    with open(JSON_FILE, "w") as f:
        json.dump(usernames, f, indent=4)

def log_message(message, color):
    print(f"{color}{message}")

def register_user(ref_code):
    for _ in range(5):  # Retry up to 5 times
        username = get_random_username()
        payload = {"username": username, "ref": ref_code}
        try:
            proxy = get_proxy()
            response = requests.post(REGISTER_URL, json=payload, proxies=proxy)
            if response.status_code == 201:
                log_message(f"Registered username {username}", Fore.GREEN)
                save_username(username, ref_code)
                return username
            elif response.status_code == 409:
                log_message(f"Username {username} already taken, retrying...", Fore.YELLOW)
                continue
            else:
                log_message(f"Failed to register {username} (Status {response.status_code}): {response.text}", Fore.RED)
                return None
        except Exception as e:
            log_message(f"Registration error: {str(e)}", Fore.RED)
            return None
    return None

def complete_tasks(username):
    for task in TASK_TYPES:
        payload = {"username": username, "taskType": task}
        try:
            proxy = get_proxy()
            response = requests.post(TASK_URL, json=payload, proxies=proxy)
            if response.status_code == 200:
                log_message(f"Completed task {task} for {username}", Fore.GREEN)
            else:
                log_message(f"Failed task {task} for {username}", Fore.YELLOW)
            time.sleep(60)
        except Exception as e:
            log_message(f"Task {task} error: {str(e)}", Fore.RED)

def main():
    try:
        num_requests = int(input("Enter number of referrals: "))
        ref_code = input("Enter your referral code: ")
        run_tasks = input("Run all tasks for each? (y/n): ").strip().lower()

        if num_requests <= 0:
            log_message("Referral number must be greater than 0", Fore.RED)
            return

        if run_tasks not in ['y', 'n']:
            log_message("Input must be 'y' or 'n'", Fore.RED)
            return

        log_message(f"Starting bot for {num_requests} referrals with code: {ref_code}", Fore.GREEN)

        for i in range(num_requests):
            log_message(f"➡️ Processing referral {i+1} of {num_requests}", Fore.YELLOW)
            username = register_user(ref_code)
            if username and run_tasks == 'y':
                complete_tasks(username)
            time.sleep(2)
    except ValueError:
        log_message("Referral number must be a number", Fore.RED)
    except Exception as e:
        log_message(f"Error: {str(e)}", Fore.RED)

if __name__ == "__main__":
    main()
