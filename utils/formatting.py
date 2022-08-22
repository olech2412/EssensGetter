import logging
import traceback

from bs4.element import NavigableString

logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s %(lineno)d - %(message)s', force=True, encoding='utf-8')


# Removes the HTML from the data
def remove_HTML(htmlContent):
    logging.info("Before formatting: " + str(htmlContent))
    if isinstance(htmlContent, list):
        for i in range(len(htmlContent)):
            first_split = str(htmlContent[i]).split(">")
            del (first_split[0])
            secondsplit = str(first_split[0]).split("</")
            del (secondsplit[1])
            htmlContent[i] = secondsplit
    elif isinstance(htmlContent, str):
        first_split = htmlContent.split(">")
        del (first_split[0])
        secondsplit = first_split[0].split("</")
        del (secondsplit[1])
        htmlContent = secondsplit
    else:
        logging.error("Unknown datatype -> no formatting")
        print("Unknown datatype -> no formatting")

    logging.info("After fromatting: " + str(htmlContent))
    print("After fromatting: " + str(htmlContent))

    return htmlContent


# Converts the data to a usable format -> email needs ascii so no special characters
def format_string(nonAsciiStr):
    logging.debug("Before formatting: " + str(nonAsciiStr) + "\n")
    nonAsciiStr = str(nonAsciiStr)
    nonAsciiStr = nonAsciiStr.replace("ä", "ae")
    nonAsciiStr = nonAsciiStr.replace("ö", "oe")
    nonAsciiStr = nonAsciiStr.replace("ü", "ue")
    nonAsciiStr = nonAsciiStr.replace("ß", "ss")
    nonAsciiStr = nonAsciiStr.replace("Ä", "Ae")
    nonAsciiStr = nonAsciiStr.replace("Ö", "Oe")
    nonAsciiStr = nonAsciiStr.replace("Ü", "Ue")
    nonAsciiStr = nonAsciiStr.replace("[", "")
    nonAsciiStr = nonAsciiStr.replace("]", "")
    nonAsciiStr = nonAsciiStr.replace("'", "")
    nonAsciiStr = nonAsciiStr.replace("à", "a")
    nonAsciiStr = nonAsciiStr.replace("è", "e")
    nonAsciiStr = nonAsciiStr.replace("ì", "i")
    nonAsciiStr = nonAsciiStr.replace("ò", "o")
    nonAsciiStr = nonAsciiStr.replace("ù", "u")
    nonAsciiStr = nonAsciiStr.replace("À", "A")
    nonAsciiStr = nonAsciiStr.replace("È", "E")
    nonAsciiStr = nonAsciiStr.replace("Ì", "I")
    nonAsciiStr = nonAsciiStr.replace("Ò", "O")
    nonAsciiStr = nonAsciiStr.replace("Ù", "U")
    nonAsciiStr = nonAsciiStr.replace("â", "a")
    nonAsciiStr = nonAsciiStr.replace("ê", "e")
    nonAsciiStr = nonAsciiStr.replace("î", "i")
    nonAsciiStr = nonAsciiStr.replace("ô", "o")
    nonAsciiStr = nonAsciiStr.replace("û", "u")
    nonAsciiStr = nonAsciiStr.replace("Â", "A")
    nonAsciiStr = nonAsciiStr.replace("Ê", "E")
    nonAsciiStr = nonAsciiStr.replace("Î", "I")
    nonAsciiStr = nonAsciiStr.replace("Ô", "O")
    nonAsciiStr = nonAsciiStr.replace("Û", "U")
    nonAsciiStr = nonAsciiStr.replace("€", "Euro")
    logging.debug("After formatting: " + str(nonAsciiStr) + "\n")
    return nonAsciiStr


# Format the prices -> remove HTML Stuff and unnecessary stuff
def format_food_price(data):
    logging.info("Prices before formatting:\n " + str(data))
    for x in range(len(data)):
        data[x] = str(data[x]).replace("<p class=\"meals__price\">\n<span class=\"u-hidden\">Preise:</span>\n", "")
        data[x] = str(data[x]).replace("</p>", "")
        data[x] = str(data[x]).replace(" ", "")
    logging.info("Prices after formatting: " + str(data))
    print("Prices after formatting: " + str(data))
    return str(data)


def format_meals_from_list(list_of_all_meals):
    """Converts the list_of_all_meals into a dictionary with all special possibilities

    Takes the fetched Data from essensGetter.py and convert it into dictionaries. Because multiple meals are possible
    each dictionary will be added to a list.
    :param list_of_all_meals:
    :return: meals
    """

    meals = list()

    for x in list_of_all_meals:
        try:
            if len(x) == 2:
                meal = {"category": x[0].__getattribute__("contents")[0], "food": "", "beilagen": "", "price": ""}

                html_food_content = x[1].__getattribute__("contents")
                for y in html_food_content:
                    if isinstance(y, NavigableString):
                        html_food_content.remove(y)

                food_list = list()
                price_list = list()
                for y in html_food_content:
                    food_list.append(y.find_all(class_="meals__name")[0].__getattribute__("contents")[0])
                    price_list.append(format_food_price(y.find_all(class_="meals__price")))
                meal["food"] = food_list
                meal["price"] = price_list

                beilagen_list = list()
                for y in html_food_content:
                    try:
                        for z in y.find_all(class_="u-list-bare")[0]:
                            if isinstance(z, NavigableString) is False:
                                beilagen_list.append(remove_HTML(str(z)))
                    except Exception as e:
                        logging.warning("No beilagen found")
                        print("No beilagen found")
                meal["beilagen"] = beilagen_list

                meals.append(meal)
        except Exception as e:
            logging.error("Error in format_meals_from_list for a meal containing 2 Attr.: " + str(e))
            print("Error in format_meals_from_list for a meal containing 2 Attr.: " + str(e))
            continue

        try:
            if len(x) == 3:
                meal = {"category": x[0].__getattribute__("contents")[0], "food": "", "beilagen": "", "price": "",
                        "additional_info": ""}

                try:
                    meal["additional_info"] = x[1].__getattribute__("contents")[0]
                except AttributeError as e:
                    logging.error("No additional info available: " + str(e))
                    print("No additional info available: " + str(e))
                    meal["additional_info"] = ""

                html_food_content = x[2].__getattribute__("contents")
                for y in html_food_content:
                    if isinstance(y, NavigableString):
                        html_food_content.remove(y)

                food_list = list()
                price_list = list()
                for y in html_food_content:
                    food_list.append(y.find_all(class_="meals__name")[0].__getattribute__("contents")[0])
                    price_list.append(format_food_price(y.find_all(class_="meals__price")))
                meal["food"] = food_list
                meal["price"] = price_list

                beilagen_list = list()
                for y in html_food_content:
                    try:
                        for z in y.find_all(class_="u-list-bare")[0]:
                            if isinstance(z, NavigableString) is False:
                                beilagen_list.append(z)
                    except Exception as e:
                        logging.warning("No beilagen available")
                        print("No beilagen available")
                meal["beilagen"] = beilagen_list

                meals.append(meal)

        except Exception as e:
            logging.exception("Error in format_meals_from_list for a meal containing 3 Attr.: " + str(e))
            print("Error in format_meals_from_list for a meal containing 3 Attr.: " + str(e))

    return meals
