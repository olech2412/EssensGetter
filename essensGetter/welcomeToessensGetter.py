import smtplib
import datetime
import logging
import sys

logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')

logging.info("A welcome email should be sent to the user")

email = str(sys.argv[1])
name = str(sys.argv[2])

current_day = str(datetime.date.strftime(datetime.date.today(), "%d.%m.%Y"))

content = "Moin, \n \n" + "Deine Email wurde angegeben um dir tagesaktuell die Gerichte, welche in der Mensa: " \
                          "Schoenauer Strasse serviert werden, zuzustellen. \n \n" + "Sollte das stimmen musst du " \
                                                                                     "nichts weiter tun. Falls es " \
                                                                                     "sich um einen Fehler handelt " \
                                                                                     "oder deine Daten (dein Name im " \
                                                                                     "Betreff) nicht korrekt " \
                                                                                     "sind " \
                                                                                     "antworte bitte auf diese Email." \
          + "\n \n" + "Bis denne," + "\n" + "dein Food-Bot - " + current_day

logging.info("Content: " + content)

SUBJECT = "Welcome to EssensGetter - " + name + " - " + current_day

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
    message = 'Subject: {}\n\n{}'.format(SUBJECT, content)
    smtpObj.sendmail(sender, email, message)

    smtpObj.quit()
    logging.info("Welcome Email sent successfully to: " + email)
    print("Welcome Email sent successfully to: " + email)
except Exception as e:
    logging.critical("Error with the email-sending: " + str(e))
    print("Error with the email-sending: " + str(e))
