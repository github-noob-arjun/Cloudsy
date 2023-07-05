#FayasNoushad
#ImJanindu
#Me

import os
import pixeldrain
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import requests
import sys
import time
import logging
import aiohttp
import asyncio
from random import randint

Cloudsy = Client(
    "Cloudsy-Bot",
    bot_token = "6075983195:AAGMNrva0scU_VFBzP-sve5_vI6qvdl6V24",
    api_id = 15681435,
    api_hash = "29021e7d8f6fe5338a45470115567f9e"
)

DOWNLOAD = "./"


def time_data(start_time):
    end = time.time()
    now = end - start_time
    now_time = now
    day = now_time // (24 * 3600)
    now_time = now_time % (24 * 3600)
    hour = now_time // 3600
    now_time %= 3600
    minutes = now_time // 60
    now_time %= 60
    seconds = now_time
    if(day!=0):
        return "%dd %dh %dm %ds" % (day, hour, minutes, seconds)
    if(hour!=0):
        return "%dh %dm %ds" % (hour, minutes, seconds)
    else:
        return "%dm %ds" % (minutes, seconds)


async def progress(current, total,up_msg, message, start_time):
    try:
        await message.edit(text = f"{up_msg} {current * 100 / total:.1f}% in {time_data(start_time)}")
    except:
        pass




@Cloudsy.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"Hello {update.from_user.mention}, 👋\n\nJust send me a media & I'll upload it to the cloud.\n\nMade with ❤️ by @Sybots",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📨 Updates", url="https://t.me/sybots"),
                 InlineKeyboardButton("🗂 Source", url="https://github.com/reindears/cloudsy")]
            ]
        )
    )

    
@Cloudsy.on_message(filters.private & filters.media)
async def medias(bot, update):
    await update.reply_text(
        "Choose a Cloud Server for Uploading",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("GoFile", callback_data="gofile"),
                 InlineKeyboardButton("Anonfiles", callback_data="anon"),
                 InlineKeyboardButton("Pixeldrain", callback_data="pixel")]
            ]
        ),
        quote=True
    )





@Cloudsy.on_callback_query(filters.regex(r"gofile"))
async def gomain(bot, msg):
    try:
        status = await msg.message.edit_text("Downloading...")
        now = time.time()
        sed = await bot.download_media(msg.message.reply_to_message, DOWNLOAD, progress=progress, progress_args=("ETA : ", status, now))
        files = {'file': open(sed, 'rb')}
        server = requests.get(url="https://api.gofile.io/getServer").json()["data"]["server"]
        await msg.message.edit_text("`uploading to Gofile.io...`")
        upload = requests.post(
            url=f"https://{server}.gofile.io/uploadFile",
            files=files
        ).json()
        link = upload["data"]["downloadPage"]
        await msg.message.edit_text(
            f"Here's the link: \n\n`{link}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Open Link", url=link),
                     InlineKeyboardButton("Share Link", url="https://t.me/share/url?url="+link)]
                ]
            )
        )
    except Exception as error:
        await msg.message.edit_text(
            text=f"Error :- `{error}`",
            disable_web_page_preview=True
        )
        return
        os.remove(file)


@Cloudsy.on_callback_query(filters.regex(r"anon"))
async def anonmain(bot, msg):
    try:
        status = await msg.message.edit_text("Downloading...")
        now = time.time()
        #file = await msg.download(progress=progress, progress_args=(status, "Downloading..."))
        sed = await bot.download_media(msg.message.reply_to_message, DOWNLOAD, progress=progress, progress_args=("ETA : ", status, now))
        files = {'file': open(sed, 'rb')}
        await msg.message.edit_text("`uploading to Anonfiles....`")
        upload = requests.post("https://api.anonfiles.com/upload", files=files)
        text = upload.json()
        Fname = text['data']['file']['metadata']['name']
        Flink = text['data']['file']['url']['full']
        Fsize = text['data']['file']['metadata']['size']['readable']
        await msg.message.edit_text(
            f"Upload Successfully ☑️\n\nFile : {Fname}\n\n💽 Size : {Fsize}\n\nHere's the link: `{Flink}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Open Link", url=Flink),
                     InlineKeyboardButton("Share Link", url="https://t.me/share/url?url="+Flink)]
                ]
            )
        )
    except Exception as error:
        await msg.message.edit_text(
            text=f"Error :- `{error}`",
            disable_web_page_preview=True
        )
        return
        os.remove(file)
        

@Cloudsy.on_callback_query(filters.regex(r"pixel"))
async def pixmain(bot, msg):
    try:
        status = await msg.message.edit_text("Downloading...")
        now = time.time()
        
        #Download
        sed = await bot.download_media(msg.message.reply_to_message, DOWNLOAD, progress=progress, progress_args=("ETA : ", status, now))
        files = {'file': open(sed, 'rb')}
        
        #upload
        await msg.message.edit_text("`uploading to pixeldrain....`")
        try:
            upload = requests.post(
                "https://pixeldrain.com/api/file",
                data={"anonymous": True}
            )
        except Exception as error:
            await msg.message.edit_text(text=f"Error :- `{error}`")    
            return upload.json()
    
        file_id = upload['id']
        try:
            data = requests.get(f"https://pixeldrain.com/api/file/{file_id}/info")
        except Exception as error:
            await msg.message.edit_text(text=f"Error :- `{error}`")
        Fname = data['name']
        Fsize = data['size']
        link = data['id']
        await msg.message.edit_text(
            f"Upload Successfully ☑️\n\nFile : {Fname}\n\n💽 Size : {Fsize}\n\nHere's the link: `https://pixeldrain.com/api/file/{link}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Open Link", url=f"https://pixeldrain.com/api/file/{link}"),
                     InlineKeyboardButton("Share Link", url="https://t.me/share/url?url="+f"https://pixeldrain.com/api/file/{link}")]
                ]
            )
        )
    except Exception as error:
        await msg.message.edit_text(
            text=f"Error :- `{error}`",
            disable_web_page_preview=True
        )
        return
        os.remove(file)
        
#@Cloudsy.on_callback_query(filters.regex(r"pixel"))
async def media_filghter(bot, data: CallbackQuery):
    
    logs = []
    now = time.time()
    await data.message.edit_text(
        text="Processing file"
    )
    
    try:
        # download
        try:
            message = await data.message.edit_text(
                text="Downloading file to server",
                disable_web_page_preview=True
            )
        except:
            pass
        sed = await bot.download_media(data.message.reply_to_message, DOWNLOAD, progress=progress, progress_args=("ETA : ", message, now))
        media = {'file': open(sed, 'rb')}
        logs.append("Download Successfully")
        
        # upload
        try:
            await message.edit_text(
                text="Uploading to Pixeldrain",
                disable_web_page_preview=True
            )
        except:
            pass
        response = pixeldrain.upload_file(media)
        
        try:
            os.remove(media)
        except:
            pass
        try:
            await message.edit_text(
                text="Uploaded Successfully",
                disable_web_page_preview=True
            )
        except:
            pass
        logs.append("Upload Successfully")
        
        # after upload
        if response["success"]:
            logs.append("Success is True")
            data = pixeldrain.info(response["id"])
        else:
            logs.append("Success is False")
            value = response["value"]
            error = response["message"]
            await message.edit_text(
                text=f"**Error {value}:-** `{error}`",
                disable_web_page_preview=True
            )
            return
    except Exception as error:
        await message.edit_text(
            text=f"Error :- `{error}`"+"\n\n"+'\n'.join(logs),
            disable_web_page_preview=True
        )
        return
    
    # pixeldrain data
    text = f"**File Name:** `{data['name']}`" + "\n"
    text += f"**Download Page:** `https://pixeldrain.com/u/{data['id']}`" + "\n"
    text += f"**Direct Download Link:** `https://pixeldrain.com/api/file/{data['id']}`" + "\n"
    text += f"**Upload Date:** `{data['date_upload']}`" + "\n"
    text += f"**Last View Date:** `{data['date_last_view']}`" + "\n"
    text += f"**Size:** `{data['size']}`" + "\n"
    text += f"**Total Views:** `{data['views']}`" + "\n"
    text += f"**Bandwidth Used:** `{data['bandwidth_used']}`" + "\n"
    text += f"**Mime Type:** `{data['mime_type']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Open Link",
                    url=f"https://pixeldrain.com/u/{data['id']}"
                ),
                InlineKeyboardButton(
                    text="Share Link",
                    url=f"https://telegram.me/share/url?url=https://pixeldrain.com/u/{data['id']}"
                )
            ]
        ]
    )
    
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Cloudsy.run()
