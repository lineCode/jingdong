import unittest
import http_handler
import base_data


class HttpSqsTestSuite(unittest.TestCase):
    def test_login(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('17094020074', '95al4b', uuid, user_agent)
        cookie = login.get_cookie()
        print cookie
        print login.get_h5_cookie(cookie)

    def test_get_couponList(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('17094020074', '95al4b', uuid, user_agent)
        login.get_couponList('pin=jd_551be3034b5ca; wskey=AAFYv6tuAEDeXTGdE8dKPGyZKmsEitVCruCM5vJCPBOEMJlAfjUgYY-ycGw3o5eJk5Plkyj3mulx9Ayc7NggzDVorBvud7zU; whwswswws=','123')
