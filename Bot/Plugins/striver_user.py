from . import *


@bot.on_message(command_creator("add_striver_user"))
async def add_striver_user(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("<code>Usage: /add_striver_user username</code>")

    username = message.command[1]

    reply = await message.reply(
        text="<code>Fetching Info...\nPlease have Patience...</code>",
        quote=True,
    )

    if (await get_user_data(message.from_user.id)).get("striver_username"):
        return await message.reply(
            "<code>You are already added to the database.</code>"
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://backend.takeuforward.org/api/profile/user/{username}"
            )
            response.raise_for_status()
            user_data = response.json()
    except:
        return await message.reply("<code>Invalid username or user not found.</code>")

    name = user_data.get("userData", {}).get("name", "Unknown User")
    email = user_data.get("userData", {}).get("email", "No Email")

    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Confirm",
                    callback_data=f"s_confirm|{username}|{message.from_user.id}",
                ),
                InlineKeyboardButton(
                    text="Delete",
                    callback_data=f"a_delete|{username}|{message.from_user.id}",
                ),
            ]
        ]
    )
    await reply.edit(
        text=f"<b>Username:</b> <code>{username}</code>\n"
        f"<b>Name:</b> <code>{name}</code>\n"
        f"<b>Email:</b> <code>{email}</code>\n\n"
        "<i>Do you want to add this user?</i>",
        reply_markup=button,
    )


@bot.on_message(command_creator("delete_striver_user"))
async def delete_striver_user(client: Client, message: Message):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Confirm",
                    callback_data=f"s_d_confirm|{message.from_user.id}",
                ),
                InlineKeyboardButton(
                    text="Delete",
                    callback_data=f"d_delete|{message.from_user.id}",
                ),
            ]
        ]
    )

    await message.reply(
        text="<b>Are you sure you want to delete your Striver user?</b>\n"
        "<i>This action cannot be undone.</i>",
        reply_markup=button,
    )


@bot.on_callback_query(filters.regex(r"^(s_confirm|l_confirm|a_delete)"))
async def handle_callback_query(client: Client, callback_query: CallbackQuery):
    action, username, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    if action == "s_confirm":
        await save_user_data(
            user_id,
            telegram_name=callback_query.from_user.first_name,
            striver_username=username,
        )
        await callback_query.answer("User added successfully!")

    elif action == "l_confirm":
        await save_user_data(
            user_id,
            telegram_name=callback_query.from_user.first_name,
            leetcode_username=username,
        )
        await callback_query.answer("User added successfully!")

    else:
        await callback_query.answer("User addition cancelled.")

    await callback_query.message.delete()


@bot.on_callback_query(filters.regex(r"^(s_d_confirm|d_delete|l_d_confirm)"))
async def handle_callback_query(client: Client, callback_query: CallbackQuery):
    action, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    if action in ["s_d_confirm", "l_d_confirm"]:
        action = "striver" if action == "s_d_confirm" else "leetcode"
        deleted = await delete_user_data(user_id=user_id, action=action)
        if not deleted:
            return await callback_query.answer(
                f"No {action.title()} user found to delete."
            )
        await callback_query.answer("User deleted successfully!")

    else:
        await callback_query.answer("User deletion cancelled.")

    await callback_query.message.delete()
