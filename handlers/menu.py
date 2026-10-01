from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import RegistroStates, MenuStates
from functions import *
from config import *
menu_router = Router()

###-------- Menu principal --------------###
@menu_router.message(MenuStates.menu_principal)
async def menu_principal(message: Message, state: FSMContext):
    texto = message.text.lower()
    # NUEVA
    if "nueva" in texto:
        await bot.send_message(
            GROUP_ID,
            f"💎 *Nueva chica interesada en generar ingresos* 💸\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n\n"
            f"⚠️ Equipo, estén pendientes: acaba de iniciar el proceso de registro."
        )
        await typing(message, 2)
        await message.answer(
            "Perfecto señorita 💎💸\n"
            "Vamos a hacerte unas preguntas rápidas.\n\n"
            "👉 ¿Eres mayor de 18 años?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.esperando_edad)

    # ANTIGUA
    elif "agencia" in texto or "antigua" in texto:
        await typing(message, 2)
        await message.answer(
            "Perfecto señorita 💛\n"
            "Cuéntame, ¿qué necesitas hoy? 💎",
            reply_markup=None
        )
        await state.set_state(RegistroStates.antigua_pregunta)

    else:
        await message.answer("No entendí señorita 💎, ¿eres nueva o ya estás en la agencia?")
        

# Pregunta 4: Seleccionar App
@dp.message(RegistroStates.seleccion_app)
async def seleccionar_app(message: Message, state: FSMContext):
    texto = message.text.lower()
    # Si elige SUGO
    if "sugo" in texto:
        await typing(message, 2)
        # Puedes enviar una foto de ejemplo
        await bot.send_photo(
            message.chat.id,
            photo=URL_STATIC+"sugo-logo.png",  # Cambia por tu imagen real
            caption="💎 Esta es la app SUGO donde generarás ingresos 💸",
            reply_markup=ReplyKeyboardRemove()
        )
        await typing(message, 2)
        # Imagen indicando dónde está el video
        await bot.send_photo(
            message.chat.id,
            photo=URL_STATIC+"pagina-sugo.png",
            caption="Perfecto señorita 💎\n"
                    "Antes de registrarte, debes ver el *video explicativo* de qué es SUGO.\n\n"
                    "Aquí tienes el contenido:\n"
                    "👉 Video explicativo (arriba en la página)\n\n"
                    "Haz clic aquí para verlo:\n"
                    "🔗 https://thecrazyagency.com/sugo/\n\n"
                    "💛 *IMPORTANTE:* Solo debes ver el video por ahora."
        )
        await typing(message, 10)
        await message.answer(
            "¿Ya viste el video completo señorita? 💎",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.vio_video_sugo)
        return

    # Si elige SALSA
    elif "salsa" in texto:
        await typing(message, 2)
        await message.answer(
            "Perfecto señorita 💎\n"
            "La app SALSA estará disponible muy pronto 💛\n"
            "Por ahora te recomendamos trabajar con SUGO 💸"
        )
        await message.answer(
            "👉 ¿Deseas registrarte en SUGO?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.esperando_disponibilidad)  # Reinicia flujo para Sugo
    else:
        await message.answer("No entendí señorita 💎, selecciona una app:")

# Pregunta 5: Si Confirma haber visto el video de que es SUGO
@dp.message(RegistroStates.vio_video_sugo)
async def validar_video_sugo(message: Message, state: FSMContext):
    texto = message.text.lower()
    # NO vio el video → repetir
    if any(x in texto for x in ["no", "n"]):
        await typing(message, 2)
        await message.answer(
            "Señorita 💛 debes ver el video antes de continuar.\n\n"
            "Aquí está nuevamente:\n"
            "🔗 https://thecrazyagency.com/sugo/\n\n"
            "Cuando termines, seleccione: *Sí 💎*",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.vio_video_sugo)
        return

    # SÍ vio el video → mostrar botón de registro
    elif any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)
        # Imagen del botón de registro
        await bot.send_photo(
            message.chat.id,
            photo=URL_STATIC+"pagina-sugo-1.png",
            caption="Perfecto señorita 💎\n Aquí está el botón para registrarte en nuestra plataforma 💸",
            reply_markup=ReplyKeyboardRemove()
        )
        await typing(message, 2)  
        # Imagen de registro
        await bot.send_photo(
            message.chat.id,
            photo=URL_STATIC+"ejemplo-registro-streamer.png",
            caption="Ahora sí debes registrarte en el formulario oficial de nuestra plataforma:\n\n"
                    "🔗 https://thecrazyagency.com/usuarias/registrar/?from=sugo"
        )
        await typing(message, 10)
        await message.answer(
            "👉 ¿Nos confirmas si ya te registraste en nuestra plataforma?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.registro_plataforma)
        return
    else:
        await message.answer("No entendí señorita 💎, ¿ya viste el video completo?")

###-------- REGISTRO DE LA STREAMER EN NUESTRA PLATAFORMA --------------###
@dp.message(RegistroStates.registro_plataforma)
async def registro_plataforma(message: Message, state: FSMContext):
    texto = message.text.lower()    
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)
        await message.answer(
            "Listo Señorita 💛\n"
            "Para confirmar tu registro, por favor escribenos tu *nombre* tal como pusiste en el formulario 💎",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(RegistroStates.pedir_nombre)
        return

#Pregunta 6: Se le pregunta el nombre para saber quien es en el registro y ver cual cuenta activar
@dp.message(RegistroStates.pedir_nombre)
async def recibir_nombre(message: Message, state: FSMContext):
    nombre = message.text.strip()
    # Guardar el nombre en el estado (opcional)
    await state.update_data(nombre=nombre)
    await typing(message, 2)
    # Notificar al grupo
    await bot.send_message(
        GROUP_ID,
        f"💎 *Nueva chica registrada en la plataforma para trabajar en SUGO* 💸\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {message.from_user.id}\n"
        f"📛 Nombre: *{nombre}*\n\n"
        f"⚠️ Deben activar su cuenta en la plataforma.\n\n"
        f"Para activarla usen:\n"
        f"/activar {message.from_user.id}"
    )
    # Mensaje para la chica
    await message.answer(
        f"Perfecto gracias {nombre}.\n"
        "Tu registro fue enviado al equipo.\n"
        "En breve activarán tu cuenta para que puedas continuar con los cursos 💎💸"
    )
    # Guardamos que ya está esperando activación
    await state.set_state(RegistroStates.esperando_activacion)

@dp.message(RegistroStates.esperando_activacion)
async def esperando_activacion(message: Message, state: FSMContext):
    texto = message.text.lower()
    # Palabras que indican que solo está respondiendo
    if any(x in texto for x in ["ok", "gracias", "vale", "listo", "perfecto", "bueno", "entendido", "ok gracias", "oki", "okey"]):
        await typing(message, 2)
        await message.answer(
            "💛 Señorita, solo debemos esperar a que el equipo active tu cuenta.\n"
            "Apenas esté lista te avisaré por aquí 💎"
        )
        await state.clear()
        return

    # Si escribe otra cosa, igual la mantenemos en espera
    await message.answer(
        "Señorita 💛, ya enviamos tu registro al equipo.\n"
        "Apenas activen tu cuenta te avisaré por aquí 💎"
    )
    await state.clear()

###---------- FINALIZA EL PRIMERO CICLO DE REGISTRO ---------###


###---------- Estado cuando ya se le ha activado la cuenta en la plataforma a la streamer ---------###
@dp.message(F.text.startswith("/activar"))
async def activar_cuenta(message: Message, state: FSMContext):
    # Solo permitir que funcione en el grupo
    if message.chat.id != GROUP_ID:
        return
    
    try:
        # Extraer el ID de la chica
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("⚠️ Debes usar: /activar <telegram_id>")
            return
        
        user_id = int(parts[1])
        # Avisar en el grupo
        await message.reply(f"💛 La cuenta de la chica con ID {user_id} fue activada correctamente.")
        # Avisar a la chica - Imagen de cómo iniciar sesión
        await bot.send_photo(
            user_id,
            photo=URL_STATIC+"ejemplo-iniciar-streamer.png",
            caption="💛 Señorita, tu cuenta ya fue activada.\n\n"
                    "✨ Ya puedes iniciar sesión.\n\n"
                    "Aquí te explico cómo iniciar sesión 💎 en la plataforma:\n\n"
                    "Solo debe seleccionar su país, su número y el PIN que añadió como contraseña.\n\n"
                    "🔗 https://thecrazyagency.com/usuarias/iniciar-sesion/"
        )
        await typing(message, 5)
        await bot.send_message(
            user_id,
            "Ahora debe iniciar sesión para continuar.\n\n"
            "Cuando haya iniciado sesión, seleccione: *Sí 💎*",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.iniciar_sesion_sugo)
        return

    
    except Exception as e:
        await message.reply(f"⚠️ Error activando la cuenta: {e}")
    
@dp.message(RegistroStates.iniciar_sesion_sugo)
async def iniciar_sesion_sugo(message: Message, state: FSMContext):
    texto = message.text.lower()

    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)
        await message.answer(
            "ok ok listo señorita 💛\n\n"
            "Cuando entre a la plataforma verá esta pantalla donde aparecen las aplicaciones disponibles en nuestra agencia 💎💸\n\n"
            "👉 ¿Le aparece el botón *Gestionar SUGO* en la plataforma?\n\n",
            reply_markup=ReplyKeyboardRemove()   # 🔥 Cierra el teclado
        )
        await state.set_state(RegistroStates.preguntar_gestionar_sugo)
        return

    if any(x in texto for x in ["no", "n"]):
        await message.answer(
            "Señorita 💛 debe iniciar sesión para continuar.\n"
            "Cuando haya iniciado sesión, seleccione *Sí 💎*.",
            reply_markup=ReplyKeyboardRemove()   # 🔥 Cierra el teclado
        )
        return

    await message.answer("Seleccione *Sí* o *No* señorita 💛.")


    
@dp.message(RegistroStates.preguntar_gestionar_sugo)
async def preguntar_gestionar_sugo(message: Message, state: FSMContext):
    texto = message.text.lower()

    # SI LE SALE GESTIONAR SUGO
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)
        await message.answer(
            "Perfecto señorita 💛\n\n"
            "Si ya le aparece el botón *Gestionar SUGO*, debe darle ahí.\n\n"
            "Dentro encontrará todos los cursos disponibles 💎💸.\n"
            "La idea es que complete *todos los cursos*, ya que cada uno es importante para su proceso dentro de SUGO."
        )
        await state.clear()
        return

    # SI NO LE SALE GESTIONAR SUGO → EXPLICAR ASOCIAR APP
    if any(x in texto for x in ["no", "n"]):
        await typing(message, 2)
        await message.answer(
            "Listo señorita 💛\n\n"
            "Si aún no le aparece el botón *Gestionar SUGO*, debe asociar su app SUGO con la plataforma.\n\n"
            "👉 Presione el botón *Generar en SUGO*.\n"
            "👉 Luego seleccione *Asociar App*.\n"
            "👉 Acepte los permisos.\n\n"
            "Una vez la app quede asociada, le aparecerá el botón *Gestionar SUGO* 💎💸"
        )
        await state.clear()
        return

    # SI ESCRIBE OTRA COSA
    await message.answer(
        "Señorita 💛 no entendí.\n"
        "¿Le aparece el botón *Gestionar SUGO*? Responda *Sí* o *No*."
    )

       
# Chica antigua
@dp.message(RegistroStates.antigua_pregunta)
async def antigua_pregunta(message: Message, state: FSMContext):
    texto = message.text
    await bot.send_message(
        GROUP_ID,
        f"📩 Mensaje de chica ANTIGUA 💎💸\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {message.from_user.id}\n\n"
        f"💬 {texto}"
    )
    await typing(message, 2)
    await message.answer(
        "Listo señorita 💛, ya envié tu mensaje al equipo.\n"
        "Una jefa o vicejefa te responderá pronto 💎"
    )
    await state.clear()

# Mensajes generales (reenviar al grupo)
@dp.message()
async def handle_message(message: Message):
    if message.chat.type == "private":
        user_id = message.from_user.id
        username = message.from_user.username or "SinUsername"
        user_map[user_id] = username

        text = (
            f"📩 Nuevo mensaje 💎💸\n"
            f"👤 Chica: @{username}\n"
            f"🆔 ID: {user_id}\n\n"
            f"💬 {message.text}"
        )
        await bot.send_message(GROUP_ID, text)

    elif message.chat.id == GROUP_ID and message.text.startswith("Resp:"):
        try:
            parts = message.text.split("\n", 1)
            user_id = int(parts[0].replace("Resp:", "").strip())
            respuesta = parts[1]
            await bot.send_message(user_id, respuesta)
        except:
            await bot.send_message(GROUP_ID, "⚠️ Formato incorrecto. Usa:\nResp: ID\nMensaje...")

async def main():
    print("💎 Bot corriendo... 💸")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
