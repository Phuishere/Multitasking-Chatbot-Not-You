from os import getenv
import smtplib, ssl

# Gmail SMTP server configuration
MAIL_SERVER = getenv("MAIL_SERVER")
MAIL_PORT = getenv("MAIL_PORT")

def send_email(subject: str, content: str, receiver_email: str,
               sender_email: str = "fuishere.ha.ha.ha@gmail.com", password: str = None, is_server: bool = False) -> str:
    """
    Function to send email to an account to restore it.

    :content: Content of the email.
    :sender_email: SENDER's email address that will send the restoring email.
    :receiver_email: RECEIVER's email address that will receive the restoring email.
    :password: App password of sender's email
    :return: Status of email sending task
    """

    # Email content
    message = f"""Subject: {subject}\n\n{content}"""

    # If server send it
    if is_server:
        sender_email = getenv("MAIL_USERNAME")
        password = getenv("MAIL_PASSWORD")  # Use the App Password here
        print(password)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Connect to the Gmail SMTP server and send the email
    try:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server: # MAIL_SERVER is usually "smtp.gmail.com"
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)  # Log in to your Gmail account
            server.sendmail(sender_email, receiver_email, message)
            return f"Email has been sent successfully!\nContent:\n{content}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Replace with your own details
    password = getenv("MAIL_PASSWORD")
    status = send_email(subject = "Test email", content = "This is test email of Jarvis", sender_email = "phuhn.a1.2124@gmail.com",
               receiver_email = "fuishere.ha.ha.ha@gmail.com", password = password)
    print(f"status: {status}")