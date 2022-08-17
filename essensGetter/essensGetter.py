from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs, Tag
import datetime
import calendar
from formatting import remove_HTML, format_food_price
from mail import send_Email
import logging

logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')

logging.info("Started")

def give_me_everything():
    data = soup.find_all(class_="meals")  # call everything that is in meals
    return data


# Fetches the prices from the website
def fetch_prices():
    data = soup.find_all(class_="meals__price")
    return data


# Fetches the category from the food
def fetch_food_category():
    data = soup.find_all(class_="title-prim")
    return remove_HTML(data)


# Fetches the names from the food
def fetch_food():
    data = soup.find_all(class_="meals__name")
    list_of_food = list()
    beilagen = list()
    test = data[0].findNext(class_="u-list-bare").__getattribute__("contents")
    for x in range(len(data)):
        try:
            list_of_food.append(data[x].__getattribute__("contents")[0])
            if data[x].findNext(class_="u-list-bare").__getattribute__("contents")[0] is not None:
                try:
                    for i in range(len(data[x].findNext(class_="u-list-bare").__getattribute__("contents"))):
                        if data[x].findNext(class_="u-list-bare").__getattribute__("contents")[i] != "\n":
                            beilagen.append(data[x].findNext(class_="u-list-bare").__getattribute__("contents")[i].get_text())
                        if i+1 == len(data[x].findNext(class_="u-list-bare").__getattribute__("contents")):
                            if(len(beilagen) == 1):
                                list_of_food.append(beilagen[0])
                            elif(len(beilagen) > 1):
                                beilagen = ", ".join(beilagen)
                                list_of_food.append(beilagen)
                            else:
                                list_of_food.append("")
                            beilagen = list()
                except Exception as e:
                    logging.warning("Warn: " + str(e) + " in " + str(data[x]))
                    print("Warn: " + str(e) + " in " + str(data[x]))
                    beilagen.append("")
            else:
                logging.warning("No beilagen found for meal: " + data[x].get_text())
                print("No beilagen found for meal: " + data[x].get_text())
                list_of_food.append("")
        except AttributeError as attribute_error:
            logging.warning("AttributeError: " + str(attribute_error) + " in " + str(data[x]))
            print("AttributeError: " + str(attribute_error) + " in " + str(data[x]))
            list_of_food.append("Keine Beilagen")


    return list_of_food


# don't do anything on weekends
if calendar.day_name[datetime.date.today().weekday()] == "Saturday" \
        or calendar.day_name[datetime.date.today().weekday()] == "Sunday":
    logging.info("Weekend -> no call on website and no other operations")
    print("Weekend -> no call on website and no other operations")
else:
    url = "https://www.studentenwerk-leipzig.de/mensen-cafeterien/speiseplan?location=140"  # URL
    session = HTMLSession()  # Initialize HTML Session
    response = session.get(url)  # call the URL

    if response.status_code != 200:  # If response != 200 don't try to read the data
        logging.critical("Response != 200 " + str(response.status_code))
    else:
        soup = bs(response.content, "html.parser")  # html parser from BeautifulSoup

        # give_me_everything() # Important to know which property's you can extract
        # convert the HTML List to usable data

        foodprice = format_food_price(fetch_prices())  # call the function to convert the HTML Stuff to usable data
        send_Email(food=fetch_food(), foodcategory=fetch_food_category(), foodprice=foodprice)
