import requests
import unittest
import auth
import base_data
import urllib
import json
import time


class HttpFirstTest(unittest.TestCase):
    def setUp(self):
        # self.uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        # self.user_agent = base_data.get_user_agent()
        self.name = '18445781858'
        self.pwd = '41848q'
        self.uuid = '823466913984714-pgveoceqje9l'
        self.user_agent = 'Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba'
        self.cookie = 'pin=jd_600c09353d777; wskey=AAFYRnzAAEA2gJb0tTAEHzWL9YM-cujTq1SnIpOfK1Bcd28zOAdt5d09Yn1U3R-rbv0tddbcr8uDp6z3trvUJy7LQ_sZEEaJ; whwswswws=00'

    def login_test(self):
        url = 'http://wlogin.m.jd.com/applogin_v2'
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12)
        print uuid

        data = auth.get_req_data('jd_600c09353d777', 'mozhisi5245', uuid)
        req = requests.post(url, data=data, headers={'User-Agent': 'Android WJLoginSDK 1.4.2'})
        resp = req.text
        print resp

        cookie = auth.get_cookie(resp)
        print cookie

    def get_user_info_test(self):
        body = '{"flag":"nickname"}'
        uuid = ''
        sign = auth.sign('newUserInfo', uuid, body)
        print sign

        url = 'http://api.m.jd.com/client.action?functionId=newUserInfo&clientVersion=5.3.0&build=36639&client=android&d_brand=ZTE&d_model=SCH-I779&osVersion=4.4.2&screen=1280*720&partner=tencent&uuid=%s&area=1_2802_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
            uuid, sign[1], sign[0])
        print url

        req = requests.post(url, data='body=' + urllib.quote(body) + '&', headers={
            'Charset': 'UTF-8',
            'Connection': 'close',
            'Cookie': self.cookie,
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
        print req.text

    def get_h5_cookie(self):
        uuid = '863175026618021-a8a6681e316b'
        cookie = 'pin=jd_5b64e3796d3d7; wskey=AAFYPUmjAEDuqaiJt62w6hHbjQfU5MazEWA4Pmj7ihIQyHim0RyT4aye2BjZJVYI83JifZBdPr2gTBPHW8oO-c-b69PSQ9eo; whwswswws='
        body = {"action": "to", "to": 'https%3A%2F%2Ftrain.m.jd.com'}
        print body
        sign = auth.sign('genToken', uuid, json.dumps(body))
        url = 'http://api.m.jd.com/client.action?functionId=genToken&clientVersion=5.3.0&build=36639&client=android&d_brand=ZTE&d_model=SCH-I779&osVersion=4.4.2&screen=1280*720&partner=tencent&uuid=%s&area=1_2802_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
            uuid, sign[1], sign[0])
        print url
        headers = {
            'Charset': 'UTF-8',
            'Connection': 'close',
            'Cookie': cookie,
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        req = requests.post(url, data='body=' + urllib.quote(json.dumps(body)) + '&', headers=headers)
        print req.text

        resp = req.json()
        # {"code":"0","tokenKey":"AAEAMKMEfWAYh1fRAvE0siwbJrEjuCmaht3Of-dkAaMMpGzemdi7WsCeMn3EaUdejhCZvQ0","url":"http://un.m.jd.com/cgi-bin/app/appjmp"}

        url = 'http://un.m.jd.com/cgi-bin/app/appjmp?tokenKey=' + resp[
            'tokenKey'] + '&to=https%3A%2F%2Ftrain.m.jd.com&lbs=%7B%22provinceId%22%3A%2218%22%2C%22districtName%22%3A%22%E5%B2%B3%E9%BA%93%E5%8C%BA%22%2C%22districtId%22%3A%2248936%22%2C%22cityId%22%3A%221482%22%2C%22cityName%22%3A%22%E9%95%BF%E6%B2%99%E5%B8%82%22%2C%22provinceName%22%3A%22%E6%B9%96%E5%8D%97%22%2C%22lng%22%3A%22112.883301%22%2C%22lat%22%3A%2228.207992%22%7D'
        session = requests.session()
        req = session.get(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'jdapp;android;5.4.1;4.4.2;863175026618021-a8a6681e316b;network/wifi;osp/android;apv/5.4.1;osv/4.4.2;uid/863175026618021-a8a6681e316b;pv/87.20;psn/863175026618021-a8a6681e316b|94;psq/15;ref/;pap/JA2015_311210|5.4.1|ANDROID 4.4.2;usc/;ucp/;umd/;utr/;adk/;ads/;Mozilla/5.0 (Linux; Android 4.4.2; NX507J Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.8 TBS/036872 Safari/537.36'})

        print session.cookies.get_dict()

        # a = {'mobilev': 'touch',
        #      'pt_key': 'app_openAAFYPUnCADBJkBmvF5KqdNzJkXaxqJXTvSn3XpeR19IrTyoFZeTjQhp4rez431oMmtKSqQUHZIA',
        #      'pwdt_id': 'jd_5b64e3796d3d7', 'sid': '3ff2638bdcf7e21e7afcf6d3f4dc57bw',
        #      'guid': '4bf7c404c3d9c7b68c91f21ec4613a74148c3599b38a85dc079252b2b833b11f', 'pt_pin': 'jd_5b64e3796d3d7'}

    def order_generate_test(self):
        url = 'http://train.m.jd.com/bookSeat/generateOrder.json'
        cookie = 'pt_key=%s;pwdt_id=%s;sid=%s;guid=%s;pt_pin=%s;mobilev=%s' % (
            'app_openAAFYPUnCADBJkBmvF5KqdNzJkXaxqJXTvSn3XpeR19IrTyoFZeTjQhp4rez431oMmtKSqQUHZIA',
            'jd_5b64e3796d3d7', '3ff2638bdcf7e21e7afcf6d3f4dc57bw',
            '4bf7c404c3d9c7b68c91f21ec4613a74148c3599b38a85dc079252b2b833b11f',
            'jd_5b64e3796d3d7', 'touch')

        headers = {'Pragma': 'no-cache',
                   'Cache-Control': 'no-cache',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Origin': 'http://train.m.jd.com',
                   'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': 'jdapp;android;5.4.1;4.4.2;863175026618021-a8a6681e316b;network/wifi;osp/android;apv/5.4.1;osv/4.4.2;uid/863175026618021-a8a6681e316b;pv/85.64;psn/863175026618021-a8a6681e316b|91;psq/65;ref/;pap/JA2015_311210|5.4.1|ANDROID 4.4.2;usc/;ucp/;umd/;utr/;adk/;ads/;Mozilla/5.0 (Linux; Android 4.4.2; NX507J Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.8 TBS/036872 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,en-US;q=0.8',
                   'cookie': cookie}
        data = 'cheCi=G5&seatType=edz&seatPrice=55300&fromStationCode=VNP&fromStationName=%E5%8C%97%E4%BA%AC%E5%8D%97&toStationCode=AOH&toStationName=%E4%B8%8A%E6%B5%B7%E8%99%B9%E6%A1%A5&trainDate=1480435200000&passengerIds=1204607&contact=%E5%90%B4%E5%8B%87%E5%88%9A&phone=13978632546&realBook=1&account=&password='
        req = requests.post(url, data=data, headers=headers)
        resp = req.json()

        print resp

        orderid = resp['orderId']

        url = 'https://train.m.jd.com/bookSeat/book/s_1480435200000_%E5%8C%97%E4%BA%AC_BJP_%E4%B8%8A%E6%B5%B7_SHH_G5_edz'
        req = requests.get(url, headers=headers, verify=False)

        print req.text

    def order_submit(self):
        url = 'https://train.m.jd.com/bookSeat/submitOrder.action'
        cookie = 'pt_key=%s;pwdt_id=%s;sid=%s;guid=%s;pt_pin=%s;mobilev=%s' % (
            'app_openAAFYPUnCADBJkBmvF5KqdNzJkXaxqJXTvSn3XpeR19IrTyoFZeTjQhp4rez431oMmtKSqQUHZIA',
            'jd_5b64e3796d3d7', '3ff2638bdcf7e21e7afcf6d3f4dc57bw',
            '4bf7c404c3d9c7b68c91f21ec4613a74148c3599b38a85dc079252b2b833b11f',
            'jd_5b64e3796d3d7', 'touch')

        headers = {'Pragma': 'no-cache',
                   'Cache-Control': 'no-cache',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Origin': 'http://train.m.jd.com',
                   'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': 'jdapp;android;5.4.1;4.4.2;863175026618021-a8a6681e316b;network/wifi;osp/android;apv/5.4.1;osv/4.4.2;uid/863175026618021-a8a6681e316b;pv/85.64;psn/863175026618021-a8a6681e316b|91;psq/65;ref/;pap/JA2015_311210|5.4.1|ANDROID 4.4.2;usc/;ucp/;umd/;utr/;adk/;ads/;Mozilla/5.0 (Linux; Android 4.4.2; NX507J Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.8 TBS/036872 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Referer': 'https://train.m.jd.com/bookSeat/book/s_1480435200000_%E5%8C%97%E4%BA%AC_BJP_%E4%B8%8A%E6%B5%B7_SHH_G5_edz',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,en-US;q=0.8',
                   'cookie': cookie}
        data = 'token=56493c1030c44cf08e861765d373b99e&token2=56493c1030c44cf08e861765d373b99e&orderId=1285071&totalFee=55300&pwd=&payTypes=&couponIds=&couponFee=0'
        req = requests.post(url, data=data, headers=headers, verify=False)
        resp = req.text
        print resp

    def test_seach_phone(self):
        body = {"mobile": "m6zea9UPXp1LKzYzd1YWow=="}
        sign = auth.sign('searchPczPriceList', self.uuid, json.dumps(body))
        url = 'http://api.m.jd.com/client.action?functionId=searchPczPriceList&clientVersion=5.3.0&build=36639&client=android&osVersion=4.4.2&screen=1920*1080&partner=waps007&uuid=%s&area=1_0_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
            self.uuid, sign[1], sign[0])
        headers = {
            'Charset': 'UTF-8',
            'jdc-backup': self.cookie,
            'Connection': 'close',
            'Cookie': self.cookie,
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        resp = requests.post(url, data='body=' + urllib.quote_plus(json.dumps(body)) + '&', headers=headers)
        print resp.text

        resp = resp.json()
        data = filter(lambda sku: sku['facePrice'] == '100', resp['skuList'])
        print len(data)
        print str(float(data[0]['jdPrice']) / 100)

    def test_queryNoticeConfig(self):
        body = {"configType": 1, "mobile": "m6zea9UPXp1LKzYzd1YWow=="}
        sign = auth.sign('queryNoticeConfig', self.uuid, json.dumps(body))
        url = 'http://api.m.jd.com/client.action?functionId=queryNoticeConfig&clientVersion=5.3.0&build=36639&client=android&d_brand=nubia&d_model=NX507J&osVersion=4.4.2&screen=1920*1080&partner=waps007&uuid=%s&area=1_0_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
            self.uuid, sign[1], sign[0])
        headers = {
            'Charset': 'UTF-8',
            'jdc-backup': self.cookie,
            'Connection': 'close',
            'Cookie': self.cookie,
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        resp = requests.post(url, data='body=' + urllib.quote_plus(json.dumps(body)) + '&', headers=headers)
        print resp.text

    def test_user_mobile(self):
        body = {}
        sign = auth.sign('getUserMobile', self.uuid, json.dumps(body))
        url = 'http://api.m.jd.com/client.action?functionId=getUserMobile&clientVersion=5.3.0&build=36639&client=android&d_brand=nubia&d_model=NX507J&osVersion=4.4.2&screen=1920*1080&partner=waps007&uuid=%s&area=1_0_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
            self.uuid, sign[1], sign[0])
        headers = {
            'Charset': 'UTF-8',
            'jdc-backup': self.cookie,
            'Connection': 'close',
            'Cookie': self.cookie,
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        resp = requests.post(url, data='body=' + urllib.quote_plus(json.dumps(body)) + '&', headers=headers)
        print resp.text

    # {"code":"0","orderId":"46431345969","money":9490}
    # body={"dxqids":"7929697981","facePrice":"100.0","isBingding":"0","isNote":"0","jdPrice":"94.80","payType":"10","type":"1","contact":"false","mobile":"t+itDImrWSiR\/V6gD6ei8A=="}&
    def test_phone_charge(self):
        body = {"facePrice": "10", "isBingding": "0", "isNote": "0", "jdPrice": "10.00",
                "payType": "0", "type": "1", "contact": "false", "mobile": '945UOUTLqNSLi+9eu1zb1g=='}
        # body = {"facePrice": "10", "isBingding": "0", "isNote": "0", "jdPrice": "10.00", "payType": "0",
        #         "type": "1", "contact": "false", "mobile": "945UOUTLqNSLi+9eu1zb1g=="}
        sign = auth.sign('submitPczOrder', self.uuid, json.dumps(body))
        url = 'http://api.m.jd.com/client.action?functionId=submitPczOrder&client=android&clientVersion=5.3.0&build=36639&d_brand=ZTE&d_model=SCH-I779&osVersion=4.4.2&screen=1280*720&partner=tencent&uuid=%s&area=1_0_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
            self.uuid, sign[1], sign[0])

        headers = {
            'Charset': 'UTF-8',
            'jdc-backup': self.cookie,
            'Connection': 'close',
            'Cookie': self.cookie,
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        resp = requests.post(url, data='body=' + urllib.quote_plus(json.dumps(body)) + '&', headers=headers)
        print resp.text

    def testfda(self):
        pay_task_data = {"sessionId": "",
                         "data": {"exData": {"orderId": "", "userId": "", "payurl": "", "Cookie": "", "pc_Cookie": ""},
                                  "amount": 9980, "ticketOrderNo": "46457211794", "siteNo": "jingdong_phone",
                                  "loginUser": "jd_5cef10a31da83", "creatTime": "2016-12-12 19:53:47.218000",
                                  "sysOrderNo": "49", "isPay": "false", "loginPwd": "qq456789"}, "module": {"worker": [
                {"type": 0, "assembly": "FBServer.Pay.TrainJD.Pay_RechargePhoneBillJD,FBServer.Pay.TrainJD.dll",
                 "parms": ""}], "payer": ["{0}"]}}
        url = 'http://op.yikao666.cn/JDTrainOpen/CreatePayTaskByPhone'
        pay_task_data = json.dumps(pay_task_data)
        resp = requests.post(url, data={'send_data': pay_task_data})
        print resp.text
