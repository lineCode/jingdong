import unittest
import http_handler
import base_data


class HttpSqsTestSuite(unittest.TestCase):
    def test_login(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('14747275361', '4u2e4sa0', uuid, user_agent)
        cookie = login.get_cookie()
        print cookie
        print login.get_h5_cookie(cookie)

    def test_get_couponList(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('17094020074', '95al4b', uuid, user_agent)
        print login.get_couponList('pin=jd_7237cebe5e1e2; wskey=AAFYv7yjAEAY3oNhf4518qnKnh2T-kTanh8UVmUyIpPVAul2_XiQru8dX4xc1f-Lx2DmSoBGZgE46Ma0mK2OnBzYGPDR8LX1; whwswswws=','9410795545')
