# -*- coding: utf-8 -*-
import unittest
import requests
import base_data
import auth
import json
import urllib

class httpHandlerTest(unittest.TestCase):
    def test_post_order(self):
        resp = requests.post(base_data.ORDER_SAVE_API_POST,json={'id':1,'data':{'status':u'下单失败','TEST':None}})
        print resp.text
    def test_set_status(self):
        resp = requests.post(base_data.ORDER_SETSTATUS_API_POST,
                             data={'order_id': 'bd95cf4b26d04d2cb85bbfc9d4a16117', 'status': '充值成功'})
        print resp.text

    def test_get_wx_payinfo(self):
        cookie = 'pin=jd_417181296b3ba; wskey=AAFZCEPFAECu4cCwW_BItToNjJMdjva2TkDa-NfZ8lXY9Tc71Ez8teFvoHKgIPYis4xLutBE8792x58wEkTcT2zhMnEVSR-w; whwswswws='
        h5_cookie={'mobilev': 'touch', 'pt_key': 'app_openAAFZCEPFADC0pTiZdMxn3QlFk3jh8Pr60qhjMOO07np7zyLdJmKX1QuNA6sF-SWkKULi6p35kk8', 'pwdt_id': 'jd_417181296b3ba', 'sid': '07713da596d5a6c7c0aaa19ebfff3b7w', 'guid': '5b317f5a3d5b7af09d4ba69b901966e066bfd06b1b35a64e5b95ad5d264e41aa', 'pt_pin': 'jd_417181296b3ba'}

        resp = requests.get('https://train.m.jd.com/pay/goToPay?orderId=51990280826&trainOrderId=5567188&onlinePayFee=18.5',headers={
            'Charset': 'UTF-8',
            'Connection': 'close',
            'Cookie': 'mobilev=touch,pt_key=app_openAAFZCEPFADC0pTiZdMxn3QlFk3jh8Pr60qhjMOO07np7zyLdJmKX1QuNA6sF-SWkKULi6p35kk8,pwdt_id=jd_417181296b3ba,sid=07713da596d5a6c7c0aaa19ebfff3b7w,guid=5b317f5a3d5b7af09d4ba69b901966e066bfd06b1b35a64e5b95ad5d264e41aa,pt_pin=jd_417181296b3ba',
            'Upgrade-Insecure-Requests:':'1',
            'User-Agent': 'JD4iPhone/134623 (iPhone; iOS 8.1.3; Scale/2.00)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},verify=False)#,allow_redirects=False
        pay_url= resp.url
        query = pay_url[pay_url.index('?')+1:].split('&')
        payload = {}
        for q in query:
            q=q.split('=')
            payload[q[0]]=q[1]
        print pay_url,query,payload

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
        sign = auth.sign('weixinPay',uuid, json.dumps(payload))

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











