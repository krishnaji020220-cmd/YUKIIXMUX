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
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from YUKIIMUSIC import app


@app.on_message(filters.command("population"))
def country_command_handler(client: Client, message: Message):
    # Extract the country code from the command
    country_code = message.text.split(maxsplit=1)[1].strip()

    # Call the external API for country information
    api_url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        country_info = response.json()
        if country_info:
            # Extract relevant information from the API response
            country_name = country_info[0].get("name", {}).get("common", "N/A")
            capital = country_info[0].get("capital", ["N/A"])[0]
            population = country_info[0].get("population", "N/A")

            response_text = (
                f"Country Information\n\n"
                f"Name: {country_name}\n"
                f"Capital: {capital}\n"
                f"Population: {population}"
            )
        else:
            response_text = "Error fetching country information from the API."
    except requests.exceptions.HTTPError as http_err:
        response_text = f"HTTP error occurred Enter correct Country code"
    except Exception as err:
        response_text = f" Error @gitwizardbypass"

    # Send the response to the Telegram chat
    message.reply_text(response_text)