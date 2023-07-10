"""Bike-Share"""

from typing import Any, Dict
import unittest
import checker_generic
import bike_share

PYTA_CONFIG = 'a2_pyta.json'
FILENAME = 'bike_share.py'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'ID': 0, 'NAME': 1, 'LATITUDE': 2, 'LONGITUDE': 3, 'CAPACITY': 4,
    'BIKES_AVAILABLE': 5, 'DOCKS_AVAILABLE': 6, 'NO_KIOSK': 'SMART',
    'EARTH_RADIUS': 6371
}


class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""

    def setUp(self):
        """Init sample inputs."""

        self.stations = [
            [7090, 'Danforth Ave / Lamb Ave',
             43.681991, -79.329455, 15, 4, 10],
            [7486, 'Gerrard St E / Ted Reeve Dr',
             43.684261, -79.299332, 22, 5, 17],
            [7571, 'Highfield Rd / Gerrard St E - SMART',
             43.671685, -79.325176, 19, 14, 5]]

        self.stations2 = [
            [7090, 'Danforth Ave / Lamb Ave',
             43.681991, -79.329455, 15, 4, 10],
            [7486, 'Gerrard St E / Ted Reeve Dr',
             43.684261, -79.299332, 22, 5, 17],
            [7571, 'Highfield Rd / Gerrard St E - SMART',
             43.671685, -79.325176, 19, 14, 5]]

# Data conversion function

    def test_convert_data(self) -> None:
        """Function convert_data."""

        self._check(bike_share.convert_data,
            [[['abc', '123', '45.6', 'true', 'False']]], type(None))

# Data query functions

    def test_is_app_only(self) -> None:
        """Function is_app_only."""

        test_list = [7090, 'Danforth Ave / Lamb Ave', 43.681991, -79.329455,
                     15, 4, 10]
        test_list_duplicate = [7090, 'Danforth Ave / Lamb Ave', 43.681991, 
                               -79.329455, 15, 4, 10]
        self._check(bike_share.is_app_only, [test_list], bool)
        self._check_no_mutation(bike_share.is_app_only, test_list,
                                test_list_duplicate)


    def test_get_station_info(self) -> None:
        """Function get_station_info."""

        types = (str, int, int, bool)
        self._test_returns_list_of(bike_share.get_station_info,
                                   [7486, self.stations], types)
        self._check_no_mutation(bike_share.get_station_info, self.stations,
                                self.stations2)


    def test_get_column_sum(self) -> None:
        """Function get_column_sum."""

        self._check(bike_share.get_column_sum, [5, self.stations], int)
        self._check_no_mutation(bike_share.get_column_sum, self.stations,
                                self.stations2)


    def test_get_stations_with_kiosks(self) -> None:
        """Function get_stations_with_kiosks."""

        types = (int, int)  # for self.stations
        self._test_returns_list_of(bike_share.get_stations_with_kiosks,
                                   [self.stations], types)
        self._check_no_mutation(bike_share.get_stations_with_kiosks, 
                                self.stations, self.stations2)


    def test_get_nearest_station(self) -> None:
        """Function get_nearest_station."""

        self._check(bike_share.get_nearest_station,
                    [43.671134, -79.325164, self.stations], int)
        self._check_no_mutation(bike_share.get_nearest_station, self.stations,
                                self.stations2)


# Data modification functions

    def test_rent_bike(self) -> None:
        """Function rent_bike."""

        self._check(bike_share.rent_bike, [7090, self.stations], bool)
        self._check_mutation(bike_share.rent_bike, self.stations,
                             self.stations2)


    def test_return_bike(self) -> None:
        """Function return_bike."""

        self._check(bike_share.return_bike, [7090, self.stations], bool)
        self._check_mutation(bike_share.return_bike, self.stations,
                             self.stations2)
     
   
    def test_upgrade_stations(self) -> None:
        """Function upgrade_stations."""

        self._check(bike_share.upgrade_stations, [20, 5, self.stations], int)
        self._check_mutation(bike_share.upgrade_stations, self.stations,
                             self.stations2)
 
       
# Check constants not changed

    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, bike_share)
        print('  check complete')

# Check helper functions

    def _check(self, func: callable, args: list, ret_type: type) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.check(func, args, ret_type)
        self.assertTrue(result[0], result[1])
        print('  check complete')

        
    def _check_no_mutation(self, func: callable, actual, expected) -> None:
        """Check that func does not mutate that argument actual so that
        it still matches expected.
        """
        self.assertTrue(expected == actual, 
                        '{0} should not mutate its arguments'.format(
                            func.__name__))

    def _check_mutation(self, func: callable, actual, expected) -> None:
        """Check that func mutates the argument actual so that
        it is different from expected.
        """
        self.assertTrue(expected != actual, 
                        '{0} should mutate its list argument'.format(
                            func.__name__))        
        
    def _test_returns_list_of(self, func, args, types):
        """Check that func when called with args returns a list of elements
        of typef from types.

        """

        print('\nChecking {}...'.format(func.__name__))

        result = checker_generic.check(func, args, list)
        self.assertTrue(result[0], result[1])

        msg = '{} should return a list of length {}'
        self.assertEqual(len(result[1]), len(types),
                         msg.format(func.__name__, len(types)))

        msg = ('Element at index {} in the list returned '
               'should be of type {}. Got {}.')
        for i, typ in enumerate(types):
            self.assertTrue(isinstance(result[1][i], typ),
                            msg.format(i, typ, result[1][i]))

        print('  check complete')


    def _check_constants(self, name2value: Dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of constant {} should be {} but is {}.'.format(
                name, expected, actual)
            self.assertEqual(expected, actual, msg)


print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
