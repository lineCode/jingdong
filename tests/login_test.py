import unittest
import http_handler
import base_data


class HttpSqsTestSuite(unittest.TestCase):
    def test_login(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('17863838528', 'xf12345678', uuid, user_agent)
        cookie = login.get_cookie()
        print cookie
        print login.get_h5_cookie(cookie)

    def test_get_couponList(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('18311647121', '97abccycycy', uuid, user_agent)
        print login.get_couponList('pin=jd_52302824002a4; wskey=AAFZ9p1RAEBviVrojb785xwFxlaxdwOV0BXXM7ODqCHwEvMBoHdvZww4qtPSf3zAPfnFegXp-0WVVm8eFnbXzw0VUwlgV039; whwswswws=','9410795545')
