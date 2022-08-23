import unittest
import essensGetter


class Test_essensGetter(unittest.TestCase):

    def test_give_me_everything(self):
        self.assertIsNot(essensGetter.give_me_everything(), None)
        self.assertIsNot(essensGetter.give_me_everything(), [])

    def test_fetch_food_from_website(self):
        self.assertIsNot(essensGetter.fetch_food_from_website(), None)
        self.assertIsNot(essensGetter.fetch_food_from_website(), [])


if __name__ == '__main__':
    unittest.main()
