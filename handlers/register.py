from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import RegistroStates, MenuStates, UsuariaRegistroStates
from database import save_user_full, update_user_field, get_user
from handlers.menu import menu_principal
from functions import *
from config import *

register_router = Router()

###-------- REGISTRAR USUARIA NUEVA --------------###
@register_router.message(UsuariaRegistroStates.nombre)
async def registrar_nombre(message: Message, state: FSMContext):
    nombre = message.text.strip()
    await state.update_data(nombre=nombre)
    update_user_field(message.from_user.id, "nombre", nombre)
    await typing(message, 1)
    await message.answer("Listo 💛 Ahora dime tu *apellido*:")
    await state.set_state(UsuariaRegistroStates.apellido)

###-------- REGISTRAR APELLIDOS --------------###
@register_router.message(UsuariaRegistroStates.apellido)
async def registrar_apellido(message: Message, state: FSMContext):
    apellido = message.text.strip()
    await state.update_data(apellido=apellido)  
    update_user_field(message.from_user.id, "apellido", apellido)
    await typing(message, 1)
    await message.answer("Vale 💛 el documento y teléfono solo se usará para recuperar tu cuenta en caso de ser necesaria.\n\n"
                         "Puedes revisar nuestras politicas de privacidad aqui: https://thecrazyagency.com/política-de-privacidad/\n\n"
                         "Ahora digame tu *documento de identidad*:")
    await state.set_state(UsuariaRegistroStates.doc)

###-------- REGISTRAR DOCUMENTO --------------###
@register_router.message(UsuariaRegistroStates.doc)
async def registrar_documento(message: Message, state: FSMContext):
    documento = message.text.strip()
    await state.update_data(documento=documento)
    await typing(message, 1)
    await message.answer(
        "Perfecto 💛\nAhora Selecciona tu *país*:",
        reply_markup=botones_paises()
    )
    await state.set_state(UsuariaRegistroStates.pais)
    
###-------- REGISTRAR PAIS --------------###
@register_router.message(UsuariaRegistroStates.pais)
async def registrar_pais(message: Message, state: FSMContext):
    pais_texto = message.text.strip()
    print("Pais Seleccionado:", pais_texto)
    # Convertir texto → código
    pais_codigo = obtener_codigo_pais(pais_texto)
    if pais_codigo is None:
        return await message.answer(
            f"❌ *{pais_texto}* no es una elección válida.\n"
            "Por favor selecciona un país de la lista.",
            reply_markup=botones_paises()
        )
        
    await state.update_data(pais=pais_codigo)
    await typing(message, 1)
    await message.answer(
        "Vale vale, ahora digame su *Numero de Telefono*:\nEl teléfono debe tener 10 digitos, sin espacios ni símbolos.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UsuariaRegistroStates.telefono)

###-------- REGISTRAR TELEFONO --------------###
@register_router.message(UsuariaRegistroStates.telefono)
async def registrar_telefono(message: Message, state: FSMContext):
    telefono = message.text.strip()
    # Validar que sean solo números y exactamente 10 dígitos
    if not telefono.isdigit() or len(telefono) != 10:
        return await message.answer("❌ El teléfono debe tener exactamente *10 números* sin espacios ni símbolos.")

    await state.update_data(telefono=telefono)
    await typing(message, 1)
    await message.answer("Listo ok 💛\nAhora vamos a crear un *PIN de 4 números*:")
    await state.set_state(UsuariaRegistroStates.pin)
    
###-------- REGISTRAR PIN 4 NUMEROS --------------###
@register_router.message(UsuariaRegistroStates.pin)
async def registrar_pin(message: Message, state: FSMContext):
    pin = message.text.strip()
    # Validar PIN de 4 números
    if not pin.isdigit() or len(pin) != 4:
        return await message.answer("❌ El PIN debe ser de *4 números*.")

    await state.update_data(pin=pin)
    await typing(message, 1)
    await message.answer(
        "Vale listo señorita, ahora dale en *Continuar* para finalizar tu registro 💎",
        reply_markup=boton_continuar()
    )
    await state.set_state(UsuariaRegistroStates.valida_registro_api)

###-------- VALIDAR REGISTRO EN API --------------###
@register_router.message(UsuariaRegistroStates.valida_registro_api)
async def validar_registro_api(message: Message, state: FSMContext):
    if message.text.lower() != "continuar":
        return await message.answer(
            "Por favor presiona *Continuar* para finalizar tu registro 💛",
            reply_markup=boton_continuar()
        )

    data = await state.get_data()
    print("data almacenada", data)    
    
    import requests
    url = "http://localhost:8000/api/register/"
    payload = {
        'first_name': data["nombre"],
        'last_name': data["apellido"],
        'country': data["pais"],
        'document': data["documento"],
        'telegram_number': data["telefono"],
        'whatsapp_number': data["telefono"],
        'phone': data["telefono"],
        'password': data["pin"],
    }
    try:
        response = requests.post(url, data=payload)
        api_json = response.json()
        print("API RESPONSE:", api_json)
    except Exception as e:
        # Error crítico en la API
        await bot.send_message(
            GROUP_ID,
            f"❌ *ERROR API REGISTRO*\n"
            f"Usuario: @{message.from_user.username}\n"
            f"ID: {message.from_user.id}\n"
            f"Error: {str(e)}"
        )
        return await message.answer(
            "❌ Hubo un error al conectar con la plataforma.\n"
            "Por favor presiona *Continuar* para intentarlo de nuevo 💛",
            reply_markup=boton_continuar()
        )
        
    # Validar respuesta de la API
    if api_json.get("message") != "Registro exitoso":
        # Notificar al grupo
        await bot.send_message(
            GROUP_ID,
            f"⚠️ *Registro fallido en API*\n"
            f"Usuario: @{message.from_user.username}\n"
            f"ID: {message.from_user.id}\n"
            f"Respuesta API: {api_json}"
        )

        return await message.answer(
            "❌ No pudimos completar tu registro.\n"
            "Por favor presiona *Continuar* para intentarlo nuevamente 💛",
            reply_markup=boton_continuar()
        )
        
    update_user_field(message.from_user.id, "registrada", 1)
    # Si llega aquí → registro exitoso
    # token = api_json.get("token")
    # if token:
    #     update_user_field(message.from_user.id, "token", token)
    
    await bot.send_message(
        GROUP_ID,
        f"💎 *Nueva chica interesada en generar ingresos* 💸\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {message.from_user.id}\n\n"
        f"⚠️ Equipo, estén pendientes: acaba de iniciar el proceso de registro."
    )
    await typing(message, 1)
    user = get_user(message.from_user.id)
    await message.answer(
        "✨ *Registro completado exitosamente*.\n"
        "En cualquier momento puedes inciar sesion en nuestro sitio web:\nhttps://thecrazyagency.com/usuarias/iniciar-sesion/\n\n"
        "Ahora elige la app con la que deseas trabajar 💛",
        reply_markup=menu_principal(user)
    )
    await state.set_state(MenuStates.menu_principal)
