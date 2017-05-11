# -*- coding: utf-8 -*-
import unittest
import requests
import base_data
import auth
import json
import urllib


class httpHandlerTest(unittest.TestCase):
    def test_post_order(self):
        resp = requests.post(base_data.ORDER_SAVE_API_POST, json={'id': 1, 'data': {'status': u'下单失败', 'TEST': None}})
        print resp.text

    def test_set_status(self):
        resp = requests.post(base_data.ORDER_SETSTATUS_API_POST,
                             data={'order_id': 'bd95cf4b26d04d2cb85bbfc9d4a16117', 'status': '充值成功'})
        print resp.text

    def test_get_wx_payinfo(self):
        cookie = 'pin=jd_417181296b3ba; wskey=AAFZCEPFAECu4cCwW_BItToNjJMdjva2TkDa-NfZ8lXY9Tc71Ez8teFvoHKgIPYis4xLutBE8792x58wEkTcT2zhMnEVSR-w; whwswswws='
        h5_cookie = {'mobilev': 'touch',
                     'pt_key': 'app_openAAFZCEPFADC0pTiZdMxn3QlFk3jh8Pr60qhjMOO07np7zyLdJmKX1QuNA6sF-SWkKULi6p35kk8',
                     'pwdt_id': 'jd_417181296b3ba', 'sid': '07713da596d5a6c7c0aaa19ebfff3b7w',
                     'guid': '5b317f5a3d5b7af09d4ba69b901966e066bfd06b1b35a64e5b95ad5d264e41aa',
                     'pt_pin': 'jd_417181296b3ba'}

        resp = requests.get(
            'https://train.m.jd.com/pay/goToPay?orderId=51990280826&trainOrderId=5567188&onlinePayFee=18.5', headers={
                'Charset': 'UTF-8',
                'Connection': 'close',
                'Cookie': 'mobilev=touch,pt_key=app_openAAFZCEPFADC0pTiZdMxn3QlFk3jh8Pr60qhjMOO07np7zyLdJmKX1QuNA6sF-SWkKULi6p35kk8,pwdt_id=jd_417181296b3ba,sid=07713da596d5a6c7c0aaa19ebfff3b7w,guid=5b317f5a3d5b7af09d4ba69b901966e066bfd06b1b35a64e5b95ad5d264e41aa,pt_pin=jd_417181296b3ba',
                'Upgrade-Insecure-Requests:': '1',
                'User-Agent': 'JD4iPhone/134623 (iPhone; iOS 8.1.3; Scale/2.00)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            verify=False)  # ,allow_redirects=False
        pay_url = resp.url
        query = pay_url[pay_url.index('?') + 1:].split('&')
        payload = {}
        for q in query:
            q = q.split('=')
            payload[q[0]] = q[1]
        print pay_url, query, payload

        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        headers = {'Accept-Encoding': 'gzip,deflate',
                   'jdc-backup': cookie,
                   'Cookie': cookie,
                   'Charset': 'UTF-8',
                   'Connection': 'Keep-Alive',
                   'Cache-Control': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'JD4iPhone/134623 (iPhone; iOS 8.1.3; Scale/2.00)'
                   }
        # payload['appId']='jd_iphone_app4'
        print  json.dumps(payload)
        sign = auth.sign('weixinPay', uuid, json.dumps(payload))

        resp = requests.post(
            url='http://api.m.jd.com/client.action?functionId=weixinPay&clientVersion=5.8.0&build=42523&client=android&d_brand=nubia&d_model=NX507J&osVersion=4.4.2&screen=1920*1080&partner=jingdong2&uuid=%s&area=1_2802_2821_0&networkType=wifi&st=%s&sign=%s&sv=111' % (
                # url = 'http://api.m.jd.com/client.action?functionId=configCouponList&clientVersion=5.8.0&build=42523&client=android&d_brand=&d_model=&osVersion=&screen=1280*720&partner=tencent&uuid=%s&area=1_2802_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
                uuid, sign[1], sign[0]),
            data='body=' + urllib.quote(json.dumps(payload)) + '&',
            headers=headers)
        # resp = requests.post(
        #     url='http://pay.m.jd.com/index.action?functionId=weixinPay',
        #     data='body=' + urllib.quote(json.dumps(payload)) + 'adid=9A72E17A-8D8C-4877-A781-35CEBB8C6E38&area=19_1607_3155_0&build=134623&client=apple&clientVersion=5.8.0&d_brand=apple&d_model=iPhone7%2C2&isBackground=N&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=dc8015f619f669cf0008bc9ea2e98f5908eec7c9&osVersion=8.1.3&partner=pp601&screen=750%2A1334&'+'uuid=%s&st=%s&sign=%s&sv=100'% (
        #         # url = 'http://api.m.jd.com/client.action?functionId=configCouponList&clientVersion=5.8.0&build=42523&client=android&d_brand=&d_model=&osVersion=&screen=1280*720&partner=tencent&uuid=%s&area=1_2802_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
        #         uuid, sign[1], sign[0]),
        #     headers=headers)
        print resp.json()

    def test_get_wx_payinfo2(self):
        cookie = 'pin=jd_4c25331e9e318; wskey=AAFZFCJnAEApyqAxlSJkcJq5PpfyEQJP3AzScHZMPYnJil_OUyj_Nplm6EMUtplSPLrmze_4_A_dnePgOgpA3ZPb-PcAOnPL; whwswswws='
        h5_cookie = {'mobilev': 'touch',
                     'pt_key': 'app_openAAFZFCJrADDn-sSej1_DxCnX2huF62fiLmAr7HLgBgj8Of4jJFwXgzpPRI0qQOQfNsvRNQ0b95k',
                     'pwdt_id': 'jd_4c25331e9e318', 'sid': 'f4686d600dab33e26b0427afa298f5cw',
                     'guid': '2bc17003cc1916830d40e7d84c4d6523ae691c8936569e8cdac7479c22e02b07',
                     'pt_pin': 'jd_4c25331e9e318'}

        session = requests.session()
        resp = requests.get(
            'https://train.m.jd.com/pay/goToPay?orderId=53087782937&trainOrderId=5751638&onlinePayFee=19.50', headers={
                'Charset': 'UTF-8',
                'Connection': 'close',
                'Cookie': 'mobilev=touch,pt_key=app_openAAFZFCJrADDn-sSej1_DxCnX2huF62fiLmAr7HLgBgj8Of4jJFwXgzpPRI0qQOQfNsvRNQ0b95k,pwdt_id=jd_4c25331e9e318,sid=f4686d600dab33e26b0427afa298f5cw,guid=2bc17003cc1916830d40e7d84c4d6523ae691c8936569e8cdac7479c22e02b07,pt_pin=jd_4c25331e9e318',
                'User-Agent': 'jdapp;android;6.0.0;4.4.2;863175026618021-a8a6681e316b;network/wifi;osp/android;apv/6.0.0;osv/4.4.2;uid/863175026618021-a8a6681e316b;pv/210.81;psn/863175026618021-a8a6681e316b|211;psq/25;ref/;pap/JA2015_311210|6.0.0|ANDROID 4.4.2;usc/direct;ucp/-;umd/none;utr/-;adk/;ads/;jdv/;Mozilla/5.0 (Linux; Android 4.4.2; NX507J Build/KVT49L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043124 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            verify=False)  # ,allow_redirects=False
        pay_url = resp.url
        query = pay_url[pay_url.index('?') + 1:].split('&')
        payload = {}
        for q in query:
            q = q.split('=')
            payload[q[0]] = q[1]

        payload['appId'] = 'jd_android_app4'
        # payload['payId']='4d5f1ae1294a40f3aa4fa1d749e8d1a7'
        # print pay_url,query,payload

        headers = {'Connection': 'keep-alive',
                   'Pragma': 'no-cache',
                   'Cache-Control': 'no-cache',
                   'Accept': '*/*',
                   'Origin': 'https://pay.m.jd.com',
                   'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': 'jdapp;android;6.0.0;6.0;861012032753710-f823b2dbaddc;network/wifi;osp/android;apv/6.0.0;osv/6.0;uid/861012032753710-f823b2dbaddc;pv/1.45;psn/861012032753710-f823b2dbaddc|3;psq/6;ref/;pap/JA2015_311210|6.0.0|ANDROID 6.0;usc/direct;ucp/-;umd/none;utr/-;adk/;ads/;jdv/;hasUPPay/0;Mozilla/5.0 (Linux; Android 6.0; CAM-AL00 Build/HONORCAM-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'https://pay.m.jd.com/cpay/index.html?appId=jd_android_app4&payId=' + payload['payId'],
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,en-US;q=0.8',
                   'Cookie': cookie
                   }
        resp = requests.post('https://pay.m.jd.com/newpay/index.action',
                             data='appId=jd_android_app4&payId=' + payload['payId'] + '&_format_=JSON', headers=headers)
        print resp.text

        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        headers = {'Accept-Encoding': 'gzip,deflate',
                   'Cookie': cookie,
                   'Charset': 'UTF-8',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.2.2; GT-P5210 Build/JDQ39E)'
                   }
        print json.dumps(payload)
        sign = auth.sign('weixinPay', uuid, json.dumps(payload))
        resp = requests.post(
            url='https://pay.m.jd.com/index.action?functionId=weixinPay&clientVersion=5.8.0&build=42523&client=android&d_brand=Xiaomi&d_model=Mi4&osVersion=4.2.2&screen=1440*810&partner=goapk001&uuid=%s&area=19_1709_20093_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
                # url = 'http://api.m.jd.com/client.action?functionId=configCouponList&clientVersion=5.8.0&build=42523&client=android&d_brand=&d_model=&osVersion=&screen=1280*720&partner=tencent&uuid=%s&area=1_2802_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
                uuid, sign[1], sign[0]),
            data='body=%7B%22payId%22%3A%22' + payload['payId'] + '%22%2C%22appId%22%3A%22jd_android_app4%22%7D&',
            # 'body=' + urllib.quote(json.dumps(payload))+ '&',
            headers=headers)
        print resp.text
