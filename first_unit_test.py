import unittest

from twitter_example_with_txt_file import Twitter


class TwitterTest(unittest.TestCase):
    def setUp(self):
        self.twitter = Twitter()

    def test_init(self):
        # twitter = Twitter()  <-- to nie jest potrzebne ponieważ za kazdym razem inicjujemy to z setup
        self.assertTrue(self.twitter)

    def test_tweet(self):
        # Given - sytuacja wejsciowa
        # twitter = Twitter()
        # When - wykonaie akcji na tym
        self.twitter.tweet("Test message")
        # Then - sprawdzenie wyników
        self.assertEqual(self.twitter.tweets, ["Test message"])


if __name__ == '__main__':
    unittest.main()