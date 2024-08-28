from yookassa import Payment
from yookassa.domain.request import PaymentRequest
import uuid


async def create_payment(amount,description,currency='RUB'):
    payment = Payment.create(
        {
            'amount': {
                'value': str(amount),
                'currency': currency
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://webhook.site/e8f5305f-bf3d-4afb-ba1e-3e0f93f23946'
            },
            "capture": True,
                "description": description,
                "metadata": {
                'order_id': str(uuid.uuid4())
        },
        })
    
    return payment


async def get_payment(payment_id):
    payment = Payment.find_one(payment_id)
    return payment.status