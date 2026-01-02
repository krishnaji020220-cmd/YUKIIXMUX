from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app, YouTube
from SHUKLAMUSIC.utils.stream.stream import stream
from config import BANNED_USERS

# ✅ Hindi + Pop song URLs for autoplay
TRENDING_SONGS = [
    "https://www.youtube.com/watch?v=dvYMyqO2PZg",
    "https://www.youtube.com/watch?v=pbxgHqPizRg",
    "https://www.youtube.com/watch?v=ZKzuh0AQSBI",
    "https://www.youtube.com/watch?v=KJhL7U95Ug8",
    "https://www.youtube.com/watch?v=WoBFeCRfV20",
    "https://www.youtube.com/watch?v=ghzMGkZC4nY",
    "https://www.youtube.com/watch?v=j5uXpKoP_xk",
    "https://www.youtube.com/watch?v=nfs8NYg7yQM",
    "https://www.youtube.com/watch?v=az4R5G5v1bA",
    "https://www.youtube.com/watch?v=GzU8KqOY8YA",
]

# ✅ FIXED COMMAND DECORATOR
@app.on_message(
    filters.command(
        ["autoplay", "autoqueue"],
        prefixes=["/", "!", "."]
    )
    & filters.group
    & ~BANNED_USERS
)
async def autoplay_handler(client, message: Message):
    chat_id = message.chat.id
    user = message.from_user

    msg = await message.reply_text("🎵 Fetching selected songs for autoplay...")

    for url in TRENDING_SONGS:
        try:
            details, file = await YouTube.track(url)
        except Exception as e:
            await msg.edit_text(f"❌ Failed to fetch a song.\n`{e}`")
            continue

        try:
            await stream(
                file,
                msg,
                user.id,
                details,
                chat_id,
                user.first_name,
                chat_id,
                streamtype="youtube",
            )
        except Exception as e:
            await msg.edit_text(f"⚠️ Error streaming a song.\n`{e}`")
            continue

    await msg.edit_text("✅ Finished autoplay queue!")
