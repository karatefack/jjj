
from uuid import uuid4
import requests
import telebot,glob
from redis import Redis
from telebot import types
db  = Redis(host="localhost",port=6379)
bot = telebot.TeleBot("5438908008:AAE215jC_Lk1zTOkIHQ9TDqhlCf9-0cwgbo",num_threads=int(210000))
from telebot.types import InputMediaPhoto
@bot.message_handler(commands=['start'])
def start(message):
    ch = "TextToImageUpdates"
    r = requests.get(f"https://api.telegram.org/bot5438908008:AAE215jC_Lk1zTOkIHQ9TDqhlCf9-0cwgbo/getchatmember?chat_id=@{ch}&user_id={message.from_user.id}").text
    if "left" not in r:
        db.set(f"member-{message.from_user.id}",f"ok")
        key = types.InlineKeyboardMarkup()
        key.row_width =1
        btn1 = types.InlineKeyboardButton(text=f"- Text To Image Updates .",url="https://t.me/texttoimagerobot")
        key.add(btn1)
        bot.reply_to(message,f"<strong>- اهلا ...\n- يمكنك صنع 9 صور حسب وصفك لها!\n- قم بأرسال هكذا :\n- /make sun\n- استبدل sun بوصفك للشيء\n- Made With ❤️ By : @trakoss - @TextToImageRobot</strong>",parse_mode="html",reply_markup=key)
    else:
        bot.reply_to(message,f"Sorry, Subscribe Here : @{ch} To Use Bot\nThen Send /start .")
@bot.message_handler(func= lambda m:True)
def get(message):
    try:
        if message.text.startswith("/make "):
            bot.reply_to(message,f"<strong>- يتم الان مراجعة طلبك ..</strong>",parse_mode="html")
            prompt = message.text.split("/make ")[1]
            body = {"prompt":f"{prompt}"}
            bot.send_chat_action(message.chat.id,"upload_photo")
            r = requests.post(f"https://bf.dallemini.ai/generate",json=body).json()
            for i in range(9):
                bot.send_chat_action(message.chat.id,"upload_photo")
                import base64,random
                w = r['images'][i]
                with open(f"pp/imageToSave{random.randint(0,234)}.png", "wb") as fh:
                    fh.write(base64.b64decode(f'{w}'))
            path = "./pp/*.png"
            vid_media = []
            for filename in glob.glob(path):
              
                with open(filename, 'rb') as fh:
                    data = fh.read()
                    media = InputMediaPhoto(data,caption=f"- Order : {prompt}")
                    vid_media.append(media)
            bot.send_media_group(message.chat.id, vid_media)
            bot.reply_to(message,f"- طلبك جاهز . ")
            for filenn in glob.glob("./pp/*.png"):
                import os
                try:
                    os.system(f"rm -rf {filenn}")
                except:
                    pass
    except:
        pass
bot.infinity_polling()
        
