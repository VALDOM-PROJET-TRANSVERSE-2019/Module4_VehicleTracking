import re
import unittest

from tracker import track2

class Tests(unittest.TestCase):
    """
    Tests de la fonction numerial sort
    """
    NUMBERS = re.compile(r'(\d+)')


if __name__ == '__main__':
    unittest.main()
