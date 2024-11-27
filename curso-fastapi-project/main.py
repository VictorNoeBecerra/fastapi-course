from typing import Optional
from fastapi import FastAPI #Importamos FastAPI
from fastapi import HTTPException
from datetime import datetime
import zoneinfo

app = FastAPI()

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "CL": "America/Santiago",
    "PE": "America/Lima",
    "VE": "America/Caracas",
    "EC": "America/Guayaquil",
    "BO": "America/La_Paz",
    "PY": "America/Asuncion",
    "UY": "America/Montevideo",
    "GY": "America/Guayaquil",
    "GF": "America/Cayenne",
    "SR": "America/Paramaribo"
}

@app.get('/')
async def root():
    return {"message" :"Welcome to my first API"}

#En el decorador 
#Si no se especifica la varible del parámetro de time() significa que se va a acceder a la ruta /time?iso_code=MX ó /time
#Si se especifica entonces se accede solo a /time/MX
@app.get('/time/{iso_code}')
async def time(iso_code: Optional[str] = None):
    
    if iso_code is None:
        print(iso_code)
        iso = 'MX'
    else:
        iso = iso_code.upper()
        
    timezone_str = country_timezones.get(iso) #America/Bogota
    
    if(timezone_str is None):
        raise HTTPException(status_code=404, detail="Timezone not found for the provided ISO code")
    
    try:
        tz = zoneinfo.ZoneInfo(timezone_str)
        current_date = datetime.now(tz)
        date_formated = current_date.strftime("%d de %B del %Y, %H:%M:%S")
        return {"time": date_formated}

    except zoneinfo.ZoneInfoNotFoundError:
        raise HTTPException(status_code=404, detail="Timezone data not found")
    
@app.get('/time')
async def time_without_code():
    return await time() 