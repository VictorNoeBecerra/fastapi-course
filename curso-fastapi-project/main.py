# main.py

from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI #Importamos FastAPI
from fastapi import HTTPException
from pydantic import BaseModel  
from datetime import datetime
import zoneinfo

from sqlmodel import select
from timezones import country_timezones
from db import SessionDep, create_all_tables
from models import Customer, CustomerCreate, Invoice, Transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)

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
@app.post('/customers', response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get('/customers', response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.exec(select(Customer).where(Customer.id == customer_id)).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data