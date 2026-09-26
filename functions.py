import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Diccionario temporal para mapear IDs internos
user_map = {}
COUNTRY_CHOICES = [
    ('col', '🇨🇴 - Colombia'),
    ('ven', '🇻🇪 - Venezuela'),
    ('arg', '🇦🇷 - Argentina'),
    ('bol', '🇧🇴 - Bolivia'),
    ('chl', '🇨🇱 - Chile'),
    ('crc', '🇨🇷 - Costa Rica'),
    ('dom', '🇩🇴 - República Dominicana'),
    ('ecu', '🇪🇨 - Ecuador'),
    ('slv', '🇸🇻 - El Salvador'),
    ('gtm', '🇬🇹 - Guatemala'),
    ('hnd', '🇭🇳 - Honduras'),
    ('mex', '🇲🇽 - México'),
    ('nic', '🇳🇮 - Nicaragua'),
    ('pan', '🇵🇦 - Panamá'),
    ('par', '🇵🇾 - Paraguay'),
    ('per', '🇵🇪 - Perú'),
    ('pry', '🇵🇷 - Puerto Rico'),
    ('uru', '🇺🇾 - Uruguay'),
]

def obtener_codigo_pais(texto_pais: str):
    for code, label in COUNTRY_CHOICES:
        if texto_pais.strip() == label:
            return code
    return None

def obtener_apps_usuario(user):
    apps = {
        "Sugo": user[2],
        "Timo": user[3],
        "Salsa": user[4],
        "Contigo": user[5],
        "Meyo": user[6],
        "Kito": user[7]
    }
    apps_asociadas = [app for app, value in apps.items() if value not in (None, "", 0)]
    apps_no_asociadas = [app for app, value in apps.items() if value in (None, "", 0)]
    print("apps_asociadas", apps_asociadas, "apps_no_asociadas", apps_no_asociadas)
    return apps_asociadas, apps_no_asociadas

def menu_principal(user):
    apps_asociadas, apps_no_asociadas = obtener_apps_usuario(user)
    kb = ReplyKeyboardBuilder()

    # Si NO tiene apps asociadas → mostrar menú para asociar
    if len(apps_asociadas) == 0:
        for app in apps_no_asociadas:
            kb.button(text=f"Generar 💸 en {app}")
        kb.button(text="Tengo una duda")
        kb.adjust(2)
        return kb.as_markup(resize_keyboard=True)

    # Si SÍ tiene apps asociadas → menú principal normal
    for app in apps_asociadas:
        kb.button(text=f"Gestionar {app}")

    kb.button(text="Quiero generar en otras apps")
    kb.button(text="Tengo una duda")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
# Simulación de escritura
async def typing(message: Message, seconds: int = 2):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(seconds)

# Botones Sí / No
def botones_si_no():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Sí 💎")
    kb.button(text="No 💸")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def botones_registro_login():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Registrarme")
    kb.button(text="Ya estoy Registrada")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def botones_paises():
    kb = ReplyKeyboardBuilder()
    for code, label in COUNTRY_CHOICES:
        kb.button(text=label)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def boton_continuar():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Continuar")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)