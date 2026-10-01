import aiohttp
from config import BASE_URL, DJANGO_TOKEN
API_URL_STREAMER = BASE_URL+"streamer/"
API_URL_APP = BASE_URL+"app/"
API_URL_APP_CHECK = BASE_URL+"streamer/app/check/"
headers = {
    "Authorization": f"Token {DJANGO_TOKEN}",
    "Accept": "application/json"
}
STREAMER_FIELDS = {
    "telegram_id",
    "full_name",
    "country",
    "phone",
    "is_adult",
    "accepts_requirements",
    "origin_bot"
}

# Gestion de APIS de Streamers 
async def get_streamer(telegram_id: int):
    # print("get_streamer", telegram_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_STREAMER}{telegram_id}/", headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                print("ERROR CONSULTAR STREAMER JSON:", e)
                return {"error": str(e)}
            
            if resp.status == 200:
                return data
            elif resp.status == 404:
                return {"message":"Nueva"}
            return None

async def register_streamer(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_STREAMER, json=data, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                print("ERROR REGISTRAR STREAMER JSON:", e)
                return {"error": str(e)}
            
            if resp.status == 201:
                return data
            
            return None

async def update_streamer_fields(telegram_id: int, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL_STREAMER}{telegram_id}/", json=data, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                print("ERROR ACTUALIZAR STREAMER JSON:", e)
                return {"error": str(e)}

            if resp.status in (200, 201):
                return data     
            elif resp.status == 400:
                return data   
            
            return None

# Gestion de APIS de StreamersApp   
async def get_streamer_app(app_id: int, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_APP}{app_id}/", headers=headers) as resp:
            print("STATUS:", resp.status, f"{API_URL_APP}{app_id}/")
            try:
                data = await resp.json()
                print("RESPUESTA API:", data)
            except Exception as e:
                print("ERROR CONSULTAR APP STREAMER JSON:", e)
                return {"error": str(e)}
            
            if resp.status == 200:
                return data
            elif resp.status == 400:
                return {"message":"Debe enviar 'streamer' y 'app_name' en el body cuando pk es 0 o None"}
            elif resp.status == 404:
                return {"message":"No App Asociada"}
            return None

async def get_streamer_app_check(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_APP_CHECK, json=data, headers=headers) as resp:
            # print("STATUS:", resp.status, API_URL_APP_CHECK)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                print("ERROR CONSULTAR APP CHECK STREAMER JSON:", e)
                return {"error": str(e)}
            
            if resp.status == 200:
                return data
            elif resp.status == 400:
                return {"message":"Debe enviar 'streamer' y 'app_name' en el body."}

async def register_streamer_app(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_APP, json=data, headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                print("ERROR REGISTRAR APP STREAMER JSON:", e)
                return {"error": str(e)}
            
            if resp.status == 201:
                return data
            
            return None

async def update_streamer_app_field(telegram_id: int, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL_APP}{telegram_id}/",json=data,headers=headers) as resp:
            # print("STATUS:", resp.status)
            try:
                data = await resp.json()
                # print("RESPUESTA API:", data)
            except Exception as e:
                print("ERROR ACTUALIZAR STREAMER APP JSON:", e)
                return {"error": str(e)}

            if resp.status in (200, 201):
                return data

            return {"error": "No se pudo actualizar StreamerApp", "status": resp.status, "data": data}
