import json
import os
import time
import requests
import threading
import sys
from enum import Enum
from colorama import init, Fore, Style

os.system("title Lynra Webhook Spammer")

init(autoreset=True)

class MessageStatus(Enum):
    SUCCESS = f"{Fore.GREEN}✓ Successfully spammed{Style.RESET_ALL}"
    FAILURE = f"{Fore.RED}✗ Failed to spam{Style.RESET_ALL}"
    RATE_LIMITED = f"{Fore.YELLOW}⚠ Rate limited (waiting to retry){Style.RESET_ALL}"
    INVALID_URL = f"{Fore.RED}✗ Invalid Discord webhook URL{Style.RESET_ALL}"
    FINISHED = f"{Fore.CYAN}✔ Spamming Completed{Style.RESET_ALL}"
    DELETED = f"{Fore.GREEN}✓ Webhook successfully deleted{Style.RESET_ALL}"
    DELETE_FAILED = f"{Fore.RED}✗ Failed to delete webhook{Style.RESET_ALL}"

ASCII_LOGO = f"""{Fore.LIGHTMAGENTA_EX}
 ██▓   ▓██   ██▓ ███▄    █  ██▀███   ▄▄▄      
▓██▒    ▒██  ██▒ ██ ▀█   █ ▓██ ▒ ██▒▒████▄    
▒██░     ▒██ ██░▓██  ▀█ ██▒▓██ ░▄█ ▒▒██  ▀█▄  
▒██░     ░ ▐██▓░▓██▒  ▐▌██▒▒██▀▀█▄  ░██▄▄▄▄██ 
░██████▒ ░ ██▒▓░▒██░   ▓██░░██▓ ▒██▒ ▓█   ▓██▒
░ ▒░▓  ░  ██▒▒▒ ░ ▒░   ▒ ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░
░ ░ ▒  ░▓██ ░▒░ ░ ░░   ░ ▒░  ░▒ ░ ▒░  ▒   ▒▒ ░
  ░ ░   ▒ ▒ ░░     ░   ░ ░   ░░   ░   ░   ▒   
    ░  ░░ ░              ░    ░           ░  ░
        ░ ░                                   
{Style.RESET_ALL}"""

class WebhookMessenger:
    def __init__(self):
        print(ASCII_LOGO)
        self.clean_temp_files()
        self.load_config()
        self.webhook_url = ""
        self.message_count = 0
        self.max_messages = 0
        self.running = True
        self.delay = 1.0  
        self.max_threads = 5  

    def clean_temp_files(self):
        if os.path.exists("]"):
            os.remove("]")

    def load_config(self):
        if not os.path.exists('config.json'):
            self.username = ".gg/lynra"
            self.avatar_url = "https://cdn.discordapp.com/attachments/1386363599353680083/1387836855067869305/output-onlinepngtools_1.png"
            return

        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            self.username = config.get("username", ".gg/lynra")
            self.avatar_url = config.get("avatar_url", "https://cdn.discordapp.com/attachments/1386363599353680083/1387836855067869305/output-onlinepngtools_1.png")
        except:
            self.username = ".gg/lynra"
            self.avatar_url = ""

    def get_webhook(self):
        print(f"{Fore.LIGHTBLUE_EX}»»{Style.RESET_ALL} {Fore.CYAN}Webhook Setup{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{'═'*30}{Style.RESET_ALL}")
        
        while True:
            webhook_url = input(f"{Fore.LIGHTYELLOW_EX}⚡ Enter webhook URL:{Style.RESET_ALL} ").strip()
            
            if not webhook_url.startswith("https://discord.com/api/webhooks/"):
                print(f"{Fore.RED}✗ Invalid URL format! Must start with: 'https://discord.com/api/webhooks/'{Style.RESET_ALL}")
                continue
                
            print(f"{Fore.CYAN}🔍 Checking webhook...{Style.RESET_ALL}")
            try:
                response = requests.get(webhook_url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"{Fore.GREEN}✓ Webhook is valid!{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}» Name: {data.get('name', 'Unknown')}")
                    print(f"» Channel ID: {data.get('channel_id', 'Unknown')}")
                    print(f"» Guild ID: {data.get('guild_id', 'Unknown')}{Style.RESET_ALL}")
                    self.webhook_url = webhook_url
                    return True
                    
                elif response.status_code == 404:
                    print(f"{Fore.RED}✗ Webhook not found (404){Style.RESET_ALL}")
                else:
                    error_msg = response.text[:200].replace('\n', ' ').strip()
                    print(f"{Fore.RED}✗ Webhook error: {response.status_code} - {error_msg}{Style.RESET_ALL}")
                    
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}✗ Error connecting to webhook: {str(e)}{Style.RESET_ALL}")
                
            print(f"{Fore.YELLOW}Please check the URL and try again.{Style.RESET_ALL}")

    def validate_webhook(self):
        return self.webhook_url.startswith("https://discord.com/api/webhooks/")

    def send_message(self, content):
        data = {
            "content": content,
            "username": self.username,
            "avatar_url": self.avatar_url
        }

        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = requests.post(self.webhook_url, json=data, timeout=10)  
                
                if response.status_code == 204:
                    print(MessageStatus.SUCCESS.value)
                    return True
                elif response.status_code == 429:
                    retry_after = response.json().get("retry_after", 5) + 1 
                    print(f"{MessageStatus.RATE_LIMITED.value} - Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    retry_count += 1
                else:
                    print(f"{MessageStatus.FAILURE.value} (Status: {response.status_code})")
                    return False
                    
            except requests.exceptions.RequestException as e:
                print(f"{MessageStatus.FAILURE.value} (Error: {str(e)})")
                time.sleep(2) 
                retry_count += 1
        
        print(f"{Fore.RED}» Max retries reached for message{Style.RESET_ALL}")
        return False

    def delete_webhook(self):
        print(f"\n{Fore.YELLOW}⚠ WARNING: This will permanently delete the webhook. Continue? (y/n){Style.RESET_ALL}")
        confirm = input("> ").strip().lower()
        
        if confirm != 'y':
            print(f"{Fore.YELLOW}» Operation cancelled.{Style.RESET_ALL}")
            return

        try:
            response = requests.delete(self.webhook_url)
            if response.status_code == 204:
                print(MessageStatus.DELETED.value)
            else:
                print(f"{MessageStatus.DELETE_FAILED.value} (Status: {response.status_code})")
        except Exception as e:
            print(f"{MessageStatus.DELETE_FAILED.value} (Error: {str(e)})")

    def run(self):
        while True:
            print(f"\n{Fore.LIGHTBLUE_EX}»»{Style.RESET_ALL} {Fore.CYAN}Main Menu{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}{'═'*30}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTCYAN_EX}1. Spam Webhook")
            print(f"2. Delete Webhook")
            print(f"3. Exit{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.LIGHTYELLOW_EX}⚡ Select an option (1-3):{Style.RESET_ALL} ").strip()
            
            if choice == '3':
                print(f"\n{Fore.LIGHTBLUE_EX}💬 Exiting...{Style.RESET_ALL}")
                break
                
            if choice not in ['1', '2']:
                print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
                continue
                

            if not self.webhook_url:
                if not self.get_webhook():
                    continue
                    
            if choice == '2':
                self.delete_webhook()
                continue
                
                while True:
                    message = input(f"\n{Fore.LIGHTCYAN_EX}💬 Enter message to spam (or 'back' to return to menu):{Style.RESET_ALL} ").strip()
                    if message.lower() == 'back':
                        break
                    if message:
                        break
                    print(f"{Fore.RED}Message cannot be empty. Try again.{Style.RESET_ALL}")

            while True:
                try:
                    self.max_messages = int(input(f"{Fore.LIGHTCYAN_EX}🔁 How many times to send it:{Style.RESET_ALL} "))
                    if self.max_messages <= 0:
                        print(f"{Fore.RED}Please enter a number greater than 0.{Style.RESET_ALL}")
                        continue
                    break
                except ValueError:
                    print(f"{Fore.RED}Enter a valid number!{Style.RESET_ALL}")

            while True:
                try:
                    delay_input = input(f"{Fore.LIGHTCYAN_EX}⏱ Delay between messages (seconds, 0.5 recommended):{Style.RESET_ALL} ").strip()
                    self.delay = max(0.1, float(delay_input))  
                    break
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")

            print(f"{Fore.LIGHTGREEN_EX}⏱ Spamming started...{Style.RESET_ALL}")
            start_time = time.time()

            for i in range(self.max_messages):
                while threading.active_count() > self.max_threads:
                    time.sleep(0.1)
                
                thread = threading.Thread(target=self.send_message, args=(message,))
                thread.start()
                
                time.sleep(0.05)
                
                if (i + 1) % 10 == 0 or (i + 1) == self.max_messages:
                    print(f"{Fore.CYAN}» Sent {i + 1}/{self.max_messages} messages{Style.RESET_ALL}")
                
                time.sleep(self.delay)

            while threading.active_count() > 1:  
                time.sleep(0.1)

            end_time = time.time()
            duration = round(end_time - start_time, 2)

            print(f"{MessageStatus.FINISHED.value} — {self.max_messages} messages sent in {duration} seconds.\n")

            again = input(f"{Fore.LIGHTYELLOW_EX}❓ Spam another webhook? (y/n):{Style.RESET_ALL} ").strip().lower()
            if again != "y":
                print(f"{Fore.LIGHTBLUE_EX}💬 Exiting...{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    try:
        messenger = WebhookMessenger()
        messenger.run()
    except Exception as e:
        print(f"{Fore.RED}» Critical error: {e}{Style.RESET_ALL}")
        sys.exit(1)
