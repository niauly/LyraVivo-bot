import os
import asyncio
from telegram import Bot
from telegram.constants import ChatAction
from datetime import datetime
from pathlib import Path

# === CONFIGURAZIONE === #
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
AUDIO_DIR = Path("etere_audio_temp")  # Cartella dei vocali locali
INTERVAL_MIN = 14400  # 4 ore
INTERVAL_MAX = 28800  # 8 ore

bot = Bot(token=BOT_TOKEN)

# === GESTIONE FILE AUDIO === #
def get_etere_files():
    """Ritorna la lista dei file .ogg presenti nella cartella audio."""
    return sorted(AUDIO_DIR.glob("*.ogg"))

def delete_file(path):
    """Cancella un file se esiste."""
    try:
        path.unlink()
    except Exception as e:
        print(f"Errore nella cancellazione di {path}: {e}")

# === INVIO ETERE === #
async def invia_etere():
    print("[Lyra] Sistema avviato. In attesa di invio vocale...")
    while True:
        etere_files = get_etere_files()

        if not etere_files:
            print("[Lyra] Nessun vocale trovato. Aspetto 10 minuti...")
            await asyncio.sleep(600)
            continue

        vocal = etere_files[0]  # Invio il primo della lista

        await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.RECORD_VOICE)
        await asyncio.sleep(2)

        with open(vocal, "rb") as audio:
            await bot.send_voice(chat_id=CHAT_ID, voice=audio)

        ora = datetime.now().strftime("%H:%M:%S")
        print(f"[{ora}] Etere inviato: {vocal.name}")

        delete_file(vocal)  # Cancello dopo invio

        await asyncio.sleep(INTERVAL_MIN)  # Aspetto il minimo previsto

if __name__ == "__main__":
    asyncio.run(invia_etere())
