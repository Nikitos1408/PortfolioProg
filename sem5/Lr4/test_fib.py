import unittest
import itertools
from gen_fib import *

class TestFib(unittest.TestCase):

    def test_fib_1(self):
        self.assertEqual(fib(1), [0, 1], 'n = 1, list must be [0, 1]')

    def test_fib_2(self):
        self.assertEqual(fib(5), [0, 1, 1, 2, 3, 5], 'elements from 0 to 5')

    def test_fib_3(self):
        self.assertIsNone(fib(-1), 'sequence starts from 0')

    def test_fib_lst_1(self):
        self.assertEqual(list(FibonacchiLst(7)), [0, 1, 1, 2, 3, 5], 'elements form 0 to 5')

    def test_fib_lst_2(self):
        self.assertEqual(list(FibonacchiLst(1)), [0, 1], 'n = 1, list must be [0, 1]')

    def test_fib_classic_iter_1(self):
        self.assertEqual(list(itertools.islice(fib_classic_iter(), 3)), [0, 1, 1], 'list must be [0, 1, 1]')

    def test_fib_classic_iter_2(self):
        self.assertEqual(list(itertools.islice(fib_classic_iter(), 1)), [0], 'only one element, list must be [0]')

    def test_fib_iter_1(self):
        self.assertEqual(list(fib_iter(range(5))), [0, 1, 1, 2, 3], 'elements from 0 to 3')

    def test_fib_iter_2(self):
        self.assertEqual(list(fib_iter(range(9))), [0, 1, 1, 2, 3, 5, 8], 'elements from 0 to 8')

if __name__ == '__main__':
    unittest.main()