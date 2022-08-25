import calendar
import datetime
import unittest
import essensGetter


class Test_essensGetter(unittest.TestCase):

    def test_essensGetter_response(self):
        self.assertEqual(essensGetter.response.status_code, 200)
        self.assertIsNot(essensGetter.response, None)
        self.assertIsNot(essensGetter.soup, None)

    def test_give_me_everything(self):
        self.assertIsNot(essensGetter.give_me_everything(), None)
        self.assertIsNot(essensGetter.give_me_everything(), [])

    def test_fetch_food_from_website(self):
        self.assertIsNot(essensGetter.fetch_food_from_website(), None)
        self.assertIsNot(essensGetter.fetch_food_from_website(), [])

    def test_essensGetter_timing(self):
        if calendar.day_name[datetime.date.today().weekday()] != "Saturday" \
                or calendar.day_name[datetime.date.today().weekday()] != "Sunday":
            self.assertIsNot(essensGetter.url, None)
            self.assertIsNot(essensGetter.url, [])

    def test_essensGetter_url(self):
        self.assertEqual(essensGetter.url, "https://www.studentenwerk-leipzig.de/mensen-cafeterien/speiseplan"
                                           "?location=140")

    def test_essensGetter_meals(self):
        self.assertIsNot(essensGetter.meals, None)
        self.assertIsNot(essensGetter.meals, [])
        self.assertTrue(len(essensGetter.meals) > 0)


if __name__ == '__main__':
    unittest.main()
