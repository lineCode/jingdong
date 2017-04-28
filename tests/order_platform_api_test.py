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
        cookie = 'pin=jd_417181296b3ba; wskey=AAFZAYpTAEBLp4wKG4pfqSgyMNFgV2Kv4tOOs7llRWzsTv2oyGknZn06-BzyypgrXBjnMtsVsqoiL_sV1xXav6TnOmwhBBqn; whwswswws='
        h5_cookie={'mobilev': 'touch', 'pt_key': 'app_openAAFZAYpUADC7duIw9Cy8J3iEMkMGHJ3POIajj-8eiseTgCZLm3rN1MblzZ9YNbwRylFmz1BMx_w', 'pwdt_id': 'jd_417181296b3ba', 'sid': '8d7955a721af205d72980fefc29395bw', 'guid': 'a127077c05730397ebb57f4f2d8ec34008d401781f70b7dacf9bc7719f232dea', 'pt_pin': 'jd_417181296b3ba'}

        session = requests.session()
        resp = requests.get('https://train.m.jd.com/pay/goToPay?orderId=51686479062&trainOrderId=5429701&onlinePayFee=573.0',headers={
            'Charset': 'UTF-8',
            'Connection': 'close',
            'Cookie': 'mobilev=touch,pt_key=app_openAAFZAYpUADC7duIw9Cy8J3iEMkMGHJ3POIajj-8eiseTgCZLm3rN1MblzZ9YNbwRylFmz1BMx_w,pwdt_id=jd_417181296b3ba,sid=8d7955a721af205d72980fefc29395bw,guid=a127077c05730397ebb57f4f2d8ec34008d401781f70b7dacf9bc7719f232dea,pt_pin=jd_417181296b3ba',
            'Upgrade-Insecure-Requests:':'1',
            'User-Agent': 'jdapp;android;6.0.0;4.4.2;863175026618021-a8a6681e316b;network/wifi;osp/android;apv/6.0.0;osv/4.4.2;uid/863175026618021-a8a6681e316b;pv/210.81;psn/863175026618021-a8a6681e316b|211;psq/25;ref/;pap/JA2015_311210|6.0.0|ANDROID 4.4.2;usc/direct;ucp/-;umd/none;utr/-;adk/;ads/;jdv/;Mozilla/5.0 (Linux; Android 4.4.2; NX507J Build/KVT49L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043124 Safari/537.36',
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
                   'User-Agent': 'okhttp/3.4.1'
                   }
        sign = auth.sign('weixinPay', uuid, json.dumps(payload))
        resp = requests.post(
            url='http://pay.m.jd.com/index.action?functionId=weixinPay&clientVersion=5.8.0&build=42523&client=android&d_brand=nubia&d_model=NX507J&osVersion=4.4.2&screen=1920*1080&partner=lmobile048&uuid=%s&networkType=wifi&st=%s&sign=%s&sv=102 ' % (
                # url = 'http://api.m.jd.com/client.action?functionId=configCouponList&clientVersion=5.8.0&build=42523&client=android&d_brand=&d_model=&osVersion=&screen=1280*720&partner=tencent&uuid=%s&area=1_2802_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
                uuid, sign[1], sign[0]),
            data='body=' + urllib.quote(json.dumps(payload)) + '&',
            headers=headers)
        print resp.json()











