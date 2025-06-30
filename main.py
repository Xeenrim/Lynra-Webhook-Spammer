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
        self.get_webhook()
        self.message_count = 0
        self.max_messages = 0
        self.running = True
        self.delay = 1.0  # Default delay between messages in seconds
        self.max_threads = 5  # Maximum concurrent threads

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
            self.webhook_url = input(f"{Fore.LIGHTYELLOW_EX}⚡ Enter webhook URL:{Style.RESET_ALL} ").strip()
            if self.validate_webhook():
                break
            print(f"{Fore.RED}Invalid URL format! Must start with: 'https://discord.com/api/webhooks/'{Style.RESET_ALL}")

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
                response = requests.post(self.webhook_url, json=data, timeout=10)  # 10 second timeout
                
                if response.status_code == 204:
                    print(MessageStatus.SUCCESS.value)
                    return True
                elif response.status_code == 429:
                    retry_after = response.json().get("retry_after", 5) + 1  # Add 1 second buffer
                    print(f"{MessageStatus.RATE_LIMITED.value} - Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    retry_count += 1
                else:
                    print(f"{MessageStatus.FAILURE.value} (Status: {response.status_code})")
                    return False
                    
            except requests.exceptions.RequestException as e:
                print(f"{MessageStatus.FAILURE.value} (Error: {str(e)})")
                time.sleep(2)  # Wait before retrying on connection error
                retry_count += 1
        
        print(f"{Fore.RED}» Max retries reached for message{Style.RESET_ALL}")
        return False

    def run(self):
        while True:
            while True:
                message = input(f"{Fore.LIGHTCYAN_EX}💬 Enter message to spam:{Style.RESET_ALL} ").strip()
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

            # Get delay between messages
            while True:
                try:
                    delay_input = input(f"{Fore.LIGHTCYAN_EX}⏱ Delay between messages (seconds, 0.5 recommended):{Style.RESET_ALL} ").strip()
                    self.delay = max(0.1, float(delay_input))  # Minimum 0.1 second delay
                    break
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")

            print(f"{Fore.LIGHTGREEN_EX}⏱ Spamming started...{Style.RESET_ALL}")
            start_time = time.time()

            # Send messages with delay and thread limiting
            for i in range(self.max_messages):
                # Wait if we've reached max threads
                while threading.active_count() > self.max_threads:
                    time.sleep(0.1)
                
                thread = threading.Thread(target=self.send_message, args=(message,))
                thread.start()
                
                # Small delay between starting threads
                time.sleep(0.05)
                
                # Show progress
                if (i + 1) % 10 == 0 or (i + 1) == self.max_messages:
                    print(f"{Fore.CYAN}» Sent {i + 1}/{self.max_messages} messages{Style.RESET_ALL}")
                
                # Add delay between messages
                time.sleep(self.delay)

            # Wait for all threads to complete
            while threading.active_count() > 1:  # 1 for main thread
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
