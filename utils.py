import requests

from .config import settings
from .models import PaymentFlutterwave


def initiate_payment_with_flutterwave(payment: PaymentFlutterwave):
    url = "https://api.flutterwave.com/v3/charges?type=mobile_money_franco"

    payload = {
        "amount": payment.amount,
        "currency": payment.currency,
        "phone_number": payment.phone,
        "email": payment.email,
        "tx_ref": payment.tx_ref,
        "country": payment.country
    }

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + settings.API_TOKEN,
        "Content-Type": "application/json"
    }

    return requests.post(url, json=payload, headers=headers)


def get_payment_status_from_flutterwave(reference: str):
    url = "https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref=" + reference

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + settings.API_TOKEN,
        "Content-Type": "application/json"
    }

    return requests.get(url, headers=headers)
