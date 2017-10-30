import unittest
import http_handler
import base_data


class HttpSqsTestSuite(unittest.TestCase):
    def test_login(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('13060470262', 'xf12345678', uuid, user_agent)
        cookie = login.get_cookie()
        print cookie
        print login.get_h5_cookie(cookie)

    def test_get_couponList(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('18311647121', '97abccycycy', uuid, user_agent)
        coupon_list=login.get_couponList('pin=jd_45881dc641d96; wskey=AAFZ9shzAEAOOPsvYBESTeF1GcRTh7ECxJWYJYYEEHeLS8Dd4pTt9_BN8HfXUBymn97RQNn8_X_zZ8eicj_eS_eIgTMt0eP-; whwswswws=00','21212811453')
        print coupon_list
        if not coupon_list:
            print 'not found'
        else:
            print 'find it'