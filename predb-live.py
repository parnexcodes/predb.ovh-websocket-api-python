#!/usr/bin/env python

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
    while True:
        uri = "wss://predb.ovh/api/v1/ws"
        async with websockets.connect(uri) as websocket:
            response = await websocket.recv()
            response_json = json.loads(response)

            # Ignore if you don't care about categories
            # The reason I used ['action'] == 'insert' is because this way , you get the pre faster.
            # If you change ['action'] == 'insert' to ['row']['name'] != 'PRE' and make another variable for category ['row']['cat'] to include the category , it won't be fastest.
            # as predb.ovh lists 'PRE' category as first when posting on websocket, then updates it to category like 'GAMES' after a few seconds (The pre will be posted late when printing it as you are waiting for it update the category.)

            if response_json['action'] == 'insert':
                pre = response_json['row']['name']
                print(f"[cyan]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/cyan] - [green][PRE][/green] [orange1]{pre}[/orange1]")

                async with aiohttp.ClientSession() as session:
                    if ENABLE_DISCORD == "True":
                        discord_post = {'content': pre}
                        try:
                            async with session.post(WEBHOOK_URL, data=discord_post):
                                pass
                        except:
                            print("Couldn't post to Discord. Configure the .env file.")

                    if ENABLE_TELEGRAM == "True":
                        tg_post = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={pre}'
                        try:
                            async with session.get(tg_post):
                                pass
                        except:
                            print("Couldn't post to Discord. Configure the .env file.")

asyncio.get_event_loop().run_until_complete(get_pre())