from typing import Union
from . import *


async def _reply(user_id: int, message: Union[Message, CallbackQuery]) -> str:
    user_data = await get_user_data(user_id)

    if not user_data:
        if isinstance(message, CallbackQuery):
            return await message.message.edit("<code>User not found.</code>")
        else:
            return await message.reply("<code>User not found.</code>")

    leetcode_username = user_data.get("leetcode_username", None)
    striver_username = user_data.get("striver_username", None)

    button = [
        InlineKeyboardButton(
            text="LeetCode",
            callback_data=f"leetcode|{message.from_user.id}",
        ),
        InlineKeyboardButton(
            text="Striver Sheet",
            callback_data=f"striver|{message.from_user.id}",
        ),
    ]
    if not leetcode_username:
        del button[0]

    if not striver_username:
        del button[1]

    reply_markup = InlineKeyboardMarkup(
        [
            button,
            [
                InlineKeyboardButton(
                    text="Delete", callback_data=f"i_delete|{message.from_user.id}"
                )
            ],
        ]
    )

    if isinstance(message, CallbackQuery):
        return await message.message.edit(
            "<b>Choose an option to view your progress:</b>",
            reply_markup=reply_markup,
        )

    return await message.reply(
        "<b>Choose an option to view your progress:</b>",
        reply_markup=reply_markup,
    )


@bot.on_message(command_creator("info"))
async def info(client: Client, message: Message):
    return await _reply(message.from_user.id, message)


@bot.on_callback_query(filters.regex(r"^_back"))
async def handle_back_to_overview(client: Client, callback_query: CallbackQuery):
    _, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    return await _reply(user_id, callback_query)


@bot.on_callback_query(filters.regex(r"^i_delete"))
async def handle_delete_message(client: Client, callback_query: CallbackQuery):
    _, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    await callback_query.answer("Message deleted...🗑️")
    return await callback_query.message.delete()
