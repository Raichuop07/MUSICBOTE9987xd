import random
import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from strings import get_string
from config import (AUTO_DOWNLOADS_CLEAR, BANNED_USERS,
                    SOUNCLOUD_IMG_URL, STREAM_IMG_URL,
                    TELEGRAM_AUDIO_URL, TELEGRAM_VIDEO_URL,
                    confirmer, votemode, adminlist)

from RiruruMusic import YouTube, app, userbot
from RiruruMusic.core.call import AltCall
from RiruruMusic.misc import SUDOERS, db
from RiruruMusic.utils.database import (
    get_active_chats,
    get_lang,
    is_active_chat,
    is_music_playing,
    is_nonadmin_chat,
    music_off,
    music_on,
    set_loop,
)
from RiruruMusic.utils.database.memorydatabase import get_upvote_count
from RiruruMusic.utils.decorators.language import languageCB
from RiruruMusic.utils.formatters import seconds_to_min
from RiruruMusic.utils.inline import (
    stream_markup, panel_markup_3,
    stream_markup_timer,
    telegram_markup,
    telegram_markup_timer,
    close_keyboard,
)
from RiruruMusic.utils.stream.autoclear import auto_clean
from RiruruMusic.utils.thumbnails import gen_thumb

wrong = {}
checker = {}
upvoters = {}
downvote = {}
downvoters = {}


@app.on_callback_query(filters.regex("PanelMarkup") & ~BANNED_USERS)
@languageCB
async def markup_panel(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    chat_id = CallbackQuery.message.chat.id
    buttons = panel_markup_3(_, videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.message_id] = False


@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    if videoid == str(None):
        buttons = telegram_markup(_, chat_id)
    else:
        buttons = stream_markup(_, videoid, chat_id)
    chat_id = CallbackQuery.message.chat.id
    try:
        await CallbackQuery.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    except:
        return
    if chat_id not in checker:
        checker[chat_id] = {}
    checker[chat_id][CallbackQuery.message.message_id] = True


@app.on_callback_query(filters.regex("unban_ass"))
async def unban_ass(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id, user_id = callback_request.split("|")
    chat_id = CallbackQuery.message.chat.id
    umm = await app.get_chat_member(int(chat_id), app.id)
    if umm.can_restrict_members:
        try:
            await app.unban_chat_member(int(chat_id), int(user_id))
        except:
            return await CallbackQuery.answer("» ғᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴀssɪsᴛᴀɴᴛ.", show_alert=True,)
        return await CallbackQuery.edit_message_text(
            f"➻ {userbot.one.name} sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴʙᴀɴɴᴇᴅ ʙʏ {CallbackQuery.from_user.mention}\n\nᴛʀʏ ᴘʟᴀʏɪɴɢ ɴᴏᴡ..."
        )
    else:
        return await CallbackQuery.answer("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴜɴʙᴀɴ ᴜsᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.", show_alert=True,)


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_6"], show_alert=True)
    mention = CallbackQuery.from_user.mention

    if command == "UpVote":
        if chat_id not in votemode:
            votemode[chat_id] = {}
        if chat_id not in upvoters:
            upvoters[chat_id] = {}
        voters = (upvoters[chat_id]).get(CallbackQuery.message.message_id)
        if not voters:
            upvoters[chat_id][CallbackQuery.message.message_id] = []
        vote = (votemode[chat_id]).get(CallbackQuery.message.message_id)
        if not vote:
            votemode[chat_id][CallbackQuery.message.message_id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.message_id]:
            (upvoters[chat_id][CallbackQuery.message.message_id]).remove(CallbackQuery.from_user.id)
            votemode[chat_id][CallbackQuery.message.message_id] -= 1
        else:
            (upvoters[chat_id][CallbackQuery.message.message_id]).append(CallbackQuery.from_user.id)
            votemode[chat_id][CallbackQuery.message.message_id] += 1

        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.message_id])

        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.message_id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.message_id]
                current = db[chat_id][0]
            except:
                return await CallbackQuery.edit_message_text("Failed to perform action.")
            try:
                if (current["vidid"] != exists["vidid"]) or (current["file"] != exists["file"]):
                    return await CallbackQuery.edit_message.text(
                        "» ᴛʜɪs ᴠᴏᴛɪɴɢ ʜᴀs ᴇɴᴅᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴀʟsᴏ ᴇɴᴅᴇᴅ ғᴏʀ ᴡʜɪᴄʜ ᴛʜɪs ᴠᴏᴛɪɴɢ ᴡᴀs sᴛᴀʀᴛᴇᴅ."
                    )
            except:
                return await CallbackQuery.edit_message_text(
                    f"ᴛʜɪs ᴠᴏᴛɪɴɢ ʜᴀs ᴇɴᴅᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ ᴏʀ sᴏᴍᴇᴏɴᴇ sᴛᴏᴘᴘᴇᴅ ɪᴛ ғᴏʀ ᴡʜɪᴄʜ ᴛʜɪs ᴠᴏᴛɪɴɢ ᴡᴀs sᴛᴀʀᴛᴇᴅ."
                )
            try:
                await CallbackQuery.edit_message_text(f"» sᴜᴄᴄᴇssғᴜʟʟʏ ɢᴏᴛ **{upvote}** ᴠᴏᴛᴇs ғᴏʀ ᴘᴇʀғᴏʀᴍɪɴɢ ᴛʜᴀᴛ ᴀᴄᴛɪᴏɴ.")
            except:
                pass
            command = counter
            mention = "**Upvotes**"

        else:
            if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.message_id]:
                await CallbackQuery.answer("Added Upvote.", show_alert=True)
            else:
                await CallbackQuery.answer("Removed Upvote.", show_alert=True)
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=f"👍 {get_upvotes}", callback_data=f"ADMIN  UpVote|{chat_id}_{counter}",)
                    ]
                ]
            )
            await CallbackQuery.answer("Upvoted", show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)

    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                admins = adminlist.get(CallbackQuery.message.chat.id)
                if not admins:
                    return await CallbackQuery.answer(_["admin_18"], show_alert=True)
                else:
                    if CallbackQuery.from_user.id not in admins:
                        return await CallbackQuery.answer(_["admin_19"], show_alert=True)

    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await CallbackQuery.answer()
        await music_off(chat_id)
        await AltCall.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_2"].format(mention), reply_markup=close_keyboard)

    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await CallbackQuery.answer()
        await music_on(chat_id)
        await AltCall.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_4"].format(mention), reply_markup=close_keyboard)

    elif command == "Stop" or command == "End":
        await CallbackQuery.answer()
        await AltCall.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.delete()
        await CallbackQuery.message.reply_text(_["admin_9"].format(mention), reply_markup=close_keyboard)
        try:
            popped = check.pop(0)
        except:
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        await CallbackQuery.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await CallbackQuery.message.reply_text(_["admin_23"].format(mention))

    elif command == "Skip":
        check = db.get(chat_id)
        txt = f"» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {mention}"
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                if AUTO_DOWNLOADS_CLEAR == str(True):
                    await auto_clean(popped)
            if not check:
                await CallbackQuery.edit_message_text(f"» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {mention}", reply_markup=close_keyboard)
                await CallbackQuery.message.reply_text(_["admin_10"].format(mention, CallbackQuery.message.chat.title), reply_markup=close_keyboard)
                try:
                    return await AltCall.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await CallbackQuery.edit_message_text(f"» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {mention}", reply_markup=close_keyboard)
                await CallbackQuery.message.reply_text(_["admin_10"].format(mention, CallbackQuery.message.chat.title), reply_markup=close_keyboard)
                return await AltCall.stop_stream(chat_id)
            except:
                return

        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        user_id = check[0]["user_id"]
        duration_min = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0

        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await CallbackQuery.message.reply_text(_["admin_11"].format(title))
            try:
                await AltCall.skip_stream(chat_id, link, video=status)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_9"])
            button = telegram_markup(_, chat_id)
            img = await gen_thumb(videoid, user_id)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(user, f"https://t.me/{app.username}?start=info_{videoid}"),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt)
        elif "vid_" in queued:
            mystic = await CallbackQuery.message.reply_text(_["call_10"], disable_web_page_preview=True)
            try:
                file_path, direct = await YouTube.download(videoid, mystic, videoid=True, video=status)
            except:
                return await mystic.edit_text(_["call_9"])
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
            try:
                await AltCall.skip_stream(chat_id, file_path, video=status, image=image)
            except Exception:
                return await mystic.edit_text(_["call_9"])
            button = stream_markup(_, videoid, chat_id)
            img = await gen_thumb(videoid, user_id)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(title[:27], f"https://t.me/{app.username}?start=info_{videoid}", duration_min, user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt)
            await mystic.delete()
        elif "index_" in queued:
            try:
                await AltCall.skip_stream(chat_id, videoid, video=status)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_9"])
            button = telegram_markup(_, chat_id)
            run = await CallbackQuery.message.reply_photo(
                photo=STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt)
        else:
            if videoid == "telegram":
                image = None
            elif videoid == "soundcloud":
                image = None
            else:
                try:
                    image = await YouTube.thumbnail(videoid, True)
                except:
                    image = None
            try:
                await AltCall.skip_stream(chat_id, queued, video=status, image=image)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_9"])

            if videoid == "telegram":
                button = telegram_markup(_, chat_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=TELEGRAM_AUDIO_URL
                    if str(streamtype) == "audio"
                    else TELEGRAM_VIDEO_URL,
                    caption=_["stream_3"].format(title, check[0]["dur"], user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            elif videoid == "soundcloud":
                button = telegram_markup(_, chat_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=SOUNCLOUD_IMG_URL
                    if str(streamtype) == "audio"
                    else TELEGRAM_VIDEO_URL,
                    caption=_["stream_3"].format(title, check[0]["dur"], user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            else:
                button = stream_markup(_, videoid, chat_id)
                img = await gen_thumb(videoid, user_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=img,
                    caption=_["stream_1"].format(title[:27], f"https://t.me/{app.username}?start=info_{videoid}", duration_min, user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt)

    else:
        playing = db.get(chat_id)
        if not playing:
            return await CallbackQuery.answer(_["queue_2"], show_alert=True)

        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)

        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)

        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]

        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"» ʙᴏᴛ ɪs ᴜɴᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴅᴜʀᴀᴛɪᴏɴ ᴇxᴄᴇᴇᴅs.\n\nᴄᴜʀʀᴇɴᴛʟʏ ᴩʟᴀʏᴇᴅ :** {bet}** ᴍɪɴᴜᴛᴇs ᴏᴜᴛ ᴏғ **{duration}** ᴍɪɴᴜᴛᴇs.",
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"» ʙᴏᴛ ɪs ᴜɴᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴅᴜʀᴀᴛɪᴏɴ ᴇxᴄᴇᴇᴅs.\n\nᴄᴜʀʀᴇɴᴛʟʏ ᴩʟᴀʏᴇᴅ :** {bet}** ᴍɪɴᴜᴛᴇs ᴏᴜᴛ ᴏғ **{duration}** ᴍɪɴᴜᴛᴇs.",
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1

        await CallbackQuery.answer()
        mystic = await CallbackQuery.message.reply_text(_["admin_32"])
        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text(_["admin_30"])
        try:
            await AltCall.seek_stream(chat_id, file_path, seconds_to_min(to_seek), duration, playing[0]["streamtype"])
        except:
            return await mystic.edit_text(_["admin_34"])
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = _["admin_33"].format(seconds_to_min(to_seek))
        await mystic.edit_text(f"{string}\n\nᴄʜᴀɴɢᴇs ᴅᴏɴᴇ ʙʏ : {mention} !")


async def markup_timer():
    while not await asyncio.sleep(4):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                if not await is_music_playing(chat_id):
                    continue
                playing = db.get(chat_id)
                if not playing:
                    continue
                duration_seconds = int(playing[0]["seconds"])
                if duration_seconds == 0:
                    continue
                try:
                    mystic = playing[0]["mystic"]
                    markup = playing[0]["markup"]
                except:
                    continue
                try:
                    check = checker[chat_id][mystic.message_id]
                    if check is False:
                        continue
                except:
                    pass
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")
                try:
                    buttons = (
                        stream_markup_timer(
                            _,
                            playing[0]["vidid"],
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                        if markup == "stream"
                        else telegram_markup_timer(
                            _,
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                    )
                    await mystic.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                except:
                    continue
            except:
                continue


asyncio.create_task(markup_timer())
