from app.database import Base
from sqlalchemy import Float, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    loans = relationship('Loan', back_populates='customer', cascade="all, delete")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    loan_id = Column(Integer, ForeignKey('loans.id', ondelete='CASCADE'), nullable=False)
    payment_type = Column(String, nullable=False)

    loan = relationship('Loan', back_populates='payments')


class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    principal_amount = Column(Float, nullable=False)
    tenure = Column(Integer, nullable=False)
    interest_rate = Column(Float, nullable=False)
    customer_id =  Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_amt = Column(Float, nullable=False)
    emi = Column(Float, nullable=False)
    completed = Column(Boolean, default=False)

    customer = relationship('User', back_populates='loans')
    payments = relationship('Payment', back_populates='loan', cascade="all, delete")
