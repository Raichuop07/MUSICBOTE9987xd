from datetime import datetime

from strings import get_command
from config import MUSIC_BOT_NAME, PING_IMG_URL

from pyrogram import filters
from pyrogram.types import Message

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.core.call import AltCall
from RiruruMusic.utils import bot_sys_stats
from RiruruMusic.utils.inline.play import close_keyboard
from RiruruMusic.utils.decorators.language import language

### Commands
PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(filters.command(PING_COMMAND) & SUDOERS)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"],
    )
    start = datetime.now()
    pytgping = await AltCall.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, MUSIC_BOT_NAME, UP, RAM, CPU, DISK, pytgping),
        reply_markup=close_keyboard
    )
