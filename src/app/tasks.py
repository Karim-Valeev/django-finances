import random
import string

from django.contrib.auth.hashers import make_password

from app.models import WalletUser
from app.models.user_model import UnverifiedUserCode
from finances import settings
from finances.celery import app
from django.core.mail import send_mail


@app.task(queue="default")
def send_code(email):
    print("Sending code to the email...")
    user = WalletUser.objects.get(email=email)
    code = generate_code()
    UnverifiedUserCode.objects.create(user=user, code=make_password(code, salt='karimka'))
    print(code)
    email_text = f"Ваш код для подтверждения почты: {code}"
    send_mail(
        "Подтверждение почты в Wallet",
        email_text,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )


def generate_code():
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(6))
