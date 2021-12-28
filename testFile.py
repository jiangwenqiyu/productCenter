import requests
import json
import copy
from _pydecimal import Decimal, Context, ROUND_HALF_UP
import decimal





# b = Context(prec=5, rounding=ROUND_HALF_UP).create_decimal_from_float(a)
# print(b*1)

url = 'http://product.xinfangsheng.com/sysback/supplyareaprice/getCommitRecordDetailByRecordNo?recordNo=RECORD202112241754060839&menuId=270&buttonId=2'
json_header = {'Accept': 'application/json, text/plain, */*',
                            'Content-Type': 'application/json;charset=UTF-8',
                            'Connection': 'close',
               'cookie':'uc_token=cb3bac116e7c4b70b793e1d38340d6c0'}
data = {}

res = requests.post(url, headers = json_header, json= data).json()
for i in res['retData']['supplyAreaPriceParamVos']:
    if i['templateCityUuid'] != '110100':
        print(i['skuNo'], i['templateCityUuid'])
        # print()






