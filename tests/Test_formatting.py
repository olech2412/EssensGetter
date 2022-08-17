import unittest
import essensGetter.formatting as formatting
import essensGetter.essensGetter as essensGetter

class Test_formatting(unittest.TestCase):

    def test_format_price(self):
        self.assertFalse(str(formatting.format_food_price(essensGetter.fetch_food())).__contains__("<p"))

    def test_format_string(self):
        self.assertTrue(str(formatting.format_string(essensGetter.fetch_food())).isascii())
        self.assertTrue(str(formatting.format_string(essensGetter.fetch_food_category())).isascii())
        self.assertTrue(str(formatting.format_string(essensGetter.fetch_prices())).isascii())