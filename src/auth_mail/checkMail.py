import smtplib
import ssl
from email.message import EmailMessage
from src.config import EMAIL, EMAIL_PASSWORD


async def send_email(email_receiver):
    # Define email sender and receiver
    email_sender = EMAIL
    email_password = EMAIL_PASSWORD

    # Set the subject and body of the email
    subject = 'Спасибо за регистрацию!'
    body = """
    Спасибо, что зарегистрировались на нашем сайте Nextop
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    try:
        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            return f"Сообщение было отправлено {email_receiver}"
    except Exception as e:
        return f"Произошла ошибка: {e}"

