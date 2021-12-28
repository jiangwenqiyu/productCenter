from environmentConfig import LoginInfo
import requests




class changeCostPrice(LoginInfo):

    def changeCost(self, info):
        # 查询商品
        url = self.host + '/sysback/supplyskurel/getSupplySkuRelList?menuId=291&buttonId=133'
        if info['isPurchaseMultiUnit'] == '1':
            data = {"nowPage":1,"pageShow":10,"supplyCode":"","supplyName":"","searchParam":"[{\"name\":\"productName_s\",\"value\":\"\"},{\"name\":\"spuNo_s\",\"value\":\"\"},{\"name\":\"skuNo_s\",\"value\":\"" + info['skuNo'] + "\"},{\"name\":\"isPurchaseMultiUnit_s\",\"value\":\"1\"},{\"name\":\"uuidNotInListStr_s\",\"value\":\"\"},{\"name\":\"uuidListStr_s\",\"value\":\"\"}]","isQueryRel":False}
        else:
            data = {"nowPage":1,"pageShow":10,"supplyCode":"","supplyName":"","searchParam":"[{\"name\":\"productName_s\",\"value\":\"\"},{\"name\":\"spuNo_s\",\"value\":\"\"},{\"name\":\"skuNo_s\",\"value\":\"" + info['skuNo'] + "\"},{\"name\":\"isPurchaseMultiUnit_s\",\"value\":\"2\"},{\"name\":\"uuidNotInListStr_s\",\"value\":\"\"},{\"name\":\"uuidListStr_s\",\"value\":\"\"}]","isQueryRel":False}

        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '修改进价查询商品失败, sku:{}\nurl:{}\ndata:{}'.format(info['skuNo'], url, data)

        assert res['retStatus'] == '1', '修改进价查询商品失败, sku:{}\nurl:{}\ndata:{}\nres:{}'.format(self.info['skuNo'], url, data, res)
        print('查询商品成功')

        # 关联带出
        url = self.host + '/sysback/supplyareaprice/getListBySkuNos?menuId=291&buttonId=133'
        data = {"skuNos":[info['skuNo']],"supplyCodes":["11297"]}
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '修改进价关联商品失败, sku:{}\nurl:{}\ndata:{}'.format(info['skuNo'], url, data)

        assert res['retStatus'] == '1', '修改进价关联商品，带出数据失败, sku:{}\nurl:{}\ndata:{}\nres:{}'.format(info['skuNo'], url, data, res)

        if info['purchasePriceType'] == '1':
            assert len(res['retData']) == 1,  '修改进价，统一进价，展示的应该是一行。spu:{}\nexp:{}\nfact:{}'.format(info['spuNo'],1, len(res['retData']))
        else:
            assert len(res['retData']) == len(info['tempSelf']), '修改进价，区域进价，展示的行数不对。spu:{}\nexp:{}\nfact:{}'.format(info['spuNo'],len(info['tempSelf']),len(res['retData']))
        print('带出商品成功')

        # 验证基本数据



class changeSalePrice(LoginInfo):
    pass


class changePrice(changeCostPrice, changeSalePrice):
    def run(self, info):
        return
        print('\n*************************************************')
        print('修改进价')




        print('\n*************************************************')
        print('修改售价')





