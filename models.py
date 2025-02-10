from sqlmodel import SQLModel, Field


# Shared properties
class PaymentBase(SQLModel):
    tx_ref: str = Field(unique=True, index=True)
    phone: str
    amount: int
    currency: str
    email: str
    country: str


# Payload sent to Flutterwave
class PaymentFlutterwave(PaymentBase):
    pass


# Payment Table
class Payment(PaymentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str | None = None
    comment: str | None = None


# Payload sent to the payment initiation endpoint
class PaymentCreate(PaymentBase):
    pass


# Payload returned by the payment initiation and verification endpoints
class PaymentPublic(PaymentBase):
    status: str
    comment: str | None = None
