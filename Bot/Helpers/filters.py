from pyrogram import filters
from pyrogram.types import Message
from Bot import TeleConf


def command_creator(*args):
    commands = []
    for command_name in args:
        commands.append(command_name)
        commands.append(f"{command_name}@{TeleConf.BOT_USERNAME}")
    return filters.command(commands)


def owner(_, __, message: Message) -> bool:
    return message.from_user.id == TeleConf.OWNER_ID if message.from_user else False


owner_cmd = filters.create(owner)
