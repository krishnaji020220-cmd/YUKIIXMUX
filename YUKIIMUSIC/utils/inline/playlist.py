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
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def botplaylist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["PL_B_1"],
                callback_data="get_playlist_playmode",
            ),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def top_play_markup(_):
    buttons = [
        [InlineKeyboardButton(text=_["PL_B_9"], callback_data="SERVERTOP global")],
        [InlineKeyboardButton(text=_["PL_B_10"], callback_data="SERVERTOP chat")],
        [InlineKeyboardButton(text=_["PL_B_11"], callback_data="SERVERTOP user")],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="get_playmarkup"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def get_playlist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data="play_playlist a"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data="play_playlist v"),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="home_play"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def top_play_markup(_):
    buttons = [
        [InlineKeyboardButton(text=_["PL_B_9"], callback_data="SERVERTOP Global")],
        [InlineKeyboardButton(text=_["PL_B_10"], callback_data="SERVERTOP Group")],
        [InlineKeyboardButton(text=_["PL_B_11"], callback_data="SERVERTOP Personal")],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="get_playmarkup"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def failed_top_markup(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="get_top_playlists",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def warning_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["PL_B_7"],
                    callback_data="delete_whole_playlist",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="del_back_playlist",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


def close_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )
    return upl