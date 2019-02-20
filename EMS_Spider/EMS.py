import requests, re, base64
from bs4 import BeautifulSoup


class req(object):
    def __init__(self, first_url, list_url, data):
        self.first_url = first_url
        self.list_url = list_url
        self.data = data

    def headers(self):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Referer':'http://cdjwc.ccu.edu.cn/jsxsd/',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'}
        return headers

    def session_request(self):
        #session会话请求
        s = requests.Session()
        html = s.post(self.first_url, data=self.data, headers=self.headers())
        score_list = s.get(self.list_url, headers=self.headers())
        return score_list.text

    def cookies_request(self):
        #取得cookies，请求
        html = requests.post(self.first_url, data=self.data, headers=self.headers(), allow_redirects=False)
        cookie = html.cookies.get_dict()
        score_list = requests.get(self.list_url, cookies=cookie, headers=self.headers())
        return score_list.text

    def score(self):
        scores = self.session_request()
        soup = BeautifulSoup(scores,'html.parser')
        tags = soup.find_all('tr')
        point = soup.find_all('span')
        print(point[-1].get_text())
        del tags[0]
        del tags[0]
        print("{}{:^14}{:^22} {}{:^36}".format('序号','学期','成绩','学分','课程名称'))
        print('')
        for x in tags:
            a = re.findall(r'>(.|..|...|....)</a',str(x))
            b =re.findall(r'>(.*?)</td>',str(x))
            print('{:^4}{:^18}{:^18}  {}{:^40}'.format(str(b[0]),b[1],a[0],b[5],b[3]))
            print('')


first_url = 'http://cdjwc.ccu.edu.cn/jsxsd/xk/LoginToXk'
list_url = 'http://cdjwc.ccu.edu.cn/jsxsd/kscj/cjcx_list'
def change_password(x):
    password_ori = x.encode('utf-8')
    password_base64 = base64.b64encode(password_ori)
    password = password_base64.decode('utf-8')
    return password
ID = change_password(input("请输入学号："))
password = change_password(input("请输入密码："))
data ={'encoded':ID+'%%%'+password}
a = req(first_url,list_url,data)
a.score()
