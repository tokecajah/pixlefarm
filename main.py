import requests
import time
from colorama import init, Fore, Style

# Inisialisasi colorama
init(autoreset=True)

# Fungsi untuk mendapatkan data pengguna
def get_user_data(auth_token):
    url = "https://api.pixelfarm.app/user"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Fungsi untuk melakukan klaim
def claim(auth_token):
    url = "https://api.pixelfarm.app/user/claim"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Fungsi untuk menampilkan waktu hitung mundur dalam format jam:menit:detik
def countdown(seconds):
    while seconds:
        hours, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(f"{Fore.RED}Countdown to next claim: {timeformat}", end='\r')
        time.sleep(1)
        seconds -= 1

# Fungsi utama untuk menjalankan bot untuk satu akun
def run_bot_for_account(auth_token):
    user_data = get_user_data(auth_token)

    print(f"\n{Style.BRIGHT}{Fore.YELLOW}{'='*40}")
    print(f"{Style.BRIGHT}{Fore.CYAN}{' '*15}PixelFarm Bot")
    print(f"{Style.BRIGHT}{Fore.CYAN}{' '*10}From github.com/himiko3939")
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'='*40}")
    print(f"\n{Style.BRIGHT}{Fore.GREEN}{'~'*40}")
    print(f"{Style.BRIGHT}{Fore.GREEN}Telegram ID       : {Fore.WHITE}{user_data['data']['telegram_id']}")
    print(f"{Style.BRIGHT}{Fore.GREEN}Telegram Username : {Fore.WHITE}{user_data['data']['telegram_username']}")
    print(f"{Style.BRIGHT}{Fore.GREEN}Gem Amount        : {Fore.WHITE}{user_data['data']['gem_amount']}")
    print(f"{Style.BRIGHT}{Fore.GREEN}Fruit Total       : {Fore.WHITE}{user_data['data']['crops'][0]['fruit_total']}")
    print(f"{Style.BRIGHT}{Fore.GREEN}Tree Type         : {Fore.WHITE}{user_data['data']['crops'][0]['tree_type']}")
    print(f"{Style.BRIGHT}{Fore.GREEN}{'~'*40}")

    claim_response = claim(auth_token)
    
    if claim_response['data']:
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}Claim Response: {Fore.GREEN}Sukses melakukan klaim!")
        new_user_data = get_user_data(auth_token)
        claimed_fruit = new_user_data['data']['crops'][0]['fruit_total'] - user_data['data']['crops'][0]['fruit_total']
        total_fruit = new_user_data['data']['crops'][0]['fruit_total']
        print(f"{Style.BRIGHT}{Fore.YELLOW}Jumlah fruit yang diklaim : {Fore.WHITE}{claimed_fruit}")
        print(f"{Style.BRIGHT}{Fore.YELLOW}Jumlah total fruit setelah klaim : {Fore.WHITE}{total_fruit}")
    else:
        print(f"\n{Style.BRIGHT}{Fore.RED}Claim Response: {Fore.RED}Gagal melakukan klaim")

# Fungsi utama untuk menjalankan bot untuk semua akun
def run_bot(auth_tokens, claim_interval):
    while True:
        for auth_token in auth_tokens:
            try:
                run_bot_for_account(auth_token)
            except Exception as e:
                print(f"{Style.BRIGHT}{Fore.RED}Error: {e}")
            # Jeda 10 detik setelah setiap akun
            print(f"\n{Style.BRIGHT}{Fore.BLUE}Menunggu 10 detik sebelum akun berikutnya...")
            time.sleep(10)
        print(f"\n{Style.BRIGHT}{Fore.GREEN}{'-'*40}")
        print(f"{Style.BRIGHT}{Fore.BLUE}Menunggu untuk klaim berikutnya...")
        countdown(claim_interval)
        print(f"\n{Style.BRIGHT}{Fore.GREEN}{'-'*40}")

# Membaca auth tokens dari file teks
with open('data.txt', 'r') as file:
    auth_tokens = [line.strip() for line in file]

# Jalankan bot dengan interval klaim setiap 6 jam
run_bot(auth_tokens, 21600)
