import datetime
import json
import os
import smtplib
import sys
import time
from email import encoders

import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
from email.mime.audio import MIMEAudio  # Аудио
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
import zipfile






def process_attachement(files):  # Функция по обработке списка, добавляемых к сообщению файлов
    data =[]
    for f in files:
        if os.path.isfile(f):  # Если файл существует
            data.append(f)  # Добавляем файл к сообщению
        elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)  # Получаем список файлов в папке
            for file in dir:  # Перебираем все файлы и...
                data.append(f + "\\" + file)  # ...добавляем каждый файл к сообщению
    return data



def log(message):
    cur_path = os.path.abspath(os.curdir)
    now = datetime.datetime.now()
    data = {"Error": message, "date": now.strftime("%d-%m-%Y %H:%M:%S")}
    with open(cur_path + '\errors.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def archive(files):
    archive = zipfile.ZipFile('Archive.zip', mode='w')
    try:
        for file in files:
            name = file.split('\\', -1)[-1]
            archive.write(file, arcname=name)
            print("File - " + name)
            print('File added.')
    except:
        print('Reading files now.')
    archive.close()
    print("File - " + file)


def mail(config, archive):
    file_full = config['path']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = config['Subject']


    try:
        # path = file_full.split('\\', -1)
        name = 'Archive.zip'

        part = MIMEBase("application", "octet-stream")
        part.set_payload(open('Archive' + ".zip", "rb").read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=\"%s.zip\"" % ('Archive'))
        msg.attach(part)
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
    with open(path + '\\'+'result_config.jsonc', 'w', encoding='utf-8') as f:
        json.dump(configure, f, ensure_ascii=False, indent=4)


cur_path = os.path.abspath(os.curdir)
try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'errors.json')
    os.remove(cur_path + "\errors.json")
except FileNotFoundError:
    print("Removed")
now = datetime.datetime.now()
try:
    with open(cur_path + "\\result_config.jsonc", "r", encoding='utf-8') as f:
        config = json.load(f)
        for i in config['path']:
            print(i)
            i = i.replace("'\'", "'\\'")
        # config['path'] = config['path'].replace("'\'", "'\\'")
        files= process_attachement(config['path'])
        archive = archive(files)
        # print(archive)
        mail(config, archive)
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
