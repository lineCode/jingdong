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
        cookies = []
        for c in resp.headers['Set-Cookie'].split(';,'):
            cookies.append(c.split(';')[0].strip())
        return ';'.join(cookies)

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
    print get_cookie('18784314177', 'xx334331')
    # get_verifycode('')

    # cookie = 'login_c=1; Expires=Mon, 9-Oct-2017 04:41:10 GMT; Path=/; HttpOnly, mp=18784314177; Expires=Mon, 9-Oct-2017 04:41:10 GMT; Path=/; HttpOnly;, TrackID=1Fg60XhviwgKQvLEjYK_z70VHP_ht5_idm3Mtx4OUAtoTQpbtR0moUYYwYFR570s9a3vkQR3Qki-C-DD_sAewX-HI6KXXBdigr4wHpWgyGL4; Domain=.jd.com; Expires=Thu, 8-Sep-2022 04:41:10 GMT; Path=/;, pinId=kLRXkVg5T_1H0wT8lNXSVLV9-x-f3wj7; Domain=.jd.com; Expires=Sun, 9-Sep-2018 04:41:10 GMT; Path=/;, pin=jd_4a17203041cf4; Domain=.jd.com; Expires=Mon, 9-Oct-2017 04:41:10 GMT; Path=/;, unick=jd_187843slgx; Domain=.jd.com; Expires=Mon, 9-Oct-2017 04:41:10 GMT; Path=/; HttpOnly;, thor=B65B3FF5284C56A4F5FBF6544F7D40956DAE9B2865A6E229B3B218B001D73476C6CF1C93541BB2593694B7674187E7D9A3591AE9DE104EB2CE3CCC1C99826A300883A9E5D383CF050DC5D43A2F12796C6BAB84C453CF25FDFC89CCA0AD434DC3CC0628DC93A1C8CC0AC4F014963527DCB82244BA4AD6032CAEFC326817256F279FFC0AF6F98826AF75BAE2A072C125359B9AE0BF4159F5DF9928995D7E013DD1; Domain=.jd.com; Path=/; HttpOnly;, ol=1; Path=/; HttpOnly;, _tp=8pB%2FDXRnhElokNnQI8xVfmlJGtIvlmsWsHovq3G17w4%3D; Domain=.jd.com; Expires=Mon, 9-Oct-2017 04:41:10 GMT; Path=/;, logining=1; Domain=.jd.com; Path=/;, _pst=jd_4a17203041cf4; Domain=.jd.com; Expires=Mon, 9-Oct-2017 04:41:10 GMT; Path=/; HttpOnly;, ceshi3.com=101; Domain=.jd.com; Path=/;'
    # cookies=[]
    # for c in cookie.split(';,'):
    #     print c
    #     cookies.append(c.split(';')[0].strip())
    #
    # print cookies
    # print ';'.join(cookies)
