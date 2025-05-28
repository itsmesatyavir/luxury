import requests
import names
import json
import os
from colorama import init, Fore
import time
import random

init(autoreset=True)
print("""
===========================================================
               🚗 Luxury Auto Referral Bot 🚗
                   Powered by FORESTARMY
===========================================================
""")
REGISTER_URL = "https://luxury-airdrop.onrender.com/api/create-username"
TASK_URL = "https://luxury-airdrop.onrender.com/api/complete-task"
JSON_FILE = "username.json"
PROXY_FILE = "proxy.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

TASK_TYPES = [
    "telegramGroup", "telegramChannel", "twitter", "twitterRepost6", "twitterRepost5",
    "twitterRepost4", "twitterRepost3", "twitterRepost2", "twitterRepost1",
    "twitterRetweet", "twitterLike"
]

def load_proxies():
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def get_proxy():
    proxies = load_proxies()
    if proxies:
        proxy = random.choice(proxies)
        log_message(f"Using proxy: {proxy}", Fore.CYAN)
        return {"http": proxy, "https": proxy}
    return None

def load_usernames():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_message("Corrupted JSON file. Resetting...", Fore.YELLOW)
            os.remove(JSON_FILE)
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
    username = names.get_first_name().lower()
    payload = {
        "username": username,
        "ref": ref_code
    }
    try:
        proxy = get_proxy()
        response = requests.post(REGISTER_URL, json=payload, headers=HEADERS, proxies=proxy)
        if response.status_code == 201:
            log_message(f"Successfully registered username: {username}", Fore.GREEN)
            save_username(username, ref_code)
            return username
        else:
            log_message(f"Failed to register {username} (Status {response.status_code}): {response.text}", Fore.RED)
            return None
    except Exception as e:
        log_message(f"Registration error: {str(e)}", Fore.RED)
        return None

def complete_tasks(username):
    for task in TASK_TYPES:
        payload = {
            "username": username,
            "taskType": task
        }
        try:
            proxy = get_proxy()
            response = requests.post(TASK_URL, json=payload, headers=HEADERS, proxies=proxy)
            if response.status_code == 200:
                log_message(f"Task {task} completed for {username}", Fore.GREEN)
            else:
                log_message(f"Task {task} failed for {username} (Status {response.status_code})", Fore.YELLOW)
            time.sleep(random.uniform(45, 75))
        except Exception as e:
            log_message(f"Error in task {task}: {str(e)}", Fore.RED)

def main():
    try:
        num_requests = int(input("Enter number of referrals to generate: "))
        ref_code = input("Enter your referral code: ")
        run_tasks = input("Do you want to run all tasks after registration? (y/n): ").strip().lower()

        if num_requests <= 0:
            log_message("Number of referrals must be greater than 0.", Fore.RED)
            return

        if run_tasks not in ['y', 'n']:
            log_message("Input must be 'y' or 'n'.", Fore.RED)
            return

        log_message(f"Starting {num_requests} referrals with code {ref_code}", Fore.GREEN)
        
        for i in range(num_requests):
            log_message(f"Processing referral {i+1} of {num_requests}", Fore.YELLOW)
            username = register_user(ref_code)
            if username and run_tasks == 'y':
                complete_tasks(username)
            time.sleep(2)
    except ValueError:
        log_message("Please enter a valid number for referrals.", Fore.RED)
    except Exception as e:
        log_message(f"Unexpected error: {str(e)}", Fore.RED)

if __name__ == "__main__":
    main()
