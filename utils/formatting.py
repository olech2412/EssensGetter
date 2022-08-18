import logging


logging.basicConfig(filename='essensGetter.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s %(levelname)s - %(message)s', force=True, encoding='utf-8')


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
        logging.error("A string is given -> no formatting ")
        print("A string is given -> no formatting ")
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
    return data
