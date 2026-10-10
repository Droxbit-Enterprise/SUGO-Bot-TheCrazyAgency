import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import *

# Función para enviar mensaje a Tema SUGO 
async def send_sugo(bot: Bot, text: str):
    await bot.send_message(
        chat_id=GROUP_ID,
        message_thread_id=TOPIC_SUGO,
        text=text
    )

# Función para enviar mensaje a Tema SOPORTE 
async def send_soporte(bot: Bot, text: str):
    await bot.send_message(
        chat_id=GROUP_ID,
        message_thread_id=TOPIC_SOPORTE,
        text=f"⚠️ Error detectado en SUGO Bot\n\n{text}"
    )

# Función para Enviar mensajes a Tema SOPORTE de Errores de API
async def report_api_error(bot, endpoint: str, error: str):
    await send_soporte(bot,
        f"📌 Endpoint: {endpoint}\n"
        f"💬 Detalle: {error}"
    )

# Funcion para determinar el paso de la chica 
def status_process(datos, validador):
    estado = None
    arreglo = {}
    if datos["full_name"]:
        texto  = datos["full_name"]
        nombre = texto.split()[0]
        
    if datos["is_under_18"] == True:
        arreglo = {"full_name":texto, "nombre":nombre, "is_under_18":True}
        estado = 0
    elif datos["full_name"] and datos["is_adult"]==False and datos["country"]==None and datos["accepts_requirements"]==False and datos["phone"]==None:       
        arreglo = {"full_name":texto, "nombre":nombre}
        estado = 1
    elif datos["full_name"] and datos["is_adult"]==True and datos["country"]==None and datos["accepts_requirements"]==False and datos["phone"]==None:
        arreglo = {"full_name":texto, "nombre":nombre, "is_adult":True}
        estado = 2
    elif datos["full_name"] and datos["is_adult"]==True and datos["country"] and datos["accepts_requirements"]==False and datos["phone"]==None:        
        arreglo = {"full_name":texto, "nombre":nombre, "is_adult":True, "country":datos["country"]} 
        estado = 3
    elif datos["full_name"] and datos["is_adult"]==True and datos["country"] and datos["accepts_requirements"]==True and datos["phone"]==None:
        arreglo = {"full_name":texto, "nombre":nombre, "is_adult":True, "country":datos["country"], "accepts_requirements":datos["accepts_requirements"]}
        estado = 4
    elif datos["full_name"] and datos["is_adult"]==True and datos["country"] and datos["accepts_requirements"]==True and datos["phone"] and validador.get("message") == 'No Asociado': 
        arreglo = {"streamer":datos["id"], "full_name":texto, "nombre":nombre, "is_adult":True, "country":datos["country"], "accepts_requirements":datos["accepts_requirements"], "phone":datos["phone"]}
        estado = 5
    elif datos["full_name"] and datos["is_adult"]==True and datos["country"] and datos["accepts_requirements"]==True and datos["phone"] and validador.get("message") == 'Asociada sin agencia aun': 
        arreglo = {
            "streamer":datos["id"], "full_name":texto, "nombre":nombre, "is_adult":True, "country":datos["country"], "accepts_requirements":datos["accepts_requirements"], "phone":datos["phone"],
            "status":validador["message"], "app_user_id":validador["app_user_id"]
        }
        estado = 6
    elif datos["full_name"] and datos["is_adult"]==True and datos["country"] and datos["accepts_requirements"]==True and datos["phone"] and validador.get("message") == 'Asociada y en espera de aprobacion de agencia': 
        arreglo = {
            "streamer":datos["id"], "full_name":texto, "nombre":nombre, "is_adult":True, "country":datos["country"], "accepts_requirements":datos["accepts_requirements"], "phone":datos["phone"],
            "status":validador["message"], "app_user_id":validador["app_user_id"],"request_agency_sent":validador["request_agency_sent"], "accepted_by_leader":validador["accepted_by_leader"], "accepted_by_sugo":validador["accepted_by_sugo"], "inside_agency":validador["inside_agency"]
        }
        estado = 7
    elif datos["full_name"] and datos["is_adult"]==True and datos["country"] and datos["accepts_requirements"]==True and datos["phone"] and validador.get("message") == 'Asociada y en Agencia': 
        arreglo = {
            "streamer":datos["id"], "full_name":texto, "nombre":nombre, "is_adult":True, "country":datos["country"], "accepts_requirements":datos["accepts_requirements"], "phone":datos["phone"],
            "status":validador["message"], "app_user_id":validador["app_user_id"],"request_agency_sent":validador["request_agency_sent"], "accepted_by_leader":validador["accepted_by_leader"], "accepted_by_sugo":validador["accepted_by_sugo"], "inside_agency":validador["inside_agency"]
        }
        estado = 8
        
    return estado, arreglo

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

# Botones Sí / No
def botones_si_no():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Sí 💎")
    kb.button(text="No 💸")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Botones de envio de de solicitud
def botones_envio_soli_si_no():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Ya envie mi Solicitud a la agencia 💎")
    kb.button(text="No he enviado la solicitud a la agencia 💸")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Botones de antigua o nueva
def botones_nueva_antigua():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Soy nueva en SUGO")
    kb.button(text="Ya tengo cuenta en SUGO")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Botones de Selección de Paises
def botones_paises():
    kb = ReplyKeyboardBuilder()
    for code, label in COUNTRY_CHOICES:
        kb.button(text=label)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Menu principal 
def menu_principal():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Perfil y verificaciones")
    kb.button(text="Como Genero Dinero")
    kb.button(text="Retiro De Dinero")
    kb.button(text="Reglas de Sugo")
    kb.button(text="¿Cómo invito a una amiga?")
    kb.button(text="Estadisticas")
    kb.button(text="Tengo una duda")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Menu Perfil y verificaciones 
def menu_perfil_verificaciones():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Añadir, Editar Perfil & Fotos")
    kb.button(text="Momentos (Ver / Publicar)")
    kb.button(text="Verificaciones & Etiquetas")
    kb.button(text="Volver al menú")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Menu Como Genero Dinero
def menu_como_generar():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Métodos para Generar")
    kb.button(text="Conversion Diamantes → Dólares")
    kb.button(text="Dónde Buscar Usuarios")
    kb.button(text="Cómo Generar (Chat / Video)")
    kb.button(text="Tareas de Recibir Diamantes")
    kb.button(text="Salas de Audio & Video")
    kb.button(text="Volver al menú")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)