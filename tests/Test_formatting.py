import unittest
import utils.formatting as formatting
import essensGetter


class Test_formatting(unittest.TestCase):

    def test_format_price(self):
        self.assertFalse(formatting.format_food_price(formatting.format_meals_from_list(essensGetter.fetch_food_from_website())[0]["price"]).__contains__("<p"))
        self.assertFalse(formatting.format_food_price(formatting.format_meals_from_list(essensGetter.fetch_food_from_website())[0]["price"]).__contains__("</p"))
        self.assertFalse(formatting.format_food_price(formatting.format_meals_from_list(essensGetter.fetch_food_from_website())[0]["price"]).__contains__("title-prim"))

    def test_format_string(self):
        for x in formatting.format_meals_from_list(essensGetter.fetch_food_from_website()):
            for y in x["price"]:
                self.assertTrue(formatting.format_string(str(y)).isascii())

            self.assertTrue(formatting.format_string(str(x["category"])).isascii())
            for y in x["food"]:
                self.assertTrue(formatting.format_string(str(y)).isascii())
            for y in x["beilagen"]:
                self.assertTrue(formatting.format_string(str(y)).isascii())

            if len(formatting.format_meals_from_list(essensGetter.fetch_food_from_website())) == 4:
                self.assertRaises(KeyError, formatting.format_meals_from_list(essensGetter.fetch_food_from_website())[0]["additional_info"])
            elif len(formatting.format_meals_from_list(essensGetter.fetch_food_from_website())) == 5:
                self.assertTrue(str(formatting.format_string(formatting.format_meals_from_list(essensGetter.fetch_food_from_website())[0]["additional_info"])).isascii())

    def test_format_meals_from_list(self):
        for x in formatting.format_meals_from_list(essensGetter.fetch_food_from_website()):
            self.assertTrue(x.__contains__("category"))
            self.assertTrue(x.__contains__("food"))
            self.assertTrue(x.__contains__("beilagen"))
            self.assertTrue(x.__contains__("price"))
            if len(x) == 5:
                self.assertTrue(str(x.__contains__("additional_info")))
            elif len(x) == 4:
                self.assertFalse(x.__contains__("additional_info"))


if __name__ == '__main__':
    unittest.main()
