import requests
import pymysql
import xlsxwriter
import time
import datetime
import cx_Oracle


url = 'http://product.xinfangsheng.com/sysback/salepriceskuupdate/getAllByBillUuid?isSaleMultiUnit=2&billUuid=RECORD202112101529390492&menuId=270&buttonId=2'
header = {'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json;charset=UTF-8',
          'Cookie':'uc_token=2af9f1375baa44ad9969a89ddd7deda7'}
data = {"billUuid":"RECORD202112101529390492"}
res = requests.post(url, headers = header, json=data).json()
for i in res['retData']:
    print(i, type(i))


