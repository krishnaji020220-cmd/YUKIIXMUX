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
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    MBUTTON = [[InlineKeyboardButton(" ᴄʜᴀᴛ-ɢᴘᴛ ", callback_data="mplus HELP_ChatGPT"),InlineKeyboardButton(" ɢʀᴏᴜᴘs ", callback_data="mplus HELP_Group"),InlineKeyboardButton("sᴛɪᴄᴋᴇʀs", callback_data="mplus HELP_Sticker")],
    [InlineKeyboardButton("ᴛᴀɢ-ᴀʟʟ ", callback_data="mplus HELP_TagAll"),
    InlineKeyboardButton(" ɪɴꜰᴏ ", callback_data="mplus HELP_Info"),InlineKeyboardButton(" ᴇxᴛʀᴀ ", callback_data="mplus HELP_Extra")],
    [InlineKeyboardButton(" ɪᴍᴀɢᴇ ", callback_data="mplus HELP_Image"),
    InlineKeyboardButton(" ᴀᴄᴛɪᴏɴ ", callback_data="mplus HELP_Action"),InlineKeyboardButton(" sᴇᴀʀᴄʜ ", callback_data="mplus HELP_Search")],    
    [InlineKeyboardButton(" ғᴏɴᴛ ", callback_data="mplus HELP_Font"),
    InlineKeyboardButton("ɢᴀᴍᴇs ", callback_data="mplus HELP_Game"),InlineKeyboardButton(" ᴛ-ɢʀᴀᴘʜ ", callback_data="mplus HELP_TG")],
    [InlineKeyboardButton(" ɪᴍᴘᴏsᴛᴇʀ ", callback_data="mplus HELP_Imposter"),
    InlineKeyboardButton(" ᴛʀᴜᴛʜ-ᴅᴀʀᴇ ", callback_data="mplus HELP_TD"),InlineKeyboardButton(" ʜᴀsᴛᴀɢ ", callback_data="mplus HELP_HT")], 
    [InlineKeyboardButton(" ᴛᴛs ", callback_data="mplus HELP_TTS"),
    InlineKeyboardButton(" ғᴜɴ ", callback_data="mplus HELP_Fun"),InlineKeyboardButton(" ǫᴜᴏᴛʟʏ ", callback_data="mplus HELP_Q")],          
    [InlineKeyboardButton("<🔘", callback_data=f"settings_back_helper"), 
    InlineKeyboardButton("🔘>", callback_data=f"managebot123 settings_back_helper"),
    ]]
