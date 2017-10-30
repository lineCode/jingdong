import unittest
import http_handler
import base_data


class HttpSqsTestSuite(unittest.TestCase):
    def test_login(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('18341082500', 'xf1234567', uuid, user_agent)
        cookie = login.get_cookie()
        print cookie
        print login.get_h5_cookie(cookie)

    def test_get_couponList(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('18311647121', '97abccycycy', uuid, user_agent)
        print login.get_couponList('pin=jd_563b89eeeeff3; wskey=AAFZ9sUOAEB6G7xgp4cWlOSVV8YikQDTpGH-o0I0x4pdlx-NKiM3gDcQd3-s5p9EJ5HLR3G_XrWE4_k2xqPf2rY6sKiM6nAx; whwswswws=','21157470337')