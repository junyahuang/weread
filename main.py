'''
定时自定义
2 8,12,19 * * * main.py
new Env('微信读书时长');
'''# 
#  微信读书
#  
     
import random
import requests
import json
import time
import hashlib
import urllib.parse
import pprint

# 如果登录过期，更新下面的cookies和heads部分即可
cookies = {
    'pgv_pvid': '5537798884',
    'RK': 'lTtxzUv2P0',
    'ptcz': 'ccf83d4c56a360e8ebf2166d5b5eacbb85fdb0ee73769d1ff4a3b735c26ca6b7',
    '_qimei_uuid42': '1890714350b100e79ba6d512a18fc724d7b284f602',
    'pac_uid': '0_s8M6MC4e7QkRd',
    'suid': 'user_0_s8M6MC4e7QkRd',
    '_qimei_q32': '4f2f9adbbb99c2b38859e725a3feb353',
    '_qimei_q36': '654a4465d49264bfb3bdf58730001e21881c',
    '_qimei_fingerprint': '9d8d0a404dd35e62e023359a2bc92ccd',
    '_qimei_h38': 'fded6d509ba6d512a18fc72402000005b18907',
    'eas_sid': 'B1Z7W2B7o0r9M800V4k8I4c413',
    'wr_gid': '278027022',
    'wr_fp': '4091178541',
    'wr_skey': 'rfVBWjC4',
    'wr_vid': '343133995',
    'wr_rt': 'web%40XHch2BcMGml2gZX9D5z_AL',
    'wr_localvid': '16e3295081473cf2b16e432',
    'wr_name': 'Jun%E5%91%80',
    'wr_avatar': 'https%3A%2F%2Fres.weread.qq.com%2Fwravatar%2FWV0018-LAcUE9woy7iq1sKdnaBEPa7%2F0',
    'wr_gender': '1',
}

headers = {
    'authority': 'weread.qq.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=dev-1730698697208,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=08657a6f277d447a886a87ad76d53e28',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'pgv_pvid=5537798884; RK=lTtxzUv2P0; ptcz=ccf83d4c56a360e8ebf2166d5b5eacbb85fdb0ee73769d1ff4a3b735c26ca6b7; _qimei_uuid42=1890714350b100e79ba6d512a18fc724d7b284f602; pac_uid=0_s8M6MC4e7QkRd; suid=user_0_s8M6MC4e7QkRd; _qimei_q32=4f2f9adbbb99c2b38859e725a3feb353; _qimei_q36=654a4465d49264bfb3bdf58730001e21881c; _qimei_fingerprint=9d8d0a404dd35e62e023359a2bc92ccd; _qimei_h38=fded6d509ba6d512a18fc72402000005b18907; eas_sid=B1Z7W2B7o0r9M800V4k8I4c413; wr_gid=278027022; wr_fp=4091178541; wr_skey=rfVBWjC4; wr_vid=343133995; wr_rt=web%40XHch2BcMGml2gZX9D5z_AL; wr_localvid=16e3295081473cf2b16e432; wr_name=Jun%E5%91%80; wr_avatar=https%3A%2F%2Fres.weread.qq.com%2Fwravatar%2FWV0018-LAcUE9woy7iq1sKdnaBEPa7%2F0; wr_gender=1',
    'origin': 'https://weread.qq.com',
    'referer': 'https://weread.qq.com/web/reader/ce032b305a9bc1ce0b0dd2ake2c32140247e2c420d92577',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '08657a6f277d447a886a87ad76d53e28-9df7602edac841ac',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
}

# 这是读的书籍信息，挑一本你读过的书
data = {
    'appId': 'wb182564874663h1617811994',
    'b': 'ce032b305a9bc1ce0b0dd2a',
    'c': 'e2c32140247e2c420d92577',
    'ci': 71,
    'co': 530,
    'sm': '[插图]广播纪元7年，智子《时间之外的往',
    'pr': 75,
    'rt': 30,
    'ts': 1731317531607,
    'rn': 191,
    'sg': '11cf328146b8dbc41cefd92906dfe5c04eb4c59fd657a5eb4d25e5533a37ce41',
    'ct': 1731317531,
    'ps': '42d32a407a51c7e6g010dee',
    'pc': '42d32a407a51c7e6g010dee',
    's': '8f27bc0c',
}

def get_wr_skey():
    url = "https://weread.qq.com/web/login/renewal"
    data = {
        "rq": "%2Fweb%2Fbook%2Fread"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    # print(response.text)
    cookie_str = response.headers['Set-Cookie']
    # print(cookie_str)
    wr_key = ""
    for cookie in cookie_str.split(';'):
        if cookie.__contains__("wr_skey"):
            wr_skey = cookie[-8:]
            print("数据初始化成功！")
            return wr_skey
             
def encode_data(data, keys_to_include=None):
    sorted_keys = sorted(data.keys())
    query_string = ''

    for key in sorted_keys:
        if keys_to_include is None or key in keys_to_include:
            value = data[key]
            encoded_value = urllib.parse.quote(str(value), safe='')
            query_string += f'{key}={encoded_value}&'

    if query_string.endswith('&'):
        query_string = query_string[:-1]

    return query_string


def cal_hash(input_string):
    _7032f5 = 0x15051505
    _cc1055 = _7032f5
    length = len(input_string)
    _19094e = length - 1

    while _19094e > 0:
        _7032f5 = 0x7fffffff & (_7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30)
        _cc1055 = 0x7fffffff & (_cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30)
        _19094e -= 2

    return hex(_7032f5 + _cc1055)[2:].lower()


url = "https://weread.qq.com/web/book/read"


# 加密盐
key = "3c5c8717f3daf09iop3423zafeqoi"
num = 1
errnum = 0
t = 0
ss =0

while True:
    # 处理数据
    print(f"-------------------第{num}次，共阅读{ss/60}分钟-------------------")
    data['ct'] = int(time.time())
    data['ts'] = int(time.time() * 1000)
    data['rn'] = random.randint(0, 1000)  # 1000以内的随机整数值
    data['sg'] = hashlib.sha256(("" + str(data['ts']) + str(data['rn']) + key).encode()).hexdigest()
    print(f"sg:{data['sg']}")
    data['s'] = cal_hash(encode_data(data))
    print(f"s:{data['s']}")

    sendData = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=sendData)
    resData = response.json()
    print(response.json())



    if 'succ' in resData:
        print("数据格式正确，阅读进度有效！")
        # 确认无s字段
        num += 1
        t = random.randint(100, 200)
        ss= ss +t
        time.sleep(t)
    else:
        print("数据格式问题,异常退出！")
        cookies['wr_skey'] = get_wr_skey()
        errnum += 1
        num -= 1

    if num == 50:
        print("阅读脚本运行已完成！")
        QLAPI.notify("微信阅读",f"阅读脚本运行已完成！共阅读{ss/60}分钟")
        break
    elif errnum >3:
        print("阅读脚本运行未正常完成！")
        QLAPI.notify("微信阅读",f"阅读脚本运行未正常完成！共阅读{ss/60}分钟")
        
        break    

    data.pop('s')
