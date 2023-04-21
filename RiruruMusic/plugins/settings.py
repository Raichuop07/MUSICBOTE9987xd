from strings import get_command
from config import BANNED_USERS, MUSIC_BOT_NAME, OWNER_ID, START_IMG_URL

from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaPhoto, InputMediaVideo, Message)

from RiruruMusic import app
from RiruruMusic.utils.database import (
    add_nonadmin_chat, cleanmode_off, cleanmode_on,
    commanddelete_off, commanddelete_on, get_aud_bit_name,
    get_authuser, get_authuser_names, get_served_chats,
    get_served_users, get_playmode, get_playtype,
    get_vid_bit_name, is_cleanmode_on, is_commanddelete_on,
    is_nonadmin_chat, is_suggestion, remove_nonadmin_chat,
    save_audio_bitrate, save_video_bitrate, set_playmode, set_playtype,
    suggestion_off, suggestion_on)
from RiruruMusic.utils.inline.settings import (
    audio_quality_markup, auth_users_markup,
    playmode_users_markup, setting_markup,
    video_quality_markup, vote_mode_markup,
    cleanmode_settings_markup)
from RiruruMusic.utils.inline.start import private_panel
from RiruruMusic.utils.decorators.admins import ActualAdminCB
from RiruruMusic.utils.decorators.language import language, languageCB
from RiruruMusic.utils.database.memorydatabase import get_upvote_count, is_skipmode, set_upvotes

### Command
SETTINGS_COMMAND = get_command("SETTINGS_COMMAND")


@app.on_message(
    filters.command(SETTINGS_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def settings_mar(client, message: Message, _):
    buttons = setting_markup(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(
    filters.regex("settings_helper") & ~BANNED_USERS
)
@languageCB
async def settings_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_8"])
    except:
        pass
    buttons = setting_markup(_)
    return await CallbackQuery.edit_message_text(
        _["setting_1"].format(CallbackQuery.message.chat.title, CallbackQuery.message.chat.id),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(client, CallbackQuery: CallbackQuery,_):
    try:
        await CallbackQuery.answer()
    except:
        pass
    if CallbackQuery.message.chat.type == "private":
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        buttons = private_panel(_, app.username, OWNER)
        image = START_IMG_URL
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        await CallbackQuery.edit_message_media(
            InputMediaPhoto(
                media=image,
                caption=_["start_2"].format(
                    CallbackQuery.from_user.first_name, MUSIC_BOT_NAME, served_users, served_chats
                ),
            ),
        )
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = setting_markup(_)
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


## Audio and Video Quality
async def gen_buttons_aud(_, aud):
    if aud == "High":
        buttons = audio_quality_markup(_, high=True)
    elif aud == "Medium":
        buttons = audio_quality_markup(_, medium=True)
    elif aud == "Low":
        buttons = audio_quality_markup(_, low=True)
    return buttons


async def gen_buttons_vid(_, aud):
    if aud == "High":
        buttons = video_quality_markup(_, high=True)
    elif aud == "Medium":
        buttons = video_quality_markup(_, medium=True)
    elif aud == "Low":
        buttons = video_quality_markup(_, low=True)
    return buttons


# without admin rights


@app.on_callback_query(
    filters.regex(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|CMANSWER|COMMANDANSWER|SUGGANSWER|ANSWERVOMODE|VOTEANSWER|CM|AQ|VQ|PM|AU|VM)$"
    )
    & ~BANNED_USERS
)
@languageCB
async def without_Admin_rights(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "SEARCHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_3"], show_alert=True)
        except:
            return
    elif command == "PLAYMODEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_10"], show_alert=True)
        except:
            return
    elif command == "PLAYTYPEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_11"], show_alert=True)
        except:
            return
    elif command == "AUTHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_4"], show_alert=True)
        except:
            return
    elif command == "COMMANDANSWER":
        try:
            return await CallbackQuery.answer(_["setting_14"], show_alert=True)
        except:
            return
    elif command == "VOTEANSWER":
        try:
            return await CallbackQuery.answer(
                "ᴡʜᴇɴ ᴛʜɪs ᴍᴏᴅᴇ ɪs ᴇɴᴀʙʟᴇᴅ, ɴᴏɴ-ᴀᴅᴍɪɴ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs ʙʏ ᴠᴏᴛᴇs.",
                show_alert=True,
            )
        except:
            return
    elif command == "ANSWERVOMODE":
        current = await get_upvote_count(CallbackQuery.message.chat.id)
        try:
            return await CallbackQuery.answer(
                f"ᴄᴜʀʀᴇɴᴛ ᴜᴘᴠᴏᴛᴇs ʀᴇǫᴜɪʀᴇᴅ ғᴏʀ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs : \n\n{current}",
                show_alert=True,
            )
        except:
            return
    elif command == "AQ":
        try:
            await CallbackQuery.answer(_["set_cb_1"], show_alert=True)
        except:
            pass
        aud = await get_aud_bit_name(CallbackQuery.message.chat.id)
        buttons = await gen_buttons_aud(_, aud)
    elif command == "VQ":
        try:
            await CallbackQuery.answer(_["set_cb_2"], show_alert=True)
        except:
            pass
        aud = await get_vid_bit_name(CallbackQuery.message.chat.id)
        buttons = await gen_buttons_vid(_, aud)
    elif command == "PM":
        try:
            await CallbackQuery.answer(_["set_cb_4"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        Direct = True if playmode == "Direct" else None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        Group = None if is_non_admin else True
        playty = await get_playtype(CallbackQuery.message.chat.id)
        Playtype = None if playty == "Everyone" else True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    
    elif command == "AU":
        try:
            await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            buttons = auth_users_markup(_, True)
        else:
            buttons = auth_users_markup(_)
    elif command == "VM":
        mode = await is_skipmode(CallbackQuery.message.chat.id)
        current = await get_upvote_count(CallbackQuery.message.chat.id)
        buttons = vote_mode_markup(_, current, mode)

    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return

@app.on_callback_query(filters.regex("FERRARIUDTI") & ~BANNED_USERS)
@ActualAdminCB
async def addition(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    mode = callback_data.split(None, 1)[1]
    if not await is_skipmode(CallbackQuery.message.chat.id):
        return await CallbackQuery.answer("Voting Mode is Disabled", show_alert=True)
    current = await get_upvote_count(CallbackQuery.message.chat.id)
    if mode == "M":
        final = current - 2
        if final == 0:
            return await CallbackQuery.answer("Lowest upvotes count can be 2.", show_alert=True)
        elif final <= 2:
            final = 2
            await set_upvotes(CallbackQuery.message.chat.id, final)
    else:
        final = current + 2
        if final == 17:
            return await CallbackQuery.answer("Highest upvotes count can be 15.", show_alert=True)
        elif final >= 15:
            final = 15
            await set_upvotes(CallbackQuery.message.chat.id, final)
    buttons = vote_mode_markup(_, final, True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return

# Audio Video Quality


@app.on_callback_query(
    filters.regex(pattern=r"^(LQA|MQA|HQA|LQV|MQV|HQV)$")
    & ~BANNED_USERS
)
@ActualAdminCB
async def aud_vid_cb(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "LQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Low")
        buttons = audio_quality_markup(_, low=True)
    elif command == "MQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Medium")
        buttons = audio_quality_markup(_, medium=True)
    elif command == "HQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "High")
        buttons = audio_quality_markup(_, high=True)
    elif command == "LQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "Low")
        buttons = video_quality_markup(_, low=True)
    elif command == "MQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "Medium")
        buttons = video_quality_markup(_, medium=True)
    elif command == "HQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "High")
        buttons = video_quality_markup(_, high=True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Play Mode Settings
@app.on_callback_query(
    filters.regex(
        pattern=r"^(|MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$"
    )
    & ~BANNED_USERS
)
@ActualAdminCB
async def playmode_ans(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "CHANNELMODECHANGE":
        is_non_admin = await is_nonadmin_chat(
            CallbackQuery.message.chat.id
        )
        if is_non_admin:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = True
        else:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = None
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    elif command == "MODECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            await set_playmode(CallbackQuery.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(CallbackQuery.message.chat.id, "Direct")
            Direct = True
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            Group = None
        else:
            Group = True
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = False
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    elif command == "PLAYTYPECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            await set_playtype(CallbackQuery.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(CallbackQuery.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            Group = None
        else:
            Group = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Auth Users Settings
@app.on_callback_query(
    filters.regex(pattern=r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS
)
@ActualAdminCB
async def authusers_mar(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "AUTHLIST":
        _authusers = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _authusers:
            try:
                return await CallbackQuery.answer(_["setting_5"], show_alert=True)
            except:
                return
        else:
            try:
                await CallbackQuery.answer(_["set_cb_7"], show_alert=True)
            except:
                pass
            j = 0
            await CallbackQuery.edit_message_text(_["auth_6"])
            msg = _["auth_7"]
            for note in _authusers:
                _note = await get_authuser(CallbackQuery.message.chat.id, note)
                user_id = _note["auth_user_id"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await client.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += (
                    f"   {_['auth_8']} {admin_name}[`{admin_id}`]\n\n"
                )
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"AU"),
                        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close")
                    ]
                ]
            )
            try:
                return await CallbackQuery.edit_message_text(
                    msg, reply_markup=upl
                )
            except MessageNotModified:
                return
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "AUTH":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_, True)
        else:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


## Clean Mode


@app.on_callback_query(
    filters.regex(pattern=r"^(CLEANMODE|COMMANDELMODE|SUGGESTIONCHANGE)$")
    & ~BANNED_USERS
)
@ActualAdminCB
async def cleanmode_mark(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass

    if command == "CLEANMODE":
        sta = None
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            sta = True
        sug = None
        if await is_suggestion(CallbackQuery.message.chat.id):
            sug = True
        cle = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            await cleanmode_off(CallbackQuery.message.chat.id)
        else:
            await cleanmode_on(CallbackQuery.message.chat.id)
            cle = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta, sug=sug)
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif command == "COMMANDELMODE":
        cle = None
        sta = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            cle = True
        sug = None
        if await is_suggestion(CallbackQuery.message.chat.id):
            sug = True
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            await commanddelete_off(CallbackQuery.message.chat.id)
        else:
            await commanddelete_on(CallbackQuery.message.chat.id)
            sta = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta, sug=sug)

    elif command == "SUGGESTIONCHANGE":
        cle = None
        sta = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            cle = True
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            sta = True
        if await is_suggestion(CallbackQuery.message.chat.id):
            await suggestion_off(CallbackQuery.message.chat.id)
            sug = False
        else:
            await suggestion_on(CallbackQuery.message.chat.id)
            sug = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta, sug=sug)

    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return
