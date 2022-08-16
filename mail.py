import os
import smtplib
import datetime
import logging
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from formatting import format_string

logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')


def send_Email(food, foodcategory, foodprice):
    # Fleischgericht
    food1 = format_string(foodcategory[0]) + " (" + format_string(foodprice[0]) + ")" + ": " \
            + format_string(food[0]) + " [" + format_string(food[1]) + "]"
    logging.info("Food1: " + food1)
    # Vegetarisches Gericht
    food2 = format_string(foodcategory[1]) + " (" + format_string(foodprice[1]) + ")" \
            + ": " + format_string(food[2]) + " [" + format_string(food[3]) + "]"
    logging.info("Food2: " + food2)

    current_day = str(datetime.date.strftime(datetime.date.today(), "%d.%m.%Y"))

    # add all Emails an Names to the list
    # TODO maybe use a dictionary instead of a list
    try:
        with open("receivers") as file:
            receivers = list()
            while line := file.readline().rstrip():
                receivers.append(line)
    except Exception as e:
        logging.critical("Error with the receivers-list: " + str(e))
        return

    names = list()
    emails = list()
    for x in range(len(receivers)):
        if x % 2 == 1:
            emails.append(receivers[x])
        else:
            names.append(receivers[x])

    content = "Moin {}, \n \n" + "Schau dir an was es heute in der Kantine (Schoenauer Strasse) zu essen gibt: \n \n" \
              + food1 + "\n" + food2 + "\n \n" + "Bis denne," + "\n" + "dein Food-Bot - " + current_day

    logging.info("Content: " + content)

    SUBJECT = "Speiseplan - {} - " + current_day

    with open("EssensGetter Logo.png", 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'Speiseplan'
    msg['From'] = 'essensGetter@t-online.de'
    msg['To'] = 'olechristoph2412@gmail.com'

    text = MIMEText('<img src="cid:image1">', 'html')
    msg.attach(text)
    fp = open('EssensGetter_Logo_small.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    try:
        smtpServer = "securesmtp.t-online.de"
        port = 587
        # Zugangsdaten
        username = "essensGetter@t-online.de"
        # Sender & Empfänger
        sender = "essensGetter@t-online.de"
        # Erzeugen einer Mail Session
        smtpObj = smtplib.SMTP(smtpServer, port)
        smtpObj.starttls()
        with open("credentials") as file:
            while line := file.readline().rstrip():
                password = line
        smtpObj.login(username, password)

        for i in range(len(names)):
            # message = 'Subject: {}\n\n{}'.format(SUBJECT.format(names[i]), content.format(names[i]))
            smtpObj.sendmail(sender, emails[i], content)

        smtpObj.quit()
        logging.info("Email sent successfully to: " + str(names))
    except Exception as e:
        logging.critical("Error with the email-sending: " + str(e))
