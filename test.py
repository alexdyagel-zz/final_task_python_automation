import unittest
from unittest import mock

from actions import choose_position
from models import UserType


class TestChoosingUserPosition(unittest.TestCase):
    def test_choose_manager(self):
        with mock.patch('builtins.input', return_value="2"):
            self.assertEqual(choose_position(), UserType.MANAGER)

    def test_choose_salesman(self):
        with mock.patch('builtins.input', return_value="1"):
            self.assertEqual(choose_position(), UserType.SALESMAN)

    def test_quit(self):
        with mock.patch('builtins.input', return_value="q"):
            self.assertRaises(SystemExit, choose_position)
