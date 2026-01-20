from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    user_id = message.from_user.id
    is_admin = user_id in ADMIN_IDS

    # Professional Header with Image (Optional: replace with your own link)
    help_img = "https://telegra.ph/file/your_cool_image_link.jpg" # Yahan apni image ka link dalo
    
    header = (
        "╔═══════════════════╗\n"
        "  ✨ 𝖢𝖱𝖨𝖢𝖪𝖤𝖳-𝖷 𝖢𝖤𝖭𝖳𝖱𝖠𝖫 ✨\n"
        "╚═══════════════════╝\n\n"
        "👋 **Welcome to the Elite Pavilion!**\n"
        "Select a category from the buttons below to explore my divine powers.\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )

    # Buttons Setup
    keyboard = [
        [
            InlineKeyboardButton("🌌 𝖴𝗌𝖾𝗋 𝖦𝗎𝗂𝖽𝖾", callback_data="user_help"),
            InlineKeyboardButton("📊 𝖲𝗍𝖺𝗍𝗌", callback_data="bot_stats")
        ],
        [
            InlineKeyboardButton("🛡️ 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/your_support_group")
        ]
    ]

    # Admin Button: Sirf Admins ko dikhega
    if is_admin:
        keyboard.append([InlineKeyboardButton("⚙️ 𝖠𝖽𝗆𝗂𝗇 𝖢𝗈𝗇𝗍𝗋𝗈𝗅", callback_data="admin_help")])

    await message.reply_text(
        text=header,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Callback for Buttons
@Client.on_callback_query(filters.regex("^(user_help|admin_help|bot_stats)$"))
async def help_callback(client, callback_query):
    data = callback_query.data
    
    if data == "user_help":
        text = (
            "📜 **𝖴𝖲𝖤𝖱 𝖢𝖮𝖬𝖬𝖠𝖭𝖣𝖲**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🏏 `/claim` ─ Claim your daily card\n"
            "🔍 `/collect` ─ Guess & catch players\n"
            "🎒 `/mycollection` ─ Your card deck\n"
            "⭐ `/fav` ─ Mark your best card\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
    elif data == "admin_help":
        text = (
            "🛠️ **𝖠𝖣𝖬𝖨𝖭 𝖯𝖠𝖭𝖤𝖫**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "➕ `/addplayer` ─ Create new card\n"
            "📢 `/broadcast` ─ Global message\n"
            "🚫 `/ban` ─ Restrict users\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
    elif data == "bot_stats":
        text = "📊 **𝖡𝖮𝖳 𝖲𝖳𝖠𝖳𝖨𝖲𝖳𝖨𝖢𝖲**\n\nUsers: 1,200+\nCards: 450+\nUptime: 99.9%"

    await callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄", callback_data="main_help")]])
    )

# Back Button Logic
@Client.on_callback_query(filters.regex("main_help"))
async def back_to_main(client, callback_query):
    # Yahan wahi purana header aur main keyboard call kardo
    await help_command(client, callback_query.message)
    await callback_query.message.delete()