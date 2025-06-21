from .__init__ import *


@bot.on_message(command_creator("logs") & owner_cmd)
async def logs(client: Client, message: Message):
    if os.path.isfile("logs.txt"):
        await message.reply_document(document="logs.txt", quote=True)
    else:
        await message.reply("<code>Logs does not exists</code>")
