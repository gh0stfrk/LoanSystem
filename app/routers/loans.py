from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas import RequestLoan, PaymentSchema
from app.database import get_db
from app.services.loans import (create_loan, make_payment, collect_ledger_info, account_overview)

loans = APIRouter(
    prefix="/loan",
    tags=['loans']
)

@loans.post("/request", description="Create a loan")
async def request_loan(loan: RequestLoan, db:Session=Depends(get_db)): 
    try:
        loan = create_loan(loan, db)
        if loan['status'] != 'success':
            return JSONResponse(
                content=loan,
                status_code=400
            )
        return JSONResponse(
            content=loan,
            status_code=200
        )
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail={
                "status":"error",
                "detail": f"{e}"
            })

@loans.post("/pay", description="Pay for a loan")
async def pay_installments(payment: PaymentSchema, db: Session = Depends(get_db)): 
    try:
        payment_status = make_payment(payment, db)
        if payment_status['status'] != 'success':
            return JSONResponse(
                content=payment_status,
                status_code=400
            )
        return JSONResponse(
            content=payment_status,
            status_code=200
        )
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail={
                "status":"error",
                "detail": f"{e}"
            })

@loans.get("/ledger/{loan_id}")
async def loan_details(loan_id: int, db: Session = Depends(get_db)):
    return collect_ledger_info(loan_id, db)


@loans.get("/overview/{customer_id}")
async def get_account_overview(customer_id: int, db: Session=Depends(get_db)):
    try:
        acc_overview = account_overview(customer_id, db)
        return acc_overview
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error": f"{e}"
            }
        )