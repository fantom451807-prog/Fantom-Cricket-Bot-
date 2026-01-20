from pyrogram import Client, filters
from config import ADMIN_IDS, OWNER_ID
from database import ban_user, unban_user, is_user_banned

# Command handler for /ban and /unban
@Client.on_message(filters.command(["ban", "unban"]) & filters.user(ADMIN_IDS))
async def ban_unban_handler(client, message):
    # If not a reply and no ID provided
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("❌ **Usage:** Reply to a user or provide their ID.\nExample: `/ban 1234567` or reply with `/ban`")
        return

    # Extracting User ID and Name
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
    else:
        try:
            target_id = int(message.command[1])
            target_name = f"User {target_id}"
        except ValueError:
            await message.reply_text("❌ Please provide a valid numerical User ID.")
            return

    admin_id = message.from_user.id

    if message.command[0] == "ban":
        # 1. Check if trying to ban the Owner
        if target_id == OWNER_ID:
            await message.reply_text("🚫 **Error:** You cannot ban the Sovereign Owner!")
            return
        
        # 2. Check if an Admin is trying to ban another Admin (Only Owner can ban Admins)
        if target_id in ADMIN_IDS and admin_id != OWNER_ID:
            await message.reply_text("🚫 **Permission Denied:** Only the Owner can ban other Admins.")
            return

        ban_user(target_id)
        await message.reply_text(f"⚔️ **User Banned!**\n👤 **Name:** {target_name}\n🆔 **ID:** `{target_id}`\n\nThe bot will now ignore this user.")
    
    elif message.command[0] == "unban":
        unban_user(target_id)
        await message.reply_text(f"✅ **User Unbanned!**\n👤 **Name:** {target_name}\n\nUser can now interact with the bot again.")

# Middleware to block banned users
@Client.on_message(group=-1)
async def check_ban(client, message):
    if message.from_user and is_user_banned(message.from_user.id):
        # Stop everything if user is banned
        await message.stop_propagation()