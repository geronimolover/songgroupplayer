"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from pyrogram import Client, filters, emoji
from utils import USERNAME, mp
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

msg=Config.msg
CHAT=Config.CHAT
ADMINS=Config.ADMINS
playlist=Config.playlist

HOME_TEXT = "ππ» **Hi [{}](tg://user?id={})**,\n\nI'm **Music Player** \nI Can Play Radio / Music / YouTube Live In Channel & Group 24x7 Nonstop. Made for @song_requestgroup π!"
HELP_TEXT = """
Use these commands in @song_requestgroup
\u2022 `/play` - reply to an audio or youTube link to play it or use /play [song name]
\u2022 `/help` - shows help for commands
\u2022 `/song` [song name] - download the song as audio track
\u2022 `/current` - shows playing time of current track
\u2022 `/playlist` - shows the current playlist with controls

Sorry, I can't help you moreπ
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "You're Not Allowed! π€£",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("π", callback_data="replay"),
                            InlineKeyboardButton("βΈ", callback_data="pause"),
                            InlineKeyboardButton("β­", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Paused !**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("π", callback_data="replay"),
                            InlineKeyboardButton("βΆοΈ", callback_data="resume"),
                            InlineKeyboardButton("β­", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Resumed !**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("π", callback_data="replay"),
                            InlineKeyboardButton("βΈ", callback_data="pause"),
                            InlineKeyboardButton("β­", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Skipped !**\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("π", callback_data="replay"),
                        InlineKeyboardButton("βΈ", callback_data="pause"),
                        InlineKeyboardButton("β­", callback_data="skip")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/free_music123"),
                InlineKeyboardButton("GROUP", url="https://t.me/Song_requestgroup"),
            ],
            [
                InlineKeyboardButton("MOVIE GROUP", url="https://t.me/all_super_movies"),
                InlineKeyboardButton("SOURCE CODE", url="https://telegra.ph/file/21e06a011217f7308c3c9.jpg
"),
            ],
            [
                InlineKeyboardButton("CLOSE π", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=reply_markup

        )

    elif query.data=="close":
        await query.message.delete()


@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/free_music123"),
                InlineKeyboardButton("GROUP", url="https://t.me/Song_requestgroup"),
            ],
            [
                InlineKeyboardButton("MOVIE GROUP", url="https://t.me/all_super_movies"),
                InlineKeyboardButton("SOURCE CODE", url="https://telegra.ph/file/21e06a011217f7308c3c9.jpg
"),
            ],
            [
                InlineKeyboardButton("β HOW TO USE β", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo="https://telegra.ph/file/2cc60cb6ad087b6f14ed7.png", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)



@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/free_music123"),
                InlineKeyboardButton("GROUP", url="https://t.me/Song_requestgroup"),
            ],
            [
                InlineKeyboardButton("MOVIE GROUP", url="https://t.me/all_super_movies"),
                InlineKeyboardButton("SOURCE CODE", url="https://telegra.ph/file/21e06a011217f7308c3c9.jpg
"),
            ],
            [
                InlineKeyboardButton("CLOSE π", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_photo(photo="https://telegra.ph/file/2cc60cb6ad087b6f14ed7.png", caption=HELP_TEXT, reply_markup=reply_markup)
    await mp.delete(message)

