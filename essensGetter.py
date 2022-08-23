from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from bs4.element import Tag, NavigableString
import datetime
import calendar
from utils.formatting import remove_HTML, format_food_price, format_meals_from_list
from utils.mail import send_Email
import logging

logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')

logging.info("Started")


def give_me_everything():
    data = soup.find_all(class_="meals")  # call everything that is in meals
    return data


# Fetches the category from the food
def fetch_food_from_website():
    html_class_meals = soup.find_all(class_="meals")[0].__getattribute__("contents")
    food_categorys = soup.find_all(class_="title-prim")

    list_of_categorys_index = list()
    list_of_all_meals = list()

    for x in html_class_meals:
        if isinstance(x,NavigableString):
            html_class_meals.remove(x)

    for x in food_categorys:
        list_of_categorys_index.append(html_class_meals.index(x))
    list_of_categorys_index.append(len(html_class_meals))

    for x in food_categorys:
        one_meal = list()
        count = list_of_categorys_index[food_categorys.index(x)]
        for y in html_class_meals[count:list_of_categorys_index[food_categorys.index(x) + 1]:1]:
            one_meal.append(y)

            if html_class_meals.index(y) == list_of_categorys_index[food_categorys.index(x) + 1] -1:
                list_of_all_meals.append(one_meal)

    return list_of_all_meals


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
        meals = format_meals_from_list(fetch_food_from_website())
        send_Email(meals)
