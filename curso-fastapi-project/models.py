#models.py

from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: str = Field(default=None)
    age:int = Field(default=None)
    
class CustomerCreate(CustomerBase):
    pass
    
class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
class Transaction(BaseModel):#transacciones
    id: int
    amount: int
    description: Optional[str]
    
class Invoice(BaseModel):#facturas
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int
    @property
    def amount_total(self):
        return sum([t.amount for t in self.transactions])