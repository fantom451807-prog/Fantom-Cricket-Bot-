from pyrogram import Client, filters
from database import get_user_collection

@Client.on_message(filters.command("mycollection"))
async def collection_handler(client, message):
    user_id = message.from_user.id
    data = get_user_collection(user_id) # Returns list of (name, rarity)

    if not data:
        return await message.reply_text("🎒 <b>Your bag is empty!</b> Catch some players first.")

    # Grouping logic
    stats = {}
    for name, rarity in data:
        key = f"{name} [{rarity}]"
        stats[key] = stats.get(key, 0) + 1

    msg = f"👤 <b>{message.from_user.first_name}'s Collection</b>\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    for i, (player, count) in enumerate(stats.items(), 1):
        multiplier = f" <b>({count})</b>" if count > 1 else ""
        msg += f"{i}. {player}{multiplier}\n"
    
    msg += "━━━━━━━━━━━━━━━━━━━━"
    await message.reply_text(msg)