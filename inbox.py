import smtplib as smtp
import os

def send_message(text):
    print("mail")

    email = "ancprotektest@yandex.ru"
    password = "1qaz2wsx3edc"
    dest_email = "moonlight12345678@yandex.ru"
    subject = "TEMA"
    email_text = "TEXT"

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                           dest_email,
                                                           subject,
                                                           text)

    server = smtp.SMTP_SSL('smtp.yandex.com')
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    server.sendmail(email, dest_email, message)
    server.quit()

def file(text_file):
    print("file")
    for linef in text_file:
        print(linef)
    print("-----------------------------------------end func-----------------------------------------")
    return text_file





def mail():
    print("a")