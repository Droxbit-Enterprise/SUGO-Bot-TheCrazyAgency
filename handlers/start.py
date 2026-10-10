from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import RegistroStates, MenuStates
from functions import *
from config import *
from utils.api import *


start_router = Router()

#############-------------- INICIOS DEL BOT --------------#############
@start_router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    # print("Inicio el /start
    telegram_id = message.from_user.id
    datos = await state.get_data()
    streamer = await get_streamer(message.bot, telegram_id)
    app_datos = None
    if streamer:
        # print("La streamer ya Existe")
        app_datos = await state.update_data(streamer=streamer.get("id"), app_name="Sugo")        
        try:
            validador_estado = await get_streamer_app_check(app_datos)        
        except ValueError as e:
            await send_soporte(
                message.bot,
                f"La chica al Iniciar la consulta no se realiza\n"
                f"Revisar los servidores o API en get_streamer_app_check\n"
                f"💬 {e}"
            )
            await message.answer(
                "Señorita estamos teniendo problemas en nuestros servidores…💎\n"
                "Nuestro Líder resolverá el problema y podrás continuar\n"
                )
        
    # print("----------------------------------------------------------------------------------\n\n"
    #       "/start datos cache", datos,"\n"
    #       "/start streamer", streamer,"\n"
    #       "/start app_datos", validador_estado)
    
    await asyncio.sleep(0.2)
    
    # Si NO existe → iniciar 
    if streamer.get("message") == "Nueva": # Si NO existe → iniciar  
        # print("Es nueva")
        await message.answer(
            "🩵 Bienvenida a *The Crazy Agency*.\n\n"
            "Soy Susi y te acompañaré y guiaré para trabajar de forma segura, profesional y con resultados reales.\n"
            "Aquí aprenderás todo sobre la app *SUGO*: cómo funciona, cómo generar ingresos, cómo mejorar tu rendimiento y cómo aprovechar cada herramienta de la plataforma.\n\n"
            "Antes de comenzar, necesito saber algo importante:\n"
            "👉 ¿Cuál es tu nombre?"
        )
        await state.set_state(RegistroStates.nombre)
    
    # Si Existe → Validar pasos 
    else:        
        await state.clear() 
        app_datos = await state.update_data()
        paso, arreglo = status_process(streamer, validador_estado)
        # print("Paso:", paso, arreglo)
        await state.update_data(arreglo)
        datos = await state.get_data()
        
        # Si Existe → Ya Registró Nombre → Pero es menor de Edad   
        if paso==0:    # Si Existe → Validar si ya es Mayor de Edad
            await message.answer(
                f"Hola señorita {datos["nombre"]} 🩵Soy Susi, que bueno verte de nuevo por acá, espero estés bien.\n\n"
                f"Nos complace saber que quieres trabajar con nosotros.\n"
                f"Anteriormente nos comentaste que eras menor de edad.\n"
                "👉 ¿Actualmente ya mayor de 18 años?",
                reply_markup=botones_si_no()
            )
            await state.set_state(RegistroStates.edad)
        # Si Existe → Ya Registró Nombre → Validar si es Mayor de Edad   
        elif paso==1:    # Si Existe → Validar pasos  
            await message.answer(
                f"Hola señorita {datos["nombre"]} 🩵Soy Susi, que bueno verte de nuevo por acá, espero estés bien.\n\n"
                f"Nos complace saber que quieres trabajar con nosotros.\n\n"
                "👉 ¿Eres mayor de 18?",
                reply_markup=botones_si_no()
            )
            await state.set_state(RegistroStates.edad)
            
        # Si Existe → Ya Registró Nombre y Edad → Validar Pais  
        elif paso==2: 
            await message.answer(                
                f"Hola señorita {datos["nombre"]} 🩵Soy Susi, que bueno verte de nuevo por acá, espero estés bien.\n\n"
                "👉 ¿De qué país eres?",
                reply_markup=botones_paises()
            )
            await state.set_state(RegistroStates.pais)            
            
        # Si Existe → Ya Registró Nombre, Edad y Pais → Validar Requisitos  
        elif paso==3:
            await message.answer(
                f"Hola señorita {datos["nombre"]} 🩵Soy Susi, que bueno verte de nuevo por acá, espero estés bien.\n\n"
                "Antes de continuar, quiero contarte los requisitos para trabajar en SUGO:\n\n"
                "📌 *Buena conexión a internet*\n"
                "📌 *Un dispositivo móvil en buen estado*\n"
                "📌 *Dedicar mínimo 6 horas diarias*\n\n"
                "Lo que generes depende de tu dedicación, constancia y las estrategias que apliques.\n\n"
                "👉 ¿Cumples con estos requisitos?",
                reply_markup=botones_si_no()
            )
            await state.set_state(RegistroStates.requisitos)
        
        # Si Existe → Ya Registró Nombre, Edad, Pais y Requisitos → Validar Número de Teléfono  
        elif paso==4:
            await message.answer(
                f"Hola señorita {datos["nombre"]} 🩵Soy Susi, que bueno verte de nuevo por acá, espero estés bien.\n\n"
                "👉 Para finalizar tu registro, dime tu número de Teléfono.\n"
                "Solo 10 dígitos, sin el código de tu país.",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(RegistroStates.telefono)  
        
        # Si Existe → Ya Registró Nombre, Edad, Pais, Requisitos y Número de Teléfono → Validar Creacion de Cuenta
        elif paso==5:
            await send_sugo(
                message.bot,
                f"⚠️ Notificación SUGO Bot\n\n"
                f"👤 @{message.from_user.username}\n"
                f"🆔 Telegram ID: {telegram_id}\n"
                f"💬 La chica {datos["full_name"]} empezó el registro nuevamente para trabajar en SUGO."
            )
            await message.answer(
                f"🩵 Hola {datos["nombre"]}, bienvenida nuevamente.\n",
                reply_markup=ReplyKeyboardRemove()
            )
            await asyncio.sleep(0.2)
            await message.answer(
                "Señorita antes de continuar quiero saber si🩵\n"
                "¿Ya tienes una cuenta en SUGO y estás dentro de nuestra agencia o eres nueva?",
                reply_markup=botones_nueva_antigua()
            )            
            await state.set_state(RegistroStates.nueva_o_antigua)
            
        # Si Existe → Ya Registró Nombre, Edad, Pais, Requisitos, Número de Teléfono y Creacion de Cuenta → Validar Solicitud envio de agencia
        elif paso==6:
            await message.answer(
                f"🩵 Hola {datos["nombre"]}, bienvenida nuevamente.\n"            
                "Señorita dejamos el registro a medias jeje🩵\n\n"
                "Sigamos con el registro para ingresar a nuestra agencia.",
                reply_markup=ReplyKeyboardRemove()
            )
            media = [
                InputMediaPhoto(
                    media=FSInputFile(IMG_URL+"enviar-soli-paso1.jpg"), 
                    caption="Sigue al pie de la letra los Siguientes Pasos"
                ),
                InputMediaPhoto(
                    media=FSInputFile(IMG_URL+"enviar-soli-paso2.jpg")
                ),
                InputMediaPhoto(
                    media=FSInputFile(IMG_URL+"enviar-soli-paso3.jpg")
                ),
            ]
            await message.bot.send_media_group(chat_id=message.chat.id, media=media)
            await asyncio.sleep(0.2)
            await message.answer(
                "Me confirmas cuando hayas enviado la solicitud para notificarle a nuestro Líder y te pueda aceptar en nuestra agencia 🩵",
                reply_markup=botones_envio_soli_si_no()
            )
            await state.set_state(RegistroStates.envia_solicitud)
        
        # Si Existe → Ya Registró Nombre, Edad, Pais, Requisitos, Número de Teléfono, Creacion de Cuenta, Envio ID → Validar aceptacion Lider y Sugo
        elif paso==7:
            # Mensaje para la chica
            await message.answer(
                "Hola, señorita 🩵\n"
                "Bueno te explico, he revisado aca y tu solicitud ya fue enviada correctamente.\n\n",
                reply_markup=ReplyKeyboardRemove()
            )
            if datos.get("accepted_by_leader") == False and datos.get("accepted_by_sugo") == False:
                await message.answer(
                    "Ahora debes esperar a que nuestro Líder te acepte en la agencia.\n"
                    "Yo te notificaré automáticamente cuando eso ocurra 💎."
                )
            elif datos.get("accepted_by_leader") == True and datos.get("accepted_by_sugo") == False:
                await message.answer(
                    "Ahora debes esperar a que SUGO te acepte en la agencia.\n"
                    "Yo te notificaré automáticamente cuando eso ocurra 💎."
                )
            
            await asyncio.sleep(0.2)
            await message.answer(
                "Mientras tanto puedes ver nuestro menu principal🩵.\n"
                "¿Qué deseas hacer hoy?",
                reply_markup=menu_principal()
            )
            await state.set_state(MenuStates.menu_principal)
        
        # Si Existe → Ya Registró Nombre, Edad, Pais, Requisitos, Número de Teléfono, Creacion de Cuenta, Envio ID, entro en la agencia → Menu principal
        elif paso==8:
            # Mensaje para la chica
            await message.answer(
                "Hola, señorita, ¿cómo te va hoy?🩵\n"
                "Bueno te explico algo, usted ya se encuentra registrada en nuestra agencia.\n",
                reply_markup=ReplyKeyboardRemove()
            )            
            await asyncio.sleep(0.2)
            await message.answer(
                "Mientras tanto puedes ver nuestro menu principal🩵.\n"
                "¿Qué deseas hacer hoy?",
                reply_markup=menu_principal()
            )
            await state.set_state(MenuStates.menu_principal)
            
#############-------------- REINICIO DEL CHAT --------------############# No Terminado
# Se ejecuta si la chica dice que es menor de edad y vuelve a responder si la misma chica escribe de nuevo
@start_router.message(F.text.lower().in_({"hola susi", "Hola Susi", "HOLA SUSI", "hola", "buenas", "hey", "holi", "ola", "holis", "Holis", "Holi", "Ola", "Hey", "Buenas", "Hola", "Holaa", "Holaaa", "holaa", "holaaa"}))
async def reiniciar_conversacion(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    # Limpiar estado para evitar conflictos
    await state.clear()
    # Ejecutar el flujo del /start
    await start(message, state)
    
    """data = await state.get_data()
    telegram_id = message.from_user.id
    print(data, telegram_id)
    streamer = await get_streamer(message.bot, telegram_id)
    # Si existe → bienvenida + menú
    if streamer and "error" not in streamer:
        texto = streamer.get("full_name", "Streamer")
        partes = texto.split()
        nombre = partes[0]
        await message.bot.send_message(
            GROUP_ID,
            f"⚠️ Notificación desde SUGO Bot\n\n"
            f"👤 @{message.from_user.username}\n"
            f"💬 La chica {nombre} empezo el registro nuevamente para trabajar en SUGO."
        )     
        await message.answer(
            f"🩵 Hola {nombre}, bienvenida nuevamente.\n"            
            "Señorita 🩵\n"
        )
        await asyncio.sleep(0.2)
        video = FSInputFile(VIDEO_URL+"Como-descargar-SUGO.mp4")
        await message.bot.send_video(
            message.chat.id,
            video=video,
            caption="Ahora debes descargar la app de SUGO para continuar tu proceso.\n\n"
                    "📲 Ingresa al siguiente enlace:\n"
                    "📄 Copias el Codigo de Invitación y cuando estes dentro lo pegas donde te indica.\n"
                    "👉 [Descargar SUGO](https://m-share.sugo.com/s/v1WSxo)\n\n"
                    "El enlace detecta tu dispositivo y te llevará al **App Store o Play Store** según corresponda.\n\n"
        )
        await asyncio.sleep(0.2)        
        photo = FSInputFile(IMG_URL+"copiar-id-perfil.jpg")
        await message.bot.send_photo(
            message.chat.id,
            photo=photo,
            caption="Una vez descargues la app, crea tu cuenta y envíame tu **ID de perfil** (lo verás en tu perfil dentro de la app).\n",
                    reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(RegistroStates.creacion_cuenta)
    
    await message.answer(
        "💎 Hola señorita, bienvenida nuevamente 🩵\n"
        "Vamos a comenzar de nuevo.\n\n"
        "👉 ¿Cuál es tu nombre?"
    )
    await state.set_state(RegistroStates.nombre)"""

#############-------------- LÍDER ACEPTA AGENCIA --------------#############
@start_router.message(Command("aceptar_lider_sugo"))
async def aceptar_lider_sugo(message: Message):
    # Solo permitir si el mensaje viene del grupo
    if message.chat.id != GROUP_ID:
        return
    # Validar que viene del tema SUGO
    if not message.is_topic_message or message.message_thread_id != TOPIC_SUGO:
        await message.answer("Este comando solo puede ejecutarse dentro del tema SUGO 💎.")
        return

    try:
        parts = message.text.split()
        telegram_id = int(parts[1])
    except:
        await message.answer("Formato incorrecto. Usa: /aceptar_lider_sugo <telegram_id>")
        return
    
    try:
        streamer = await get_streamer(message.bot, telegram_id)
        nombre = streamer.get("full_name") 
        # print("streamer", streamer)
        validador_estado = await get_streamer_app_check({"streamer":streamer.get("id"), "app_name":"Sugo"})   
        # print("validador_estado", validador_estado)
        app_user_id = validador_estado.get("app_user_id") 
        # print("app_user_id", app_user_id) 
        
        if validador_estado.get("message")=="Asociada y en Agencia":
            # Avisar al grupo
            await message.answer(
                f"✔ La streamer {nombre} con ID SUGO {app_user_id} y ID Telegram {telegram_id} ya había sido Aceptada por Usted Líder y SUGO.\n"
                "Proceso completado."
            )
        elif validador_estado.get("message")=="Asociada y en espera de aprobacion de agencia" and validador_estado.get("accepted_by_leader")==False:                  
            respuesta = await update_streamer_app_field(app_user_id, {"app_name":"Sugo","accepted_by_leader":True})
            # print("respuesta error", respuesta.get("error"))
            # Avisar a la chica
            await message.bot.send_message(
                telegram_id,
                "Señorita 🩵\n"
                "Nuestro Líder te ha aceptado en la agencia.\n\n"
                "Ahora solo falta que SUGO apruebe tu cuenta.\n"
                "Te notificaré cuando eso ocurra 💎."
            )
            # Avisar al grupo
            await message.answer(
                f"✔ La streamer {nombre} con ID SUGO {app_user_id} y ID Telegram {telegram_id} fue aceptada en la agencia por usted Líder.\n"
                "Ahora solo falta que SUGO la apruebe."
            )
        elif validador_estado.get("message")=="Asociada y en espera de aprobación de agencia" and validador_estado.get("accepted_by_leader")==True:
            # Avisar al grupo
            await message.answer(f"✔ La streamer con ID SUGO {app_user_id} y ID Telegram {telegram_id} ya había sido Aceptada por usted Líder.")
        else: 
            await send_soporte(                
                message.bot,
                f"Registro de App no encontrado para esa App\n"
            ) 
    except ValueError as e:
        await send_soporte(
            message.bot,
            f"Líder usted al confirmar que acepto a la chica, no se actualizó\n"
            f"Revisar los servidores o API\n"
            f"💬 {e}"
        )
        
#############-------------- LÍDER ACEPTA EN SUGO --------------#############
@start_router.message(Command("aceptar_sugo"))
async def aceptar_sugo(message: Message):
    if message.chat.id != GROUP_ID:
        return
    # Validar que viene del tema SUGO
    if not message.is_topic_message or message.message_thread_id != TOPIC_SUGO:
        await message.answer("Este comando solo puede ejecutarse dentro del tema SUGO 💎.")
        return
    
    try:
        parts = message.text.split()
        telegram_id = int(parts[1])
    except:
        await message.answer("Formato incorrecto. Usa: /aceptar_sugo <telegram_id>")
        return
    
    # Obtener app_user_id desde la API
    try:        
        streamer = await get_streamer(message.bot, telegram_id)
        nombre = streamer.get("full_name") 
        # print("streamer", streamer)
        validador_estado = await get_streamer_app_check({"streamer":streamer.get("id"), "app_name":"Sugo"})   
        # print("validador_estado", validador_estado)
        app_user_id = validador_estado.get("app_user_id") 
        # print("app_user_id", app_user_id) 
        if validador_estado.get("message")=="Asociada y en Agencia":
            # Avisar al grupo
            await message.answer(
                f"✔ La streamer con ID SUGO {app_user_id} y ID Telegram {telegram_id} ya había sido Aceptada en SUGO.\n"
                "Proceso de ingreso a la agencia completado."
            )

        elif validador_estado.get("message")=="Asociada y en espera de aprobacion de agencia" and validador_estado.get("accepted_by_sugo")==False and validador_estado.get("inside_agency")==False:                  
            respuesta = await update_streamer_app_field(app_user_id, {"app_name":"Sugo","accepted_by_sugo":True,"inside_agency":True})
            # print("respuesta error", respuesta.get("error"))
            # Avisar a la chica
            await message.bot.send_message(
                telegram_id,
                "Señorita 🩵\n"
                "¡Felicidades! 🎉\n"
                "Tu cuenta fue aceptada en SUGO.\n\n"
                "Ya puedes continuar con tu proceso dentro de la agencia.\n"
                "Yo estaré contigo en cada paso 💎."
            )
            # Avisar al grupo
            await message.answer(
                f"✔ La streamer {nombre} con ID SUGO {app_user_id} y ID Telegram {telegram_id} fue aceptada en la agencia por SUGO.\n"                
                "Proceso de ingreso a la agencia completado."
            )

        else: 
            await send_soporte(
                message.bot,
                f"Registro de App no encontrado para esa App\n"
            )

    except ValueError as e:
        await send_soporte(
            message.bot,
            f"Líder usted al confirmar que Sugo acepto a la chica, no se actualizó\n"
            f"Revisar los servidores o API\n"
            f"💬 {e}"
        )


# @start_router.message(Command("get_topic_id"))
# async def get_topic_id(message: Message):
#     if message.is_topic_message:
#         await message.answer(f"Topic ID: {message.message_thread_id}")
#     else:
#         await message.answer("Este comando debe ejecutarse dentro del tema SUGO.")
