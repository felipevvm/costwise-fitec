from src.extensions import mail
from flask_mail import Message
def send_email(email, username, reset_url):
    msg = Message("Reset Password",
                  recipients=[email])
    msg.body = f"""
    RECUPERAÇÃO DE SENHA
    Caro(a) {username},
    Clique no link para criar uma nova senha:
    {reset_url}
    """
    mail.send(msg)