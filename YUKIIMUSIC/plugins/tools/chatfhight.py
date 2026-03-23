import time
import asyncio
import os
import random
import aiohttp
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message

import config
from YUKIIMUSIC import app
from YUKIIMUSIC.misc import mongodb

# 🔥 MONGODB COLLECTION FOR LEADERBOARD 🔥
game_db = mongodb["wordgame_leaderboard"]

# --- GLOBAL TRACKERS ---
last_message_time = {}
active_games = {}
user_cooldowns = {} # Dictionaries to store cooldown times for incorrect guesses
INACTIVITY_LIMIT = 300  # 5 minutes in seconds
PENALTY_TIME = 60 # 1 minute wait time for wrong guess

# --- FILE PATHS ---
TEMPLATE_PATH = "YUKIIMUSIC/assets/template.jpg"
FONT_PATH = "YUKIIMUSIC/assets/arial.ttf"

# --- RANDOM WARNING MESSAGES ---
WARNING_MESSAGES = [
    "<emoji id='6334789677396002338'>⏱</emoji> Time passes. Tick tock, tick tock...",
    "⚠️ Alarm: time is running out!!",
    "🥱 It's too quiet here... let's play a game!",
    "👀 Anyone there? Get ready to type..."
]

# --- EMOJI & COUNTRY LISTS ---
EMOJIS = ["🍏","🍎","🍐","🍊","🍋","🍌","🍉","🍇","🍓","🫐","🍈","🍒","🍑","🥭","🍍","🥥","🥝","🍅","🍆","🥑","🥦","🥬","🥒","🌶","🌽","🥕","🥔","🍠","🥐","🥯","🍞","🥖","🥨","🧀","🥚","🍳","🧈","🥞","🧇","🥓","🥩","🍗","🍖","🌭","🍔","🍟","🍕","🥪","🥙","🌮","🌯","🥗","🥘","🥫","🍝","🍜","🍲","🍛","🍣","🍱","🥟","🍤","🍙","🍚","🍘","🍥","🥮","🍢","🍡","🍧","🍨","🍦","🥧","🧁","🍰","🎂","🍮","🍭","🍬","🍫","🍿","🍩","🍪","🍯","🥛","🍼","☕","🍵","🧃","🥤","🍺","🍻","🥂","🍷","🥃","🍸","🍹","🧉","🍾","🧊"]

COUNTRIES = [
    {"name": "India", "code": "in"}, {"name": "USA", "code": "us"}, {"name": "Japan", "code": "jp"}, 
    {"name": "Brazil", "code": "br"}, {"name": "Canada", "code": "ca"}, {"name": "UK", "code": "gb"},
    {"name": "France", "code": "fr"}, {"name": "Germany", "code": "de"}, {"name": "Italy", "code": "it"},
    {"name": "Russia", "code": "ru"}, {"name": "China", "code": "cn"}, {"name": "Australia", "code": "au"},
    {"name": "Spain", "code": "es"}, {"name": "Mexico", "code": "mx"}, {"name": "South Korea", "code": "kr"},
    {"name": "Argentina", "code": "ar"}, {"name": "Egypt", "code": "eg"}, {"name": "South Africa", "code": "za"},
    {"name": "Turkey", "code": "tr"}, {"name": "Saudi Arabia", "code": "sa"}, {"name": "Pakistan", "code": "pk"},
    {"name": "Indonesia", "code": "id"}, {"name": "Nigeria", "code": "ng"}, {"name": "Kenya", "code": "ke"}
]

# --- PREMIUM HACK INJECTION ---
async def inject_premium_markup(chat_id, message_id, markup):
    try:
        token = getattr(config, "BOT_TOKEN", getattr(app, "bot_token", None))
        url = f"https://api.telegram.org/bot{token}/editMessageReplyMarkup"
        payload = {"chat_id": chat_id, "message_id": message_id, "reply_markup": {"inline_keyboard": markup}}
        async with aiohttp.ClientSession() as session:
            await session.post(url, json=payload)
    except Exception as e:
        print(f"❌ Markup Injection Error: {e}")

# ==========================================
#              IMAGE GENERATION LOGIC
# ==========================================

def create_game_image(text, is_emoji=False):
    output_path = f"game_{random.randint(1000,9999)}.jpg"
    
    if not os.path.exists(TEMPLATE_PATH):
        os.makedirs(os.path.dirname(TEMPLATE_PATH), exist_ok=True)
        img = Image.new('RGB', (800, 400), color=(15, 15, 15))
        img.save(TEMPLATE_PATH)

    bg = Image.open(TEMPLATE_PATH).convert("RGBA")
    
    if not is_emoji:
        draw = ImageDraw.Draw(bg)
        try: font = ImageFont.truetype(FONT_PATH, 65)
        except: font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (bg.size[0] - text_w) / 2, ((bg.size[1] - text_h) / 2) - 10
        draw.text((x, y), text, fill="white", font=font)
        bg = bg.convert("RGB")
        bg.save(output_path)
        return output_path

async def create_emoji_or_flag_image(identifier, is_flag=False):
    output_path = f"game_{random.randint(1000,9999)}.jpg"
    
    if is_flag:
        url = f"https://flagcdn.com/256x192/{identifier}.png"
    else:
        hex_code = "-".join(f"{ord(c):x}" for c in identifier).replace("-fe0f", "")
        url = f"https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/72x72/{hex_code}.png"
    
    bg = Image.open(TEMPLATE_PATH).convert("RGBA")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    img_bytes = await resp.read()
                    temp_name = f"temp_{random.randint(100,999)}.png"
                    with open(temp_name, "wb") as f: f.write(img_bytes)
                    img_layer = Image.open(temp_name).convert("RGBA")
                    
                    if not is_flag:
                        img_layer = img_layer.resize((160, 160), Image.Resampling.LANCZOS)
                        
                    bg.paste(img_layer, ((bg.size[0]-img_layer.size[0])//2, (bg.size[1]-img_layer.size[1])//2), img_layer)
                    os.remove(temp_name)
    except Exception:
        pass 
        
    bg = bg.convert("RGB")
    bg.save(output_path)
    return output_path

# ==========================================
#              WORD GAME LOGIC
# ==========================================

async def get_random_word():
    fallback_words = ["BACTERIAL", "GAMUT", "PANDEMIC", "AESTHETIC", "RESONATE", "ILLUSION", "HELLFIRE", "DEVELOPER", "YUKII", "MUSIC"]
    if not hasattr(config, "GROQ_API_KEY") or not config.GROQ_API_KEY:
        return random.choice(fallback_words)
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {config.GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [{"role": "user", "content": "Reply with only ONE random difficult English word. Do not add punctuation or explanation. Just the word."}],
            "temperature": 0.9
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                data = await resp.json()
                word = data['choices'][0]['message']['content'].strip().upper()
                word = ''.join(e for e in word if e.isalnum())
                return word if word else random.choice(fallback_words)
    except Exception:
        return random.choice(fallback_words)

def hide_letters(word):
    # Hide roughly half of the letters randomly
    num_to_hide = max(1, len(word) // 2)
    indices_to_hide = random.sample(range(len(word)), num_to_hide)
    hidden_word = list(word)
    for i in indices_to_hide:
        hidden_word[i] = "_"
    return "".join(hidden_word)

async def start_word_game(chat_id):
    try:
        original_word = await get_random_word()
        
        # 50% chance for missing letters
        is_missing = random.choice([True, False])
        display_word = hide_letters(original_word) if is_missing else original_word
        
        img_path = create_game_image(display_word)
        caption = "<emoji id='6334696528145286813'>⚡</emoji> **Be the first to write the word shown in the photo to climb the mini-game leaderboard.**\n\n<emoji id='6334789677396002338'>⏱</emoji> **Time remaining:** 10 minutes"
        
        sent_msg = await app.send_photo(chat_id, photo=img_path, caption=caption, has_spoiler=True)
        if os.path.exists(img_path): os.remove(img_path) 
        
        active_games[chat_id] = {"type": "word", "answer": original_word, "start_time": time.time(), "message_id": sent_msg.id}
        
        # Inject Give Up button only if it's a missing letters game
        if is_missing:
            markup = [[{"text": "🏳️ Give Up", "callback_data": f"giveup_{chat_id}", "style": "danger"}]]
            await inject_premium_markup(chat_id, sent_msg.id, markup)
            
    except Exception: pass

# ==========================================
#              EMOJI GAME LOGIC
# ==========================================

async def start_emoji_game(chat_id):
    try:
        correct_emoji = random.choice(EMOJIS)
        options = random.sample([e for e in EMOJIS if e != correct_emoji], 11)
        options.append(correct_emoji)
        random.shuffle(options)

        img_path = await create_emoji_or_flag_image(correct_emoji, is_flag=False)
        caption = "👇 **Identify the emoji written in the photo and select it here to move up the minigame rankings!**\n\n<emoji id='6334789677396002338'>⏱</emoji> **Time remaining:** 10 minutes"
        
        sent_msg = await app.send_photo(chat_id, photo=img_path, caption=caption, has_spoiler=True)
        if os.path.exists(img_path): os.remove(img_path)

        markup = []
        row = []
        for em in options:
            row.append({"text": em, "callback_data": f"emg_{chat_id}_{em}", "style": "primary"})
            if len(row) == 3:
                markup.append(row)
                row = []
        if row: markup.append(row)

        await inject_premium_markup(chat_id, sent_msg.id, markup)
        active_games[chat_id] = {"type": "emoji", "answer": correct_emoji, "start_time": time.time(), "message_id": sent_msg.id}
    except Exception as e:
        print(f"Emoji game error: {e}")

# ==========================================
#              FLAG GAME LOGIC
# ==========================================

async def start_flag_game(chat_id):
    try:
        correct_country = random.choice(COUNTRIES)
        options_pool = [c for c in COUNTRIES if c['code'] != correct_country['code']]
        options = random.sample(options_pool, min(11, len(options_pool)))
        options.append(correct_country)
        random.shuffle(options)

        img_path = await create_emoji_or_flag_image(correct_country['code'], is_flag=True)
        caption = "🌍 **Guess the country from its flag and select the correct option below!**\n\n<emoji id='6334789677396002338'>⏱</emoji> **Time remaining:** 10 minutes"
        
        sent_msg = await app.send_photo(chat_id, photo=img_path, caption=caption, has_spoiler=True)
        if os.path.exists(img_path): os.remove(img_path)

        markup = []
        row = []
        for c in options:
            row.append({"text": c['name'], "callback_data": f"flg_{chat_id}_{c['code']}", "style": "primary"})
            if len(row) == 2: # 2 buttons per row for country names as they are longer
                markup.append(row)
                row = []
        if row: markup.append(row)

        await inject_premium_markup(chat_id, sent_msg.id, markup)
        active_games[chat_id] = {"type": "flag", "answer": correct_country['code'], "name": correct_country['name'], "start_time": time.time(), "message_id": sent_msg.id}
    except Exception as e:
        print(f"Flag game error: {e}")

# ==========================================
#              CALLBACK HANDLERS
# ==========================================

async def check_cooldown(user_id, callback_query):
    # Returns True if user is still in cooldown
    if user_id in user_cooldowns:
        time_passed = time.time() - user_cooldowns[user_id]
        if time_passed < PENALTY_TIME:
            wait_time = int(PENALTY_TIME - time_passed)
            await callback_query.answer(f"⏳ Penalty active! Wait {wait_time} more seconds before guessing again.", show_alert=True)
            return True
    return False

@app.on_callback_query(filters.regex(r"^(emg|flg)_"))
async def guess_game_callback(client, callback_query):
    user = callback_query.from_user
    
    # Check Cooldown
    if await check_cooldown(user.id, callback_query):
        return

    data = callback_query.data.split("_")
    game_type = data[0] # emg or flg
    chat_id = int(data[1])
    selected_option = data[2]
    
    if chat_id not in active_games:
        return await callback_query.answer("Game ended or expired!", show_alert=True)
        
    game_data = active_games[chat_id]
    
    # Prevent crossing games
    if (game_type == "emg" and game_data.get("type") != "emoji") or (game_type == "flg" and game_data.get("type") != "flag"):
         return await callback_query.answer("Invalid game interaction!", show_alert=True)
         
    correct_answer = game_data["answer"]
    
    if selected_option == correct_answer:
        time_taken = round(time.time() - game_data["start_time"], 1)
        
        # Display Info based on game type
        if game_type == "emg":
            points_won = 3
            success_text = f"{correct_answer} **The emoji was guessed by {user.mention} in {time_taken} seconds!**\n*+{points_won} points*"
        else:
            points_won = 5
            success_text = f"🌍 **{game_data['name']} was guessed correctly by {user.mention} in {time_taken} seconds!**\n*+{points_won} points*"

        del active_games[chat_id] 
        
        # Update Points
        user_data = await game_db.find_one({"user_id": user.id})
        if user_data:
            await game_db.update_one({"user_id": user.id}, {"$set": {"points": user_data["points"] + points_won, "name": user.first_name}})
        else:
            await game_db.insert_one({"user_id": user.id, "name": user.first_name, "points": points_won})
            
        await callback_query.message.delete()
        
        # Prepare "Start in DM" Button if needed
        markup = [[{"text": "🤖 Start Bot in DM to Claim Profile!", "url": f"https://t.me/{app.username}?start=claim", "style": "success"}]]
        
        run = await client.send_message(chat_id, success_text)
        await inject_premium_markup(chat_id, run.id, markup) # Always show button, if they already started it just opens bot
        
    else:
        # Wrong Guess -> Penalty
        user_cooldowns[user.id] = time.time()
        await callback_query.answer("❌ Wrong answer! You have a 1-minute penalty.", show_alert=True)

@app.on_callback_query(filters.regex(r"^giveup_"))
async def giveup_callback(client, callback_query):
    data = callback_query.data.split("_")
    chat_id = int(data[1])
    
    if chat_id not in active_games or active_games[chat_id].get("type") != "word":
        return await callback_query.answer("Game already ended!", show_alert=True)
        
    game_data = active_games[chat_id]
    correct_word = game_data["answer"]
    
    del active_games[chat_id]
    await callback_query.message.delete()
    
    await client.send_message(
        chat_id, 
        f"🏳️ **Game Over!** {callback_query.from_user.mention} gave up.\n\nThe correct word was: **{correct_word}**"
    )

# ==========================================
#              COMMANDS & TRACKERS
# ==========================================

@app.on_message(filters.command("testword") & filters.group)
async def test_word_cmd(client, message: Message):
    if message.from_user: await start_word_game(message.chat.id)

@app.on_message(filters.command("testemoji") & filters.group)
async def test_emoji_cmd(client, message: Message):
    if message.from_user: await start_emoji_game(message.chat.id)
    
@app.on_message(filters.command("testflag") & filters.group)
async def test_flag_cmd(client, message: Message):
    if message.from_user: await start_flag_game(message.chat.id)

@app.on_message(filters.group & ~filters.bot, group=10)
async def chat_activity_tracker(client, message: Message):
    chat_id = message.chat.id
    if not message.from_user: return
    user_id = message.from_user.id
    last_message_time[chat_id] = time.time()
    
    # Text checking for WORD GAME only
    if chat_id in active_games and active_games[chat_id].get("type") == "word" and message.text:
        correct_word = active_games[chat_id]["answer"]
        if message.text.strip().upper() == correct_word:
            time_taken = round(time.time() - active_games[chat_id]["start_time"], 1)
            del active_games[chat_id] 
            
            try: await client.send_reaction(chat_id=chat_id, message_id=message.id, emoji="❤️")
            except: pass
                
            user_data = await game_db.find_one({"user_id": user_id})
            if user_data:
                await game_db.update_one({"user_id": user_id}, {"$set": {"points": user_data["points"] + 15, "name": message.from_user.first_name}})
            else:
                await game_db.insert_one({"user_id": user_id, "name": message.from_user.first_name, "points": 15})
            
            msg = (f"<emoji id='6334696528145286813'>⚡</emoji> **How fast!** ({time_taken} seconds)\n"
                   f"<emoji id='6334471179801200139'>🎉</emoji> {message.from_user.mention} guessed the word in record time!\n"
                   f"Correct Word: **{correct_word}**\n*+15 in the global game ranking*")
                   
            run = await message.reply_text(msg)
            
            # Prepare "Start in DM" Button
            markup = [[{"text": "🤖 Start Bot in DM to Claim Profile!", "url": f"https://t.me/{app.username}?start=claim", "style": "success"}]]
            await inject_premium_markup(chat_id, run.id, markup)

@app.on_message(filters.command(["wordleaderboard", "gametop"]) & filters.group)
async def word_leaderboard(client, message: Message):
    top_users = game_db.find().sort("points", -1).limit(10)
    text = "<emoji id='6334381440754517833'>🏆</emoji> **Mini-Game Global Leaderboard** <emoji id='6334381440754517833'>🏆</emoji>\n\n"
    count, has_users = 1, False
    async for user in top_users:
        has_users = True
        text += f"**{count}.** {user.get('name', 'Unknown User')} - `{user['points']}` points\n"
        count += 1
    if not has_users: text += "No one has scored points yet! Wait for a game to start."
    await message.reply_text(text)

async def inactivity_checker_loop():
    while True:
        await asyncio.sleep(60) 
        current_time = time.time()
        
        # 1. Check for expired games
        for chat_id, game_data in list(active_games.items()):
            if (current_time - game_data["start_time"]) > 600:
                try: await app.delete_messages(chat_id, game_data["message_id"])
                except: pass
                del active_games[chat_id]
                if chat_id in last_message_time: del last_message_time[chat_id]

        # 2. Check for inactivity to start a new game randomly
        for chat_id, last_time in list(last_message_time.items()):
            if (current_time - last_time) > INACTIVITY_LIMIT and chat_id not in active_games:
                try:
                    warning = await app.send_message(chat_id, random.choice(WARNING_MESSAGES))
                    await asyncio.sleep(3)
                    await warning.delete()
                    
                    # 33% chance for each game
                    game_choice = random.choice(["word", "emoji", "flag"])
                    if game_choice == "word":
                        await start_word_game(chat_id)
                    elif game_choice == "emoji":
                        await start_emoji_game(chat_id)
                    else:
                        await start_flag_game(chat_id)
                except Exception: pass

asyncio.create_task(inactivity_checker_loop())
