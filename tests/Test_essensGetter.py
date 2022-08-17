import unittest
import essensGetter.essensGetter as essensGetter


class Test_essensGetter(unittest.TestCase):

    def test_give_me_everything(self):
        self.assertIsNot(essensGetter.give_me_everything(), None)
        self.assertIsNot(essensGetter.give_me_everything(), [])

    def test_fetch_prices(self):
        self.assertIsNot(essensGetter.fetch_prices(), None)
        self.assertIsNot(essensGetter.fetch_prices(), [])
        self.assertGreater(len(essensGetter.fetch_prices()), 0)

        if len(essensGetter.fetch_prices()) == 1:
            self.assertGreater(len(essensGetter.fetch_food()), 1)
            self.assertLess(len(essensGetter.fetch_food()), 3)
            self.assertEquals(len(essensGetter.fetch_food_category()), 1)
        elif len(essensGetter.fetch_prices()) == 2:
            self.assertGreater(len(essensGetter.fetch_food()), 2)
            self.assertLess(len(essensGetter.fetch_food()), 5)
            self.assertEquals(len(essensGetter.fetch_food_category()), 2)

    def test_fetch_food_category(self):
        self.assertIsNot(essensGetter.fetch_food_category(), None)
        self.assertIsNot(essensGetter.fetch_food_category(), [])
        self.assertGreater(len(essensGetter.fetch_food_category()), 0)
        self.assertLess(len(essensGetter.fetch_food_category()), 3)

    def test_fetch_food(self):
        self.assertIsNot(essensGetter.fetch_food(), None)
        self.assertIsNot(essensGetter.fetch_food(), [])
        self.assertGreater(len(essensGetter.fetch_food()), 0)
        self.assertLess(len(essensGetter.fetch_food()), 5)


if __name__ == '__main__':
    unittest.main()
