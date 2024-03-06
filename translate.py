import requests
import time
import hashlib
import uuid
from bs4 import BeautifulSoup

youdao_url = 'https://openapi.youdao.com/api'   # 有道api地址
header = {"User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"}

def get_sentenses(translate_text, debug=False):
    url = 'https://mobile.youdao.com/singledict?q='+ translate_text +'&dict=blng_sents_part&le=eng&more=false'#目标访问网站url
    #伪装头信息的引入
    req = requests.get(url=url,headers = header) #返回爬取网站信息
    req.encoding = 'utf-8'  #查看head中charset可以查找到编码信息
    html = req.text #转化为文本

    soup = BeautifulSoup(html, 'html.parser')
    if debug:
        for div in soup.find_all('div', class_='col2'):
            print(div.text)
    return soup.find_all('div', class_='col2')

def translate(translate_text="which", debug=False):
    # 翻译文本生成sign前进行的处理
    input_text = ""

    # 当文本长度小于等于20时，取文本
    if(len(translate_text) <= 20):
        input_text = translate_text
        
    # 当文本长度大于20时，进行特殊处理
    elif(len(translate_text) > 20):
        input_text = translate_text[:10] + str(len(translate_text)) + translate_text[-10:]
        
    time_curtime = int(time.time())   # 秒级时间戳获取
    app_id = "77253d1112b6155f"   # 应用id
    uu_id = uuid.uuid4()   # 随机生成的uuid数，为了每次都生成一个不重复的数。
    app_key = "rBFWd8OO3uoraptl76V6TSnJkok3TyGP"   # 应用密钥

    sign = hashlib.sha256((app_id + input_text + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()   # sign生成


    data = {
        'q':translate_text,   # 翻译文本
        'from':"en",   # 源语言
        'to':"zh-CHS",   # 翻译语言
        'appKey':app_id,   # 应用id
        'salt':uu_id,   # 随机生产的uuid码
        'sign':sign,   # 签名
        'signType':"v3",   # 签名类型，固定值
        'curtime':time_curtime,   # 秒级时间戳
    }

    r = requests.get(youdao_url, params = data).json()   # 获取返回的json()内容
    trans_res   = None
    us_phonetic = None
    uk_phonetic = None
    explains    = None
    webdict     = None
    if 'translation' in r.keys():
        trans_res   = r['translation'][0]
    if 'basic' in r.keys():
        if 'us-phonetic' in r['basic'].keys():
            us_phonetic = r['basic']['us-phonetic']
        if 'uk-phonetic' in r['basic'].keys():
            uk_phonetic = r['basic']['uk-phonetic']
        if 'explains' in r['basic'].keys():
            explains    = r['basic']['explains']
    if 'webdict' in r.keys():
        if 'url' in r['webdict'].keys():
            webdict     = r['webdict']['url']

    if debug:
        print(f"：{trans_res}")  
        print(f"美：/{us_phonetic}/")   
        print(f"英：/{uk_phonetic}/")   
        for explain in explains:
            print(f"{explain}")   
        print(f"webdict: {webdict}")
    return us_phonetic, uk_phonetic, explains