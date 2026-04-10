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
from pyrogram import filters
from YUKIIMUSIC import app
from YUKIIMUSIC.misc import SUDOERS

@app.on_message(filters.video & filters.private & SUDOERS)
async def get_video_id(client, message):
    # Jaise hi tu video bhejega, bot uski file_id reply kar dega
    file_id = message.video.file_id
    await message.reply_text(f"**Yᴇ ʀᴀʜɪ Tᴇʀɪ Fɪʟᴇ ID:**\n\n`{file_id}`")
    
