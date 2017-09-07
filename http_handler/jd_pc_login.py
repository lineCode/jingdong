import requests
import time

def get_cookie():
    logoutUrl = "https://passport.jd.com/uc/login?ltype=logout"

    return ''

def get_verifycode(verifycode_url):
    url='https://passport.jd.com/uc/showAuthCode?r='
    resp = requests.get(url)
    if '\"verifycode\":true"' in resp.text:
        resp = requests.get('https://%s&yys=%d'%(verifycode_url.replace('&amp;','&'),int(time.time())))
        print resp.content
    else:
        return None


