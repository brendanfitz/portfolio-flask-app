port = 465
smtp_server = "smtp.gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "Rangers Game Tonight!"
message["From"] = sender_email
message["To"] = receiver_email
