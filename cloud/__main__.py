from pyrogram import Client
import os


TOKEN = "6075983195:AAGMNrva0scU_VFBzP-sve5_vI6qvdl6V24"
APP_ID = 15681435
API_HASH = "29021e7d8f6fe5338a45470115567f9e"

if __name__ == "__main__" :
    plugins = dict(
        root="cloud"
    )
    app = Client(
        "Cloudsy",
        bot_token=TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run() 
