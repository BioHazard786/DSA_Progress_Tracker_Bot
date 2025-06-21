from Bot import bot, loop
from Bot.Database.mongo_db import mongo
from Bot.logging import LOGGER


async def cleanup():
    """
    Cleanup function to stop the bot and close the loop.
    """
    LOGGER(__name__).info("Stopping Services...")
    mongo.close()
    await bot.stop()
    loop.stop()
    LOGGER(__name__).info("Services Stopped")


if __name__ == "__main__":
    try:
        LOGGER(__name__).info("Bot started")
        bot.loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        LOGGER(__name__).error(err.with_traceback(None))
    finally:
        bot.loop.run_until_complete(cleanup())
