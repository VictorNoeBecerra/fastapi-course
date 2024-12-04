# app\routers\customers.py

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select
from db import SessionDep

from models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, StatusEnum

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn´t exists")
    # Se quitan los campos imitidos para que 
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data_dict)
    session.commit()
    session.refresh(customer)
    return customer

@router.post('/customers/{customer_id}/plans/{plan_id}', response_model=CustomerPlan,  tags=['Customers'])
async def subscribe_customer_to_plan(
    customer_id:int, 
    plan_id:int, 
    session:SessionDep, 
    plan_status: StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not plan_db or not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customers or plans doesn´t exist.")

    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get('/customers/{customer_id}/plans', tags=['Customers'])
async def get_customer_subscriptions(
    customer_id:int, 
    session:SessionDep,
    plan_status: StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    if not customer_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, status="Customer doesn't exist")
    
    sentence = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
        )
    plans = session.exec(sentence).all()
    
    return plans