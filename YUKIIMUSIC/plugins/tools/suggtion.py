import asyncio
from pyrogram import filters
from pyrogram.types import Message, ChatMemberUpdated

# YUKIIMUSIC bot instance
from YUKIIMUSIC import app 

# ─────────────────────────────
# IN-MEMORY DATABASE
# ─────────────────────────────
# Note: This is an in-memory dictionary. It will track changes as long as the bot is running. 
# If you want it to remember names even after bot restarts, you can link this to your MongoDB later.
USER_DATA = {}

# ─────────────────────────────
# AESTHETIC SMALL CAPS TEXT CONVERTER
# ─────────────────────────────
def smallcaps(text):
    chars = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 
        'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 
        'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 
        'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ғ', 'G': 'ɢ', 
        'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 
        'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ', 
        'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ'
    }
    return ''.join(chars.get(c, c) for c in str(text))

# ─────────────────────────────
# HELPER FUNCTION
# ─────────────────────────────
def get_full_name(user):
    if not user:
        return "Unknown"
    name = user.first_name or ""
    if user.last_name:
        name += f" {user.last_name}"
    return name.strip()

# ─────────────────────────────
# TRACKER LOGIC
# ─────────────────────────────
async def check_user_profile(client, chat_id, user):
    if not user or user.is_bot:
        return

    user_id = user.id
    current_name = get_full_name(user)
    current_username = f"@{user.username}" if user.username else "None"

    # If user is not in database, add them silently
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {
            "name": current_name,
            "username": current_username
        }
        return

    old_info = USER_DATA[user_id]
    old_name = old_info["name"]
    old_username = old_info["username"]

    changes = []
    
    # Check if Name changed
    if old_name != current_name:
        changes.append(f"{smallcaps('name from')} **{old_name}** {smallcaps('to')} **{current_name}**")
    
    # Check if Username changed
    if old_username != current_username:
        changes.append(f"{smallcaps('username from')} **{old_username}** {smallcaps('to')} **{current_username}**")

    # If any changes found, alert the group and update database
    if changes:
        USER_DATA[user_id] = {
            "name": current_name,
            "username": current_username
        }
        
        alert_text = f"👀 **{smallcaps('Profile Update Detected')}** 👀\n\n{user.mention} {smallcaps('has changed their')} " + f" {smallcaps('and')} ".join(changes) + "!"
        
        try:
            await client.send_message(chat_id, alert_text)
        except Exception:
            pass # Ignore if bot lacks permissions to send message

# ─────────────────────────────
# EVENT HANDLERS
# ─────────────────────────────

# 1. Listen to all normal messages in the group
# group=10 ensures this runs in the background without blocking other commands like /play
@app.on_message(filters.group & ~filters.bot, group=10)
async def on_user_message(client, message: Message):
    if message.from_user:
        await check_user_profile(client, message.chat.id, message.from_user)

# 2. Listen to Chat Member Updates (When someone joins, gets promoted, etc.)
@app.on_chat_member_updated(filters.group, group=11)
async def on_user_join_or_update(client, update: ChatMemberUpdated):
    # Check the new_chat_member object to see their current profile
    if update.new_chat_member and update.new_chat_member.user:
        await check_user_profile(client, update.chat.id, update.new_chat_member.user)

