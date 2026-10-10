from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers.start import start_router
from handlers.register import register_router
from handlers.menu import menu_router
from utils.api import init_api_session

async def main():
    await init_api_session()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(menu_router)
    print("🔥 SUGO Bot está corriendo correctamente... 💎")
    
    while True:
        try:
            await dp.start_polling(
                bot,
                skip_updates=True,
                handle_signals=False,
                allowed_updates=["message", "callback_query"],
                polling_timeout=2
            )
        except Exception as e:
            print("Error en polling:", e)

        await asyncio.sleep(0.1)  # 🔥 BAJA CPU DRÁSTICAMENTE

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())