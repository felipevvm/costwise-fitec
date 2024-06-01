from src.extensions import mail
from flask_mail import Message


def send_email(email, username, reset_url):
    msg = Message("Reset Password",
                  recipients=[email])
    msg.body = f"""
    RECUPERAÇÃO DE SENHA
    Caro(a) {username},
    Use o link abaixo para recuperar sua senha:
    {reset_url}
    
    Se você não solicitou a recuperação de senha, por favor, ignore este e-mail.
    """
    mail.send(msg)
