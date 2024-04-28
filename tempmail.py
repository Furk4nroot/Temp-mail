from flask import Flask
from threading import Thread
import telebot
import requests
import json
import os

app = Flask(__name__)
bot = telebot.TeleBot('6552178739:AAEpVFy2d_lDLSSpl77jtWZkk_VnqwchozA')
admin = "5580826500"

# MADE BY NEP CODER @alexhex1
def file_exists(file_path):
    return os.path.exists(file_path)

# MADE BY NEP CODER @alexhex1
    if not os.path.exists("admin"):
      os.makedirs("admin")

# MADE BY NEP CODER @DEVSNP
    total_file = "admin/mail.txt"
    if not os.path.exists(total_file):
      with open(total_file, 'w') as f:
          f.write("0")




if not os.path.exists("admin"):
    os.makedirs("admin")

# MADE BY NEP CODER @DEVSNP
total_file = "admin/total.txt"
if not os.path.exists(total_file):
    with open(total_file, 'w') as f:
        f.write("0")

total_file = "admin/mail.txt"
if not os.path.exists(total_file):
    with open(total_file, 'w') as f:
        f.write("0")

# MADE BY NEP CODER @alexhex1
total_file = "admin/total.txt"
if not os.path.exists(total_file):
    with open(total_file, 'w') as f:
        f.write("0")


# MADE BY NEP CODER @DEVSNP
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    ulogin = message.from_user.username
# MADE BY NEP CODER @DEVSNP
    users_directory = "admin/users/"
    if not os.path.exists(users_directory):
        os.makedirs(users_directory)

    if not file_exists(f"{users_directory}{user_id}.json"):
        bot.send_message(admin, f"<b>🚀 New User Joined The Bot\n\nUser Id : {user_id}\n\nFirst Name: {fname}\n\nLast name: {lname}</b>")
        open(f"{users_directory}{user_id}.json", "w").close()
# MADE BY NEP CODER @DEVSNP
    mess = f"<b>🔰 Merhaba ☀️{fname}☀️\n🔰Tû bi xêr hati  @{bot.get_me().username}\n\nBot  : @dijvarhack tarafından oluşturuldu</b>"
    keyboard_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard_markup.row("🚀 e-postam")
    keyboard_markup.row("📧 yeni e-posta oluştur", "📨 gelen kutusu")
    keyboard_markup.row("📊  İstatistik")
    bot.send_message(user_id, mess, reply_markup=keyboard_markup, parse_mode='HTML')



# MADE BY NEP CODER @DEVSNP
@bot.message_handler(func=lambda message: message.text == '📧 yeni e-posta oluştur')
def generate_email(message):
    user_id = message.from_user.id

    url = "https://api.internal.temp-mail.io/api/v3/email/new"
    headers = {"Content-Type": "application/json"}
    data = {"min_name_length": 10, "max_name_length": 10}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        email = response.json()['email']
        bot.send_message(user_id, f"<b>e-postanız başarılı bir şekilde olusturuldu\n{email}</b>", parse_mode='HTML')
        with open(f"admin/mail{user_id}.json", "w") as mail_file:
            mail_file.write(json.dumps({"email": email}))
        h = int(open("admin/mail.txt").read()) + 1
        with open("admin/mail.txt", "w") as mail_count_file:
            mail_count_file.write(str(h))
    else:
        bot.send_message(user_id, "<b>Error occurred while generating email</b>", parse_mode='HTML')
# MADE BY NEP CODER @DEVSNP
@bot.message_handler(func=lambda message: message.text == '🚀 e-postam')
def get_user_email(message):
    user_id = message.from_user.id

    file_path = f"admin/mail{user_id}.json"
    if file_exists(file_path):
        email = json.load(open(file_path))['email']
        bot.send_message(user_id, f"<b>sizin e-postanız\n\n{email}</b>", parse_mode='HTML')
    else:
        bot.send_message(user_id, "<b>❌️ e-posta oluşturulmadı</b>", parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '📨 gelen kutusu')
def check_inbox(message):
    user_id = message.from_user.id

    file_path = f"admin/mail{user_id}.json"
    if file_exists(file_path):
        email = json.load(open(file_path))['email']
        response = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages")
        if len(response.text) < 8:
            bot.send_message(user_id, "❌️ e-posta gelmedi henüz")
        else:
            emails = json.loads(response.text)
            for data in emails:
                msg = f"<b>e-posta geldi\n\nId: {data['id']}\n\nSubject: {data['subject']}\n\nText: {data['body_text']}</b>"
                bot.send_message(user_id, msg, parse_mode='HTML')
    else:
        bot.send_message(user_id, "<b>⛔️ Lütfen önce e-posta olusturun</b>", parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '📊  İstatistik')
def bot_status(message):
    user_id = message.from_user.id

    tmail = int(open("admin/mail.txt").read())
    usr = int(open("admin/total.txt").read())
    img_url = "https://quickchart.io/chart?bkg=white&c={'type':'bar','data':{'labels':[''],'datasets':[{'label':'Total-Users','data':[" + str(usr) + "]},{'label':'Total-Mail Created','data':[" + str(tmail) + "]}]}}"

    caption = f"📊 Bot Canlı İstatistik 📊\n\n⚙ Toplam oluşturulan e-posta : {tmail}\n✅️ Toplam kullanıcılar : admin görebilir \n\n🔥 By: @alexhex1"
    bot.send_photo(user_id, img_url, caption=caption)

# MADE BY NEP CODER @DEVSNP
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):

    if str(message.from_user.id) == admin:
        bot.send_message(message.chat.id, "Send the message you want to broadcast to all users. ✨")
        bot.register_next_step_handler(message, send_broadcast)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command. ⛔️")

# MADE BY NEP CODER @DEVSNP
def send_broadcast(message):
    broadcast_text = message.text
    users_directory = "admin/users/"
    user_ids = [file.split('.')[0] for file in os.listdir(users_directory)]


    for user_id in user_ids:
        try:
            bot.send_message(user_id, broadcast_text)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")

    bot.send_message(admin, "Broadcast sent to all users! 📣")




@app.route('/')
def index():
    return "Alive"

def run():
    app.run(host='127.0.0.1', port=2020)

def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()

# MADE BY NEP CODER @DEVSNP
bot.polling()
