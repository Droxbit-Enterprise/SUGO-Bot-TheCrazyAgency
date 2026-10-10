from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from database import get_user, save_user_full, update_user_field
from states import RegistroStates, MenuStates, UsuariaRegistroStates
from functions import *
from config import *
start_router = Router()

###-------- INICIOS DEL BOT --------------###
# Comando /start
@start_router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear() 
    user = get_user(message.from_user.id)    
    print("Verifica si es nueva", user)
    # Si no existe → crearla
    if user is None:
        save_user_full(
            telegram_id=message.from_user.id,
            nombre="",
            sugo_id="",
            timo_id="",
            salsa_id="",
            contigo_id="",
            meyo_id="",
            kito_id="",
            es_mayor=0,
            tiene_wifi=0,
            tiene_tiempo=0,
            registrada=0,
            inicio_sesion=0,
            apellido="",
        )
        user = get_user(message.from_user.id)
        print("Usuaria creada:", user)

    # Si NO está registrada pero ya respondió edad → continuar en WIFI
    if user[8] == 1 and user[9] == 0:
        await asyncio.sleep(0.2)
        await message.answer(
            "Perfecto señorita 💛 Continuemos con tu registro.\n\n"
            "👉 ¿Tienes teléfono propio y acceso a internet estable?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.wifi)
        return

    # Si ya respondió edad + wifi → continuar en disponibilidad
    if user[8] == 1 and user[9] == 1 and user[10] == 0:
        await asyncio.sleep(0.2)
        await message.answer(
            "Perfecto señorita 💛 Continuemos con tu registro.\n\n"
            "👉 ¿Tienes disponibilidad al menos 4 o 6 horas diarias para trabajar?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.disponibilidad)
        return
    
    # Si ya respondió edad + wifi + disponibilidad → continuar en validador_registro
    if user[8] == 1 and user[9] == 1 and user[10] == 1 and user[11] == 0:    
        await asyncio.sleep(0.2)
        # Si ya respondió nombre y apellido → continuar en documento
        if user[1]:
            await state.update_data(nombre=user[1])
            if user[13]:              
                await state.update_data(apellido=user[13])  
                await message.answer(            
                    "Hola, "+user[1]+" "+user[13]+" continuemos con el Registro:\n\n"
                    "el documento y teléfono solo se usará para recuperar tu cuenta en caso de ser necesaria.\n"
                    "Puedes revisar nuestras politicas de privacidad aqui: https://thecrazyagency.com/política-de-privacidad/\n\n"
                    "Ahora digame tu *documento de identidad*:",
                    reply_markup=ReplyKeyboardRemove()
                )
                await state.set_state(UsuariaRegistroStates.doc)
                return
            
            await message.answer(            
                "Hola, "+user[1]+" continuemos con el Registro:\n\n"
                "👉 Ahora dime tu *Apellido* porfavor:",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(UsuariaRegistroStates.apellido)
            return
            
        
        await message.answer(            
            "Hola Regresaste señorita 💛 Continuemos con tu registro.\n"
            "Antes de continuar, necesito validar si ya tienes una cuenta en nuestra plataforma:\n\n"
            "👉 *thecrazyagency.com*\n\n"
            "Por favor elige una opción:",
            reply_markup=botones_registro_login()
        )
        await state.set_state(RegistroStates.validador_usuaria)
        return
    
    
    
    # Si ya está registrada → menú principal
    if user and user[11] == 1 and user[8] == 1 and user[9] == 1 and user[10] == 1:  # columna 'registrada'
        await message.answer(
            "💎 Hola nuevamente señorita.\n¿Qué deseas hacer hoy?",
            reply_markup=menu_principal(user)
        )
        await state.set_state(MenuStates.menu_principal)
        return
    
    # Si NO está registrada → iniciar registro
    await asyncio.sleep(0.2)
    await bot.send_photo(
        message.chat.id,
        photo=URL_STATIC+"Logo+-+The+Crazy+Agency.jpg",
        caption="💛 Bienvenida señorita a The Crazy Agency.\n\n"
                "Somos una agencia de streamers que acompaña a chicas que desean generar ingresos desde casa de forma segura y guiada."
    )
    await asyncio.sleep(0.2)
    await message.answer(
        "Señorita 💛\n"
        "Para iniciar tu registro necesito saber:\n\n"
        "👉 ¿eres mayor de 18?",        
        reply_markup=botones_si_no()
    )
    await state.set_state(RegistroStates.edad)

###-------- REINICIO DEL CHAT --------------###
# Se ejecuta si la chica dice que es menor de edad y vuelve a responder si la misma chica escribe de nuevo
@start_router.message(F.text.lower().in_({"hola", "buenas", "hey", "holi", "ola", "holis", "Holis", "Holi", "Ola", "Hey", "Buenas", "Hola"}))
async def reiniciar_conversacion(message: Message, state: FSMContext):
    await state.clear()
    await asyncio.sleep(0.2)
    await message.answer(
        "💎 Hola señorita, bienvenida nuevamente 💛\n"
        "Vamos a comenzar de nuevo.\n\n"
        "👉 ¿eres mayor de 18?",  
        reply_markup=botones_si_no()
    )
    await state.set_state(RegistroStates.edad)

###-------- PREGUNTA DE EDAD --------------###
@start_router.message(RegistroStates.edad)
async def confirmar_mayor_edad(message: Message, state: FSMContext):
    texto = message.text.lower()
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await state.update_data(es_mayor=1)
        update_user_field(message.from_user.id, "es_mayor", 1)
        await asyncio.sleep(0.2)
        await message.answer(
            "Perfecto 💎\n👉 ¿Tienes teléfono propio y acceso a internet estable?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.wifi)

    elif any(x in texto for x in ["no", "No", "n", "not"]):
        await asyncio.sleep(0.2)
        await state.clear()
        await message.answer(
            "Lo siento señorita 💛, por ahora no puedes continuar.\n"
            "Si deseas volver a empezar cuando seas mayor de edad, solo escribe *hola* o usa el comando /start 💎",
            reply_markup=ReplyKeyboardRemove()
        )        
        await bot.send_message(
            GROUP_ID,
            f"⚠️ La chica es menor de edad\n"
            f"👤 @{message.from_user.username}\n"
            f"💬 Esta chica quiere trabajar pero es menor de edad."
        )
        return

    else:
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Respuesta no reconocida en *edad*\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 {message.text}"
        )
        await message.answer("No entendí tu respuesta señorita 💎, ¿eres mayor de 18?")

###-------- PREGUNTA DE WIFI / TELÉFONO --------------###
@start_router.message(RegistroStates.wifi)
async def confirmar_wifi(message: Message, state: FSMContext):
    texto = message.text.lower()        
    if any(x in texto for x in ["si", "sí", "s", "yes"]):        
        await state.update_data(tiene_wifi=1)
        update_user_field(message.from_user.id, "tiene_wifi", 1)
        await asyncio.sleep(0.2)        
        await message.answer(
            "Perfecto 💎\n👉 ¿Tienes disponibilidad al menos 4 o 6 horas diarias para trabajar?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.disponibilidad)
    
    elif any(x in texto for x in ["no", "No", "n", "not"]):
        await asyncio.sleep(0.2)
        await state.clear()
        await message.answer(
            "Lo siento señorita 💛, necesitas un teléfono e internet estable para trabajar con nosotros, por ahora no puedes continuar.\n"
            "Si deseas volver a empezar cuando Tengas un teléfono y conexión a internet, solo escribe *hola* o usa el comando /start 💎",
            reply_markup=ReplyKeyboardRemove()
        )
        
        return

    else:
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Respuesta no reconocida en *wifi*\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 {message.text}"
        )
        await message.answer("No entendí tu respuesta señorita 💎, ¿tienes un buen teléfono e internet estable?")

###-------- PREGUNTA DE DISPONIBILIDAD --------------###
@start_router.message(RegistroStates.disponibilidad)
async def confirmar_disponibilidad(message: Message, state: FSMContext):
    texto = message.text.lower()    
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await state.update_data(tiene_tiempo=1)
        update_user_field(message.from_user.id, "tiene_tiempo", 1)
        await asyncio.sleep(0.2)
        user = get_user(message.from_user.id)
        await message.answer(
            "Perfecto señorita 💎💸\n"
            "Ya cumples los requisitos minimos para empezar a trabajar con *The Crazy Agency* 💛\n\n",
            reply_markup=ReplyKeyboardRemove()           
        )
        if user[11] == 0: 
            await asyncio.sleep(0.2)
            await message.answer(
                "Antes de continuar, necesito validar si ya tienes una cuenta en nuestra plataforma:\n\n"
                "👉 *thecrazyagency.com*\n\n"
                "Por favor elige una opción:",
                reply_markup=botones_registro_login()
            )
            await state.set_state(RegistroStates.validador_usuaria)
            return
        else:
            await message.answer(
                "Continuemos con el menu principal:\n"
                "¿Qué deseas hacer hoy?",
                reply_markup=menu_principal(user)
            )
            await state.set_state(MenuStates.menu_principal)
            return
            
            
    elif any(x in texto for x in ["no", "No", "n", "not"]):
        await typing(message, 3)
        await state.clear()
        await message.answer(
            "Lo siento señorita 💛, necesitas disponibilidad para trabajar al menos unas 4 a 6 horas diarias 💸 con nosotros, por ahora necesitamos chicas para que generen bien.\n"
            "Si deseas volver a empezar cuando Tengas disponilidad de tiempo para trabajar, solo escribe *hola* o usa el comando /start 💎",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    else:
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Respuesta no reconocida en *disponibilidad*\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 {message.text}"
        )
        await message.answer("No entendí tu respuesta señorita 💎, Tienes disponibilidad al menos 4 o 6 horas diarias para trabajar?")

###-------- VALIDA EL REGISTRO EN PLATAFORMA --------------###
@start_router.message(RegistroStates.validador_usuaria)
async def validador_registro(message: Message, state: FSMContext):
    texto = message.text.lower()    
    # --- REGISTRARME ---
    if "registrarme" in texto:
        await asyncio.sleep(0.2)
        await message.answer(
            "Perfecto señorita, Vamos a crear tu cuenta en nuestra plataforma.\n\n"
            "👉 Primero dime tu *Nombre*:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(UsuariaRegistroStates.nombre)
        return
            
    # --- YA ESTOY REGISTRADA ---
    if "ya estoy registrada" in texto:
        await asyncio.sleep(0.2)
        await message.answer(
            "Perfecto señorita, Vamos a validar tu cuenta.\n\n"
            "👉 Primero dime tu *país*:",
            reply_markup=botones_paises()
        )
        await state.set_state(UsuariaRegistroStates.iniciar_sesion)
        return

    else:
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Respuesta no reconocida en *validador_usuaria*\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 {message.text}"
        )
        await message.answer(
            "No entendí tu respuesta señorita 💎, necesito validar si ya tienes una cuenta en nuestra plataforma?",
            reply_markup=botones_registro_login()
        )
    
    
    
    
    
    # user = get_user(message.from_user.id)    
    # if user[11] == 0:            
    #     await message.answer(
    #         "Ahora cuéntame, ¿con qué aplicación deseas trabajar?  Nosotros de momento trabajamos con estas apps",
    #         reply_markup=menu_principal(user)
    #     )
    #     await state.set_state(RegistroStates.menu)
    # else:            
    #     await message.answer(
    #         "Ahora cuéntame, ¿con qué aplicación deseas trabajar?  Nosotros de momento trabajamos con estas apps",
    #         reply_markup=menu_principal(user)
    #     )
    #     await state.set_state(RegistroStates.menu)
