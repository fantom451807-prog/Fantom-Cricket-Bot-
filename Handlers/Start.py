from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_user

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user
    add_user(user.id, user.username or "No Username")
    
    caption = (
        f"✨ <b>Welcome to the Arena, {user.first_name}!</b> ✨\n\n"
        f"I am the ultimate <b>CricketX Collector Bot</b>. Build your dream team!\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>Owner:</b> @imfantommm\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("🛡️ Support", url="https://t.me/cricketxcollect")]
    ])

    await message.reply_text(text=caption, reply_markup=keyboard, disable_web_page_preview=True)
