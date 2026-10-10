import aiohttp
from config import BASE_URL, DJANGO_TOKEN
from functions import send_soporte

API_URL_STREAMER = BASE_URL+"streamer/"
API_URL_APP = BASE_URL+"app/"
API_URL_APP_CHECK = BASE_URL+"streamer/app/check/"
headers = {
    "Authorization": f"Token {DJANGO_TOKEN}",
    "Accept": "application/json"
}

session: aiohttp.ClientSession | None = None

STREAMER_FIELDS = {
    "telegram_id",
    "full_name",
    "country",
    "phone",
    "is_adult",
    "accepts_requirements",
    "origin_bot"
}
# Iniciamos la Sesión
async def init_api_session():
    global session
    session = aiohttp.ClientSession(headers=headers)

# Gestion de APIS de Streamers 
async def get_streamer(bot, telegram_id: int):
    endpoint = f"{API_URL_STREAMER}{telegram_id}/"
    try:
        async with session.get(endpoint, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                # print(f"JSON inválido: {e}")
                await report_api_error(bot, endpoint, f"JSON inválido: {e}")
                return {"error": str(e), "endpoint": endpoint}
            
            if resp.status == 200:
                return data
            elif resp.status == 404:
                return {"message":"Nueva"}
            # print(f"Status inesperado: {resp.status}")
            await report_api_error(bot, endpoint, f"Status inesperado: {resp.status}")
            return {"error": f"Status {resp.status}"}
            
    except Exception as e:
        # print("ERROR CONSULTAR STREAMER JSON:", e)
        await report_api_error(bot, endpoint, f"Excepción: {e}")
        return {"error": str(e), "endpoint": endpoint}

async def register_streamer(bot, data: dict):
    endpoint = API_URL_STREAMER
    try:
        async with session.post(endpoint, json=data, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                # print(f"JSON inválido: {e}")
                await report_api_error(bot, endpoint, f"JSON inválido: {e}")
                return {"error": str(e), "endpoint": endpoint}
            
            if resp.status == 201:
                return data
            
            # print(f"Status inesperado: {resp.status}")
            await report_api_error(bot, endpoint, f"Status inesperado: {resp.status}")
            return {"error": f"Status {resp.status}"}

    except Exception as e:
        # print("ERROR REGISTRAR STREAMER JSON:", e)
        await report_api_error(bot, endpoint, f"Excepción: {e}")
        return {"error": str(e), "endpoint": endpoint}

async def update_streamer_fields(bot, telegram_id: int, data: dict):
    endpoint = f"{API_URL_STREAMER}{telegram_id}/"
    try:
        async with session.patch(endpoint, json=data, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                # print(f"JSON inválido: {e}")
                await report_api_error(bot, endpoint, f"JSON inválido: {e}")
                return {"error": str(e), "endpoint": endpoint}

            if resp.status in (200, 201):
                return data     
            elif resp.status == 400:
                return data
            # print(f"Status inesperado: {resp.status}")
            await report_api_error(bot, endpoint, f"Status inesperado: {resp.status}")
            return {"error": f"Status {resp.status}"}
            
    except Exception as e:
        # print("ERROR ACTUALIZAR STREAMER JSON:", e)
        await report_api_error(bot, endpoint, f"Excepción: {e}")
        return {"error": str(e), "endpoint": endpoint}

# Gestion de APIS de StreamersApp   
async def get_streamer_app(bot, app_id: int, data: dict):
    endpoint = f"{API_URL_APP}{app_id}/"
    try:
        async with session.get(endpoint, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                # print(f"JSON inválido: {e}")
                await report_api_error(bot, endpoint, f"JSON inválido: {e}")
                return {"error": str(e), "endpoint": endpoint}
            
            if resp.status == 200:
                return data
            elif resp.status == 400:
                return {"message":"Debe enviar 'streamer' y 'app_name' en el body cuando pk es 0 o None"}
            elif resp.status == 404:
                return {"message":"No App Asociada"}
            
            # print(f"Status inesperado: {resp.status}")
            await report_api_error(bot, endpoint, f"Status inesperado: {resp.status}")
            return {"error": f"Status {resp.status}"}
            
    except Exception as e:
        # print("ERROR CONSULTAR STREAMER-APP JSON:", e)
        await report_api_error(bot, endpoint, f"Excepción: {e}")
        return {"error": str(e), "endpoint": endpoint}

async def get_streamer_app_check(bot, data: dict):
    endpoint = API_URL_APP_CHECK
    try:
        async with session.post(endpoint, json=data, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                # print(f"JSON inválido: {e}")
                await report_api_error(bot, endpoint, f"JSON inválido: {e}")
                return {"error": str(e), "endpoint": endpoint}
            
            if resp.status == 200:
                return data
            elif resp.status == 400:
                return {"message":"Debe enviar 'streamer' y 'app_name' en el body."}            
            # print(f"Status inesperado: {resp.status}")
            await report_api_error(bot, endpoint, f"Status inesperado: {resp.status}")
            return {"error": f"Status {resp.status}"}
                
    except Exception as e:
        # print("ERROR CONSULTAR STREAMER-APP-CHECK JSON:", e)
        await report_api_error(bot, endpoint, f"Excepción: {e}")
        return {"error": str(e), "endpoint": endpoint}

async def register_streamer_app(bot, data: dict):
    endpoint = API_URL_APP
    try:
        async with session.post(endpoint, json=data, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                # print(f"JSON inválido: {e}")
                await report_api_error(bot, endpoint, f"JSON inválido: {e}")
                return {"error": str(e), "endpoint": endpoint}
            
            if resp.status == 201:
                return data            
            # print(f"Status inesperado: {resp.status}")
            await report_api_error(bot, endpoint, f"Status inesperado: {resp.status}")
            return {"error": f"Status {resp.status}"}
                
    except Exception as e:
        # print("ERROR REGISTRAR STREAMER JSON:", e)
        await report_api_error(bot, endpoint, f"Excepción: {e}")
        return {"error": str(e), "endpoint": endpoint}

async def update_streamer_app_field(bot, telegram_id: int, data: dict):
    endpoint = f"{API_URL_APP}{telegram_id}/"
    try:
        async with session.patch(endpoint,json=data,headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                # print(f"JSON inválido: {e}")
                await report_api_error(bot, endpoint, f"JSON inválido: {e}")
                return {"error": str(e), "endpoint": endpoint}

            if resp.status in (200, 201):
                return data
            # print(f"Status inesperado: {resp.status}")
            await report_api_error(bot, endpoint, f"Status inesperado: {resp.status}")
            return {"error": f"Status {resp.status}"}
                
    except Exception as e:
        # print("ERROR ACTUALIZAR STREAMER-APP JSON:", e)
        await report_api_error(bot, endpoint, f"Excepción: {e}")
        return {"error": str(e), "endpoint": endpoint}
