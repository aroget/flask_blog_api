import os
import sendgrid
import urllib.request as urllib
from sendgrid.helpers.mail import Email, Content, Mail, Personalization, Substitution

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

TEMPLATES = {
    'WELCOME_EMAIL': '94d7e34f-69cb-4744-a920-e07758c3e842',
    'INVITE_EMAIL': '94d7e34f-69cb-4744-a920-e07758c3e842',
    'NEW_POST_EMAIL': '94d7e34f-69cb-4744-a920-e07758c3e842',
}


def send_welcome_email(to_email = None, to_name = None):
    mail = Mail()

    mail.from_email = Email("noreply@email.com", "App Name")
    mail.subject = "Thanks for Joining!"

    personalization = Personalization()
    personalization.add_to(Email(to_email, to_name))
    personalization.add_substitution(Substitution("%firstname%", to_name))

    mail.add_personalization(personalization)

    mail.template_id = TEMPLATES['WELCOME_EMAIL']

    send_email(data=mail.get())

def send_email(data):
    try:
        response = sg.client.mail.send.post(request_body=data)
    except urllib.HTTPError as e:
        print (e.read())
        exit()