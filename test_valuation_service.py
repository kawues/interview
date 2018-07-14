import unittest
import re
import valuation_service


class ValuationServiceTest(unittest.TestCase):


    def test_convert_to_pln(self):

        currencies = []
        currencies.append('GBP,1.5\n')
        currencies.append('EU,2.0\n')
        data = []
        data.append('1,1000,GBP,2,3\n')
        data.append('2,1050,EU,1,1\n')

        converted_data = valuation_service.convert_to_pln(currencies, data)
        self.assertTrue('PLN' in converted_data[0])
        self.assertTrue('PLN' in converted_data[1])
        self.assertFalse('GBP' in converted_data[0])
        self.assertFalse('GBP' in converted_data[1])
        self.assertFalse('EU' in converted_data[0])
        self.assertFalse('EU' in converted_data[1])
        self.assertEqual(converted_data[0].split(",")[1], str(float(data[0].split(",")[1]) * float(currencies[0].split(",")[1])))


    def test_sort_by_price(self):

        data = []
        data.append('1,1000,PLN,2,3\n')
        data.append('2,1080,PLN,1,1\n')
        data.append('3,1010,PLN,1,2\n')
        data.append('4,1050,PLN,1,1\n')
        data.append('5,1100,PLN,1,2\n')
        data.append('6,1000,PLN,1,1\n')
        data.append('7,1140,PLN,1,3\n')
        matching_id = 1

        product_list = valuation_service.sort_by_price(matching_id, data)
        self.assertEqual(3, len(product_list))


    def test_aggregate_products(self):


        data = []
        data.append('1,1000,PLN,2,3\n')
        data.append('2,1080,PLN,1,1\n')
        data.append('3,1010,PLN,1,1\n')
        data.append('4,1050,PLN,1,2\n')
        data.append('5,1100,PLN,1,1\n')
        data.append('6,1000,PLN,1,2\n')
        data.append('7,1140,PLN,1,1\n')
        matchings = []
        matchings.append('1,2')
        matchings.append('2,2')
        matchings.append('3,1')

        result = valuation_service.aggregate_products(matchings, data)
        self.assertEqual(len(result), 3)
        assert re.match(r'[0-9],[0-9]+\.[0-9]+,[0-9]+\.[0-9]+,PLN,2$', result[0])
        assert re.match(r'[0-9],[0-9]+\.[0-9]+,[0-9]+\.[0-9]+,PLN,0$', result[1])
        assert re.match(r'[0-9],[0-9]+\.[0-9]+,[0-9]+\.[0-9]+,PLN,0$', result[2])



