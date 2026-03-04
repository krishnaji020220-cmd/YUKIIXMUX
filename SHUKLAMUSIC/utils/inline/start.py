import config
from SHUKLAMUSIC import app

# 🔥 HELLFIRE DEVS HACK: Raw API Button Generator (WITH AUTO-URL FIXER)
def api_btn(text, callback_data=None, url=None, style=None, custom_emoji_id=None):
    btn = {"text": text}
    if callback_data:
        btn["callback_data"] = callback_data
    if url:
        # Raw API strictly requires http/https/tg links. Yeh usko auto-fix karega:
        url_str = str(url)
        if not url_str.startswith("http") and not url_str.startswith("tg://"):
            url_str = f"https://t.me/{url_str.replace('@', '')}"
        btn["url"] = url_str
    if style:
        btn["style"] = style  # 'primary' (Blue), 'danger' (Red), 'secondary' (Grey)
    if custom_emoji_id:
        btn["icon_custom_emoji_id"] = str(custom_emoji_id) 
    return btn

def start_panel(_):
    buttons = [
        [
            # Add to Group (Blue + 💖 Emoji)
            api_btn(
                text=_["S_B_1"], 
                url=f"https://t.me/{app.username}?startgroup=true", 
                style="primary", 
                custom_emoji_id="6001132493011425597"
            ),
            # Support Chat (Red + 💀 Emoji)
            api_btn(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT, 
                style="danger", 
                custom_emoji_id="5999100917645841519"
            ),
        ],
    ]
    return buttons


def private_panel(_):
    # Owner ID list error bypass:
    safe_owner_id = config.OWNER_ID[0] if isinstance(config.OWNER_ID, list) else config.OWNER_ID
    
    buttons = [
        [
            # Add to Group (Blue + 😎 Emoji)
            api_btn(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style="primary",
                custom_emoji_id="6080202089311507876"
            )
        ],
        [
            # Settings/Help (Grey + 🐾 Emoji)
            api_btn(
                text=_["S_B_4"], 
                callback_data="settings_back_helper", 
                style="secondary", 
                custom_emoji_id="6080176744709495278"
            ),
            # Mimi Tunes (Blue + 🌺 Emoji)
            api_btn(
                text="˹ᴍɪᴍɪ ᴛᴜɴᴇs˼♪", 
                url="http://t.me/IAM_MIMBOT", 
                style="primary", 
                custom_emoji_id="5413840936994097463"
            ),
        ],
        [
            # Updates/Channel (Blue + 🔫 Emoji)
            api_btn(
                text=_["S_B_6"], 
                url=config.SUPPORT_CHANNEL, 
                style="primary", 
                custom_emoji_id="5415586682286128590"
            ),
            # Support Chat (Red + ☠️ Emoji)
            api_btn(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT, 
                style="danger", 
                custom_emoji_id="5413415116756500503"
            ),
        ],
        [
            # Owner (Red + 😈 Emoji)
            api_btn(
                text=_["S_B_5"], 
                url=f"tg://user?id={safe_owner_id}", 
                style="danger", 
                custom_emoji_id="5413546177683539369"
            ),
        ],
    ]
    return buttons
    
