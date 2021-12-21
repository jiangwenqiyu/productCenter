from environmentConfig import LoginInfo
import requests
import random
import time
import json


excep_temp = '\nurl:{}\ndata:{}\nexception:{}'
error_temp = '\nurl:{}\ndata:{}\nres:{}'
# 查询售价单据信息
class viewSalePrice(LoginInfo):
    # 创建数据字典   sku-销售省:成本价    修改进价单据中，所有被影响到的主供城市
    def getSupplySkuCityInfo(self, info):
        print('获取主供城市，成本变动的数据字典')
        # 先把数据去重，得到供应商-sku，然后在查询信息
        query_condition = set()
        for i in info:
            w = '{},{}'.format(i[0], i[1])
            query_condition.add(w)

        # 查询供应商-sku-销售省-被参照城市-成本比例-成本（只看是主供的）
        print('供应商-sku维度,查询所有的省信息')
        url = self.host + '/sysback/supplyarea/getSupplySaleAreaProudctListInner?menuId=281&buttonId=2'
        supplyInfo = []
        for rel in query_condition:
            temp = []
            a = rel.split(',')
            supply = a[0]
            skuNo = a[1]
            data = {"nowPage":1,"pageShow":50,"searchParam":"[{\"name\":\"categoryName\",\"value\":\"\"},{\"name\":\"productName\",\"value\":\"\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"skuNo\",\"value\":\"" + skuNo + "\"},{\"name\":\"supplierCode\",\"value\":\"" + supply + "\"},{\"name\":\"supplierName\",\"value\":\"\"},{\"name\":\"saleAreaName\",\"value\":\"\"},{\"name\":\"saleProvinceName\",\"value\":\"\"},{\"name\":\"categoryName_q\",\"value\":\"Like\"},{\"name\":\"productName_q\",\"value\":\"Like\"},{\"name\":\"brandName_q\",\"value\":\"Like\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"skuNo_q\",\"value\":\"EQ\"},{\"name\":\"supplierCode_q\",\"value\":\"EQ\"},{\"name\":\"supplierName_q\",\"value\":\"Like\"},{\"name\":\"saleAreaName_q\",\"value\":\"Like\"},{\"name\":\"saleProvinceName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
            flag = False
            for i in range(10):
                try:
                    logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
                    with open('reqLog.txt', 'a') as f:
                        f.write(logInfo)
                    res = requests.post(url, headers = self.json_header, json = data).json()
                    assert res['retStatus'] == '1' and len(res['retData']['results']) != 0
                    flag = True
                    break
                except:
                    time.sleep(1.5)
                    continue
            assert flag, '查询供货信息获取数据失败\nrel:{}'.format(rel)
            for i in res['retData']['results']:
                if i['isMainSupply'] == '1':
                    saleProvince = i['saleProvinceUuid']
                    beTemplatedCity = i['templateCityUuid']
                    tempRate = float(i['costPriceRatio'])
                    cost = i['mainUnitCostPrice']
                    temp.append(supply)
                    temp.append(skuNo)
                    temp.append(saleProvince)
                    temp.append(beTemplatedCity)
                    temp.append(tempRate)
                    temp.append(cost)
            supplyInfo.append(temp)
        print('查询成功')

        # 主供中，供应商、sku、被参照城市，与修改的一致，那么这个销售城市，就是会被影响的售价城市
        print('获取被影响的主供城市, 以及按照比例计算后的成本价')
        rel = dict()
        try:
            for i in supplyInfo:
                for x in info:
                    if i[0] == x[0] and i[1] == x[1] and i[3] == x[2]:  # 供应商、sku相同,且供货信息的被参照城市，等于修改进价的城市
                        # 按照当前参照比例，计算应该的成本价
                        currentCost = ((i[4] * 100) * (x[12] * 100)) / 10000
                        # 构建数据字典  sku-销售省:成本价
                        key = '{},{}'.format(i[1], i[2])
                        rel[key] = currentCost
        except Exception as e:
            assert False, '发生异常, {}\n{}\n{}'.format(e,supplyInfo, info)

        print('获取成功！')
        return rel


    # sku-主省:加价类型,现金加价率,分销差率,售价加价率
    def getSalePriceInfo(self, info):
        print('根据sku获取售价的数据字典')
        url = self.host + '/sysback/salepriceskuupdate/getBySkuNos?menuId=299&buttonId=133'
        data = []
        sku_quchong = set()
        for i in info:
            sku_quchong.add(i[1])
        data = list(sku_quchong)
        flag = False
        for i in range(10):
            try:
                logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
                with open('reqLog.txt', 'a') as f:
                    f.write(logInfo)
                res = requests.post(url, headers = self.json_header, json = data).json()
                assert res['retStatus'] == '1', '售价关联sku失败\nurl:{}\ndata:{}\nres:{}'.format(url,data,res)
                flag = True
                break
            except Exception as e:
                print(e)
        assert flag, '售价关联sku失败\nurl:{}\ndata:{}\nres:{}'.format(url,data,res)

        # 构建数据字典
        rel = dict()
        for i in res['retData']['t']:
            key = '{},{}'.format(i['skuNo'], i['provinceCode'])
            value = '{},{},{},{}'.format(i['oldInput']['addPriceType'],i['oldInput']['cashAddRateOrMoney'],i['oldInput']['distribCashDiffRateOrMoney'],i['oldInput']['saleAddRateOrMoney'])
            rel[key] = value

        print('获取成功')
        return rel


    # 取交集，若存在，则有售价单据，若不存在，则不应有售价单据    返回期望的  sku-城市:成本价,现金价,分销价,售价
    def judgeRecord(self, jinjia, shoujia):
        print('判断是否应该生成售价单据')
        jin = set()
        for i in jinjia:
            jin.add(i)

        sale = set()
        for i in shoujia:
            sale.add(i)

        if jin & sale != set():  # 返回期望的  sku-城市:成本价,现金价,分销价,售价
            print('应该生成售价单据')
            exp_data = dict()
            jiaoji = jin & sale
            for i in jiaoji:
                temp = dict()
                cost = jinjia[i]
                obj = shoujia[i].split(',')
                addType = float(obj[0])
                cashRate = float(obj[1])
                distributeRate = float(obj[2])
                saleRate = float(obj[3])
                # print(cost, cashRate, distributeRate, saleRate)
                # print(type(cost), type(cashRate), type(distributeRate), type(saleRate))
                if addType == '1':  # 金额
                    cash = (cost*100 + cashRate*100) / 100
                    distribute = (cash * 100 - distribute*100) / 100
                    sale = (cost*100 + saleRate*100) / 100
                else:                # 比例
                    cash = (cost * 100 + (cost*100*(cashRate*100))/100) / 100
                    distribute = ((cash * 100) * (distributeRate * 100)) / 10000
                    sale = (cost*100 + ((cost*100) * (saleRate*100))/100) / 100

                exp_data[i] = '{},{},{},{}'.format(cost, cash, distribute, sale)
            print('进价主供城市与售价主城市的交集字典,构建成功')
            return True, exp_data       # 应该生成单据

        else:

            print('无需生成售价单据')
            return False, ''      # 不应生成单据

    # 查找单据
    def findRecord(self, status, record):

        url = self.host + '/sysback/product/update/getSpuByRecord/querySpuList?menuId=270&buttonId=2'
        record = record + "_1"
        data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"recordNo\",\"value\":\"" + record + "\"},{\"name\":\"pusherName\",\"value\":\"\"},{\"name\":\"pusherDeptName\",\"value\":\"\"},{\"name\":\"pushTime\",\"value\":\"\"},{\"name\":\"commitType\",\"value\":\"\"},{\"name\":\"commitState\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"Like\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"recordNo_q\",\"value\":\"Like\"},{\"name\":\"pusherName_q\",\"value\":\"Like\"},{\"name\":\"pusherDeptName_q\",\"value\":\"Like\"},{\"name\":\"pushTime_q\",\"value\":\"RightLike\"},{\"name\":\"commitType_q\",\"value\":\"IN\"},{\"name\":\"commitState_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}

        if status:
            print('开始查找售价单据')
            t = time.time() + 600

            while time.time() < t:
                try:
                    logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
                    with open('reqLog.txt', 'a') as f:
                        f.write(logInfo)
                    res = requests.post(url, headers = self.json_header, json = data).json()
                except Exception as e:
                    continue

                if len(res['retData']['results']) != 0:
                    flag = True
                    print('查询售价单据成功')
                    return True                   # 应该生成，并且已经查到了
            print('查询失败')
            assert False, '超过10分钟没有查询到售价单据\n进价单据号:{}'.format(record[0:-2])   # 该生成没生成

        else:
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json = data).json()
            if len(res['retData']['results']) != 0:
                assert False, '进价单据中没有符合的数据，不应生成售价单据, 但是却生成了\n单据号:{}'.format(record)    # 不该生成但是生成了
            else:
                return False   # 不该生成，实际也没生成





    # 对比售价
    def compareSalePrice(self, exp_data, record):
        print('开始验证售价单据')
        record = record + '_1'
        url = self.host + '/sysback/salepriceskuupdate/getAllByBillUuid?isSaleMultiUnit=2&billUuid={}&menuId=270&buttonId=2'.format(record)
        data = {"billUuid":record}
        try:
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '查询自动生成的售价单据请求失败\n单据号:{}'.format(record)
        assert res['retStatus'] == '1', '查询自动生成的售价单据返回失败\n单据号:{}'.format(record)

        # 获取单据里的数据字典  sku-城市:成本价,现金价,分销价,售价
        fact = dict()
        fact_key = set()
        for i in res['retData']['recordMainList']:
            for x in i['recordDetailList']:
                obj = json.loads(x['recordContent'])
                key = '{},{}'.format(obj['nowInput']['skuNo'], obj['nowInput']['provinceCode'])
                fact_key.add(key)
                cost = obj['nowInput']['mainUnitPrice']
                cash = obj['nowInput']['cashPrice']
                dis = obj['nowInput']['cashDistribMoney']
                sale = obj['nowInput']['salePrice']
                fact[key] = '{},{},{},{}'.format(cost, cash, dis, sale)

        exp_key = set()
        for key in exp_data:
            exp_key.add(key)

        jiaoji_key = fact_key & exp_key
        assert jiaoji_key != set(), '单据与预期的数据没有交集\n单据:{}\n预期的:{}'.format(record, exp_key)

        for key in jiaoji_key:
            fact_obj = fact[key].split(',')
            exp_obj = exp_data[key].split(',')
            assert float(fact_obj[0]) == float(exp_obj[0]), '判断自动生成的售价单据, 成本价不对\n单据:{}\n期望值:{}\n单据值:{}'.format(record, float(exp_obj[0]), float(fact_obj[0]))
            assert float(fact_obj[1]) == float(exp_obj[1]), '判断自动生成的售价单据, 现金价不对\n单据:{}\n期望值:{}\n单据值:{}'.format(record, float(exp_obj[1]), float(fact_obj[1]))
            assert float(fact_obj[2]) == float(exp_obj[2]), '判断自动生成的售价单据, 分销价不对\n单据:{}\n期望值:{}\n单据值:{}'.format(record, float(exp_obj[2]), float(fact_obj[2]))
            assert float(fact_obj[3]) == float(exp_obj[3]), '判断自动生成的售价单据, 售价不对\n单据:{}\n期望值:{}\n单据值:{}'.format(record, float(exp_obj[3]), float(fact_obj[3]))
        print('验证完成')



    # 接收进价的单据信息
    def viewInfo(self, info, record):
        jinjia = self.getSupplySkuCityInfo(info)
        shoujia = self.getSalePriceInfo(info)
        status, exp_data = self.judgeRecord(jinjia, shoujia)
        isHaveRecord = self.findRecord(status, record)   # 查找有没有售价单据
        if isHaveRecord:
            self.compareSalePrice(exp_data, record)
        else:
            print('没有售价单据,无需验证')
            return

# 修改进价
class alterCosePrice(viewSalePrice):
    # 关联商品获取  供应商-sku，500个
    def getSupplySku_500(self):
        print('查询500个商品')
        # self.host = 'http://product.t4.xinfangsheng.com'
        # self.json_header['cookie'] = 'uc_token=e957c609b1554018ae97fe1dc86e9cf1'

        url = self.host + '/sysback/supplyskurel/getSupplySkuRelList?menuId=291&buttonId=133'
        data = {"nowPage":1,"pageShow":1,"supplyCode":"","supplyName":"","searchParam":"[{\"name\":\"productName_s\",\"value\":\"\"},{\"name\":\"spuNo_s\",\"value\":\"\"},{\"name\":\"skuNo_s\",\"value\":\"\"},{\"name\":\"isPurchaseMultiUnit_s\",\"value\":\"2\"},{\"name\":\"uuidNotInListStr_s\",\"value\":\"\"},{\"name\":\"uuidListStr_s\",\"value\":\"\"}]","isQueryRel":False}
        try:
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '批量修改进价，查询sku请求失败\nurl:{}\ndata:{}\nexception:{}'.format(url, data, e)

        assert res['retStatus'] == '1', '批量修改进价，首次查询sku返回失败{}'.format(error_temp.format(url, data, res))

        totalNum = res['retData']['totalNum']
        page = int(totalNum / 1000)
        data['pageShow'] = 1000
        data['nowPage'] = random.randint(1, page)

        try:
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '批量修改进价，查询sku请求失败{}'.format(excep_temp.format(url, data, e))

        assert res['retStatus'] == '1', '批量修改进价，二次查询sku返回失败{}'.format(error_temp.format(url, data, res))
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
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
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
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '修改进价暂存请求失败{}'.format(excep_temp.format(url, data, e))

        assert res['retStatus'] == '1', '修改进价暂存返回失败{}'.format(error_temp.format(url, data, res))
        recordNo = res['retData']['recordNo']
        print('暂存成功, {}'.format(recordNo))

        # 提交
        print('正在提交')
        url = self.host + '/sysback/supplyareaprice/commitSupplyPrice?recordNo={}&menuId=270&buttonId=2'.format(recordNo)
        data = {}
        try:
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '修改进价提交请求失败{}'.format(excep_temp.format(url, data, e))
        assert res['retStatus'] == '1', '修改进价提交返回失败{}\n单据号:{}'.format(error_temp.format(url, data, res), recordNo)
        print('提交成功')
        return priceInfo, recordNo

    # 检查审核通过
    def viewStatus(self, recordNo):
        url = self.host + '/sysback/product/update/getSpuByRecord/querySpuList?menuId=270&buttonId=2'
        data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"recordNo\",\"value\":\"" + recordNo + "\"},{\"name\":\"pusherName\",\"value\":\"\"},{\"name\":\"pusherDeptName\",\"value\":\"\"},{\"name\":\"pushTime\",\"value\":\"\"},{\"name\":\"commitType\",\"value\":\"\"},{\"name\":\"commitState\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"Like\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"recordNo_q\",\"value\":\"Like\"},{\"name\":\"pusherName_q\",\"value\":\"Like\"},{\"name\":\"pusherDeptName_q\",\"value\":\"Like\"},{\"name\":\"pushTime_q\",\"value\":\"RightLike\"},{\"name\":\"commitType_q\",\"value\":\"IN\"},{\"name\":\"commitState_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
        try:
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json = data).json()
        except:
            return False

        if res['retData']['results'][0]['commitState'] == 'OK':
            print('审核通过！')
            return True
        else:
            return False

    # 对比数据, 提交之后判断2分钟，如果状态没变过来，认为审批失败
    def compareData(self, exp_priceInfo, recordNo):
        print('开始比对表单数据')
        url = self.host + '/sysback/supplyareaprice/getUpdateDetailByRecordNo?recordNo={}&menuId=270&buttonId=2'.format(recordNo)
        data = {}
        try:
            logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
            with open('reqLog.txt', 'a') as f:
                f.write(logInfo)
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '查询进价单据请求失败\nurl:{}\n单据:{}\nexc:{}'.format(url, recordNo, e)

        assert res['retStatus'] == '1', '查询进价单据返回失败\nurl:{}\n单据:{}\nres:{}'.format(url, recordNo, res)
        print('表单数据获取成功, 开始构建数据字典')
        # 构建字典  供应商+sku+城市:进价原值、进价现值、成本价原值、成本价现值
        show_info = dict()
        show_key = set()
        sk = []
        for i in res['retData']['listDetail']:
            key = '{},{},{}'.format(i['supplyUuid'], i['skuNo'], i['templateCityUuid'])
            temp = []
            temp.append(i['mainPurchasePrice'])
            temp.append(i['mainPurchasePriceUpdate'])
            temp.append(i['mainUnitCostPrice'])
            temp.append(i['mainUnitCostPriceUpdate'])
            show_info[key] = temp
            show_key.add(key)
            sk.append(key)
        # 构建字典
        exp_info = dict()
        exp_key = set()
        for i in exp_priceInfo:
            key = '{},{},{}'.format(i[0], i[1], i[2])
            temp = []
            temp.append(i[5])
            temp.append(i[11])
            temp.append(i[10])
            temp.append(i[12])
            exp_info[key] = temp
            exp_key.add(key)

        # 判断行数
        if len(show_key) != len(res['retData']['listDetail']):
            for k in show_key:
                for t in range(len(sk)):
                    if k == sk[t]:
                        del sk[t]
                        break

            assert len(show_key) == len(res['retData']['listDetail']), '进价单据中，按照供应商-sku-城市维度,存在重复行数据\n单据:{}\n重复的内容:{}'.format(recordNo, sk)

        assert show_key ^ exp_key == set(), '进价单据，提交时候的数据行数，与查看单据的行数，不一致\n单据:{}\n提交-单据:{}\n单据-提交:{}'.format(recordNo, exp_key-show_key, show_key-exp_key)

        # 对比进价原值、现值
        for key in show_key:
            fact = show_info[key]
            exp = exp_info[key]
            assert fact[0] == exp[0], '进价单据,进价原值,与提交时候的原值不一致\n单据:{}\n定位行:{}\n提交原值:{}\n单据原值:{}'.format(recordNo, key, exp[0], fact[0])
            assert fact[1] == exp[1], '进价单据,进价现值,与提交时候的现值不一致\n单据:{}\n定位行:{}\n提交现值:{}\n单据现值:{}'.format(recordNo, key, exp[1], fact[1])
            assert fact[2] == exp[2], '进价单据,成本价原值,与提交时候的原值不一致\n单据:{}\n定位行:{}\n提交原值:{}\n单据原值:{}'.format(recordNo, key, exp[2], fact[2])
            assert fact[3] == exp[3], '进价单据,成本价现值,与提交时候的现值不一致\n单据:{}\n定位行:{}\n提交现值:{}\n单据现值:{}'.format(recordNo, key, exp[3], fact[3])
        print('表单数据比对结束, 未发现异常')


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

        assert flag, '修改进价单据审核失败, {}'.format(recordNo)

        self.compareData(exp_priceInfo, recordNo)


        # 查询售价单据
        print('查看自动生成的售价单据')
        self.viewInfo(exp_priceInfo, recordNo)

        # 返回单据的信息,给判断售价用
        # return exp_priceInfo, recordNo


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
                logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
                with open('reqLog.txt', 'a') as f:
                    f.write(logInfo)
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
                    logInfo = '*****************************************\n修改进价单点测试:{}\n{}\n'.format(url, data)
                    with open('reqLog.txt', 'a') as f:
                        f.write(logInfo)
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
        print('批量修改进价')
        info, record = self.alterCostPrice()




# Test().run()