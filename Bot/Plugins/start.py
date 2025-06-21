from .__init__ import *


@bot.on_message(command_creator("start"))
async def start(client: Client, message: Message):
    return await message.reply("<code>Hello :)</code>")
