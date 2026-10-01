from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers.start import start_router
# from handlers.menu import menu_router
# from handlers.register import register_router

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    # dp.include_router(menu_router)
    # dp.include_router(register_router)
    print("🔥 SUGO Bot está corriendo correctamente... 💎")

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())