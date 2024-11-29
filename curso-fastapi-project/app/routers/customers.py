# app\routers\customers.py

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep

from models import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()

@router.post('/customers', response_model=Customer, tags=['Customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get('/customers', response_model=list[Customer], tags=['Customers'])
async def list_customers(session: SessionDep):
    statement = select(Customer)
    return session.exec(statement).all()

@router.get('/customers/{customer_id}', response_model=Customer, tags=['Customers'])
async def get_customer(customer_id: int, session: SessionDep):
    statement =  select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer doesn´t exists")
    return customer

@router.delete('/customers/{customer_id}', tags=['Customers'])
async def delete_customer(customer_id: int, session: SessionDep):
    statement = select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer doesn´t exists, anyone has been deleted")
    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted"}

@router.put('/customers/{customer_id}', response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
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
