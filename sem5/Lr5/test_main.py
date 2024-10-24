import unittest
from main import Currency

class TestCurrency(unittest.TestCase):
    
    def setUp(self):
        self.valid_ids = ['R01235', 'R01010']  # Пример корректных ID валют
        self.invalid_ids = ['R9999']  # Пример некорректного ID
        self.currency = Currency(self.valid_ids + self.invalid_ids)

    def test_invalid_currency_id(self):
        #Тест на возврат неверного ID с None значением
        result = self.currency.result
        expected_result = {'R9999': None}
        self.assertEqual(result, expected_result)
    

if __name__ == '__main__':
    unittest.main()