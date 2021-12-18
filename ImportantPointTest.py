from environmentConfig import LoginInfo
import requests
import random
import time

excep_temp = '\nurl:{}\ndata:{}\nexception:{}'
error_temp = '\nurl:{}\ndata:{}\nres:{}'

class alterCosePrice(LoginInfo):
    # 关联商品获取  供应商-sku，500个
    def getSupplySku_500(self):
        print('查询500个商品')
        self.host = 'http://product.t4.xinfangsheng.com'
        self.json_header['cookie'] = 'uc_token=e957c609b1554018ae97fe1dc86e9cf1'

        url = self.host + '/sysback/supplyskurel/getSupplySkuRelList?menuId=291&buttonId=133'
        data = {"nowPage":1,"pageShow":1,"supplyCode":"","supplyName":"","searchParam":"[{\"name\":\"productName_s\",\"value\":\"\"},{\"name\":\"spuNo_s\",\"value\":\"\"},{\"name\":\"skuNo_s\",\"value\":\"\"},{\"name\":\"isPurchaseMultiUnit_s\",\"value\":\"2\"},{\"name\":\"uuidNotInListStr_s\",\"value\":\"\"},{\"name\":\"uuidListStr_s\",\"value\":\"\"}]","isQueryRel":False}
        try:
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '批量修改进价，查询sku请求失败\nurl:{}\ndata:{}\nexception:{}'.format(url, data, e)

        assert res['retStatus'] == '1', '批量修改进价，查询sku返回失败{}'.format(error_temp.format(url, data, res))

        totalNum = res['retData']['totalNum']
        page = int(totalNum / 1000)
        data['pageShow'] = 1000
        data['nowPage'] = random.randint(1, page)

        try:
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '批量修改进价，查询sku请求失败{}'.format(excep_temp.format(url, data, e))

        assert res['retStatus'] == '1', '批量修改进价，查询sku返回失败{}'.format(error_temp.format(url, data, res))
        rel = random.sample(res['retData']['results'], 500)

        ret_result = []
        for i in rel:
            temp = []
            temp.append(i['supplyUuid'])
            temp.append(i['skuNo'])
            ret_result.append(temp)
        print('获取成功')
        return ret_result

    # 获取  0供应商-1sku-2城市-3进价类型-4加价类型-5进价-6运费比例-7包装比例-8加工比例-9返利比例-10成本价, 进价类型 1 全国统一  2 区域     加价类型  1金额  2比例   是否主供  1是 2否
    def getSupplySkuCityPrice(self, supplySku_500):
        url = self.host + '/sysback/supplyareaprice/getListBySkuNos?menuId=291&buttonId=133'
        data = {"skuNos":[],"supplyCodes":[]}
        skuNos = []
        supplyCodes = []
        for i in supplySku_500:
            supplyCodes.append(i[0])
            skuNos.append(i[1])
        data['skuNos'] = skuNos
        data['supplyCodes'] = supplyCodes
        try:
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '批量修改进价, 关联商品请求报错{}'.format(excep_temp.format(url, data, e))
        assert res['retStatus'] == '1', '批量修改进价, 关联商品报错{}'.format(error_temp.format(url, data, res))
        print('商品关联成功')
        priceInfo = []
        allInfo = []
        for i in res['retData']:
            temp = []
            temp.append(i['supplyUuid'])
            temp.append(i['skuNo'])
            temp.append(i['templateCityUuid'])
            temp.append(i['purchasePriceType'])
            temp.append(i['addPriceType'])
            temp.append(i['mainPurchasePrice'])
            if i['freightRatio'] == None:
                temp.append(0)
            else:
                temp.append(i['freightRatio'])

            if i['packRatio'] == None:
                temp.append(0)
            else:
                temp.append(i['packRatio'])

            if i['processChargesRatio'] == None:
                temp.append(0)
            else:
                temp.append(i['processChargesRatio'])

            if i['rebateRatio'] == None:
                temp.append(0)
            else:
                temp.append(i['rebateRatio'])

            temp.append(i['mainUnitCostPrice'])

            priceInfo.append(temp)
            allInfo.append(i)
        print('商品信息获取成功')
        return priceInfo, allInfo

    # 修改进价 + 1, 暂存，提交   0供应商-1sku-2城市-3进价类型-4加价类型-5进价-6运费比例-7包装比例-8加工比例-9返利比例-10成本价-11进价现值-12成本价现值
    def alterPurchasePrice(self, priceInfo, allInfo):
        print('修改进价')
        url = self.host + '/sysback/supplyareaprice/batchUpdateSupplyAreaPrice?recordNo=&menuId=291&buttonId=133'
        data = []

        for i in range(len(allInfo)):
            purchase = (priceInfo[i][5]*100 + 100) / 100
            if priceInfo[i][4] == '1':
                cost = (purchase*100 + priceInfo[i][6]*100 + priceInfo[i][7]*100 + priceInfo[i][8]*100 - priceInfo[i][9]*100) / 100
            else:
                cost = ((purchase*100*priceInfo[i][6]*100 + purchase*100*priceInfo[i][7]*100 + purchase*100*priceInfo[i][8]*100 - purchase*100*priceInfo[i][9]*100) / 100 + purchase*100) / 100

            priceInfo[i].append(purchase)
            priceInfo[i].append(cost)

            allInfo[i]['mainPurchasePriceUpdate'] = purchase   # 现进价
            allInfo[i]['mainPurchasePriceFloatRadio'] = round((purchase - priceInfo[i][5]) / priceInfo[i][5], 2)   # 进价浮动比例
            allInfo[i]['mainUnitCostPriceUpdate'] = cost   # 现成本价
            allInfo[i]['mainUnitCostFloatPrice'] = round((cost - priceInfo[i][10]) / priceInfo[i][10], 2)   # 成本价浮动比例

            data.append(allInfo[i])

        # 暂存
        try:
            res = requests.post(url, headers = self.json_header, json = data).json()
            print(data[0]['mainPurchasePriceFloatRadio'])
        except Exception as e:
            assert False, '修改进价暂存请求失败{}'.format(excep_temp.format(url, data, e))

        assert res['retStatus'] == '1', '修改进价暂存返回失败{}'.format(error_temp.format(url, data, res))
        recordNo = res['retData']['recordNo']
        print('暂存成功')

        # 提交
        url = self.host + '/sysback/supplyareaprice/commitSupplyPrice?recordNo={}&menuId=270&buttonId=2'.format(recordNo)
        data = {}
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '修改进价提交请求失败{}'.format(excep_temp.format(url, data, e))
        assert res['retStatus'] == '1', '修改进价提交返回失败{}'.format(error_temp.format(url, data, res))
        print('提交成功')
        return priceInfo, recordNo

    # 检查审核通过
    def viewStatus(self, recordNo):
        url = self.host + '/sysback/product/update/getSpuByRecord/querySpuList?menuId=270&buttonId=2'
        data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"recordNo\",\"value\":\"" + recordNo + "\"},{\"name\":\"pusherName\",\"value\":\"\"},{\"name\":\"pusherDeptName\",\"value\":\"\"},{\"name\":\"pushTime\",\"value\":\"\"},{\"name\":\"commitType\",\"value\":\"\"},{\"name\":\"commitState\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"Like\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"recordNo_q\",\"value\":\"Like\"},{\"name\":\"pusherName_q\",\"value\":\"Like\"},{\"name\":\"pusherDeptName_q\",\"value\":\"Like\"},{\"name\":\"pushTime_q\",\"value\":\"RightLike\"},{\"name\":\"commitType_q\",\"value\":\"IN\"},{\"name\":\"commitState_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
        try:
            res = requests.post(url, headers = self.json_header, json = data).json()
        except:
            return False

        if res['retData']['results'][0]['commitState'] == 'OK':
            return True
        else:
            return False

    # 对比数据, 提交之后判断2分钟，如果状态没变过来，认为审批失败
    def compareData(self, exp_priceInfo, recordNo):
        url = self.host + '/sysback/supplyareaprice/getUpdateDetailByRecordNo?recordNo={}&menuId=270&buttonId=2'.format(recordNo)
        data = {}
        try:
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '查询进价单据请求失败\nurl:{}\n单据:{}\nexc:{}'.format(url, recordNo, e)

        assert res['retStatus'] == '1', '查询进价单据返回失败\nurl:{}\n单据:{}\nres:{}'.format(url, recordNo, res)
        # 构建字典  供应商+sku+城市:进价原值、进价现值、成本价原值、成本价现值
        show_info = dict()
        show_key = set()
        for i in res['retData']['listDetail']:
            key = '{},{},{}'.format(i['supplyUuid'], i['skuNo'], i['templateCityUuid'])
            temp = []
            temp.append(i['mainPurchasePrice'])
            temp.append(i['mainPurchasePriceUpdate'])
            temp.append(i['mainUnitCostPrice'])
            temp.append(i['mainUnitCostPriceUpdate'])
            show_info[key] = temp
            show_key.add(key)
        # 构建字典
        exp_info = dict()
        exp_key = set()
        for i in exp_priceInfo:
            pass


    # 大量修改进价
    def alterCostPrice(self):
        supplySku_500 = self.getSupplySku_500()
        priceInfo, allInfo = self.getSupplySkuCityPrice(supplySku_500)
        exp_priceInfo, recordNo = self.alterPurchasePrice(priceInfo, allInfo)

        t = time.time() + 120
        flag = False
        while time.time() < t:
            if self.viewStatus(recordNo):
                flag = True
                break
            time.sleep(2)

        if flag == False:
            assert False, '修改进价单据审核失败, {}'.format(recordNo)

        self.compareData(exp_priceInfo, recordNo)




class Test(alterCosePrice):
    # 参照比例
    def templateRate(self):

        import xlrd
        work = xlrd.open_workbook('参照比例配置.xlsx')
        sheet = work.sheet_by_name('表头')
        temlate_rel = []
        for i in range(1, sheet.nrows):
            temp = []
            temp.append(sheet.cell_value(i, 2))
            temp.append(sheet.cell_value(i, 7))
            temp.append(round(sheet.cell_value(i, 11), 3))
            temlate_rel.append(temp)

        url = self.host + '/sysback/supplyinfopriceratio/getPriceRatioByAreaCode?menuId=239&buttonId=2'
        error_req = []
        assert_word = ''

        for i in temlate_rel:
            data = [{"saleCityUuid":"{}".format(i[0]),"templateCityUuid":"{}".format(i[1])}]
            try:
                res = requests.post(url, headers = self.json_header, json=data).json()
            except:
                data[0]['exp'] = i[2]
                error_req.append(data)
                continue
            try:
                assert res['retStatus'] == '1', '获取参照城市比例失败\nurl:{}\ndata:{}\nres:{}'.format(url, data, res)
            except Exception as e:
                assert_word += str(e) + '\n'

            try:
                assert float(res['retData'][0]['costPriceRatio']) == i[2], '{}, 实际:{}, 系统:{} 接口参照比例错误'.format(data, i[2], float(res['retData'][0]['costPriceRatio']))
            except Exception as e:
                assert_word += str(e) + '\n'

        if error_req != []:
            for data in error_req:
                exp = data[0]['exp']
                del data[0]['exp']
                try:
                    res = requests.post(url, headers = self.json_header, json=data).json()
                except:
                    assert_word += '请求失败, data:{}'.format(data)
                    continue
                else:
                    try:
                        assert res['retStatus'] == '1', '获取参照城市比例失败\nurl:{}\ndata:{}\nres:{}'.format(url, data, res)
                    except Exception as e:
                        assert_word += str(e) + '\n'

                    try:
                        assert float(res['retData'][0]['costPriceRatio']) == exp, '{}, 实际:{}, 系统:{} 接口参照比例错误'.format(data, exp, float(res['retData'][0]['costPriceRatio']))
                    except Exception as e:
                        assert_word += str(e) + '\n'

        if assert_word != '':
            assert False, '自动校验参照比例异常\n' + assert_word



    def run(self):
        print('\n*************************************************')
        print('校验参照比例')
        # self.templateRate()

        print('\n*************************************************')
        print('大量修改进价')
        self.alterCostPrice()


Test().run()