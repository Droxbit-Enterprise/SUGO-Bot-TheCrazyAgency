from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import RegistroStates, MenuStates
from functions import *
from config import *
from utils.api import *

menu_router = Router()

#############-------------- REINICIO DEL CHAT --------------############# No Terminado
# Se ejecuta si la chica dice que es menor de edad y vuelve a responder si la misma chica escribe de nuevo
@menu_router.message(F.text.lower().in_({"volver al menu", "volver al menú", "Volver al menú", "Volver al menu"}))
async def volver_menu_principal(message: Message, state: FSMContext):
    await asyncio.sleep(0.2)
    await message.answer(
        "Menú principal\n"
        "¿Qué deseas hacer hoy?",
        reply_markup=menu_principal()
    )
    await state.set_state(MenuStates.menu_principal)


###-------- Menu principal --------------###
@menu_router.message(MenuStates.menu_principal)
async def muestra_menu_principal(message: Message, state: FSMContext):
    texto = message.text.lower()
    if "Perfil y verificaciones" in texto or "perfil y verificaciones" in texto:
        await asyncio.sleep(0.2)
        await message.answer(
            "Perfil y verificaciones.\n"
            "Elige una opción y te explicaré todo paso a paso",
            reply_markup=menu_perfil_verificaciones()
        )
    elif message.text == "Como Genero Dinero" or message.text == "Retiro De Dinero" or message.text == "Reglas de Sugo" or message.text == "¿Cómo invito a una amiga?" or message.text == "Estadisticas" or message.text == "Tengo una duda":
        await asyncio.sleep(0.2)
        await message.answer(
            "Lo siento por el momento aún Sigo en Desarrollo.\n"
            "Pero tan pronto el líder me terminé de programar estaré aquí para ayudarte en todo lo que necesites ;) \n\n"
            "Puedes comunicarte con nuestro líder aqui @thecrazyagency",
            reply_markup=menu_principal()
        )