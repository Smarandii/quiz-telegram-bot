import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from modules.content import FORMS_FILE_PATH
SENDER = 'sds.project.bot@gmail.com'
PASSWORD = 'sds_project_bot2020'
PORT = 465


def create_message(sender, receiver, message_text, subject):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    return message


def get_attachment():
    file_name = FORMS_FILE_PATH
    attachment_file = open(file_name, 'rb')
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(attachment_file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', "attachment; filename= " + file_name)
    return attachment


def send_email_message(message, receiver):
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT) as server:
        server.login(SENDER, PASSWORD)
        text = message.as_string()
        server.sendmail(SENDER, receiver, text)
    print(f"Sent {receiver}")
    pass


def send_forms(receiver=SENDER):
    """This function send form.csv file to sds.project.bot@gmail.com"""
    message_text = """\
            Анкеты 
            """

    message = create_message(sender=SENDER,
                             receiver=receiver,
                             message_text=message_text,
                             subject='Анекты')

    attachment = get_attachment()
    message.attach(attachment)
    send_email_message(message, receiver)


if __name__ == '__main__':
    send_forms()
