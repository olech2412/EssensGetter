from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import datetime
import calendar
from formatting import convert_HTML_List, remove_HTML, format_food_price
from mail import send_Email


def give_me_everything():
    data = soup.find_all(class_="meals")  # call everything that is in meals
    for i in range(len(data)):  # print the property's
        print(data[i])


# Fetches the prices from the website
def fetch_prices():
    data = soup.find_all(class_="meals__price")
    return data


# Fetches the addons of the meals
def fetch_beilagen():
    data = soup.find_all(class_="u-list-bare")
    return data


# Fetches the category from the food
def fetch_food_category():
    data = soup.find_all(class_="title-prim")
    return remove_HTML(data)


# Fetches the names from the food
def fetch_Food_Name():
    data = soup.find_all(class_="meals__name")
    return remove_HTML(data)

print(calendar.day_name[datetime.date.today().weekday()])
# don't do anything on weekends
if calendar.day_name[datetime.date.today().weekday()] == "Saturday" or calendar.day_name[datetime.date.today().weekday()] == "Sunday":
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
        beilagen = convert_HTML_List(fetch_beilagen())  # call the function to convert the HTML List to usable data
        foodprice = format_food_price(fetch_prices())  # call the function to convert the HTML Stuff to usable data
        send_Email(foodname=fetch_Food_Name(), foodcategory=fetch_food_category(), foodzusatz1=str(beilagen[0]),
                   foodzusatz2=(beilagen[1]), foodprice=foodprice)
