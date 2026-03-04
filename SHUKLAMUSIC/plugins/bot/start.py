import traceback # Upar imports mein daal lena agar nahi hai

# 🔥 HELLFIRE LIVE ERROR TRACKER INJECTION
async def inject_premium_markup(chat_id, message_id, markup):
    try:
        # Token fallback (kabhi-kabhi app.bot_token None ho jata hai Pyrogram mein)
        token = getattr(config, "BOT_TOKEN", getattr(app, "bot_token", None))
        url = f"https://api.telegram.org/bot{token}/editMessageReplyMarkup"
        
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": {"inline_keyboard": markup}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                response_data = await resp.json()
                
                # Agar API ne reject kiya, toh sidha chat mein message aayega!
                if not response_data.get("ok"):
                    err = response_data.get("description", "Unknown API Error")
                    print(f"❌ API REJECTED: {err}")
                    await app.send_message(
                        chat_id, 
                        f"⚠️ **Telegram API Ne Buttons Reject Maar Diye!**\n\n**Reason:** `{err}`\n\n*(Check kar, shayad API inline buttons mein custom emojis ya style allow nahi kar rahi)*"
                    )
                else:
                    print("✅ Premium Buttons Injected Successfully!")
                    
    except Exception as e:
        print(f"❌ CODE CRASH: {e}")
        await app.send_message(chat_id, f"⚠️ **Code Crash Ho Gaya Bypass Mein:**\n`{e}`")
        
