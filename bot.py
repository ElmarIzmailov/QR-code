import telebot
import qrcode
from TOKEN_bot import bot_Token
from telebot import types

bot = telebot.TeleBot(token=bot_Token)

@bot.message_handler(commands=['start'])
def message_send(message):
    marckup = telebot.types.InlineKeyboardMarkup()
    marckup1 = telebot.types.InlineKeyboardButton("📝 Create QR code", callback_data="qr_code")
    marckup.add(marckup1)
   
    bot.send_message(message.chat.id, "👋 Hi {}\n📝 I am a qrcode generating bot".format(message.from_user.first_name),reply_markup=marckup)
    
@bot.callback_query_handler(func=lambda call: True)
def main(call):
    if call.data == "qr_code":
        path = bot.send_message(call.message.chat.id, "📝 You pressed the button that creates a qr code\nhttps://")
        bot.register_next_step_handler(path, get_path)

def get_path(message):
    global path
    path = message.text

    if path.startswith("https://"):
        qr_img = qrcode.make(path)
        qr_img.save("qrcode.png")

        with open("qrcode.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo)

    else:
        bot.send_message(message.chat.id, "/start")

bot.polling(none_stop=True)
