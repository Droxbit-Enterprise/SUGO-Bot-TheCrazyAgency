from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import RegistroStates, MenuStates, UsuariaRegistroStates
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
    streamer = await get_streamer(telegram_id)
    app_datos = None
    if streamer:
        # print("La streamer ya Existe")
        app_datos = await state.update_data(streamer=streamer.get("id"), app_name="Sugo")        
        try:
            validador_estado = await get_streamer_app_check(app_datos)        
        except ValueError as e:
            await send_soporte(
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
    
    # Si NO existe → iniciar 
    if streamer.get("message") == "Nueva": # Si NO existe → iniciar  
        # print("Es nueva")
        await typing(message, 2)
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
        # Si Existe → Ya Registró Nombre → Validar si es Mayor de Edad   
        if paso==1:    # Si Existe → Validar pasos  
            await typing(message, 2)
            await message.answer(
                f"Hola señorita {datos["nombre"]} 🩵Soy Susi, que bueno verte de nuevo por acá, espero estés bien.\n\n"
                f"Nos complace saber que quieres trabajar con nosotros.\n\n"
                "👉 ¿Eres mayor de 18?",
                reply_markup=botones_si_no()
            )
            await state.set_state(RegistroStates.edad)
            
        # Si Existe → Ya Registró Nombre y Edad → Validar Pais  
        elif paso==2: 
            await typing(message, 2)
            await message.answer(                
                f"Hola señorita {datos["nombre"]} 🩵Soy Susi, que bueno verte de nuevo por acá, espero estés bien.\n\n"
                "👉 ¿De qué país eres?",
                reply_markup=botones_paises()
            )
            await state.set_state(RegistroStates.pais)            
            
        # Si Existe → Ya Registró Nombre, Edad y Pais → Validar Requisitos  
        elif paso==3:
            await typing(message, 2)
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
            await typing(message, 2)
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
                f"⚠️ Notificación SUGO Bot\n\n"
                f"👤 @{message.from_user.username}\n"
                f"💬 La chica {datos["nombre"]} empezó el registro nuevamente para trabajar en SUGO."
            )
            await typing(message, 1)
            await message.answer(
                f"🩵 Hola {datos["nombre"]}, bienvenida nuevamente.\n"            
                "Señorita 🩵\n",
                reply_markup=ReplyKeyboardRemove()
            )
            await typing(message, 3)     
            photo = FSInputFile(IMG_URL+"Como-descargar-SUGO-paso-1.jpg")   
            await bot.send_photo(
                message.chat.id,
                photo=photo,
                caption="Ahora debes descargar la app de SUGO para continuar tu proceso.\n\n"
                "📲 Ingresa al siguiente enlace:\n"
                "👉 https://m-share.sugo.com/s/v1WSxo\n\n"
                "El enlace detecta tu dispositivo y te llevará al **App Store o Play Store** según corresponda.\n"
            )
            await typing(message, 3) 
            media = [
                InputMediaPhoto(media=FSInputFile(IMG_URL+"Como-descargar-SUGO-paso-2.jpg"),
                    caption=("Aquí eliges tu método para registrarte si tienes Android o iOS - iPhone\n")),
                InputMediaPhoto(media=FSInputFile(IMG_URL+"Como-descargar-SUGO-paso-3.jpg")),
            ]
            await bot.send_media_group(chat_id=message.chat.id, media=media)   
            await typing(message, 3) 
            media = [
                InputMediaPhoto(media=FSInputFile(IMG_URL+"Como-descargar-SUGO-paso-4.jpg"),
                    caption=("Registras Tus Datos procura no usar tus datos reales, usa un apodo jeje y luego Confirmas que eres una chica\n")),
                InputMediaPhoto(media=FSInputFile(IMG_URL+"Como-descargar-SUGO-paso-5.jpg")),
            ]
            await bot.send_media_group(chat_id=message.chat.id, media=media) 
            await typing(message, 3) 
            media = [    
                InputMediaPhoto(media=FSInputFile(IMG_URL+"Como-descargar-SUGO-paso-6.jpg"),
                    caption=("El Código de Invitación que copiaste anteriormente lo pegas y Vinculas donde te indico\n")),
                InputMediaPhoto(media=FSInputFile(IMG_URL+"Como-descargar-SUGO-paso-7.jpg")),
            ]
            await bot.send_media_group(chat_id=message.chat.id, media=media) 
            await typing(message, 3) 
            photo = FSInputFile(IMG_URL+"copiar-id-perfil.jpg")
            await bot.send_photo(
                message.chat.id,
                photo=photo,
                caption="Una vez Completes estos pasos envíame tu **ID de perfil** (lo verás en tu perfil dentro de la app).\n",
                        reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(RegistroStates.creacion_cuenta)
            
        # Si Existe → Ya Registró Nombre, Edad, Pais, Requisitos, Número de Teléfono y Creacion de Cuenta → Validar Solicitud envio de agencia
        elif paso==6:
            await typing(message, 1)
            await message.answer(
                f"🩵 Hola {datos["nombre"]}, bienvenida nuevamente.\n"            
                "Señorita dejamos el registro a medias jeje🩵\n\n"
                "Sigamos con el registro para ingresar a nuestra agencia.",
                reply_markup=ReplyKeyboardRemove()
            )
            await typing(message, 2)
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
            await bot.send_media_group(chat_id=message.chat.id, media=media)
            await typing(message, 2)
            await message.answer(
                "Me confirmas cuando hayas enviado la solicitud para notificarle a nuestro Líder y te pueda aceptar en nuestra agencia 🩵",
                reply_markup=botones_envio_soli_si_no()
            )
            await state.set_state(RegistroStates.envia_solicitud)
        
        # Si Existe → Ya Registró Nombre, Edad, Pais, Requisitos, Número de Teléfono, Creacion de Cuenta, Envio ID → Validar aceptacion Lider y Sugo
        elif paso==7:
            await typing(message, 1)
            # Mensaje para la chica
            await message.answer(
                "Hola, señorita 🩵\n"
                "Bueno te explico, Tu solicitud fue enviada correctamente.\n\n",
                reply_markup=ReplyKeyboardRemove()
            )
            await typing(message, 2)
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
                
            await typing(message, 2)
            await message.answer(
                "Mientras tanto puedes ver nuestra Playlist en YouTube\n"
                "https://youtube.com/playlist?list=PLLjWFpoyiQijtEvt7-Kak6XyHCF7X21uG&si=-4ChuBNhW6A0Y9Co \n"
                "Eso es Todo por el momento, Como verás soy Susi y estoy en Desarrollo espero pronto ayudarte más en SUGO\n\n"
                "Te dejo aquí el Telegram del líder para que le escribas y le pidas más información y te añada al grupo de SUGO\n"
                "@thecrazyagency que tengas mucho éxito en la app y que generes mucho dinero."
            )

        # Si Existe → Ya Registró Nombre, Edad, Pais, Requisitos, Número de Teléfono, Creacion de Cuenta, Envio ID, entro en la agencia → Menu principal
        elif paso==8:
            await typing(message, 1)
            # Mensaje para la chica
            await message.answer(
                "Hola, señorita, ¿cómo te va hoy?🩵\n"
                "Bueno te explico algo, usted ya se encuentra registrada en nuestra agencia.\n",
                reply_markup=ReplyKeyboardRemove()
            )
                
            await typing(message, 2)
            await message.answer(
                "Como verás soy Susi y estoy en Desarrollo espero pronto ayudarte más en SUGO\n"
                "hasta aquí hemos llegado hasta el momento"
                "Mientras tanto puedes ver nuestra Playlist en YouTube para que aprendas a usar Sugo\n"
                "https://youtube.com/playlist?list=PLLjWFpoyiQijtEvt7-Kak6XyHCF7X21uG&si=-4ChuBNhW6A0Y9Co \n\n"                
                "Te dejo aquí el Telegram del líder para que le escribas y le pidas más información y te añada al grupo de SUGO\n"
                "@thecrazyagency que tengas mucho éxito en la app y que generes mucho dinero."
            )
            
#############-------------- REINICIO DEL CHAT --------------############# No Terminado
# Se ejecuta si la chica dice que es menor de edad y vuelve a responder si la misma chica escribe de nuevo
@start_router.message(F.text.lower().in_({"susi", "Susi", "SUSI", "hola", "buenas", "hey", "holi", "ola", "holis", "Holis", "Holi", "Ola", "Hey", "Buenas", "Hola", "Holaa", "Holaaa", "holaa", "holaaa"}))
async def reiniciar_conversacion(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    # Limpiar estado para evitar conflictos
    await state.clear()
    # Ejecutar el flujo del /start
    await start(message, state)
    
    """data = await state.get_data()
    telegram_id = message.from_user.id
    print(data, telegram_id)
    streamer = await get_streamer(telegram_id)
    # Si existe → bienvenida + menú
    if streamer and "error" not in streamer:
        texto = streamer.get("full_name", "Streamer")
        partes = texto.split()
        nombre = partes[0]
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Notificación desde SUGO Bot\n\n"
            f"👤 @{message.from_user.username}\n"
            f"💬 La chica {nombre} empezo el registro nuevamente para trabajar en SUGO."
        )     
        await typing(message, 1)
        await message.answer(
            f"🩵 Hola {nombre}, bienvenida nuevamente.\n"            
            "Señorita 🩵\n"
        )
        await typing(message, 3)
        video = FSInputFile(VIDEO_URL+"Como-descargar-SUGO.mp4")
        await bot.send_video(
            message.chat.id,
            video=video,
            caption="Ahora debes descargar la app de SUGO para continuar tu proceso.\n\n"
                    "📲 Ingresa al siguiente enlace:\n"
                    "📄 Copias el Codigo de Invitación y cuando estes dentro lo pegas donde te indica.\n"
                    "👉 [Descargar SUGO](https://m-share.sugo.com/s/v1WSxo)\n\n"
                    "El enlace detecta tu dispositivo y te llevará al **App Store o Play Store** según corresponda.\n\n"
        )
        await typing(message, 2)        
        photo = FSInputFile(IMG_URL+"copiar-id-perfil.jpg")
        await bot.send_photo(
            message.chat.id,
            photo=photo,
            caption="Una vez descargues la app, crea tu cuenta y envíame tu **ID de perfil** (lo verás en tu perfil dentro de la app).\n",
                    reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(RegistroStates.creacion_cuenta)
    
    await typing(message, 2)
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
        streamer = await get_streamer(telegram_id)
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
            await bot.send_message(
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
                f"Registro de App no encontrado para esa App\n"
            ) 
    except ValueError as e:
        await send_soporte(
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
        streamer = await get_streamer(telegram_id)
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
            await bot.send_message(
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
                f"Registro de App no encontrado para esa App\n"
            )

    except ValueError as e:
        await send_soporte(
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
