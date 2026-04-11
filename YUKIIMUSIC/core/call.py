# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual property of HellfireDevs.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.

import YUKIIMUSIC.yuki_guard
import asyncio
import os
import random
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded

import config
from YUKIIMUSIC import LOGGER, YouTube, app
from YUKIIMUSIC.misc import db
from YUKIIMUSIC.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
    is_autoplay_on, # 🔥 Autoplay Database Import
)
from YUKIIMUSIC.utils.exceptions import AssistantErr
from YUKIIMUSIC.utils.formatters import check_duration, seconds_to_min, speed_converter
from YUKIIMUSIC.utils.inline.play import stream_markup, music_end_markup
from YUKIIMUSIC.utils.stream.autoclear import auto_clean
from YUKIIMUSIC.utils.thumbnails import get_thumb
from strings import get_string

autoend = {}
counter = {}


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="YUKIIAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)
        self.userbot2 = Client(
            name="YUKIIAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)
        self.userbot3 = Client(
            name="YUKIIAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)
        self.userbot4 = Client(
            name="YUKIIAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)
        self.userbot5 = Client(
            name="YUKIIAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def stop_stream_force(self, chat_id: int):
        for ass in [self.one, self.two, self.three, self.four, self.five]:
            try:
                await ass.leave_group_call(chat_id)
            except:
                pass
        try:
            await _clear_(chat_id)
        except:
            pass

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        assistant = await group_assistant(self, chat_id)
        if str(speed) != str("1.0"):
            base = os.path.basename(file_path)
            chatdir = os.path.join(os.getcwd(), "playback", str(speed))
            if not os.path.isdir(chatdir):
                os.makedirs(chatdir)
            out = os.path.join(chatdir, base)
            if not os.path.isfile(out):
                vs = {"0.5": 2.0, "0.75": 1.35, "1.5": 0.68, "2.0": 0.5}.get(str(speed), 1.0)
                proc = await asyncio.create_subprocess_shell(
                    cmd=f"ffmpeg -i {file_path} -filter:v setpts={vs}*PTS -filter:a atempo={speed} {out}",
                    stdin=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.communicate()
            else:
                pass
        else:
            out = file_path
        
        dur = await asyncio.get_event_loop().run_in_executor(None, check_duration, out)
        dur = int(dur)
        played, con_seconds = speed_converter(playing[0]["played"], speed)
        duration = seconds_to_min(dur)
        
        stream = AudioVideoPiped(out, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo(), additional_ffmpeg_parameters=f"-ss {played} -to {duration}") if playing[0]["streamtype"] == "video" else AudioPiped(out, audio_parameters=HighQualityAudio(), additional_ffmpeg_parameters=f"-ss {played} -to {duration}")
        
        if str(db[chat_id][0]["file"]) == str(file_path):
            await assistant.change_stream(chat_id, stream)
            db[chat_id][0].update({"played": con_seconds, "dur": duration, "seconds": dur, "speed_path": out, "speed": speed})

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            db.get(chat_id).pop(0)
        except:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def skip_stream(self, chat_id: int, link: str, video: Union[bool, str] = None, image: Union[bool, str] = None):
        assistant = await group_assistant(self, chat_id)
        stream = AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(link, audio_parameters=HighQualityAudio())
        await assistant.change_stream(chat_id, stream)

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        stream = AudioVideoPiped(file_path, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo(), additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}") if mode == "video" else AudioPiped(file_path, audio_parameters=HighQualityAudio(), additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}")
        await assistant.change_stream(chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOGGER_ID)
        await assistant.join_group_call(config.LOGGER_ID, AudioVideoPiped(link), stream_type=StreamType().pulse_stream)
        await asyncio.sleep(0.2)
        await assistant.leave_group_call(config.LOGGER_ID)

    async def join_call(self, chat_id: int, original_chat_id: int, link, video: Union[bool, str] = None, image: Union[bool, str] = None):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)
        stream = AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(link, audio_parameters=HighQualityAudio())
        try:
            await assistant.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
        except NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except AlreadyJoinedError:
            raise AssistantErr(_["call_9"])
        except TelegramServerError:
            raise AssistantErr(_["call_10"])
        
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            if len(await assistant.get_participants(chat_id)) == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    # ==========================================
    # 🔥 CORE CHANGE STREAM LOGIC (FIXED) 🔥
    # ==========================================
    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop -= 1
                await set_loop(chat_id, loop)
            await auto_clean(popped)
            
            # 🔥 AUTOPLAY INTEGRATION
            if not check:
                if await is_autoplay_on(chat_id):
                    if popped and "vidid" in popped and popped["vidid"] not in ["telegram", "soundcloud"]:
                        try:
                            prev_title = popped.get("title", "music")
                            clean_query = f"{prev_title.split('|')[0].split('(')[0].strip()} similar audio"
                            
                            next_vidid = None
                            try:
                                # Random related pick
                                _, _, _, check_vidid = await YouTube.slider(clean_query, random.randint(1, 4))
                                if check_vidid and check_vidid != popped["vidid"]:
                                    next_vidid = check_vidid
                            except: pass

                            if not next_vidid:
                                # Fallback random aesthetic
                                _, _, _, next_vidid = await YouTube.slider(random.choice(["Lofi chill", "NCS latest", "Trending Pop"]), 1)

                            if next_vidid:
                                track_details, _ = await YouTube.track(next_vidid, videoid=True)
                                check.append({
                                    "vidid": next_vidid,
                                    "title": track_details["title"],
                                    "by": "ᴀᴜᴛᴏᴘʟᴀʏ",
                                    "chat_id": chat_id,
                                    "dur": track_details["duration_min"],
                                    "seconds": track_details["duration_sec"],
                                    "file": f"vid_{next_vidid}", 
                                    "streamtype": "audio",
                                })
                                # Do NOT return. Let it fall to the 'else' block below.
                        except Exception as e:
                            LOGGER(__name__).error(f"Autoplay Error: {e}")

                # If still no check (Autoplay off or failed), then leave.
                if not check:
                    try:
                        if popped and "mystic" in popped:
                            language = await get_lang(chat_id)
                            _ = get_string(language)
                            end_msg = _["MUSIC_ENDED"]
                            try:
                                await popped["mystic"].edit_caption(caption=end_msg, reply_markup=music_end_markup(_))
                            except:
                                await popped["mystic"].edit_text(text=end_msg, disable_web_page_preview=True, reply_markup=music_end_markup(_))
                    except: pass
                    
                    await _clear_(chat_id)
                    return await client.leave_group_call(chat_id)

        except Exception as e:
            LOGGER(__name__).error(f"Change Stream Error: {e}")
            await _clear_(chat_id)
            try: return await client.leave_group_call(chat_id)
            except: return

        # 🔥 PLAYBACK ENGINE (Executes if song is in queue)
        else:
            queued = check[0]["file"]
            language = await get_lang(chat_id)
            _ = get_string(language)
            title = (check[0]["title"]).title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]
            videoid = check[0]["vidid"]
            db[chat_id][0]["played"] = 0
            video = True if str(streamtype) == "video" else False

            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0: return await app.send_message(original_chat_id, text=_["call_6"])
                stream = AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(link, audio_parameters=HighQualityAudio())
                try: await client.change_stream(chat_id, stream)
                except: return await app.send_message(original_chat_id, text=_["call_6"])
                
                img = await get_thumb(videoid)
                button = stream_markup(_, chat_id)
                run = await app.send_photo(chat_id=original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{videoid}", title[:23], check[0]["dur"], user), reply_markup=InlineKeyboardMarkup(button))
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            elif "vid_" in queued:
                mystic = await app.send_message(original_chat_id, _["call_7"])
                try:
                    file_path, direct = await YouTube.download(videoid, mystic, videoid=True, video=video)
                except: return await mystic.edit_text(_["call_6"])
                
                stream = AudioVideoPiped(file_path, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(file_path, audio_parameters=HighQualityAudio())
                try: await client.change_stream(chat_id, stream)
                except: return await app.send_message(original_chat_id, text=_["call_6"])
                
                img = await get_thumb(videoid)
                button = stream_markup(_, chat_id)
                await mystic.delete()
                run = await app.send_photo(chat_id=original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{videoid}", title[:23], check[0]["dur"], user), reply_markup=InlineKeyboardMarkup(button))
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

            elif "index_" in queued:
                stream = AudioVideoPiped(videoid, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(videoid, audio_parameters=HighQualityAudio())
                try: await client.change_stream(chat_id, stream)
                except: return await app.send_message(original_chat_id, text=_["call_6"])
                button = stream_markup(_, chat_id)
                run = await app.send_photo(chat_id=original_chat_id, photo=config.STREAM_IMG_URL, caption=_["stream_2"].format(user), reply_markup=InlineKeyboardMarkup(button))
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            else:
                stream = AudioVideoPiped(queued, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(queued, audio_parameters=HighQualityAudio())
                try: await client.change_stream(chat_id, stream)
                except: return await app.send_message(original_chat_id, text=_["call_6"])
                
                img = config.TELEGRAM_AUDIO_URL if videoid == "telegram" else (config.SOUNCLOUD_IMG_URL if videoid == "soundcloud" else await get_thumb(videoid))
                button = stream_markup(_, chat_id)
                run = await app.send_photo(chat_id=original_chat_id, photo=img, caption=_["stream_1"].format(config.SUPPORT_CHAT, title[:23], check[0]["dur"], user), reply_markup=InlineKeyboardMarkup(button))
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

    async def ping(self):
        pings = [await ass.ping for ass in [self.one, self.two, self.three, self.four, self.five] if ass.is_running]
        return str(round(sum(pings) / len(pings), 3)) if pings else "0"

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Clients...\n")
        for ass in [self.one, self.two, self.three, self.four, self.five]:
            if ass.client.session_string:
                await ass.start()

    async def decorators(self):
        @self.one.on_kicked()
        @self.two.on_kicked()
        @self.three.on_kicked()
        @self.four.on_kicked()
        @self.five.on_kicked()
        @self.one.on_closed_voice_chat()
        @self.two.on_closed_voice_chat()
        @self.three.on_closed_voice_chat()
        @self.four.on_closed_voice_chat()
        @self.five.on_closed_voice_chat()
        @self.one.on_left()
        @self.two.on_left()
        @self.three.on_left()
        @self.four.on_left()
        @self.five.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.one.on_stream_end()
        @self.two.on_stream_end()
        @self.three.on_stream_end()
        @self.four.on_stream_end()
        @self.five.on_stream_end()
        async def stream_end_handler1(client, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.change_stream(client, update.chat_id)


YUKII = Call()
          
