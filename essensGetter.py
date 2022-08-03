from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
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
    for i in range(len(data)):  # print the property's
        print(data[i])


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
    for x in range(len(data)):
        try:
            list_of_food.append(data[x].__getattribute__("contents")[0])
            list_of_food.append(data[x].findNext(class_="u-list-bare").__getattribute__("contents")[1].__getattribute__("contents")[0])
        except AttributeError as attribute_error:
            logging.warning("AttributeError: " + str(attribute_error) + " in " + str(data[x]))
            list_of_food.append("")


    return list_of_food


# don't do anything on weekends
if calendar.day_name[datetime.date.today().weekday()] == "Saturday" \
        or calendar.day_name[datetime.date.today().weekday()] == "Sunday":
    logging.info("Weekend -> no call on website and no other operations")
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
