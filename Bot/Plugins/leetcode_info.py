from Bot.Helpers.leetcode_utils import API, USER_PROGRESS_QUERY
from . import *


async def fetch_user_progress(username):
    """Fetch user progress data from the API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                API,
                json={
                    "query": USER_PROGRESS_QUERY,
                    "variables": {"username": username},
                },
            )
            response.raise_for_status()
            response = response.json()
            if (
                "errors" in response
                or response.get("data", {}).get("matchedUser") is None
            ):
                return None

            return response["data"]
    except:
        return None


def create_progress_message(username, progress_data):
    """Create the detailed progress message"""

    # Extract data from the nested structure
    all_questions = progress_data["allQuestionsCount"]
    user_stats = progress_data["matchedUser"]["submitStats"]["acSubmissionNum"]

    # Get total counts for each difficulty
    total_counts = {item["difficulty"]: item["count"] for item in all_questions}
    completed_counts = {item["difficulty"]: item["count"] for item in user_stats}

    # Extract values
    total = total_counts["All"]
    completed = completed_counts["All"]
    percentage = round((completed / total) * 100, 1) if total > 0 else 0

    easy_total = total_counts["Easy"]
    medium_total = total_counts["Medium"]
    hard_total = total_counts["Hard"]

    easy_completed = completed_counts["Easy"]
    medium_completed = completed_counts["Medium"]
    hard_completed = completed_counts["Hard"]

    overall_progress_bar = create_progress_bar(completed, total)
    easy_progress_bar = create_progress_bar(easy_completed, easy_total)
    medium_progress_bar = create_progress_bar(medium_completed, medium_total)
    hard_progress_bar = create_progress_bar(hard_completed, hard_total)

    message_text = f"<b>📊 LeetCode Progress for {username}</b>\n\n"

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


@bot.on_callback_query(filters.regex("^leetcode"))
async def handle_leetcode_info(client: Client, callback_query: CallbackQuery):
    _, user_id = callback_query.data.split("|")
    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("This command is not initiated by you...❎")

    user_data = await get_user_data(user_id)

    username = user_data.get("leetcode_username", None)

    if not username:
        await callback_query.message.delete()
        return await callback_query.answer("Username not found.")

    await callback_query.message.edit(
        text="<code>Fetching Info...\nPlease have Patience...</code>",
    )

    progress = await fetch_user_progress(username)
    if not progress:
        return await callback_query.message.edit(
            "<code>Failed to fetch user data.</code>"
        )

    message_text = create_progress_message(username, progress)
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="« Back",
                    callback_data=f"_back|{user_id}",
                )
            ]
        ]
    )

    await callback_query.message.edit(text=message_text, reply_markup=button)
