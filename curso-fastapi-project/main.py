# main.py

from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI #Importamos FastAPI
from fastapi import HTTPException, status
from pydantic import BaseModel  
from datetime import datetime
import zoneinfo

from sqlmodel import select
from timezones import country_timezones
from db import SessionDep, create_all_tables
from models import Customer, CustomerCreate, CustomerUpdate, Invoice, Transaction

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
    statement = select(Customer)
    return session.exec(statement).all()

@app.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id: int, session: SessionDep):
    statement =  select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer doesn´t exists")
    return customer

@app.delete('/customers/{customer_id}')
async def delete_customer(customer_id: int, session: SessionDep):
    statement = select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer doesn´t exists, anyone has been deleted")
    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted"}

@app.put('/customers/{customer_id}', response_model=Customer, status_code=status.HTTP_201_CREATED)
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    statement = select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer doesn´t exists")
    # Se quitan los campos imitidos para que 
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data_dict)
    session.commit()
    session.refresh(customer)
    return customer

@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data