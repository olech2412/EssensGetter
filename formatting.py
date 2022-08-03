import logging


logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')


# Removes the HTML from the data
def remove_HTML(object):
    logging.info("Before formatting: " + str(object))
    if isinstance(object, list):
        for i in range(len(object)):
            first_split = str(object[i]).split(">")
            del (first_split[0])
            secondsplit = str(first_split[0]).split("</")
            del (secondsplit[1])
            object[i] = secondsplit
    elif isinstance(object, str):
        logging.error("A string is given -> no formatting ")
    else:
        logging.error("Unknown datatype -> no formatting")

    logging.info("After fromatting: " + str(object))

    return object


# Converts the data to a usable format -> email needs ascii so no special characters
def format_string(string):
    logging.debug("Before formatting: " + str(string) + "\n")
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
    logging.debug("After formatting: " + str(string) + "\n")
    return string


# Format the prices -> remove HTML Stuff and unnecessary stuff
def format_food_price(data):
    logging.info("Prices before formatting: " + str(data))
    for x in range(len(data)):
        data[x] = str(data[x]).replace("<p class=\"meals__price\">\n<span class=\"u-hidden\">Preise:</span>\n", "")
        data[x] = str(data[x]).replace("</p>", "")
        data[x] = str(data[x]).replace(" ", "")
    logging.info("Prices after formatting: " + str(data))
    return data
