
# Fix event loop for Python 3.10+ at the very top
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
from info import *
from body.database import total_user, chnl_ids, get_all_users, get_all_channels



# Fix event loop for Python 3.10+
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Auto Cap",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "body"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.force_channel = FORCE_SUB
        if FORCE_SUB:
            try:
                link = await self.export_chat_invite_link(FORCE_SUB)
                self.invitelink = link
            except Exception as e:
                print(e)
                print("Make Sure Bot admin in force sub channel")
                self.force_channel = None
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")
        await self.send_message(ADMIN, f"**{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️**")

bot = Bot()

# Admin command: /total_users
@bot.on_message(filters.private & filters.user(ADMIN) & filters.command(["total_users"]))
async def total_users_handler(client, message):
    count = await total_user()
    await message.reply_text(f"Total users: <b>{count}</b>")

# Admin command: /total_channels
@bot.on_message(filters.private & filters.user(ADMIN) & filters.command(["total_channels"]))
async def total_channels_handler(client, message):
    count = await chnl_ids.count_documents({})
    await message.reply_text(f"Total channels: <b>{count}</b>")


# Admin command: /users - list all users with names and mention links
@bot.on_message(filters.private & filters.user(ADMIN) & filters.command(["users"]))
async def users_list_handler(client, message):
    users = await get_all_users()
    if not users:
        await message.reply_text("No users found.")
        return
    text = "<b>All Users:</b>\n"
    for user in users:
        user_id = user.get('_id')
        try:
            user_obj = await client.get_users(user_id)
            name = user_obj.first_name or "Unknown"
            mention = user_obj.mention(style="link")
            text += f"ID: <code>{user_id}</code> | Name: {name} | {mention}\n"
        except Exception:
            text += f"ID: <code>{user_id}</code> | Name: Unknown\n"
    if len(text) > 4096:
        for i in range(0, len(text), 4096):
            await message.reply_text(text[i:i+4096], disable_web_page_preview=True)
    else:
        await message.reply_text(text, disable_web_page_preview=True)


# Admin command: /channels - list all channels with names, invite links, captions
@bot.on_message(filters.private & filters.user(ADMIN) & filters.command(["channels"]))
async def channels_list_handler(client, message):
    channels = await get_all_channels()
    if not channels:
        await message.reply_text("No channels found.")
        return
    text = "<b>All Channels:</b>\n"
    for ch in channels:
        ch_id = ch.get('chnl_id')
        caption = ch.get('caption', '')
        try:
            chat = await client.get_chat(ch_id)
            ch_name = chat.title or chat.first_name or "Unknown"
            # Try to get invite link
            try:
                invite_link = chat.invite_link or await client.export_chat_invite_link(ch_id)
            except Exception:
                invite_link = "No invite link"
        except Exception:
            ch_name = "Unknown"
            invite_link = "No invite link"
        text += f"ID: <code>{ch_id}</code> | Name: {ch_name}\nInvite: {invite_link}\nCaption: {caption}\n---\n"
    if len(text) > 4096:
        for i in range(0, len(text), 4096):
            await message.reply_text(text[i:i+4096], disable_web_page_preview=True)
    else:
        await message.reply_text(text, disable_web_page_preview=True)

# Admin command: /stats - show bot statistics
@bot.on_message(filters.private & filters.user(ADMIN) & filters.command(["stats"]))
async def stats_handler(client, message):
    user_count = await total_user()
    channel_count = await chnl_ids.count_documents({})
    await message.reply_text(f"<b>Bot Stats:</b>\nUsers: <code>{user_count}</code>\nChannels: <code>{channel_count}</code>")

    bot.run()
bot.run()