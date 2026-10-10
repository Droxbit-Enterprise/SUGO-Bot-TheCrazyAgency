from aiogram.fsm.state import State, StatesGroup

class RegistroStates(StatesGroup):
    nombre = State()
    edad = State()
    pais = State()
    requisitos = State()
    telefono = State()
    nueva_o_antigua = State()
    id_antigua = State()
    creacion_cuenta = State()
    envia_solicitud = State()
    
class MenuStates(StatesGroup):
    menu_principal = State()
    
