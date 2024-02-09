import smtplib
import sys
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def email_bank(from_email , password , to_email , date , id , number):
    server_dict = {'gmail': 'smtp.gmail.com', 'outlook': 'smtp-mail.outlook.com', 'yahoo': 'smtp.mail.yahoo.com', 'proton': 'smtp.protonmail.ch', 'protonmail': 'smtp.protonmail.ch'}
    decide = from_email.split("@")
    server_decide = decide[1].split(".") 
    serve = server_decide[0]
    if serve in server_dict.keys():
        server = server_dict[serve]  
    else:
        return ("Email provider not supported currently")  
    try:
        smtp = smtplib.SMTP(server , 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(from_email , password)
    except OSError as e:
        return (f"Error occured: {e}")
    sub = "Debit Card application status"
    message = f"""Respected sir / ma'am\nThank you for choosing ABC Bank. We are happy to have you on board. As we have noticed, you have applied for a Debit Card on {date} and we are pleased to provide you the Debit Card number for your User ID {id}. \n\n\n\nYour debit card number is: {number}"""
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = sub
    msg.attach(MIMEText(message , "plain"))
    txt1 = msg.as_string()
    try:
        smtp.sendmail(from_email , to_email , txt1)
        return (f"Mail sent to your registered email address")
    except OSError as er:
        return (f"Error ocurred: {er}")