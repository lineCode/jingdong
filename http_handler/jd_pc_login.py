import requests
import time
import re
from bs4 import BeautifulSoup
import log_ex as logger
import json
import rk
import urllib


def get_cookie(username, password):
    logger.info('pc:login')
    logoutUrl = "https://passport.jd.com/uc/login?ltype=logout"
    resp = requests.get(logoutUrl)
    logger.info('get pc cookie')
    cookie = resp.headers['Set-Cookie']
    text = resp.text
    payload = {}
    bsop = BeautifulSoup(text, 'html.parser')

    verify_code_img = bsop.find('img', {'id': 'JD_Verification1'})
    verify_code = ''
    if verify_code_img:
        url = verify_code_img['src2']
        logger.info('verifycodeurl:' + url)
        verify_code = get_verifycode(url)
    else:
        logger.info('verifycode not need')

    hidden_ipputs = bsop.findAll('input', {'type': 'hidden'})
    for _input in hidden_ipputs:
        payload[_input['name']] = _input['value']

    if payload:
        payload['loginname'] = username
        payload['loginpwd'] = password
        payload['nloginpwd'] = password
        payload['authcode'] = verify_code
    else:
        raise Exception('pc payload get error')

    logger.debug('login.cookie=>%s,payload=>%s' % (cookie, payload))
    login_url = 'https://passport.jd.com/uc/loginService?uuid=%s&type=logout&r=%s&version=2015' \
                % (payload['uuid'], int(time.time()))

    resp = requests.post(login_url, payload, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
        "Cache-Control": "no-cache",
        "Referer": "https://passport.jd.com/uc/login?ltype=logout",
        "Host": "passport.jd.com",
        "Cookie": cookie
    })

    if '({"success":"http://www.jd.com"})' == resp.text:
        logger.info('login success')
        return resp.headers['Set-Cookie']

    logger.info('login faild')
    return None


def get_verifycode(verifycode_url):
    url = 'https://passport.jd.com/uc/showAuthCode?r='
    resp = requests.get(url)
    if '\"verifycode\":true' in resp.text:
        for i in range(2):
            resp = requests.get(
                'https:%s&yys=%d' % (verifycode_url.replace('&amp;', '&'), int(round(time.time() * 1000)))
                , headers={
                    'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
                })
        logger.info('send image to rk')
        rc = rk.RClient('15974253250', '1qaz2wsx', '78409', 'e024badb361646e1a38a2afca8cf23f6')
        result = rc.rk_create(resp.content, 3000)
        logger.debug('rk=>' + json.dumps(result))
        if result and result['Result']:
            logger.info('verify code =>' + result['Result'])
            return result['Result']
    else:
        return None


if __name__ == "__main__":
    get_cookie('18784314177', 'xx334331')
    # get_verifycode('')
