#!/usr/bin/env python
# This script was made by parnex.
# Getting Pre with the category isn't the fastest way (use this if you don't care about pre time.)
# This will Skip Releases of Groups like ENDURANCE whose Pre are added as 'PRE' in predb.ovh api and not as 'TV-X264` etc. (idk why , maybe problem with predb.ovh api)

import asyncio
import websockets
import json
import platform
import os
import aiohttp
from datetime import datetime
from rich import print

try:
    TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
    CHANNEL_ID = os.environ['CHANNEL_ID']
    WEBHOOK_URL = os.environ['WEBHOOK_URL']
    ENABLE_DISCORD = os.environ['ENABLE_DISCORD']
    ENABLE_TELEGRAM = os.environ['ENABLE_TELEGRAM']
except:
    from dotenv import load_dotenv
    load_dotenv()
    TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    ENABLE_DISCORD = os.getenv('ENABLE_DISCORD')
    ENABLE_TELEGRAM = os.getenv('ENABLE_TELEGRAM')    

print('Starting [green]PreDB Watcher[/green]')
print(f"Python version: {platform.python_version()}")
print(f"Running on: {platform.system()} {platform.release()} ({os.name})")

async def get_pre():
    lastname = None
    while True:
        uri = "wss://predb.ovh/api/v1/ws"
        async with websockets.connect(uri) as websocket:
            response = await websocket.recv()
            response_json = json.loads(response)

            # Set response_json['row']['cat'] != 'PRE' to response_json['row']['cat'] == 'GAMES' to post releases of a specific category only.
            if response_json['row']['cat'] != 'PRE':
                pre = response_json['row']['name']
                cat = response_json['row']['cat']
                pre_with_cat = f'{cat} {pre}'

                if pre_with_cat != lastname:
                    print(f"[cyan]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/cyan] - [green][{cat}][/green] [orange1]{pre}[/orange1]")

                    async with aiohttp.ClientSession() as session:
                        if ENABLE_DISCORD == "True":
                            discord_post = {'content': pre_with_cat}
                            try:
                                async with session.post(WEBHOOK_URL, data=discord_post):
                                    pass
                            except:
                                print("Couldn't post to Discord. Configure the .env file.")

                        if ENABLE_TELEGRAM == "True":
                            tg_post = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={pre_with_cat}'
                            try:
                                async with session.get(tg_post):
                                    pass
                            except:
                                print("Couldn't post to Telegram. Configure the .env file.")
                lastname = pre_with_cat

asyncio.get_event_loop().run_until_complete(get_pre())