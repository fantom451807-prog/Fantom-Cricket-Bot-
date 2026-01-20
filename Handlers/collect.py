from pyrogram import Client, filters
from database import save_collected_player
from handlers.setdrop import last_dropped

@Client.on_message(filters.command("collect"))
async def collect_player(client, message):
    chat_id = message.chat.id
    if chat_id not in last_dropped:
        return await message.reply("❌ **There is no player to collect right now!**")
    
    if len(message.command) < 2:
        return await message.reply("❌ **Please provide the player name!**")

    guess = " ".join(message.command[1:]).lower()
    correct_data = last_dropped[chat_id]
    
    if guess == correct_data["name"]:
        save_collected_player(message.from_user.id, correct_data["name"].title(), correct_data["rarity"])
        del last_dropped[chat_id]
        await message.reply(f"🎉 **{message.from_user.first_name}** successfully caught **{correct_data['name'].title()}**!")
    else:
        await message.reply("❌ **Wrong name! Look closely and try again.**")