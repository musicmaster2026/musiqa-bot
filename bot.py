import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Salom! Men avtomatik musiqa qidiruvchi botman.\n"
        "Menga qoʻshiq nomi yoki ijrochini yozib yuboring, men uni topib beraman!"
    )

@dp.message()
async def search_and_send_music(message: types.Message):
    query = message.text
    status_msg = await message.answer("🔍 Qoʻshiq qidirilmoqda, iltimos kuting...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if not info['entries']:
                await status_msg.edit_text("❌ Afsuski, bunday qoʻshiq topilmadi.")
                return

            video_info = info['entries'][0]
            filename = f"{video_info['title']}.mp3"
            title = video_info.get('title', 'Musiqa')

            await status_msg.edit_text("📤 Musiqa topildi! Telegram'ga yuklanmoqda...")
            audio_file = types.FSInputFile(filename)
            await message.answer_audio(audio=audio_file, title=title)
            
            if os.path.exists(filename):
                os.remove(filename)
            await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("⚠️ Xatolik yuz berdi. Keyinroq qayta urinib koʻring.")
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
