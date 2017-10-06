import os
import sendgrid
import urllib.request as urllib
from sendgrid.helpers.mail import Email, Content, Mail

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

TEMPLATES = {
    'WELCOME_EMAIL': '94d7e34f-69cb-4744-a920-e07758c3e842',
    'INVITE_EMAIL': '94d7e34f-69cb-4744-a920-e07758c3e842',
    'NEW_POST_EMAIL': '94d7e34f-69cb-4744-a920-e07758c3e842',
}

def send_email(templateId=TEMPLATES['WELCOME_EMAIL']):
    from_email = Email("test@example.com")
    to_email = Email("andresroget@gmail.com")
    subject = "Hello Welcome to our App"
    content = Content("text/html", "_")
    mail = Mail(from_email, subject, to_email, content)
    mail.template_id = templateId

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except urllib.HTTPError as e:
        print (e.read())
        exit()