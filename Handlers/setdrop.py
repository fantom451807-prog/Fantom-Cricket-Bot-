from pyrogram import Client, filters
from database import get_random_player
from config import ADMIN_IDS

# Memory storage
drop_config = {} 
last_dropped = {} 

@Client.on_message(filters.command("setdrop") & filters.user(ADMIN_IDS))
async def setdrop(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ **Usage:** `/setdrop 5` (Drops after 5 messages)")
    
    try:
        limit = int(message.command[1])
        drop_config[message.chat.id] = [limit, 0]
        await message.reply(f"✅ **Drop Frequency set to {limit} messages!**")
    except ValueError:
        await message.reply("❌ Please provide a valid number.")

@Client.on_message(filters.group & ~filters.bot)
async def monitor_messages(client, message):
    chat_id = message.chat.id
    if chat_id not in drop_config:
        return
    
    drop_config[chat_id][1] += 1
    if drop_config[chat_id][1] >= drop_config[chat_id][0]:
        drop_config[chat_id][1] = 0
        
        p = get_random_player()
        if not p: return
        
        name, rarity, file_id = p
        last_dropped[chat_id] = {"name": name.lower(), "rarity": rarity}
        
        await message.reply_photo(
            photo=file_id, 
            caption=(
                f"🚀 **A WILD PLAYER APPEARED!**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💎 **Rarity:** {rarity}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Type `/collect <name>` to grab this player!"
            )
        )