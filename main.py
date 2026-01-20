from pyrogram import Client, types
from config import API_ID, API_HASH, BOT_TOKEN
import logging

# Logging enable karo taaki error dikhe
logging.basicConfig(level=logging.INFO)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "cricket_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="handlers"), # Ensure folder name is exactly 'handlers'
            workers=20
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"✅ Bot is Online: @{me.username}")
        
        # Setting the Menu
        await self.set_bot_commands([
            types.BotCommand("start", "Start the bot ✨"),
            types.BotCommand("mycollection", "View your team 🎒"),
            types.BotCommand("fav", "Favorite player ⭐"),
            types.BotCommand("setdrop", "Set drop rate [Admin] ⚙️"),
            types.BotCommand("addplayer", "Add player [Admin] 🏏")
        ])

if __name__ == "__main__":
    Bot().run()