import logging

logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')


# Converts Beilagen to usable data
def convert_HTML_List(data):
    zusaetze_ges = data
    zusaetze_gericht1 = list()
    zusaetze_gericht2 = list()

    logging.info("Before formatting: " + str(zusaetze_ges))

    # remove HTML from the data
    for x in range(len(zusaetze_ges)):
        zusaetze_ges[x] = str(zusaetze_ges[x]).replace("<li>", "")
        zusaetze_ges[x] = str(zusaetze_ges[x]).replace("</li>", "")
        zusaetze_ges[x] = str(zusaetze_ges[x]).replace("<ul>", "")
        zusaetze_ges[x] = str(zusaetze_ges[x]).replace("</ul>", "")
        zusaetze_ges[x] = str(zusaetze_ges[x]).replace("<ul >\n", "")
        zusaetze_ges[x] = str(zusaetze_ges[x]).replace("'", "")
        zusaetze_ges[x] = str(zusaetze_ges[x]).replace("<ul class=\"u-list-bare\">", "")

    # remove the first and the last \n so the values can be seperate by ", "
    zusaetze_gericht1 = str(zusaetze_ges[0])
    zusaetze_gericht1 = zusaetze_gericht1[1:]
    zusaetze_gericht1 = zusaetze_gericht1[:-1]
    if str(zusaetze_gericht1).__contains__("\n"):
        zusaetze_gericht1 = str(zusaetze_gericht1).replace("\n", ", ")  # seperate the values by ", "

    zusaetze_gericht2 = str(zusaetze_ges[1])
    zusaetze_gericht2 = zusaetze_gericht2[1:]
    zusaetze_gericht2 = zusaetze_gericht2[:-1]
    if str(zusaetze_gericht2).__contains__("\n"):
        zusaetze_gericht2 = str(zusaetze_gericht2).replace("\n", ", ")

    logging.info("After formatting: " + str(zusaetze_gericht1) + "&&" +  str(zusaetze_gericht2))

    return zusaetze_gericht1, zusaetze_gericht2  # return the Beilagen as


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
