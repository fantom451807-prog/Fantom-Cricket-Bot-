from pyrogram import Client, filters
import sqlite3
from database import set_fav, get_fav, get_conn

@Client.on_message(filters.command("fav"))
async def fav_handler(client, message):
    user_id = message.from_user.id
    
    if len(message.command) < 2:
        # If just /fav is typed, show the current favorite
        fav = get_fav(user_id)
        if not fav:
            return await message.reply_text("❌ You haven't set a favorite player yet!")
        return await message.reply_photo(fav[1], caption=f"⭐ **Your Favorite Player:** {fav[0]}")

    # Set new favorite
    player_name = " ".join(message.command[1:]).strip()
    
    # Check if user actually owns this player
    conn = get_conn(); cursor = conn.cursor()
    cursor.execute("SELECT name FROM collections WHERE user_id = ? AND LOWER(name) = ?", (user_id, player_name.lower()))
    owned = cursor.fetchone()
    
    if not owned:
        return await message.reply_text("❌ You don't own this player!")

    # Get photo from players table
    cursor.execute("SELECT file_id FROM players WHERE LOWER(name) = ?", (player_name.lower(),))
    photo = cursor.fetchone()
    conn.close()

    if photo:
        set_fav(user_id, owned[0], photo[0])
        await message.reply_text(f"✅ **{owned[0]}** has been set as your favorite!")