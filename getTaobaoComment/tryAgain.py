# import modules
import requests
import time
import re
import pandas as pd
import logging; logging.basicConfig(level=logging.INFO)

# two ways
# 1.get the text of html, then analysis it by beautifulsoup4
# 2.if way1 doesn`t work, try to catch json which save the data of comment
# how to find the json we need?  capture package!
# 一般来说可以通过beautifulsoup4分析html，得到评论，但是淘宝不支持。
# 所以需要抓包。淘宝的评论是存储在json的
urlf = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=573211741544&userNumId=2996293737&currentPageNum='
urll = '&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098%23E1hv29vEvbQvUvCkvvvvvjiPnLqUAj1URFMvgjivPmPwtjEvnL5wtj3ERFSWQjDnKphv8vvvphvvvvvvvvCHqQvv9apvvhi8vvvmjvvvoyIvvvUUvvC8o9vvv9kEvpvVvpCmp%2F2WuphvmvvvpLPkePYxmphvLUCuYSOaKBm65dUf8zcGV3K4VzibsW94jCOqb64B9Cka%2BfvsxI2UVB6t%2BFBCAfyprETAVAYlGb8reTtKvi7t%2BsI65zECgWpaeEkXa6gCvpvVvUCvpvvv2QhvCvvvMMGtvpvhvvCvp8wCvvpvvhHh3QhvCvmvphv%3D&_ksTS=1592227463181_1489&callback=jsonp_tbcrate_reviews_list'

# declare list to save data
# 声明一个list，存储抓取到的结果
# 为什么在这里声明而不再循环中？因为后面的存储到本地需要全局变量
data_list =[]

# use loop and sleep to catch the data
# 循环和休眠相结合，避免淘宝察觉是爬虫
for i in range(1, 20, 1):
    #拼接url
    url = urlf + str(i) + urll
    logging.info('url: %s' % url)

    #伪装，可以从抓包的界面获取这些信息
    headers ={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45',
        # 从哪个页面发出的数据申请，每个网站可能略有不同
        'referer': 'https://item.taobao.com/item.htm?spm=a230r.1.14.25.7069184bVHtn37&id=573211741544&ns=1&abbucket=4',
        # 哪个用户想要看数据，是游客还是注册用户,建议使用登录后的cookie
        'cookie': 't=0d5b7e1822e2dad3071d2c6e70a110cf; cna=Dl3GFuc/XAECAXM8Ahmm9tMi; thw=cn; tracknick=%5Cu52A0%5Cu7CD6%5Cu8702%5Cu871C%5Cu767D%5Cu5F00%5Cu6C34; hng=CN%7Czh-CN%7CCNY%7C156; lgc=%5Cu52A0%5Cu7CD6%5Cu8702%5Cu871C%5Cu767D%5Cu5F00%5Cu6C34; enc=yuL6k6WFbA4%2Fu0IiKA5P39%2B8I3KBNACT4JeyjRGhhrDOneSGJWH3JM4VrXBW%2FcXVl8VCb5JkAEyixzz33yfGpA%3D%3D; v=0; cookie2=5a202c8d80a0c7d05ce7f149bddb000f; _tb_token_=ee13ea3be3f40; _m_h5_tk=e8af5d0cb5e195e83d94fb955dd13d17_1592234607479; _m_h5_tk_enc=eb5d145a024fe2c77a2e83cb6c0ea317; _samesite_flag_=true; sgcookie=EmRKJWN0rgildICY4z0dk; unb=2324459526; uc3=lg2=V32FPkk%2Fw0dUvg%3D%3D&id2=UUtJY9XuxiusJg%3D%3D&vt3=F8dBxGDXLYUh2e8LIko%3D&nk2=30p1A2oyaHDvxfEV%2B2o%3D; csg=4e0142d9; cookie17=UUtJY9XuxiusJg%3D%3D; dnk=%5Cu52A0%5Cu7CD6%5Cu8702%5Cu871C%5Cu767D%5Cu5F00%5Cu6C34; skt=897cc1c7d39b528b; existShop=MTU5MjIyNDIxNQ%3D%3D; uc4=nk4=0%403b4Vd22%2BvWBwUEdBlqMY19dFihGdrUTiPw%3D%3D&id4=0%40U2lzTQL5JM2lwpbYiFcwAw914O%2BY; _cc_=W5iHLLyFfA%3D%3D; _l_g_=Ug%3D%3D; sg=%E6%B0%B469; _nk_=%5Cu52A0%5Cu7CD6%5Cu8702%5Cu871C%5Cu767D%5Cu5F00%5Cu6C34; cookie1=UoLee5RraSt4zEizw%2BDKGCc%2BIzMyBtp8DOzr4knt1c8%3D; mt=ci=-1_1; tfstk=ceVPBSvIn_CP6JGCBbGERn0bKTTRa9au-IoqEROvE3THriDobscvvqbuIqoyDoHl.; uc1=cookie21=VT5L2FSpccLuJBreK%2BBd&cookie15=URm48syIIVrSKA%3D%3D&cart_m=0&cookie14=UoTV7gOvE2udMw%3D%3D&existShop=false&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&pas=0; l=eBQ0O8_IQ5i02LrwKOfZhurza779HIRfguPzaNbMiOCP_3f95ORGWZxlhf8pCnGVn6JwR3RdNsBbBuTslyzhlevVQElBs2JazdTh.; isg=BOrqRwhDQELmyMysd9CbDEhDO1CMW2610ZaNJ3Sj7z3Ip4thXOmkxOfRN9O7V-ZN',
    }

    # 请求，以获取响应
    response = requests.get(url, headers= headers)
    if response.status_code !=200:
        print('wrong!!!!!!!!!!!!!!!   '+response.status_code)
        break

    data =response.text
    logging.info(data)
    # 休眠10s
    time.sleep(10)
    # 用正则表达式匹配评论，得到符合要求的content
    result = re.findall('"content":"(.*?)"', data)
    logging.info('result[%d]: %s' % (i, result))

    data_list.extend(result)

#保存至本地
if data_list !=[]:
    df = pd.DataFrame()
    df["评论"] = data_list
    df.to_excel("评论.xlsx")