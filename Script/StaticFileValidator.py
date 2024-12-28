import requests
from colorama import init, Fore, Style
import sys

# Initialize colorama
init(autoreset=True)

def main():
    base_url = "https://static.blockmango.net/client/{}/client.zip"
    for num in range(20000, 30000):
        url = base_url.format(num)
        try:
            response = requests.get(url, stream=True, timeout=5)
            if response.status_code == 200:
                # Hyperlink format: \033]8;;<URL>\033\\<TEXT>\033]8;;\033\\
                hyperlink = f"\033]8;;{url}\033\\[{num}] File works!{Style.RESET_ALL}\033]8;;\033\\"
                print(Fore.GREEN + hyperlink)
            else:
                print(Fore.RED + f"[{num}] Access denied!")
        except requests.RequestException:
            print(Fore.RED + f"[{num}] Access denied!")
        finally:
            response.close()

if __name__ == "__main__":
    main()