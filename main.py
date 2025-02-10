from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from .utils import initiate_payment_with_flutterwave, get_payment_status_from_flutterwave
from .models import PaymentPublic, PaymentCreate, Payment, PaymentFlutterwave
from .database import create_db_and_tables, engine


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/payments/initiate", response_model=PaymentPublic)
def initiate_payment(*, session: Session = Depends(get_session), payment: PaymentCreate):
    # Check if a payment with this reference already exists
    p = session.exec(select(Payment).where(Payment.tx_ref == payment.tx_ref)).first()
    if p:
        raise HTTPException(status_code=422, detail="Payment already exists")

    # Recording in the database
    db_payment = Payment.model_validate(payment)
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)

    # Sending payment to Flutterwave
    flutterwave_payment = PaymentFlutterwave.model_validate(db_payment)
    response = initiate_payment_with_flutterwave(flutterwave_payment)
    data = response.json()

    if response.status_code == 200:
        db_payment.status = data["data"]["status"]
        db_payment.comment = data["data"]["processor_response"]
    else:
        db_payment.status = "failed"
        if "message" in data:
            db_payment.comment = data["message"]

    # Status update in the database
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)

    return db_payment


@app.get("/payments/verify", response_model=PaymentPublic)
def verify_payment(*, session: Session = Depends(get_session), transaction_id: str):
    payment = session.exec(select(Payment).where(Payment.tx_ref == transaction_id)).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.status is None or payment.status == "pending":
        response = get_payment_status_from_flutterwave(payment.tx_ref)
        data = response.json()
        if response.status_code != 200:
            return payment
        if data["status"] != "success":
            return payment

        payment.status = data["data"]["status"]
        payment.comment = data["data"]["processor_response"]

        # Status update in the database
        session.add(payment)
        session.commit()
        session.refresh(payment)

    return payment
