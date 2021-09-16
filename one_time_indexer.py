# Cursos Pro Android by Skueletor ©️ 2021
import logging
import logging.config

# Obtener configuraciones de registro
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)

import asyncio
from pyrogram import Client
from info import SESSION, USER_SESSION, API_ID, API_HASH, BOT_TOKEN, CHANNELS
from utils import save_file


async def main():
    """Guarde archivos antiguos en la base de datos con la ayuda del bot de usuario"""

    user_bot = Client(USER_SESSION, API_ID, API_HASH)
    bot = Client(SESSION, API_ID, API_HASH, bot_token=BOT_TOKEN)

    await user_bot.start()
    await bot.start()

    try:
        for channel in CHANNELS:
            async for user_message in user_bot.iter_history(channel):
                message = await bot.get_messages(
                    channel,
                    user_message.message_id,
                    replies=0,
                )
                for file_type in ("document", "video", "audio"):
                    media = getattr(message, file_type, None)
                    if media is not None:
                        break
                else:
                    continue
                media.file_type = file_type
                media.caption = message.caption
                await save_file(media)
    finally:
        await user_bot.stop()
        await bot.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())