import requests
import re
from lxml import etree
import time
import hashlib
import re
import json
import pymysql

def geturl():
    url = 'http://vendor.heneng.cn:16791/api/gwc'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '123',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'vendor.heneng.cn:16791',
        'Origin': 'http://vendor.heneng.cn:16790',
        'Pragma': 'no-cache',
        'Referer': 'http://vendor.heneng.cn:16790/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
#定值，除了页码有改变
    for page in range(1,21):
        i = str(int(time.time() * 1000))
        payload1 = '{"action":"P_SUP_Bid_GetNotice","p1":"","p2":"",' \
            f'"p3":{page},"p4":20,"p5":"","p6":"-1","p7":""}}'
#获取时间戳
        #ts1 = str(int(time.time() * 1000))
        print(payload1)
#MD5加密过程生成str_md5
        strs = payload1 + str(i) + "HNSUP.2018._.123"
        m = hashlib.md5()
        b = strs.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        #print(str_md5)
        data = {
            'ak': str_md5,
            'i': str(i),
            'payload': payload1,
        }
        response = requests.post(url=url,headers=headers, data=json.dumps(data))
        content = json.loads(response.text)
        print(content)
        content = content['data']
        #print(content)
        get_content(content)

#获取内容
def get_content(content):
    for i in content:
        item = {}
        item['title'] = i['noticetitle']
        item['publishdate'] = i['publishdate']
        item['signenddate'] = i['signenddate']
        item['tenderingunitname'] = i['tenderingunitname']
        item['condition'] = i['condition']
        item['noticeexplain'] = ''.join(re.findall(r'[\u4e00-\u9fa5]+',i['noticeexplain'].replace('微软雅黑','')))
        insert(item)
#加载入库
def insert(item):
    try:
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='redhat',
                             database='mysql',
                             port=3306,
                             charset='utf8')
        cursor = db.cursor()
        sql = ("insert into text11(title,runoob_title,runoob_author1,runoob_author2,runoob_author3,runoob_author4) values('%s','%s','%s','%s','%s','%s')" %(item["title"],item['publishdate'],item['signenddate'],item['tenderingunitname'],item['condition'],item['noticeexplain']))
        cursor.execute(sql)
        #保存成功
        print('save to mysql',item)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print('出现错误')

if __name__ == '__main__':
    geturl()



