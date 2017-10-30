# -*- coding: utf-8 -*-
import auth
import re
import json
import requests
import urllib
import time
import log_ex as logger

class Order:
    def __init__(self, uuid, user_agent, cookie):
        self.uuid = uuid
        self.user_agent = user_agent
        if cookie:
            self.cookie = 'pt_key=%s;pwdt_id=%s;sid=%s;guid=%s;pt_pin=%s;mobilev=%s' % (
                cookie['pt_key'], cookie['pwdt_id'], cookie['sid'], cookie['guid'],
                cookie['pt_pin'], cookie['mobilev'])
            self.headers = {'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Origin': 'http://train.m.jd.com',
                            'X-Requested-With': 'XMLHttpRequest',
                            'User-Agent': self.user_agent,
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,en-US;q=0.8',
                            'cookie': self.cookie}

    # {"passengerId": 1232896, "success": true}
    def add_passenger(self, passenger):
        url = 'https://train.m.jd.com/passenger/add.json'
        self.headers[
            'Referer'] = 'https://train.m.jd.com/bookSeat/book/s_1482508800000_%E6%96%B0%E4%BD%99_XUG_%E7%BB%8D%E5%85%B4_SOH_G2334_edz'

        p_ids = []
        for p in passenger:
            data = 'contactName=%s&idCardType=1&idCardInfo=%s' % (
                urllib.quote_plus(p['name'].encode('utf-8')), p['IDCard'])

            logger.debug('POST %s \n%s' % (url, data))
            resp = requests.post(url, data=data, headers=self.headers, verify=False)

            logger.debug('resp %s' % resp.text)
            resp_body = resp.json()
            if resp_body['success']:
                p_ids.append(str(resp_body['passengerId']))
            else:
                raise Exception('add passenger error')

        return p_ids

    def add_contract(self, name, phone):
        url = 'https://train.m.jd.com/contact/add.json'
        self.headers[
            'Referer'] = 'https://train.m.jd.com/bookSeat/book/s_1482508800000_%E6%96%B0%E4%BD%99_XUG_%E7%BB%8D%E5%85%B4_SOH_G2334_edz'

        data = 'contactName=%s&contactPhone=%s' % (urllib.quote_plus(name.encode('utf-8')), phone)
        resp = requests.post(url, data=data, headers=self.headers, verify=False)

        logger.debug('resp %s' % resp.text)
        resp_body = resp.json()
        if resp_body['success']:
            return resp_body['contactId']
        else:
            raise Exception('add contract error')

    def gen_order(self, train, passenger_ids):
        url = 'http://train.m.jd.com/bookSeat/generateOrder.json'

        # seatType = str(train['data']['exData1'])
        # if seatType == '1':
        #     seatType = 'yz'
        # elif seatType == 'O':
        #     seatType = 'edz'
        # else:
        #     raise Exception('seat type not support')

        logger.info('seach ticket')
        ticket = self.seach_ticket(train)
        if ticket:
            start_time = ticket[0]['trainInfo']['startTime']
        else:
            raise Exception('find out ticket faild')

        data = {'account': '', 'trainDate': train['data']['ticketsInfo'][0]['dptDate'],
                'toStationCode': train['data']['ticketsInfo'][0]['arrStation'],
                'toStationName': train['data']['ticketsInfo'][0]['destination'].encode("utf-8"), 'seatType': ticket[2],
                'realBook': '1',
                'acceptNoSeat':0,
                'ticketType':1,
                'phone': train['data']['contactInfo']['mobileNo'],
                'fromStationName': train['data']['ticketsInfo'][0]['departure'].encode("utf-8"),
                'contactId': train['data']['contactInfo']['contractId'],
                'contact': train['data']['contactInfo']['name'].encode("utf-8"), 'password': '',
                'passengerIds': passenger_ids,
                'seatPrice': int(train['data']['ticketsInfo'][0]['ticketPrice'] * 100) * len(passenger_ids.split(',')),
                'fromStationCode': train['data']['ticketsInfo'][0]['dptStation'],
                # 'cheCi': train['data']['ticketsInfo'][0]['coachNo'],
                'cheCi': ticket[0]['trainInfo']['trainCode'],
                'trainTime': start_time,
                'hasInsurance': False,
                'insuranceCode': 0,
                'hasInvoice': False,
                'invoiceJson': {},
                'isGrab': False,
                'userRank': '',
                'deadline': ''
                }
        # print data
        encode_data = urllib.urlencode(data)
        logger.debug('POST %s \n%s' % (url, encode_data))
        # data = 'cheCi=G5&seatType=edz&seatPrice=55300&fromStationCode=VNP&fromStationName=%E5%8C%97%E4%BA%AC%E5%8D%97&toStationCode=AOH&toStationName=%E4%B8%8A%E6%B5%B7%E8%99%B9%E6%A1%A5&trainDate=1480435200000&passengerIds=1204607&contact=%E5%90%B4%E5%8B%87%E5%88%9A&phone=13978632546&realBook=1&account=&password='
        resp = requests.post(url, data=data, headers=self.headers)
        logger.debug('resp %s' % resp.text)
        resp_body = resp.json()

        if resp_body and resp_body['success']:
            orderid = resp_body['orderId']
            data['orderid'] = orderid
            return data
        else:
            raise Exception('generate order faild.\n%s' % resp.text)

    def get_token(self, data):
        url = 'https://train.m.jd.com/bookSeat/book/s_%s_%s_%s_%s_%s_%s_%s' % (
            data['trainDate'], urllib.quote_plus(data['fromStationName']), data['fromStationCode'],
            urllib.quote_plus(data['toStationName']), data['toStationCode'], data['cheCi'], data['seatType'])

        logger.debug('GET %s' % url)
        resp = requests.get(url, headers=self.headers, verify=False)
        resp_body = resp.text
        # logger.debug('resp:%s' % resp_body)

        token = re.findall(r'<input type="hidden" name="token" value="(\w+)" />', resp_body)
        if token:
            data['token'] = token[0]
            data['referer'] = url
            return data
        else:
            raise Exception('token not found')

    def submit(self, data):
        url = 'https://train.m.jd.com/bookSeat/submitOrder.json'
        self.headers['Referer'] = data['referer'] + '?ran=%d' % int(time.time())

        data = 'token=%s&orderId=%s&totalFee=%d&pwd=%s' % (
            data['token'], data['orderid'], data['seatPrice'], data['coupon'])

        logger.debug('POST %s\n%s' % (url, data))

        self.headers['Origin'] = 'https://train.m.jd.com'
        self.headers['Upgrade-Insecure-Requests'] = '1'

        req = requests.post(url, data=data, headers=self.headers, verify=False)
        resp = req.text
        logger.debug('resp:%s' % resp)

        if resp.find(u'系统异常') == -1:
            return True
        else:
            return False

    def get_details(self, orderid):
        url = 'http://train.m.jd.com/orderDetail/orderDetail?orderId=%s&un_area=1_0_0_0' % orderid
        logger.debug('GET %s' % url)

        resp = requests.get(url, headers=self.headers)
        resp_body = resp.text

        # logger.debug('resp:%s' % resp_body)

        erpOrderId = re.findall(r'<input type="hidden" name="erpOrderId" value="(\w+)" />', resp_body)
        onlinePayFee = re.findall(r'<input type="hidden" name="onlinePayFee" value="(.*)"/>', resp_body)

        if erpOrderId and onlinePayFee:
            return {'erpOrderId': erpOrderId[0], 'onlinePayFee': onlinePayFee[0]}
        else:
            return None

    def seach_ticket(self, train):
        url = 'http://train.m.jd.com/ticket/searchTickets.json'
        data = {  # 'ticketRequest.trainCode': train['data']['ticketsInfo'][0]['coachNo'],
            'ticketRequest.trainDate': train['data']['ticketsInfo'][0]['dptDate'],
            'ticketRequest.fromStation': train['data']['ticketsInfo'][0]['dptStation'],
            'ticketRequest.toStation': train['data']['ticketsInfo'][0]['arrStation'],
            'ticketRequest.fromStationName': train['data']['ticketsInfo'][0]['departure'].encode("utf-8"),
            'ticketRequest.toStationName': train['data']['ticketsInfo'][0]['destination'].encode("utf-8")}

        headers = {'Host': 'train.m.jd.com',
                   'Pragma': 'no-cache',
                   'Cache-Control': 'no-cache',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Origin': 'http://train.m.jd.com',
                   'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': self.user_agent,
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Referer': 'http://train.m.jd.com/ticket/site/s_1480089600000_%E5%8C%97%E4%BA%AC_BJP_%E4%B8%8A%E6%B5%B7_SHH_G5',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,en-US;q=0.8',
                   'Cookie': self.cookie
                   }
        resp = requests.post(url, data=data, headers=headers)
        # print train
        return self.filter_ticket(resp.json()['tickets'], [train['data']['ticketsInfo'][0]['ticketPrice'],
                                                           train['data']['ticketsInfo'][0]['ticketPrice'] + float(
                                                               train['data']['exData2']['priceSection'])])

    def filter_ticket(self, tickets, price_range):
        for t in tickets:
            for s in t['seatList']:
                if int(s['num']) > 0 and float(s['price']) >= price_range[0] and float(s['price']) <= price_range[1]:
                    # print  s['price'], s['type'], int(s['num'])
                    return t, s['price'], s['type']
