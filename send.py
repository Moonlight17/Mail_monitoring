import smtplib as smtp
import os


def send_message():
    print("mail")

    email = "president-plus-66@yandex.ru"
    password = "vidfgsguddubmnec"
    dest_email = "moonlight12345678@yandex.ru"
    subject = "Usage"
    email_text = "12346789"

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                           dest_email,
                                                           subject,
                                                           email_text)
    # gmail_user = 'you@gmail.com'
    # gmail_password = 'P@ssword!'

    try:
        server = smtp.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email, password)
    except:
        print ('Something went wrong...')

# def file(text_file):
#     print("file")
#     for linef in text_file:
#         print(linef)
#     print("-----------------------------------------end func-----------------------------------------")


def mail():
    with open('text.txt', 'r')as text_file:
        text = text_file.read().split('\n')
        # print("text_file:", text_file)
        return text
    send_message(text)
