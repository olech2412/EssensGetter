from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import smtplib
import datetime
import calendar


def format_string(string):
    string = str(string)
    string = string.replace("ä", "ae")
    string = string.replace("ö", "oe")
    string = string.replace("ü", "ue")
    string = string.replace("ß", "ss")
    string = string.replace("Ä", "Ae")
    string = string.replace("Ö", "Oe")
    string = string.replace("Ü", "Ue")
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.replace("'", "")
    string = string.replace("à", "a")
    string = string.replace("è", "e")
    string = string.replace("ì", "i")
    string = string.replace("ò", "o")
    string = string.replace("ù", "u")
    string = string.replace("À", "A")
    string = string.replace("È", "E")
    string = string.replace("Ì", "I")
    string = string.replace("Ò", "O")
    string = string.replace("Ù", "U")
    string = string.replace("â", "a")
    string = string.replace("ê", "e")
    string = string.replace("î", "i")
    string = string.replace("ô", "o")
    string = string.replace("û", "u")
    string = string.replace("Â", "A")
    string = string.replace("Ê", "E")
    string = string.replace("Î", "I")
    string = string.replace("Ô", "O")
    string = string.replace("Û", "U")
    string = string.replace("€", "Euro")
    return string


def send_Email(foodname, foodcategory, foodzusatz1, foodzusatz2, foodprice):

    food1 = format_string(foodcategory[0]) + " (" + format_string(foodprice[0]) + ")" + ": " + format_string(foodname[0]) + " [" + format_string(foodzusatz1) + "]"
    food2 = "\n" + format_string(foodcategory[1]) + " (" + format_string(foodprice[1]) + ")" +  ": " + format_string(foodname[1]) + " [" + format_string(foodzusatz2) + "]"

    current_day = str(datetime.date.strftime(datetime.date.today(), "%d.%m.%Y"))

    # add all Emails an Names to the list
    # TODO maybe use a dictionary instead of a list
    with open("recievers") as file:
        recievers = list()
        while (line := file.readline().rstrip()):
            recievers.append(line)

    names = list()
    emails = list()
    for x in range(len(recievers)):
        if x % 2 == 1:
            emails.append(recievers[x])
        else:
            names.append(recievers[x])

    content = "Moin {}, \n \n" + "Schau dir an was es heute in der Kantine (Schoenauer Strasse) zu essen gibt: \n \n" + food1 + "\n" + food2 + "\n \n" + "Bis denne," + "\n" + "dein Food-Bot - " + current_day

    SUBJECT = "Speiseplan - {} - " + current_day

    smtpServer = "securesmtp.t-online.de"
    port = 587
    # Zugangsdaten
    username = "essensGetter@t-online.de"
    password = "***********"
    # Sender & Empfänger
    sender = "essensGetter@t-online.de"
    # Erzeugen einer Mail Session
    smtpObj = smtplib.SMTP(smtpServer, port)
    smtpObj.starttls()
    smtpObj.login(username, password)

    for i in range(len(names)):
        message = 'Subject: {}\n\n{}'.format(SUBJECT.format(names[i]), content.format(names[i]))
        smtpObj.sendmail(sender, emails[i], message)

    smtpObj.quit()


def convert_HTML_List(data):
    zusätzeGes = data
    zusätzeGericht1 = list()
    zusätzeGericht2 = list()

    # remove HTML from the data
    for x in range(len(zusätzeGes)):
        zusätzeGes[x] = str(zusätzeGes[x]).replace("<li>", "")
        zusätzeGes[x] = str(zusätzeGes[x]).replace("</li>", "")
        zusätzeGes[x] = str(zusätzeGes[x]).replace("<ul>", "")
        zusätzeGes[x] = str(zusätzeGes[x]).replace("</ul>", "")
        zusätzeGes[x] = str(zusätzeGes[x]).replace("<ul >\n", "")
        zusätzeGes[x] = str(zusätzeGes[x]).replace("'", "")
        zusätzeGes[x] = str(zusätzeGes[x]).replace("<ul class=\"u-list-bare\">", "")

    zusätzeGericht1 = str(zusätzeGes[0])
    zusätzeGericht1 = zusätzeGericht1[1:]
    zusätzeGericht1 = zusätzeGericht1[:-1]
    if str(zusätzeGericht1).__contains__("\n"):
        zusätzeGericht1 = str(zusätzeGericht1).replace("\n", ", ")

    zusätzeGericht2 = str(zusätzeGes[1])
    zusätzeGericht2 = zusätzeGericht2[1:]
    zusätzeGericht2 = zusätzeGericht2[:-1]
    if str(zusätzeGericht2).__contains__("\n"):
        zusätzeGericht2 = str(zusätzeGericht2).replace("\n", ", ")

    return zusätzeGericht1, zusätzeGericht2


# Removes the HTML from the data
def remove_HTML(object):
    if isinstance(object, list):
        for i in range(len(object)):
            firstsplit = str(object[i]).split(">")
            del (firstsplit[0])
            secondsplit = str(firstsplit[0]).split("</")
            del (secondsplit[1])
            object[i] = secondsplit
    elif isinstance(object, str):
        print("String")
    else:
        print("Komischer Input - wird nicht verarbeitet")

    return object


# Call the whole website
def give_me_everything():
    data = soup.find_all(class_="meals")  # call everything that is in meals
    for i in range(len(data)):  # print the propertys
        print(data[i])

# Fetches the prices from the website
def fetch_prices():
    data = soup.find_all(class_="meals__price")
    return data

# Fetches the addons of the meals
def fetch_zusätze():
    data = soup.find_all(class_="u-list-bare")
    return data


# Fetches the categegorys from the food
def fetch_Food_Category():
    data = soup.find_all(class_="title-prim")
    return remove_HTML(data)

# Fetches the names from the food
def fetch_Food_Name():
    data = soup.find_all(class_="meals__name")
    return remove_HTML(data)

# Format the prices -> remove HTML Stuff and unnecessary stuff
def format_food_price(data):
    for x in range(len(data)):
        data[x] = str(data[x]).replace("<p class=\"meals__price\">\n<span class=\"u-hidden\">Preise:</span>\n", "")
        data[x] = str(data[x]).replace("</p>", "")
        data[x] = str(data[x]).replace(" ", "")

    return data


if (calendar.day_name[datetime.date.today().weekday()] == "Saturday" or calendar.day_name[
    datetime.date.today().weekday()] == "Sunday"):
    print("Heute ist ein Wochenende")
else:
    url = "https://www.studentenwerk-leipzig.de/mensen-cafeterien/speiseplan?location=140"  # URL
    session = HTMLSession()  # Initialize HTML Session
    response = session.get(url)  # call the URL

    if response.status_code != 200:  # If response != 200 don't try to read the data
        print("Error! Response = " + str(response.status_code))
    else:
        soup = bs(response.content, "html.parser")  # html parser from BeautifulSoup

        # give_me_everything() # Important to know which property's you can extract
        beilagen = convert_HTML_List(fetch_zusätze())  # call the function to convert the HTML List to usable data
        foodprice = format_food_price(fetch_prices())  # call the function to convert the HTML Stuff to usable data
        send_Email(foodname=fetch_Food_Name(), foodcategory=fetch_Food_Category(), foodzusatz1=str(beilagen[0]), foodzusatz2=(beilagen[1]), foodprice=foodprice)