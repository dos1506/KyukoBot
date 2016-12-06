import requests
from bs4 import BeautifulSoup
import re
import mojimoji

class KyukoInfo:
    
    def __init__(self):
        self.date = None
        self.department = None
        self.time = None
        self.teacher = None
        self.subject = None
        self.status = None
    
    def __getitem__(self, element):
        if element == 'date':
            return self.date
        elif element == 'department':
            return self.department
        elif element == 'time':
            return self.time
        elif element == 'teacher':
            return self.teacher
        elif element == 'subject':
            return self.subject
        elif element == 'status':
            return self.status
        else:
           raise IndexError() 

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):
        return str(self.__dict__)
    
    def __str__(self):
        return str(self.__dict__)

    def to_dict(self):
        return self.__dict__
      


def fetchKyukoInfo():
    url = 'http://hirose.sendai-nct.ac.jp/kyuko/kyuko.cgi'
    try:
        html = requests.get(url)
    except ConnectionError:
        return {'ERROR': 'Connection Error'}
    except Timeout:
        return {'ERROR': 'Timeout'}
    except TooManyRedirects:
        return {'ERROR': 'Too Many Redirects'}

    if html.status_code != 200:
        return {'ERROR': html.status_code}

    html.encoding = 'shif_jis'

    soup = BeautifulSoup(html.content, 'html5lib')
    attrs = {'width': 650}
    kyuko = list()

    for elem in soup.findAll('table', attrs):
        kyuko.append(parseKyukoRecord(elem))

    return kyuko

def parseKyukoRecord(record):
    num_map = {'�T': 'I', '�U': 'II', '�V': 'III'}

    detail = KyukoInfo()
    detail.date    = list(re.findall('([0-9]{,2})月([0-9]{,2})日<.*>\((.*)\)</font>', str(record.b))[0])
    detail.department, detail.time = [x.string for x in record.select('td font b')]
    detail.teacher = record.select('td font[color=#00008B]')[0].string.strip()
    detail.status  = re.findall('./img/(.*).gif', str(record.select('img')))[0]

    subject        = record.select('tr td tr font')[0].string
    # ローマ数字から半角英数字へ変換
    for num in num_map:
       if num in subject:
           subject = subject.replace(num, num_map[num])
    detail.subject = subject

    # 全角英数字を半角英数字へ変換
    detail.department = mojimoji.zen_to_han(str(detail.department))
    detail.subject    = mojimoji.zen_to_han(str(detail.subject))
    detail.time       = mojimoji.zen_to_han(str(detail.time))

    return detail
