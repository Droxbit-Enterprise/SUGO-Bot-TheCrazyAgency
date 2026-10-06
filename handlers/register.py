from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import RegistroStates, MenuStates, UsuariaRegistroStates
from handlers.menu import menu_principal
from functions import *
from config import *
from utils.api import *

register_router = Router()

#############-------------- REGISTRAR NOMBRE --------------############# 
@register_router.message(RegistroStates.nombre)
async def registrar_nombre(message: Message, state: FSMContext):
    texto  = message.text.strip()   
    partes = texto.split()
    nombre = partes[0]
    apellidos = None
    if len(partes) == 4:
        apellidos = " ".join(partes[2:]) 
    else:        
        apellidos = " ".join(partes[1:]) if len(partes) > 1 else ""
        
    try: 
        telegram_id = message.from_user.id
        await state.update_data(telegram_id=telegram_id, full_name=texto, nombre=nombre, origin_bot=ORIGIN_BOT)
        datos = await state.get_data()
        respuesta = await register_streamer(datos)
        # print("\nREGISTRO Nombre:", respuesta)
        if respuesta.get("message") == 'Registro exitoso':        
            await typing(message, 2)
            await message.answer(
                f"Perfecto señorita {nombre} 🩵 espero estés bien.\n\n"
                f"Nos complace saber que quieres trabajar con nosotros.\n\n"
                "👉 ¿Eres mayor de 18?",
                reply_markup=botones_si_no()
            )
            await state.set_state(RegistroStates.edad)
    except ValueError as e:
        await send_soporte(
            f"La chica al registrar su Nombre no se registró correctamente\n"
            f"Revisar los servidores o API\n"
            f"💬 {e}"
        )
        await message.answer(
            "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
            "Nuestro Líder resolverá el problema y podrás continuar con tu registro\n"
            "Puedes dejarnos tu nombre nuevamente en 5 minutos."
        )

#############-------------- REGISTRAR EDAD --------------############# 
@register_router.message(RegistroStates.edad)
async def confirmar_mayor_edad(message: Message, state: FSMContext):
    texto = message.text.lower()
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        try:
            telegram_id = message.from_user.id 
            respuesta = await update_streamer_fields(telegram_id, {"is_adult": True})
            # print("\nREGISTRO Mayor de Edad:", respuesta)
            await state.update_data(is_adult=1)       
            if respuesta.get("message") == 'Actualización exitosa':  
                await typing(message, 2)
                await message.answer(
                    "Claro señorita ahora…💎\n"
                    "👉 ¿De qué país eres?",
                    reply_markup=botones_paises()
                )
                await state.set_state(RegistroStates.pais)
        except ValueError as e:
            await send_soporte(
                f"La chica al confirmar que es mayor de edad no se actualizó correctamente\n"
                f"Revisar los servidores o API\n"
                f"💬 {e}"
            )
            await message.answer(
                "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
                "Nuestro Líder resolverá el problema y podrás continuar con tu registro\n"
                "Puedes dejarnos saber si eres mayor de 18 años nombre nuevamente en 5 minutos\n"
                "Puedes Responder si o no."
            )


    elif any(x in texto for x in ["no", "No", "n", "not"]):
        await typing(message, 2)
        await message.answer(
            "Lo siento señorita 🩵, por ahora no puedes continuar.\n"
            "Si deseas volver a empezar cuando seas mayor de edad, solo escribe *hola* o usa el comando /start 💎",
            reply_markup=ReplyKeyboardRemove()
        )        
        await send_sugo(
            f"⚠️ Notificación SUGO Bot\n\n"
            f"La chica es menor de edad\n"
            f"👤 @{message.from_user.username}\n"
            f"💬 Esta chica quiere trabajar en SUGO pero, es menor de edad."
        )
        await state.clear()
        return
    else:
        await message.answer("No entendí tu respuesta señorita 💎, ¿eres mayor de 18?")
        
#############-------------- REGISTRAR PAIS --------------############# 
@register_router.message(RegistroStates.pais)
async def registrar_pais(message: Message, state: FSMContext):
    texto = message.text.strip()
    pais_codigo = None
    for code, label in COUNTRY_CHOICES:
        if texto == label:
            pais_codigo = code
            break
    if not pais_codigo:
        await message.answer("Selecciona un país válido 🩵.", reply_markup=botones_paises())
        return
    try:
        telegram_id = message.from_user.id 
        respuesta = await update_streamer_fields(telegram_id, {"country": pais_codigo})
        # print("\nREGISTRO País:", respuesta)
        await state.update_data(country=pais_codigo)     
        if respuesta.get("message") == 'Actualización exitosa':  
            await typing(message, 2)
            await message.answer(
                "Perfecto señorita 🩵\n"
                "Antes de continuar, quiero contarte los requisitos para trabajar en SUGO:\n\n"
                "📌 *Buena conexión a internet*\n"
                "📌 *Un dispositivo móvil en buen estado*\n"
                "📌 *Dedicar mínimo 6 horas diarias*\n\n"
                "Lo que generes depende de tu dedicación, constancia y las estrategias que apliques.\n\n"
                "👉 ¿Cumples con estos requisitos?",
                reply_markup=botones_si_no()
            )
            await state.set_state(RegistroStates.requisitos)
    except ValueError as e:
        await send_soporte(
            f"La chica al seleccionar su País, no se actualizó\n"
            f"Revisar los servidores o API\n"
            f"💬 {e}"
        )
        await message.answer(
            "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
            "Nuestro Líder resolverá el problema y podrás continuar con tu registro\n"
            "Puedes Elegir tu país nuevamente en 5 minutos.\n"
        )  
    
#############-------------- CONFIRMAR REQUISITOS --------------############# 
@register_router.message(RegistroStates.requisitos)
async def confirmar_requisitos(message: Message, state: FSMContext):
    texto = message.text.lower()
    if any(x in texto for x in ["si", "sí", "s", "yes"]):    
        try:
            telegram_id = message.from_user.id 
            respuesta = await update_streamer_fields(telegram_id, {"accepts_requirements": True})
            # print("\nREGISTRO Requisitos:", respuesta)
            if respuesta.get("message") == 'Actualización exitosa':  
                await state.update_data(accepts_requirements=1)
                await typing(message, 2)
                await message.answer(
                    "Perfecto señorita 🩵\n"
                    "👉 Para finalizar tu registro, dime tu número de Teléfono.\n"
                    "Solo 10 dígitos, sin el código de tu país.",
                    reply_markup=ReplyKeyboardRemove()
                )
                await state.set_state(RegistroStates.telefono)
        except ValueError as e:
            await send_soporte(
                f"La chica al aceptar los requisitos, no se actualizó\n"
                f"Revisar los servidores o API\n"
                f"💬 {e}"
            )
            await message.answer(
                "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
                "Nuestro Líder resolverá el problema y podrás continuar con tu registro\n"
                "Puedes confirmar que cumples todos los requisitos nuevamente en 5 minutos.\n"
            )

    elif any(x in texto for x in ["no", "n", "not"]):
        await typing(message, 2)
        await message.answer(
            "Entiendo señorita 🩵\n"
            "Por ahora no puedes trabajar en SUGO.\n"
            "Cuando cumplas los requisitos, puedes volver a escribir *hola* o usar /start."
        )
        await state.clear()
        return    
    else:
        await message.answer("No entendí tu respuesta señorita 💎, ¿cumples con los requisitos?")
    
#############-------------- REGISTRAR TELÉFONO --------------############# 
@register_router.message(RegistroStates.telefono)
async def registrar_telefono(message: Message, state: FSMContext):
    numero = message.text.strip()
    # Validar que sean solo números
    if not numero.isdigit():
        await message.answer("El número debe contener solo dígitos 🩵. Intenta nuevamente.")
        return
    # Validar longitud exacta
    if len(numero) != 10:
        await message.answer("El número debe tener exactamente 10 dígitos 🩵. Intenta nuevamente.")
        return        
    try:
        telegram_id = message.from_user.id 
        respuesta = await update_streamer_fields(telegram_id, {"phone": numero})
        # print("\nREGISTRO Número:", respuesta)
        if respuesta.get("message") == 'Actualización exitosa': 
            await state.update_data(phone=numero)
            data = await state.get_data()
            await send_sugo(
                f"⚠️ Notificación SUGO Bot\n\n"
                f"👤 @{message.from_user.username}\n"
                f"🆔 Telegram ID: {telegram_id}\n"
                f"💬 La chica {data['full_name']} empezó  el registro para trabajar en SUGO."
            )    
            await typing(message, 3)    
            photo = FSInputFile("/home/webuser/apps/sugo-bot/media/img/Como-descargar-SUGO-paso-1.jpg")   
            await bot.send_photo(
                message.chat.id,
                photo=photo,
                caption="Perfecto señorita 🩵\n"
                "Ahora debes descargar la app de SUGO para continuar tu proceso.\n\n"
                "📲 Ingresa al siguiente enlace:\n"
                "👉 https://m-share.sugo.com/s/v1WSxo\n\n"
                "El enlace detecta tu dispositivo y te llevará al **App Store o Play Store** según corresponda.\n"
            )
            await typing(message, 3) 
            media = [
                InputMediaPhoto(media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/Como-descargar-SUGO-paso-2.jpg"),
                    caption=("Aquí eliges tu método para registrarte si tienes Android o iOS - iPhone\n")),
                InputMediaPhoto(media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/Como-descargar-SUGO-paso-3.jpg")),
            ]
            await bot.send_media_group(chat_id=message.chat.id, media=media)   
            await typing(message, 3) 
            media = [
                InputMediaPhoto(media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/Como-descargar-SUGO-paso-4.jpg"),
                    caption=("Registras Tus Datos procura no usar tus datos reales, usa un apodo jeje y luego Confirmas que eres una chica\n")),
                InputMediaPhoto(media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/Como-descargar-SUGO-paso-5.jpg")),
            ]
            await bot.send_media_group(chat_id=message.chat.id, media=media) 
            await typing(message, 3) 
            media = [    
                InputMediaPhoto(media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/Como-descargar-SUGO-paso-6.jpg"),
                    caption=("El Código de Invitación que copiaste anteriormente lo pegas y Vinculas donde te indico\n")),
                InputMediaPhoto(media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/Como-descargar-SUGO-paso-7.jpg")),
            ]
            await bot.send_media_group(chat_id=message.chat.id, media=media) 
            await typing(message, 3) 
            photo = FSInputFile("/home/webuser/apps/sugo-bot/media/img/copiar-id-perfil.jpg")
            await bot.send_photo(
                message.chat.id,
                photo=photo,
                caption="Una vez Completes estos pasos envíame tu **ID de perfil** (lo verás en tu perfil dentro de la app).\n",
                        reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(RegistroStates.creacion_cuenta)

    except ValueError as e:
        await send_soporte(
            f"La chica al registrar su número  de teléfono, no se actualizó\n"
            f"Revisar los servidores o API\n"
            f"💬 {e}"
        )
        await message.answer(
            "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
            "Nuestro Líder resolverá el problema y podrás continuar con tu registro\n"
            "Puedes darme tu número de teléfono nuevamente en 5 minutos.\n"
        )
   
#############-------------- RECIBIR ID DE SUGO --------------#############
@register_router.message(RegistroStates.creacion_cuenta)
async def recibir_id_app(message: Message, state: FSMContext):
    app_user_id = message.text.strip()

    if not app_user_id.isdigit():
        await message.answer("El ID debe ser numérico 🩵. Intenta nuevamente.")
        return
    try:
        datos = await state.get_data()
        await state.update_data( app_user_id=app_user_id, app_name="Sugo", )
        datos = await state.get_data()
        respuesta = await register_streamer_app(datos)
        
        # print("\nREGISTRO ID APP:", respuesta)
        await typing(message, 2)
        await message.answer(
            "Vamos avanzando señorita 🩵\n"
            "Sigamos con el registro para ingresar a nuestra agencia.\n\n"
        )   
        media = [
            InputMediaPhoto(
                media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/enviar-soli-paso1.jpg"), 
                caption="Sigue al pie de la letra los Siguientes Pasos"
            ),
            InputMediaPhoto(
                media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/enviar-soli-paso2.jpg")
            ),
            InputMediaPhoto(
                media=FSInputFile("/home/webuser/apps/sugo-bot/media/img/enviar-soli-paso3.jpg")
            ),
        ]
        await bot.send_media_group(chat_id=message.chat.id, media=media)
        await typing(message, 2)
        await message.answer(
            "Me confirmas cuando hayas enviado la solicitud para notificarle a nuestro Líder y te pueda aceptar en nuestra agencia 🩵",
            reply_markup=botones_envio_soli_si_no()
        )
        await state.set_state(RegistroStates.envia_solicitud)
        
    except ValueError as e:
        await send_soporte(
            f"La chica al registrar su ID, no se actualizó\n"
            f"Revisar los servidores o API\n"
            f"💬 {e}"
        )
        await message.answer(
            "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
            "Nuestro Líder resolverá el problema y podrás continuar con tu registro\n"
            "Puedes darme tu ID de SUGO nuevamente en 5 minutos.\n"
        )

#############-------------- ENVÍO DE SOLICITUD --------------#############
@register_router.message(RegistroStates.envia_solicitud)
async def recibir_solicitud(message: Message, state: FSMContext):
    texto = message.text.lower()

    if "ya envié mi solicitud" in texto or "ya envie mi solicitud" in texto:
        datos = await state.get_data()
        telegram_id = message.from_user.id
        nombre = datos.get("nombre", "La streamer")
        app_user_id = datos.get("app_user_id")
        try:
            respuesta = await update_streamer_app_field(app_user_id, {"app_name":"Sugo","request_agency_sent":True})
            # print("respuesta - update_streamer_app_field", respuesta)
            # Notificar al grupo
            await send_sugo(
                f"📩 *Nueva solicitud de ingreso - SUGO Bot*\n\n"
                f"👤 @{message.from_user.username}\n"
                f"🆔 Sugo ID: `{app_user_id}`\n"
                f"💎 {nombre} acaba de enviar su solicitud para ingresar a la agencia.\n"
                f"⚠️ Líder, revisa en la app de SUGO para aceptarla.\n\n"
                "Comandos: \n"
                f"Para aceptar a la Chica: /aceptar_lider_sugo {telegram_id}\n"
                f"Para confirmar que Sugo acepto a la chica: /aceptar_sugo {telegram_id}"
            )
            await typing(message, 2)
            # Mensaje para la chica
            await message.answer(
                "Perfecto señorita 🩵\n"
                "Tu solicitud fue enviada correctamente.\n\n"
                "Ahora debes esperar a que nuestro Líder te acepte en la agencia.\n"
                "Yo te notificaré automáticamente cuando eso ocurra 💎.",
                reply_markup=ReplyKeyboardRemove()
            )
            await typing(message, 2)
            await message.answer(
                "Mientras tanto puedes ver nuestra Playlist en YouTube\n"
                "https://youtube.com/playlist?list=PLLjWFpoyiQijtEvt7-Kak6XyHCF7X21uG&si=-4ChuBNhW6A0Y9Co \n"
                "Eso es Todo por el momento, Como verás soy Susi y estoy en Desarrollo espero pronto ayudarte más en SUGO\n\n"
                "Te dejo aquí el Telegram del líder para que le escribas y le pidas más información y te añada al grupo de SUGO\n"
                "@thecrazyagency que tengas mucho éxito en la app y que generes mucho dinero."
            )
            await state.clear()
            return
            
            # await message.answer(
            #     "Mientras tanto puedes ver nuestro menu principal🩵",
            #     reply_markup=menu_principal()
            # )
            # await state.set_state(MenuStates.menu_principal)
        except ValueError as e:
            await send_soporte(
                f"La chica al confirmar que envío su formulario de ingreso, no se actualizó\n"
                f"Revisar los servidores o API\n"
                f"💬 {e}"
            )
            await message.answer(
                "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
                "Nuestro Líder resolverá el problema y podrás continuar con tu registro\n"
                "Puedes confirmarme nuevamente en 5 minutos.\n"
            )
    await message.answer("Señorita, selecciona una opción válida 🩵.")
