import os
import json
import aiohttp
import base64
import random
import asyncio
import re
from PIL import Image
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

from SHUKLAMUSIC import app
from config import BANNED_USERS, NSFWAPI

# ─────────────────────────────
# 🔥 NSFW STATE, EMOJIS & DATABASE
# ─────────────────────────────
chat_nsfw_state = {}
BANNED_STICKERS = set() # Single stickers
BANNED_PACKS = set()    # Pura pack block karne ke liye

PREMIUM_EMOJIS = [
    '🎀', '✨', '❌', '⚠️', '🛡️', '🤖', '💀', '👀'
]

# ─────────────────────────────
# 🛠️ MANUAL BAN COMMAND
# ─────────────────────────────
@app.on_message(filters.command("bansticker") & filters.reply & filters.group)
async def ban_manual_sticker(client, message: Message):
    if not message.reply_to_message.sticker:
        return await message.reply("<blockquote>⚠️ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ ʙᴀɴ ɪᴛ!</blockquote>", parse_mode=ParseMode.HTML)
    
    sticker = message.reply_to_message.sticker
    sticker_id = sticker.file_unique_id
    pack_name = sticker.set_name
    
    # Check command structure like /bansticker pack
    if len(message.command) > 1 and message.command[1].lower() == "pack" and pack_name:
        BANNED_PACKS.add(pack_name)
        text = f"<blockquote>✅ ғᴜʟʟ sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ʙʟᴀᴄᴋʟɪsᴛ! {random.choice(PREMIUM_EMOJIS)}</blockquote>"
    else:
        BANNED_STICKERS.add(sticker_id)
        text = f"<blockquote>✅ sɪɴɢʟᴇ sᴛɪᴄᴋᴇʀ ᴀᴅᴅᴇᴅ ᴛᴏ ʙʟᴀᴄᴋʟɪsᴛ! {random.choice(PREMIUM_EMOJIS)}</blockquote>"
    
    try:
        await message.reply_to_message.delete()
    except: pass
    
    msg = await message.reply(text, parse_mode=ParseMode.HTML)
    await asyncio.sleep(15)
    try:
        await msg.delete()
    except: pass

# ─────────────────────────────
# 🛠️ ON/OFF COMMAND
# ─────────────────────────────
@app.on_message(filters.command(["nsfw", "vision"]) & filters.group & ~BANNED_USERS)
async def toggle_nsfw(client, message: Message):
    chat_id = message.chat.id
    emo = random.choice(PREMIUM_EMOJIS)
    
    if len(message.command) < 2:
        state = chat_nsfw_state.get(chat_id, True)
        status = "ᴏɴ ✅" if state else "ᴏғғ ❌"
        msg_text = f"<blockquote>ᴠɪsɪᴏɴ sᴄᴀɴɴᴇʀ ɪs ᴄᴜʀʀᴇɴᴛʟʏ **{status}**.\nᴛᴏ ᴄʜᴀɴɢᴇ, ᴛʏᴘᴇ: `/nsfw on` ᴏʀ `/nsfw off` {emo}</blockquote>"
        return await message.reply(msg_text, parse_mode=ParseMode.HTML)
    
    cmd = message.command[1].lower()
    if cmd == "on":
        chat_nsfw_state[chat_id] = True
        msg_text = f"<blockquote>✅ ᴠɪsɪᴏɴ sᴄᴀɴɴᴇʀ ɪs ɴᴏᴡ ᴏɴ. {emo}</blockquote>"
    elif cmd == "off":
        chat_nsfw_state[chat_id] = False
        msg_text = f"<blockquote>❌ ᴠɪsɪᴏɴ sᴄᴀɴɴᴇʀ ɪs ɴᴏᴡ ᴏғғ. {emo}</blockquote>"
        
    msg = await message.reply(msg_text, parse_mode=ParseMode.HTML)
    await asyncio.sleep(15)
    try:
        await msg.delete()
    except: pass

# ─────────────────────────────
# 👁️ GROQ VISION ENGINE (Percentage Hack)
# ─────────────────────────────
async def analyze_media_groq(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        jpg_path = image_path + ".jpg"
        img.save(jpg_path, "JPEG")
        
        with open(jpg_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
            
        headers = {
            "Authorization": f"Bearer {NSFWAPI}",
            "Content-Type": "application/json"
        }
        
        # 🔥 The Percentage Prompt Hack
        prompt = "Analyze this image for NSFW, nudity, or adult suggestive content. Reply ONLY with a valid JSON format: {\"nsfw_percentage\": X} where X is a number from 0 to 100 representing the probability of it being NSFW. Do not output any other text."
        
        payload = {
            "model": "llama-3.2-11b-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 20
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=20) as resp:
                data = await resp.json()
                os.remove(jpg_path)
                
                if "choices" in data:
                    text = data["choices"][0]["message"]["content"].strip()
                    # JSON Extract hack (in case LLM adds backticks)
                    match = re.search(r'\{.*\}', text, re.DOTALL)
                    if match:
                        res_dict = json.loads(match.group())
                        return int(res_dict.get("nsfw_percentage", 0))
                    return 0 # Default safe if parsing fails
                elif "error" in data:
                    # Agar Groq safety policy ki wajah se error fenke (highly explicit)
                    if "safety" in str(data).lower():
                        return 100 
                return -1
                    
    except Exception as e:
        print(f"Groq Vision Crash: {e}")
        return -1

# ─────────────────────────────
# 🧪 TEST STICKER COMMAND
# ─────────────────────────────
@app.on_message(filters.command("teststic") & filters.reply)
async def test_sticker(client, message: Message):
    if not message.reply_to_message.sticker and not message.reply_to_message.photo:
        return await message.reply("<blockquote>⚠️ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴏʀ ᴘʜᴏᴛᴏ ᴛᴏ ᴛᴇsᴛ!</blockquote>", parse_mode=ParseMode.HTML)
    
    wait_msg = await message.reply("<blockquote>⏳ sᴄᴀɴɴɪɴɢ ɪᴍᴀɢᴇ ᴠɪᴀ ɢʀᴏǫ ᴠɪsɪᴏɴ...</blockquote>", parse_mode=ParseMode.HTML)
    
    dl_path = None
    target_msg = message.reply_to_message
    
    try:
        if target_msg.sticker and (target_msg.sticker.is_animated or target_msg.sticker.is_video):
            if target_msg.sticker.thumbs:
                thumb_id = target_msg.sticker.thumbs[0].file_id
                dl_path = await client.download_media(thumb_id)
        else:
            dl_path = await target_msg.download()
            
        if not dl_path:
            return await wait_msg.edit("<blockquote>❌ FAILED TO DOWNLOAD MEDIA.</blockquote>", parse_mode=ParseMode.HTML)

        score = await analyze_media_groq(dl_path)
        
        if os.path.exists(dl_path):
            os.remove(dl_path)
            
        if score == -1:
            return await wait_msg.edit("<blockquote>❌ API ERROR OR CRASH.</blockquote>", parse_mode=ParseMode.HTML)
            
        action = "🟢 SAFE (Ignored)"
        if score >= 80:
            action = "🔴 HIGH NSFW (Banning Full Pack)"
        elif score >= 50:
            action = "🟠 MED NSFW (Banning Single Sticker)"
            
        result_text = f"<blockquote>👁️ **ᴠɪsɪᴏɴ ᴛᴇsᴛ ʀᴇsᴜʟᴛs:**\n\n📊 **sᴄᴏʀᴇ:** {score}%\n🎯 **ᴀᴄᴛɪᴏɴ:** {action}</blockquote>"
        await wait_msg.edit(result_text, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        await wait_msg.edit(f"<blockquote>❌ Error: {e}</blockquote>", parse_mode=ParseMode.HTML)

# ─────────────────────────────
# 🚨 MAIN SCANNER (SILENT & SMART PACK BAN)
# ─────────────────────────────
@app.on_message((filters.photo | filters.sticker) & filters.group & ~BANNED_USERS)
async def nsfw_scanner(client, message: Message):
    chat_id = message.chat.id
    if not chat_nsfw_state.get(chat_id, True):
        return

    # 1. SMART DATABASE CHECK (Fastest)
    if message.sticker:
        sticker_id = message.sticker.file_unique_id
        pack_name = message.sticker.set_name
        
        if sticker_id in BANNED_STICKERS or (pack_name and pack_name in BANNED_PACKS):
            try:
                await message.delete()
            except Exception: pass
            return

    # 2. DOWNLOAD & SCAN
    dl_path = None
    try:
        if message.sticker and (message.sticker.is_animated or message.sticker.is_video):
            if message.sticker.thumbs:
                dl_path = await client.download_media(message.sticker.thumbs[0].file_id)
            else:
                return 
        else:
            dl_path = await message.download()
        
        if dl_path:
            score = await analyze_media_groq(dl_path)
            
            if os.path.exists(dl_path):
                os.remove(dl_path)
                
            # Logic: >= 80% (Ban Pack), >= 50% (Ban Sticker)
            if score >= 50:
                if message.sticker:
                    if score >= 80 and message.sticker.set_name:
                        BANNED_PACKS.add(message.sticker.set_name)
                    else:
                        BANNED_STICKERS.add(message.sticker.file_unique_id)
                        
                try:
                    await message.delete()
                except Exception as e:
                    if "MESSAGE_DELETE_FORBIDDEN" in str(e) or "chat_admin_required" in str(e).lower():
                         perm_msg = await client.send_message(chat_id, f"<blockquote>⚠️ ɪ ɴᴇᴇᴅ 'ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs' ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʀᴇᴍᴏᴠᴇ ɴsғᴡ ᴄᴏɴᴛᴇɴᴛ! 🛡️</blockquote>", parse_mode=ParseMode.HTML)
                         await asyncio.sleep(10)
                         try: await perm_msg.delete()
                         except: pass
                         
    except Exception as e:
        print(f"Scanner crash: {e}")
        if dl_path and os.path.exists(dl_path):
            os.remove(dl_path)
            
