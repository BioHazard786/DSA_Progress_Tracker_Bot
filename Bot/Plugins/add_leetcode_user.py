from Bot.Helpers.leetcode_utils import API, USER_PROFILE_QUERY
from . import *


@bot.on_message(command_creator("add_leetcode_user"))
async def add_leetcode_user(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("<code>Usage: /add_leetcode_user username</code>")

    username = message.command[1]

    reply = await message.reply(
        text="<code>Fetching Info...\nPlease have Patience...</code>",
        quote=True,
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                API,
                json={
                    "query": USER_PROFILE_QUERY,
                    "variables": {"username": username},
                },
            )
            response.raise_for_status()
            user_data = response.json()
    except:
        return await reply.edit(
            "<code>Failed to fetch user data. Please try again later.</code>"
        )

    # Check if there are errors in the response or if matchedUser is None
    if "errors" in user_data or user_data.get("data", {}).get("matchedUser") is None:
        return await reply.edit("<code>Invalid username or user not found.</code>")

    if (await get_user_data(message.from_user.id)).get("leetcode_username"):
        return await reply.edit("<code>You are already added to the database.</code>")

    # Extract user stats from the LeetCode API response
    matched_user = user_data["data"]["matchedUser"]

    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Confirm",
                    callback_data=f"l_confirm|{username}|{message.from_user.id}",
                ),
                InlineKeyboardButton(
                    text="Delete",
                    callback_data=f"a_delete|{username}|{message.from_user.id}",
                ),
            ]
        ]
    )
    await reply.edit(
        text=f"<b>Username:</b> <code>{matched_user['username']}</code>\n"
        f"<b>Name:</b> <code>{matched_user['profile']['realName']}</code>\n\n"
        "<i>Do you want to add this user?</i>",
        reply_markup=button,
    )
