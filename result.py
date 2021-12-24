import datetime
import json
import os
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def log(message):
    cur_path = os.path.abspath(os.curdir)
    now = datetime.datetime.now()
    data = {"Error": message, "date": now.strftime("%d-%m-%Y %H:%M:%S")}
    with open(cur_path + '\errors.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def mail(config):
    file_full = config['path']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = config['Subject']
    try:
        path = file_full.split('\\', -1)
        name = path[-1]
        file = open(file_full)
        attachment = MIMEText(file.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=name)
        msg.attach(attachment)
    except FileNotFoundError:

        log("Отсутствует отправляемый файл")
        exit(1)
    try:
        smtpObj = smtplib.SMTP_SSL(config['auth']['server'], config['auth']['port'])
        smtpObj.login(config['auth']['email'], config['auth']['password'])
        smtpObj.sendmail(config['mail_to'], config['mail_to'], msg.as_string())
        smtpObj.quit()
    except smtplib.SMTPAuthenticationError:
        log("Ошибка логина или пароля")
        exit(1)
    except UnicodeEncodeError:
        log("В логине или пароле есть русский символ")
        exit(1)
    except ConnectionRefusedError:
        log("Стоит проверить порт подключения")
        exit(1)
    except Exception as e:  # pylint: disable=broad-except
        log("Стоит проверить сервер подключения")
        sys.exit(f"SMTP exception {e}")
        exit(1)


def config(path):
    configure = {"auth": {"email": "###@ancprotek.ru", "password": "###", "server": "mail.ancprotek.ru", "port": "465"},
                 "Subject": "File from project", "path": "text.txt", "mail_to": "serov@ancprotek.ru"}
    with open(path + '\config.jsonc', 'w', encoding='utf-8') as f:
        json.dump(configure, f, ensure_ascii=False, indent=4)


cur_path = os.path.abspath(os.curdir)
try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'errors.json')
    os.remove(cur_path + "\errors.json")
except FileNotFoundError:
    print("Removed")
now = datetime.datetime.now()
try:
    with open(cur_path + "\config.jsonc", "r", encoding='utf-8') as f:
        config = json.load(f)
        config['path'] = config['path'].replace("'\'", "'\\'")
        mail(config)
except json.decoder.JSONDecodeError:
    log("Проверьте правильность определения пути")
    exit(1)
except FileNotFoundError:
    data = {"Error": "Отсутствует кофигурационный файл. В этой же папке был создан шаблонный",
            "date": now.strftime("%d-%m-%Y %H:%M:%S")}
    with open(cur_path + '\errors.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    config(cur_path)
    print("Отсутствует кофигурационный файл")
    exit(1)

time.sleep(3)
