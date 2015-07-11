#!/usr/bin/env python3

# (c) Copyright Cameron Conn 2015
# This file is licensed GPLv3 or Later
# See LICENSE for details


import unittest
import photoanon


class TestConversionMethods(unittest.TestCase):
    '''
    Test conversion between DMS and decimal notation
    '''
    def test_dms_to_dec(self):
        '''
        Test conversion from DMS to decimal
        '''
        # Test for correct handling
        dms_1 = '84/1 23/1 17/1'
        self.assertAlmostEqual(photoanon._to_deg(dms_1 + ' E'), 84.38805, delta=0.00001)
        self.assertAlmostEqual(photoanon._to_deg(dms_1 + ' W'), -84.38805, delta=0.00001)
        self.assertAlmostEqual(photoanon._to_deg(dms_1 + ' N'), 84.38805, delta=0.00001)
        self.assertAlmostEqual(photoanon._to_deg(dms_1 + ' S'), -84.38805, delta=0.00001)

        # Test for direction
        self.assertRaisesRegex(ValueError, 'Invalid direction', callable=photoanon._to_deg, args=dms_1 + ' K')

        # Test for no direction
        dms_2 = '121/1 23/1 17/1'
        with self.assertRaisesRegex(ValueError, 'Bad coordinate format'):
            photoanon._to_deg(dms_2)

        # Test bounds checking
        dms_3 = '180/1 0/1 1/1 N'
        self.assertRaisesRegex(AssertionError, 'Coordinate out of range', callable=photoanon._to_deg, args=dms_3)

        dms_4 = '180/1 0/1 1/1 S'
        self.assertRaisesRegex(AssertionError, 'Coordinate out of range', callable=photoanon._to_deg, args=dms_4)

    def test_dec_to_dms_to_dec(self):
        '''
        Test conversion from decimal to DMS and back
        '''
        test_nums = (151.37472006900322, 30.950775038902805, 98.8191006873883, 179.49947847141897,
                     -7.366472622351381, 161.925677312287, 32.02985369316008, 29.109375201227294,
                     -43.66702774873653, -10.845880520386117)

        for num in test_nums:
            dms = photoanon._to_dms(num)
            dms += ' N' if num >= 0 else ' S'
            dec_conv = photoanon._to_deg(dms)

            self.assertAlmostEqual(num, dec_conv, places=12)


    def test_dec_to_dms(self):
        '''
        Test conversion from decimal to DMS
        '''
        dec_1 = 85.6845321
        self.assertEqual(photoanon._to_dms(dec_1), '85/1 41/1 2316898633/536870912')


if __name__ == '__main__':
    unittest.main()
