import smtplib

def send_mail(your_email, your_password, to, subject, body):
    """
    Sends email.
    """

    # * sending mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(your_email, your_password)
    server.sendmail(your_email, to, f"Subject: {subject}\n\n{body}")
    server.quit()

    # print(f"Email to `{to}` has been sent successfully!")