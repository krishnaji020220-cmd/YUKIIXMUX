# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual SUDEEPBOTS.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: sudeepgithub@gmail.com

import YUKIIMUSIC.yuki_guard
import asyncio
import importlib
import logging # Added for silencer
import os #  Added for auto-injector

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from YUKIIMUSIC import LOGGER, app, userbot
from YUKIIMUSIC.core.call import YUKII
from YUKIIMUSIC.misc import sudo
from YUKIIMUSIC.plugins import ALL_MODULES
from YUKIIMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

from YUKIIMUSIC.core.deploy import send_deploy_message

# ==========================================
#  ERROR SILENCER ENGINE 
# ==========================================
class SilenceAnnoyingError(logging.Filter):
    def filter(self, record):
        if record.exc_info and "'UpdateGroupCall' object has no attribute 'chat_id'" in str(record.exc_info[1]):
            return False 
        return True 

logging.getLogger("pyrogram.dispatcher").addFilter(SilenceAnnoyingError())
# ==========================================

# ==========================================
# AUTO-INJECTOR FOR TERMINAL SHORTCUTS 
# ==========================================
def setup_terminal_shortcuts():
    """Ye function clients ke VPS mein auto-shortcuts inject karega"""
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        yuki_script = os.path.join(base_dir, "yuki.py")
        bashrc_path = os.path.expanduser("~/.bashrc")
        
        alias_update = f"alias update='python3 {yuki_script} update'\n"
        alias_version = f"alias version='python3 {yuki_script} version'\n"
        
        if os.path.exists(bashrc_path):
            with open(bashrc_path, "r") as f:
                content = f.read()
                
            with open(bashrc_path, "a") as f:
                if "alias update=" not in content:
                    f.write(f"\n# YUKI Auto Updater Aliases\n{alias_update}")
                if "alias version=" not in content:
                    f.write(alias_version)
    except Exception as e:
        pass 
# ==========================================

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("YUKIIMUSIC.plugins" + all_module)
    LOGGER("YUKIIMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")
    await userbot.start()
    await YUKII.start()
    try:
        await YUKII.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("YUKIIMUSIC").error(
            "𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗦𝗧𝗥𝗔𝗡𝗚𝗘𝗥 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........"
        )
        exit()
    except:
        pass
    await YUKII.decorators()
    LOGGER("YUKIIMUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝐒 𝛖 𝐝 ֟፝ᥱ 𝛆 𝛒 </𝟑\n╚═════ஜ۩۞۩ஜ════╝"
    )
    
    asyncio.create_task(send_deploy_message())
    
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("YUKIIMUSIC").info("𝗦𝗧𝗢𝗣 𝐒 𝛖 𝐝 ֟፝ᥱ 𝛆 𝛒 </𝟑 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")


if __name__ == "__main__":
    setup_terminal_shortcuts() # 🔥 Bot start hote hi sabse pehle shortcuts banayega
    asyncio.get_event_loop().run_until_complete(init())
        
