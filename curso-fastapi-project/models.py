#models.py

from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: str = Field(default=None)
    age:int = Field(default=None)
    
class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass
    
class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
class TransactionBase(SQLModel):#transacciones
    amount: int
    description: Optional[str]

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase, table=True):#transacciones
    id: int = Field(default=None, primary_key=True)
    # customer_id: int = Field(default=None, foreign_key="customer.id")
    
class InvoiceBase(SQLModel):
    total: int

class InvoiceCreate(InvoiceBase):
    customer_id: int
    transactions: List[Transaction]

class InvoiceUpdate(InvoiceBase):
    pass

class Invoice(InvoiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(back_populates="invoices")