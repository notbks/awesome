import os
import requests
from DecryptLogin import login
import pickle
import logging; logging.basicConfig(level=logging.INFO)

auctionNumId='13734572962'
userNumId= '90405449'
currentPageNum= '1'
pageSize= '20'
orderType= 'sort_weight'

url0 ='https://item.taobao.com/item.htm?spm=a310p.7395781.1998038982.3&id=13734572962'
url1 ='https://rate.taobao.com/feedRateList.htm?auctionNumId=%s&userNumId=%s&currentPageNum=%s&pageSize=%s&orderType=%s' % (auctionNumId, userNumId, currentPageNum, pageSize, orderType)
header = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.3',
    'Referer': 'https://item.taobao.com/item.htm',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Connection': 'keep-alive',
}



# response1 =requests.get(url1, headers=header, verify =False)
# print(response1.text)

class getComment():

    #初始化函数
    def __init__(self, **kwargs):
        logging.info('init~~~')
        if os.path.isfile('session.pkl') :
            self.session = pickle.load(open('session.pkl', 'rb'))
            logging.info('there is already session here~')
        else:
            self.session = self.login()
            f = open('session.pkl', 'wb')
            pickle.dump(self.session, f)
            f.close()
            logging.info('Login secessfully~ and write down the session too')

    #DecryptLogin封装好的自动登陆淘宝
    @staticmethod
    def login():
        lg = login.Login()
        infos_return, session = lg.taobao()
        return session

    #run！
    def run(self, url, page):
        params = {
            'auctionNumId' : '13734572962',
            'userNumId' :'90405449',
            'currentPageNum' : str(page),
            'pageSize' : '20',
            'orderType' : 'sort_weight',
        }

        response =self.session.get(url, params=params)
        logging.info(response.json())

        if response.status_code !=200:
            logging.info('something went wrong~ status_code: %d' % response.status_code)

        else:
            logging.info(response.json())


url = 'https://rate.taobao.com/feedRateList.htm?'

if __name__ =='__main__':
    crawl =getComment()
    crawl.run(url, 1)