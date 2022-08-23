import smtplib
import datetime
import logging
from utils.formatting import format_string

logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')


def send_Email(meals):
    actual_meals = list()
    for x in meals:
        if x["beilagen"] == []:
            x["beilagen"].append("Keine Beilagen")
        if len(x) == 5:
            food_list_conv = list()

            for y in x["food"]:
                food_list_conv.append(format_string(y) + " - " + format_string(x["price"][x["food"].index(y)]) + "\n")

            food = format_string(str(x["category"]) + " --" + str(x["additional_info"])) + "-- : \n" + "".join(
                food_list_conv)
            actual_meals.append(food)
        elif len(x) == 4:
            food = format_string(str(x["category"])) + ": " + "\n" + format_string(str(x["food"])) \
                   + " [" + format_string(str(x["beilagen"])) + "]" + " - " + format_string(str(x["price"])) \
                   + "\n"
            actual_meals.append(food)

    current_day = str(datetime.date.strftime(datetime.date.today(), "%d.%m.%Y"))

    # add all Emails and Names to the list
    try:
        with open("utils/receivers") as file:
            receivers = list()
            while line := file.readline().rstrip():
                receivers.append(line)
    except Exception as e:
        logging.critical("Error with the receivers-list: " + str(e))
        print("Error with the receivers-list: " + str(e))
        return

    names = list()
    emails = list()
    for x in range(len(receivers)):
        if x % 2 == 1:
            emails.append(receivers[x])
        else:
            names.append(receivers[x])

    content = "Moin {}, \n \n" + "Schau dir an was es heute in der Kantine (Schoenauer Strasse) zu essen gibt: \n \n" \
              + actual_meals[0] + "\n" + actual_meals[
                  1] + "\n \n" + "Bis denne," + "\n" + "dein Food-Bot - " + current_day

    logging.info("Content: " + content)

    SUBJECT = "Speiseplan - {} - " + current_day

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
        with open("utils/credentials") as file:
            while line := file.readline().rstrip():
                password = line
        smtpObj.login(username, password)

        for i in range(len(names)):
            message = 'Subject: {}\n\n{}'.format(SUBJECT.format(names[i]), content.format(names[i]))
            smtpObj.sendmail(sender, emails[i], message)

        smtpObj.quit()
        logging.info("Email sent successfully to: " + str(names))
    except Exception as e:
        logging.critical("Error with the email-sending: " + str(e))
