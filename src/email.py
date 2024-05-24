from src.extensions import mail
from flask_mail import Message


def send_email(email, username, reset_token):
    msg = Message("Reset Password",
                  recipients=[email])
    msg.body = f"""
    RECUPERAÇÃO DE SENHA
    Caro(a) {username},
    Use o token abaixo para criar uma nova senha:
    {reset_token}
    """
    mail.send(msg)
