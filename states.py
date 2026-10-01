from aiogram.fsm.state import State, StatesGroup

class RegistroStates(StatesGroup):
    nombre = State()
    edad = State()
    pais = State()
    requisitos = State()
    telefono = State()
    creacion_cuenta = State()
    envia_solicitud = State()
    
    
    
    seleccion_app = State()
    seleccion_inicial = State()
    apellidos = State()
    documento = State()
    tiempo = State()
    pin = State()
    whatsapp = State()
    confirmacion = State()
    vio_video_sugo = State()
    registro_plataforma = State()
    antigua_pregunta = State()
    pedir_nombre = State()
    esperando_activacion = State()
    iniciar_sesion_sugo = State()
    preguntar_gestionar_sugo = State()
    numero_telefono = State()
    preguntar_gestionar_sugo = State()
    preguntar_gestionar_sugo = State()
    preguntar_gestionar_sugo = State()
    
class MenuStates(StatesGroup):
    menu_principal = State()
    
class UsuariaRegistroStates(StatesGroup):
    valida_registro_api = State()
    iniciar_sesion = State()
    nombre = State()
    apellido = State()
    doc = State()
    pais = State()
    telefono = State()
    pin = State()
    telefono_wp = State()
    telefono_tg = State()