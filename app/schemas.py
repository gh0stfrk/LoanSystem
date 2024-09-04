from pydantic import BaseModel, confloat
from typing import Literal, List


class CreateUser(BaseModel):
    email:str
    password: str


class RequestLoan(BaseModel):
    customer_id: int
    loan_amount: float
    rate_of_interest: confloat(gt=1.0, lt=100.0)
    tennure_in_years: int


class PaymentSchema(BaseModel):
    amount: float
    loan_id: int
    payment_type: Literal['emi', 'lumpsum']


class PaymentInfo(BaseModel):
    amount: float
    payment_type: str

    class Config:
        from_attributes = True

class LoanInfo(BaseModel):
    customer_id: int
    loan_id: int
    balance: float
    emi: float
    months_left: int
    payments: List[PaymentInfo]


class LoanOverview(BaseModel):
    loan_id: int
    principal_amount: float   
    total_amount: float       
    emi_amount: float        
    total_interest: float     
    amount_paid: float        
    remaining_emis: int


class AccountOverview(BaseModel):
    customer_id: int
    email: str
    loans: List[LoanOverview]