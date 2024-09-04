import math
from typing import List
from sqlalchemy.orm import Session
from app.models import Loan, Payment
from app.services.users import get_user
from sqlalchemy import func
from app.schemas import (
    RequestLoan,
    PaymentSchema,
    PaymentInfo,
    LoanInfo,
    LoanOverview,
    AccountOverview,
)


def calculate_interest(principal_amount, tennure, interest_rate):
    annual_int = principal_amount * tennure * interest_rate
    return annual_int


def get_loans_for_user(db: Session, user_id: int) -> List[Loan]:
    loans = db.query(Loan).filter(Loan.customer_id == user_id).all()
    return loans


def calculate_emi(total_amt, tennure):
    emi = total_amt / (tennure * 12)
    return emi


def calcualte_remaning_months(total_amt, emi):
    if total_amt < emi:
        return 1
    elif total_amt == 0:
        return 0
    return total_amt // emi


def recalculate_emi(total, remaining_months):
    return math.ceil(total / remaining_months)


def get_loan(loan_id: int, db: Session) -> Loan:
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    return loan


def save_payment(amount, loan_id, payment_type, db: Session):
    payment = Payment(loan_id=loan_id, amount=amount, payment_type=payment_type)
    db.add(payment)
    db.commit()
    return payment


def pay_emi(loan: Loan, db: Session) -> dict:
    loan.total_amt -= loan.emi
    if loan.total_amt <= 0:
        loan.completed = True
        loan.total_amt = 0
        loan.emi = 0
    payment = save_payment(loan.emi, loan.id, "emi", db)
    # db.commit()
    return {
        "status": "success",
        "loan": loan.id,
        "transaction": {
            "type": "emi",
            "paid": payment.amount,
            "balance": loan.total_amt,
            "current_emi": loan.emi,
            "period_left": f"{calcualte_remaning_months(loan.total_amt, loan.emi)} months",
        },
    }


def pay_lumpsum(payment: PaymentSchema, loan: Loan, db: Session):
    paid, rem_months, new_emi = 0, 0, 0
    if payment.amount > loan.total_amt:
        paid = loan.total_amt
        loan.total_amt = 0
        loan.emi = 0
        loan.completed = True
    else:
        paid = payment.amount
        loan.total_amt -= paid
        rem_months = calcualte_remaning_months(loan.total_amt, loan.emi)
        new_emi = recalculate_emi(loan.total_amt, rem_months)
        loan.emi = new_emi
    payment = save_payment(paid, loan.id, "lumpsum", db)
    # db.commit
    return {
        "status": "success",
        "loan": loan.id,
        "transaction": {
            "type": "lumpsum",
            "paid": paid,
            "balance": math.ceil(loan.total_amt),
            "new_emi": loan.emi,
            "period_left": f"{calcualte_remaning_months(loan.total_amt, loan.emi)} months",
        },
    }


def make_payment(payment: PaymentSchema, db: Session) -> dict:
    if not (loan := get_loan(payment.loan_id, db)):
        return {
            "status": "failed",
            "detail": f"Loan with {payment.loan_id} id does not exist",
        }
    if loan.completed or loan.total_amt <= 0:
        return {"status": "success", "detail": "Loan is paid"}
    p_type = payment.payment_type
    if p_type == "lumpsum":
        status = pay_lumpsum(payment, loan, db)
    elif p_type == "emi":
        status = pay_emi(loan, db)
    else:
        status = {"status": "failed", "detail": f"Invalid payment type [{p_type}]"}
    return status


def create_loan(loan_req: RequestLoan, db: Session) -> dict:
    if not (get_user(loan_req.customer_id, db)):
        return {
            "status": "failed",
            "reason": f"Customer with id {loan_req.customer_id} does not exist",
        }

    total_amt = loan_req.loan_amount + calculate_interest(
        loan_req.loan_amount, loan_req.tennure_in_years, loan_req.rate_of_interest / 100
    )
    emi = calculate_emi(total_amt, loan_req.tennure_in_years)

    loan = Loan(
        principal_amount=loan_req.loan_amount,
        tenure=loan_req.tennure_in_years,
        interest_rate=loan_req.rate_of_interest / 100,
        total_amt=total_amt,
        emi=emi,
        customer_id=loan_req.customer_id,
    )
    db.add(loan)
    db.commit()
    return {
        "status": "success",
        "loan": {
            "id": loan.id,
            "total_amout": loan.total_amt,
            "interest": f"{loan.interest_rate * 100}%",
            "emi": round(loan.emi, 2),
            "return_period": f"{loan.tenure * 12} months",
        },
    }


def get_loan_payments(loan_id: int, db: Session) -> List[PaymentInfo]:
    payments = db.query(Payment).filter(Payment.loan_id == loan_id).all()
    list_of_payments = [PaymentInfo.from_orm(obj) for obj in payments]
    return list_of_payments


def collect_ledger_info(loan_id: int, db: Session):
    loan = get_loan(loan_id, db)
    if loan:
        ledger_info = LoanInfo(
            customer_id=loan.customer_id,
            loan_id=loan.id,
            balance=loan.total_amt,
            emi=loan.emi,
            months_left=calcualte_remaning_months(loan.total_amt, loan.emi),
            payments=get_loan_payments(loan.id, db),
        )
        return ledger_info
    return {"status": "failed", "detail": f"No loan with id {loan_id}"}


def loan_overview(loans: List[Loan], db: Session) -> List[LoanOverview]:
    if not loans:
        return []
    overviews = []
    for loan in loans:
        amount_paid = (
            db.query(func.sum(Payment.amount))
            .filter(Payment.loan_id == loan.id)
            .scalar()
            or 0.0
        )
        interest = calculate_interest(
            loan.principal_amount, loan.tenure, loan.interest_rate
        )
        ov = LoanOverview(
            loan_id=loan.id,
            principal_amount=loan.principal_amount,
            total_amount=loan.principal_amount + interest,
            emi_amount=loan.emi,
            total_interest=interest,
            amount_paid=amount_paid,
            remaining_emis=calcualte_remaning_months(loan.total_amt, loan.emi),
        )
        overviews.append(ov)
    return overviews


def account_overview(customer_id: int, db: Session):
    user = get_user(customer_id, db)
    if not user:
        return {"status": "failed", "detail": "Invalid customer id"}
    loans = get_loans_for_user(db, user.id)
    overviews = loan_overview(loans, db)
    account_ov = AccountOverview(customer_id=user.id, email=user.email, loans=overviews)
    return account_ov
