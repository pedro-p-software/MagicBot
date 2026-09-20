import unittest

from text_utils import split_message


class SplitMessageTests(unittest.TestCase):
    def test_short_message_is_not_changed(self):
        self.assertEqual(split_message("Olá"), ["Olá"])

    def test_long_message_is_split_within_telegram_limit(self):
        parts = split_message("word " * 1000, limit=100)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(len(part) <= 100 for part in parts))
