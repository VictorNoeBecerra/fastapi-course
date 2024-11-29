# main.py

from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI #Importamos FastAPI
from fastapi import HTTPException
from datetime import datetime
import zoneinfo

from .routers import customers, transactions, invoices
from timezones import country_timezones
from db import create_all_tables
from models import Invoice, Transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)

@app.get('/')
async def root():
    return {"message" :"Welcome to my first API"}

#En el decorador 
#Si no se especifica la varible del parámetro de time() significa que se va a acceder a la ruta /time?iso_code=MX ó /time
#Si se especifica entonces se accede solo a /time/MX
@app.get('/time/{iso_code}')
async def time(iso_code: Optional[str] = None, time_format: Optional[bool] = False):
    
    if iso_code is None:
        print(iso_code)
        iso = 'MX'
    else:
        iso = iso_code.upper()
        
    timezone_str = country_timezones.get(iso) #America/Bogota
    format = '%d de %B del %Y, %H:%M:%S' if time_format else '%d de %B del %Y, %I:%M:%S %p'
    
    if(timezone_str is None):
        raise HTTPException(status_code=404, detail="Timezone not found for the provided ISO code")
    
    try:
        tz = zoneinfo.ZoneInfo(timezone_str)
        current_date = datetime.now(tz)
        
        date_formated = current_date.strftime(format)
        return {"time": date_formated}

    except zoneinfo.ZoneInfoNotFoundError:
        raise HTTPException(status_code=404, detail="Timezone data not found")
    
@app.get('/time')
async def time_without_code():
    return await time() 

db_customers = []

@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data