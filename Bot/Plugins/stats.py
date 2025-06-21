from .__init__ import *


@bot.on_message(command_creator("stats"))
async def stats(_: Client, message: Message):
    currentTime = get_readable_time(time.time() - TeleConf.BOT_START_TIME)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())

    stats = (
        "<b>≧◉◡◉≦ Bot is Up and Running successfully.</b>\n\n"
        f"<b>➜ Bot Uptime :</b> <code>{currentTime}</code>\n"
        f"<b>➜ Total Disk Space :</b> <code>{total}</code>\n"
        f"<b>➜ Used :</b> <code>{used}</code>\n"
        f"<b>➜ Free :</b> <code>{free}</code>\n"
        f"<b>➜ Memory Usage :</b> <code>{round(process.memory_info()[0] / 1024**2)} MiB</code>\n\n"
        f"<b>➜ Upload :</b> <code>{sent}</code>\n"
        f"<b>➜ Download :</b> <code>{recv}</code>\n\n"
        f"<b>➜ CPU :</b> <code>{cpuUsage}%</code> | "
        f"<b>➜ RAM :</b> <code>{memory}%</code> | "
        f"<b>➜ DISK :</b> <code>{disk}%</code>"
    )
    await message.reply(stats)
