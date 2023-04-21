from pyrogram import filters

from config import LOG
from strings import get_command

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.database import add_off, add_on
from RiruruMusic.utils.decorators.language import language

# Commands
LOGGER_COMMAND = get_command("LOGGER_COMMAND")


@app.on_message(filters.command(LOGGER_COMMAND) & SUDOERS)
@language
async def logger(client, message, _):
    usage = _["log_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await add_on(LOG)
        await message.reply_text(_["log_2"])
    elif state == "disable":
        await add_off(LOG)
        await message.reply_text(_["log_3"])
    else:
        await message.reply_text(usage)
