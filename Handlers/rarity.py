from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("rarity"))
async def rarity_command(client, message):
    # Professional Header with Cool Fonts
    text = (
        "╔═══════════════════╗\n"
        "  ✨ 𝖢𝖱𝖨𝖢𝖪𝖤𝖳-𝖷 𝖱𝖠𝖱𝖨𝖳𝖨𝖤𝖲 ✨\n"
        "╚═══════════════════╝\n\n"
        "📊 **𝖣𝗂𝗌𝖼𝗈𝗏𝖾𝗋 𝗍𝗁𝖾 𝖣𝗂𝗏𝗂𝗇𝖾 𝖧𝗂𝖾𝗋𝖺𝗋𝖼𝗁𝗒**\n"
        "𝖤𝗏𝖾𝗋𝗒 𝖼𝖺𝗋𝖽 𝗁𝖺𝗌 𝗂𝗍𝗌 𝗈𝗐𝗇 𝗌𝗍𝖺𝗍𝗎𝗌. 𝖧𝖾𝗋𝖾 𝗂𝗌 𝗍𝗁𝖾 \n"
        "𝗅𝗂𝗌𝗍 𝗈𝖿 𝖺𝗅𝗅 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗋𝖺𝗋𝗂𝗍𝗂𝖾𝗌:\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ 𝖱𝗈𝗈𝗄𝗂𝖾 (𝖢𝗈𝗆𝗆𝗈𝗇)\n"
        "2️⃣ 𝖡𝗋𝗈𝗇𝗓𝖾\n"
        "3️⃣ 𝖲𝗂𝗅𝗏𝖾𝗋\n"
        "4️⃣ 𝖫𝖾𝗀𝖾𝗇𝖽𝖺𝗋𝗒\n"
        "5️⃣ 𝖤𝗅𝗂𝗍𝖾\n"
        "6️⃣ 𝖬𝖺𝗌𝗍𝖾𝗋\n"
        "7️⃣ 𝖧𝖾𝗋𝗈𝗂𝖼\n"
        "8️⃣ 𝖦𝖮𝖠𝖳! (𝖴𝗅𝗍𝗂𝗆𝖺𝗍𝖾)\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 *𝖧𝗂𝗀𝗁𝖾𝗋 𝗋𝖺𝗋𝗂𝗍𝗒 𝖼𝖺𝗋𝖽𝗌 𝖺𝗋𝖾 𝗁𝖺𝗋𝖽𝖾𝗋 𝗍𝗈 𝖼𝗈𝗅𝗅𝖾c𝗍!*"
    )

    # Buttons for more info or interaction
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏆 𝖫𝖾𝖺𝖽𝖾𝗋𝖻𝗈𝖺𝗋𝖽", callback_data="coming_soon"),
            InlineKeyboardButton("💎 𝖲𝗁𝗈𝗉", callback_data="coming_soon")
        ],
        [
            InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄 𝗍𝗈 𝖧𝖾𝗅𝗉", callback_data="main_help")
        ]
    ])

    await message.reply_text(
        text=text,
        reply_markup=keyboard
    )

# Callback for 'Coming Soon' alerts
@Client.on_callback_query(filters.regex("coming_soon"))
async def coming_soon_alert(client, callback_query):
    await callback_query.answer("🚀 This feature is coming soon in the next update!", show_alert=True)