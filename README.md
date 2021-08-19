# predb.ovh-websocket-api-python
 A python script to get live responses from predb.ovh Websocket API and post the Pre to Telegram or Discord (Optional).

# Setup

Edit the **.env** file

**Default Config**

```
ENABLE_DISCORD = "False"
ENABLE_TELEGRAM = "False"
WEBHOOK_URL = "test"
TG_BOT_TOKEN = "bot token"
CHANNEL_ID = "@channel name or -channel/group id"
```

Set `ENABLE_DISCORD = "True"` and Update `WEBHOOK_URL` if you want to send Pre to **Discord** channel.

Set `ENABLE_TELEGRAM = "True"` and Update `TG_BOT_TOKEN`, `CHANNEL_ID` if you want to send Pre to **Telegram** channel.

# Run

`pip install -r requirements.txt`

`python predb-live.py`

or

`python predb-live-categories.py` to show category of pre.

# LICENSE

See [LICENSE](https://github.com/parnexcodes/predb.ovh-websocket-api-python/blob/main/LICENSE)