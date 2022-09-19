from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import StringIO
import pandas as pd
import smtplib

def send_email_notif(**kwargs):
    """
    Send email notification with the most proffitable products.
    
    kwargs:
        user(str): Email address of the sender.
        pwd(str): Password of the sender.
        recipient(str): Email address of the recipient.
        subject(str): Subject of the email.
        body(str): Body of the email.
        category_id(str): Category id of the products.
    """
    user = kwargs["user"]
    pwd = kwargs["pwd"]
    recipient = kwargs["recipient"]
    subject = kwargs["subject"]
    body = kwargs["body"]
    category_id = kwargs["category_id"]
    df = pd.read_csv(f"/opt/airflow/dags/datasets/{category_id}_clean.csv")
    send_most_proffitable_products_mail(user, pwd, recipient, subject, body, f"{category_id}_clean.csv", df)

def send_most_proffitable_products_mail(user, pwd, recipient, subject, body, filepath, df):
    """
    Send email notification with the most proffitable products.
    
    Args:
        user(str): Email address of the sender.
        pwd(str): Password of the sender.
        recipient(str): Email address of the recipient.
        subject(str): Subject of the email.
        body(str): Body of the email.
        filepath(str): Path of the file to be attached.
        df(pandas.DataFrame): Dataframe with the most proffitable products.
    """

    FROM = user
    TO = recipient
    TEXT = body

    #Filter df with records that have total_earnings > 7000000.
    df = df[df["total_earnings"] > 7000000]

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg.add_header('Content-Type','text/html')
        msg.attach(MIMEText(TEXT, 'html'))
        textStream = StringIO()
        df.to_csv(textStream,index=False)
        msg.attach(MIMEApplication(textStream.getvalue(), Name=filepath))

        server.sendmail(FROM, TO, msg.as_string().encode('utf-8'))
        server.close()
    except:
        print ("failed to send mail")