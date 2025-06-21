from . import *


async def fetch_user_topics(username):
    """Fetch user topics data from the API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://backend.takeuforward.org/api/profile/user/topics/{username}"
            )
            response.raise_for_status()
            return response.json()
    except:
        return None


async def fetch_user_progress(username):
    """Fetch user progress data from the API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://backend.takeuforward.org/api/profile/user/progress/{username}"
            )
            response.raise_for_status()
            return response.json()
    except:
        return None


def create_overview_message(username, topics_data):
    """Create the overview message with topics statistics"""
    message_text = f"<b>📊 Profile Statistics for {username}</b>\n\n"

    topic_lines = []

    for topic_key, count in topics_data.items():
        topic_name = TOPICS[topic_key]
        topic_lines.append(f"<b>{topic_name}:</b> <code>{count} problems</code>")

    # Sort topics by count (descending)
    def extract_count(line):
        match = re.search(r"(\d+)", line)
        return int(match.group(1)) if match else 0

    topic_lines.sort(key=extract_count, reverse=True)

    message_text += "\n".join(topic_lines)

    return message_text


def create_sheet_buttons(username, user_id):
    """Create the inline keyboard markup for sheet selection"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Striver A2Z Sheet",
                    callback_data=f"sheet_a2z|{username}|{user_id}",
                ),
                InlineKeyboardButton(
                    text="Striver SDE Sheet",
                    callback_data=f"sheet_sde|{username}|{user_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Striver 79 Sheet",
                    callback_data=f"sheet_79|{username}|{user_id}",
                ),
                InlineKeyboardButton(
                    text="Blind 75 Sheet",
                    callback_data=f"blind_75|{username}|{user_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="« Back",
                    callback_data=f"_back|{user_id}",
                )
            ],
        ]
    )


def create_sheet_progress_message(username, sheet, sheet_data):
    """Create the detailed sheet progress message"""
    # Define sheet names for display
    sheet_names = {
        "sheet_a2z": "Striver A2Z Sheet",
        "sheet_sde": "Striver SDE Sheet",
        "sheet_79": "Striver 79 Sheet",
        "blind_75": "Blind 75 Sheet",
    }

    sheet_name = sheet_names.get(sheet, sheet.replace("_", " ").title())

    # Format the progress message
    total = sheet_data["total"]
    completed = sheet_data["completed"]
    percentage = sheet_data["percentage"]

    easy_total = sheet_data["easy"]
    medium_total = sheet_data["medium"]
    hard_total = sheet_data["hard"]

    easy_completed = sheet_data["easy_completed"]
    medium_completed = sheet_data["medium_completed"]
    hard_completed = sheet_data["hard_completed"]

    overall_progress_bar = create_progress_bar(completed, total)
    easy_progress_bar = create_progress_bar(easy_completed, easy_total)
    medium_progress_bar = create_progress_bar(medium_completed, medium_total)
    hard_progress_bar = create_progress_bar(hard_completed, hard_total)

    message_text = f"<b>📊 {sheet_name} Progress for {username}</b>\n\n"

    message_text += "<b>🎯 Overall Progress:</b>\n"
    message_text += (
        f"{overall_progress_bar} <code>{completed}/{total} ({percentage}%)</code>\n\n"
    )

    message_text += "<b>📈 Difficulty Breakdown:</b>\n\n"

    message_text += f"<b>🟢 Easy:</b> <code>{easy_completed}/{easy_total}</code>\n"
    message_text += f"{easy_progress_bar}\n\n"

    message_text += (
        f"<b>🟡 Medium:</b> <code>{medium_completed}/{medium_total}</code>\n"
    )
    message_text += f"{medium_progress_bar}\n\n"

    message_text += f"<b>🔴 Hard:</b> <code>{hard_completed}/{hard_total}</code>\n"
    message_text += f"{hard_progress_bar}\n\n"

    # Add motivational message based on progress
    if percentage == 100:
        message_text += "🎉 <b>Congratulations! You've completed this sheet!</b>"
    elif percentage >= 75:
        message_text += "🔥 <b>Excellent progress! You're almost there!</b>"
    elif percentage >= 50:
        message_text += "💪 <b>Great work! Keep pushing forward!</b>"
    elif percentage >= 25:
        message_text += "🚀 <b>Good start! Stay consistent!</b>"
    else:
        message_text += "💡 <b>Just getting started! Every problem counts!</b>"

    return message_text


@bot.on_callback_query(filters.regex("^striver"))
async def handle_striver_info(client: Client, callback_query: CallbackQuery):
    _, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    user_data = await get_user_data(user_id)

    username = user_data.get("striver_username", None)

    if not username:
        await callback_query.message.delete()
        return await callback_query.answer("Username not found.")

    await callback_query.message.edit(
        text="<code>Fetching Info...\nPlease have Patience...</code>",
    )

    topics_data = await fetch_user_topics(username)
    if not topics_data:
        return await callback_query.message.edit(
            "<code>Failed to fetch user data.</code>"
        )

    message_text = create_overview_message(username, topics_data)
    button = create_sheet_buttons(username, callback_query.from_user.id)

    await callback_query.message.edit(text=message_text, reply_markup=button)


@bot.on_callback_query(filters.regex(r"^(sheet_a2z|sheet_sde|sheet_79|blind_75)"))
async def handle_sheet_callback(client: Client, callback_query: CallbackQuery):
    sheet, username, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    progress = await fetch_user_progress(username)
    if not progress:
        await callback_query.answer("Failed to fetch sheet data.", show_alert=True)
        return await callback_query.message.delete()

    # Get the specific sheet data
    sheet_data = progress.get(sheet)
    if not sheet_data:
        await callback_query.answer("Sheet data not found.", show_alert=True)
        return await callback_query.message.delete()

    message_text = create_sheet_progress_message(username, sheet, sheet_data)

    # Create back button
    back_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="« Back to Overview",
                    callback_data=f"back_to_overview|{username}|{user_id}",
                )
            ]
        ]
    )

    await callback_query.message.edit_text(text=message_text, reply_markup=back_button)


@bot.on_callback_query(filters.regex(r"^back_to_overview"))
async def handle_back_to_overview(client: Client, callback_query: CallbackQuery):
    _, username, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    topics_data = await fetch_user_topics(username)
    if not topics_data:
        await callback_query.answer("Failed to fetch user data.", show_alert=True)
        return await callback_query.message.delete()

    message_text = create_overview_message(username, topics_data)
    button = create_sheet_buttons(username, user_id)

    await callback_query.message.edit_text(text=message_text, reply_markup=button)
