# app/routers/invoices.py

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Invoice, Customer, Transaction

router = APIRouter()

@router.post('/invoices', response_model=Invoice, tags=['Invoices'])
async def create_invoice(invoice_data: Invoice, session: SessionDep):
    # Validación del cliente relacionado
    customer_statement = select(Customer).where(Customer.id == invoice_data.customer.id)
    customer = session.exec(customer_statement).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer doesn't exist")
    
    # Validación de las transacciones relacionadas
    for transaction in invoice_data.transactions:
        transaction_statement = select(Transaction).where(Transaction.id == transaction.id)
        db_transaction = session.exec(transaction_statement).first()
        if not db_transaction:
            raise HTTPException(status_code=404, detail=f"Transaction with id {transaction.id} doesn't exist")
    
    # Creación del invoice
    invoice = Invoice.model_validate(invoice_data.model_dump())
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice

@router.get('/invoices', response_model=list[Invoice], tags=['Invoices'])
async def list_invoices(session: SessionDep):
    statement = select(Invoice)
    return session.exec(statement).all()

@router.get('/invoices/{invoice_id}', response_model=Invoice, tags=['Invoices'])
async def get_invoice(invoice_id: int, session: SessionDep):
    statement = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(statement).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice doesn't exist")
    return invoice

@router.put('/invoices/{invoice_id}', response_model=Invoice, status_code=status.HTTP_201_CREATED, tags=['Invoices'])
async def update_invoice(invoice_id: int, invoice_data: Invoice, session: SessionDep):
    statement = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(statement).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice doesn't exist")
    
    # Se actualizan los campos proporcionados en invoice_data
    invoice_data_dict = invoice_data.model_dump(exclude_unset=True)
    invoice.sqlmodel_update(invoice_data_dict)
    session.commit()
    session.refresh(invoice)
    return invoice

@router.delete('/invoices/{invoice_id}', tags=['Invoices'])
async def delete_invoice(invoice_id: int, session: SessionDep):
    statement = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(statement).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice doesn't exist")
    session.delete(invoice)
    session.commit()
    return {"message": "Invoice deleted successfully"}
