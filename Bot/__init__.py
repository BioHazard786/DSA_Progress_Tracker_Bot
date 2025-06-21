# GLOBAL INIT
import glob
import asyncio
from Bot.config import TeleConf
from importlib import import_module
from pyrogram import Client, enums
from os.path import dirname, basename, isfile, join
from Bot.constants import BANNER
from Bot.logging import LOGGER
# import uvloop

# uvloop.install()  # Optional: Use uvloop for better performance
__all__ = ["bot", "loop"]

LOGGER(__name__).info(BANNER)

LOGGER(__name__).info("Initiating the client...")
bot = Client(
    TeleConf.SESSION_NAME,
    api_id=TeleConf.API_ID,
    api_hash=TeleConf.API_HASH,
    bot_token=TeleConf.BOT_TOKEN,
    parse_mode=enums.ParseMode.HTML,
    max_concurrent_transmissions=1000,
).start()


LOGGER(__name__).info("Setting up event loop...")
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

# Setting Bot Username
TeleConf.BOT_USERNAME = bot.get_me().username

LOGGER(__name__).info("Importing Plugins...")
# * Importing modules
files = glob.glob(join(join(dirname(__file__), "Plugins"), "*py"))
plugins = [
    basename(f)[:-3] for f in files if isfile(f) and not f.endswith("__init__.py")
]

for plugin in plugins:
    import_module("Bot.Plugins." + plugin)
