# Create secure connection with server and send email
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, sender_email_password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
