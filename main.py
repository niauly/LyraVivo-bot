
import os
import asyncio
import random
from telegram import Bot
from datetime import datetime
from telegram.constants import ChatAction

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

etere_vocali = [
    "https://github.com/niauly/LyraVivo/raw/main/static/etere1.ogg",
    "https://github.com/niauly/LyraVivo/raw/main/static/etere2.ogg",
    "https://github.com/niauly/LyraVivo/raw/main/static/etere3.ogg"
]

async def invia_etere():
    while True:
        vocal = random.choice(etere_vocali)
        await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.RECORD_VOICE)
        await asyncio.sleep(2)
        await bot.send_voice(chat_id=CHAT_ID, voice=vocal)
        ora = datetime.now().strftime("%H:%M:%S")
        print(f"[{ora}] Etere inviato.")
        await asyncio.sleep(random.randint(14400, 28800))  # tra 4 e 8 ore

if __name__ == "__main__":
    asyncio.run(invia_etere())
