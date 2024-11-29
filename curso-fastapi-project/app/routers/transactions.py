# app\routers\transactions.py

from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import Transaction, TransactionCreate, TransactionUpdate
from db import SessionDep

router = APIRouter()

@router.get('/transactions', response_model=list[Transaction], tags=['Transactions'])
async def list_transactions(session: SessionDep):
    statement = select(Transaction)
    return session.exec(statement).all()

@router.get('/transactions/{transaction_id}', tags=['Transactions'])
async def search_transaction(transaction_id: int, session:SessionDep):
    statement = select(Transaction).where(Transaction.id == transaction_id)
    transaction = session.exec(statement).first()
    
    if transaction is None:
        return HTTPException(status_code=404, detail="Transaction doesn´t exist")
    return transaction

@router.post('/transactions', response_model=Transaction, tags=['Transactions'])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction = Transaction.model_validate(transaction_data.model_dump())
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.put('/transactions/{transaction_id}', response_model=Transaction, status_code=status.HTTP_201_CREATED, tags=['Transactions'])
async def update_transaction(transaction_id: int, transaction_data: TransactionUpdate, session: SessionDep):
    statement = select(Transaction).where(Transaction.id == transaction_id)
    transaction = session.exec(statement).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction doesn't exist")
    
    transaction_data_dict = transaction_data.model_dump(exclude_unset=True)
    transaction.sqlmodel_update(transaction_data_dict)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.delete('/transactions/{transaction_id}', tags=['Transactions'])
async def delete_transaction(transaction_id: int, session:SessionDep):
    statement = select(Transaction).where(Transaction.id == transaction_id)
    transaction = session.exec(statement)
    
    if not transaction:
        raise HTTPException(status_code=404, detail='Customer doesn´t exist')
    
    session.delete(transaction)
    session.commit()
    return {"message": "Customer deleted successfuly"}