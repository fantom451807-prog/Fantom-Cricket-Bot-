from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from config import ADMIN_IDS, LOG_GROUP_ID
from database import add_player_to_db

# Store data in memory
ADD_PLAYER_DATA = {}

@Client.on_message(filters.command("addplayer") & filters.user(ADMIN_IDS))
async def addplayer_start(client, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("💬 PM ME", url=f"https://t.me/{client.me.username}?start=addplayer")]])
        await message.reply_text("❌ **This command only works in Private Messages!**", reply_markup=keyboard)
        return

    ADD_PLAYER_DATA[message.from_user.id] = {"step": "get_name"}
    await message.reply_text(
        "✨ **Enter Player Name:**",
        reply_markup=ForceReply(selective=True)
    )

@Client.on_message(filters.private & filters.user(ADMIN_IDS) & (filters.text | filters.photo))
async def process_add_player(client, message):
    user_id = message.from_user.id
    if user_id not in ADD_PLAYER_DATA:
        return

    step = ADD_PLAYER_DATA[user_id].get("step")

    if step == "get_name" and message.text:
        ADD_PLAYER_DATA[user_id]["name"] = message.text
        ADD_PLAYER_DATA[user_id]["step"] = "get_rarity"
        
        buttons = [
            [InlineKeyboardButton("⚪ Common", callback_data="rare_Common"), 
             InlineKeyboardButton("🔵 Rare", callback_data="rare_Rare")],
            [InlineKeyboardButton("🟡 Epic", callback_data="rare_Epic"), 
             InlineKeyboardButton("🔴 Legendary", callback_data="rare_Legendary")],
            [InlineKeyboardButton("🔮 Mythic", callback_data="rare_Mythic"), 
             InlineKeyboardButton("🌌 Cosmic", callback_data="rare_Cosmic")],
            [InlineKeyboardButton("💎 Exotic", callback_data="rare_Exotic"), 
             InlineKeyboardButton("🎗️ Event", callback_data="rare_Event")],
            [InlineKeyboardButton("🔥 Limited", callback_data="rare_Limited"), 
             InlineKeyboardButton("🔱 Celestial", callback_data="rare_Celestial")]
        ]
        await message.reply_text(
            f"✅ **Name:** `{message.text}`\n\n**Select Rarity Level:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif step == "get_photo" and message.photo:
        ADD_PLAYER_DATA[user_id]["photo_id"] = message.photo.file_id
        ADD_PLAYER_DATA[user_id]["step"] = "confirm"
        
        name = ADD_PLAYER_DATA[user_id]["name"]
        rarity = ADD_PLAYER_DATA[user_id]["rarity"]
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Confirm & Save", callback_data="final_confirm"),
             InlineKeyboardButton("❌ Cancel", callback_data="final_cancel")]
        ])
        
        await message.reply_photo(
            photo=message.photo.file_id,
            caption=(
                f"𓆩👑 **PLAYER PREVIEW** 👑𓆪\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 **Name:** {name}\n"
                f"💎 **Rarity:** {rarity}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Check details above and click Confirm!"
            ),
            reply_markup=keyboard
        )

# Fixed Callback Logic
@Client.on_callback_query(filters.regex("^(rare_|final_)"))
async def handle_callbacks(client, callback_query):
    user_id = callback_query.from_user.id
    
    if user_id not in ADD_PLAYER_DATA:
        await callback_query.answer("❌ Session Expired! Start again with /addplayer", show_alert=True)
        return

    data = callback_query.data

    if data.startswith("rare_"):
        rarity = data.split("_")[1]
        ADD_PLAYER_DATA[user_id]["rarity"] = rarity
        ADD_PLAYER_DATA[user_id]["step"] = "get_photo"
        await callback_query.edit_message_text(
            f"💎 **Rarity Set:** {rarity}\n\n📸 Now **Send the Player's Photo.**"
        )

    elif data == "final_confirm":
        # Getting data before deleting it
        p_name = ADD_PLAYER_DATA[user_id].get("name")
        p_rarity = ADD_PLAYER_DATA[user_id].get("rarity")
        p_photo = ADD_PLAYER_DATA[user_id].get("photo_id")
        
        if not p_name or not p_photo:
            await callback_query.answer("Error: Data Missing!", show_alert=True)
            return

        # 1. Save to Database
        try:
            add_player_to_db(p_name, p_rarity, p_photo)
        except Exception as e:
            await callback_query.message.edit_caption(f"❌ Database Error: {e}")
            return

        # 2. Update Admin Message
        await callback_query.message.edit_caption("✅ **Successfully added to the System!**")
        await callback_query.answer("Player Saved!", show_alert=True)

        # 3. Send Notification to Group
        try:
            await client.send_photo(
                chat_id=LOG_GROUP_ID,
                photo=p_photo,
                caption=(
                    f"📢 **NEW PLAYER ADDED!**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 **Name:** {p_name}\n"
                    f"💎 **Rarity:** {p_rarity}\n"
                    f"⚡ **Added By:** {callback_query.from_user.mention}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━"
                )
            )
        except Exception as e:
            print(f"Failed to send to group: {e}")

        # Clean up memory
        del ADD_PLAYER_DATA[user_id]

    elif data == "final_cancel":
        await callback_query.message.edit_caption("❌ **Operation Cancelled.**")
        del ADD_PLAYER_DATA[user_id]