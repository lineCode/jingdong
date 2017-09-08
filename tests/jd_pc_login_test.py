import unittest
import http_handler


class jd_pc_login_test(unittest.TestCase):
    def test_get_cookie(self):
        http_handler.jd_pc_login.get_cookie()