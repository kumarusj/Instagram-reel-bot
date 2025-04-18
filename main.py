import os
import telebot
import instaloader

TOKEN = os.getenv("7002494152:AAEb_bxGOicRsV1Tindmndl4Rc4fTcABNHE")
bot = telebot.TeleBot(TOKEN)
loader = instaloader.Instaloader()

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Send me an Instagram Reel link!")

@bot.message_handler(func=lambda message: "instagram.com/reel" in message.text)
def download_reel(message):
    url = message.text
    try:
        shortcode = url.split("/reel/")[1].split("/")[0]
        loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target="reel")
        for file in os.listdir("reel"):
            if file.endswith(".mp4"):
                with open(f"reel/{file}", "rb") as video:
                    bot.send_video(message.chat.id, video)
                os.remove(f"reel/{file}")
        os.rmdir("reel")
    except Exception as e:
        bot.reply_to(message, f"Failed to download reel: {str(e)}")

bot.polling()
