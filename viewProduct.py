import requests
import time
import random
from random import randint, random, uniform, sample
from makeProduct import CommonFunction

class ProductManagement(CommonFunction):
    def run(self, JycList):
        self.SupplyInfoQuerry(JycList)
        self.SpuManagement(JycList)  #已完成
        self.SkuManagement(JycList)  #已完成

    def GetCalcUnit(self):
        CalcUnitList = list()
        url = self.host + '/sysback/unit/baseQueryList?menuId=253&buttonId=148'
        data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"unitName\",\"value\":\"\"},{\"name\":\"unitName_q\",\"value\":\"Like\"}]"}
        res = requests.post(url, headers=self.json_header, json=data).json()
        data['pageShow'] = res['retData']['totalNum']
        try:
            res = requests.post(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        for i in res['retData']['results']:
            CalcUnitList.append(i['unitName'])

        CalcUnit = sample(CalcUnitList, 1)[0]
        # print(CalcUnit)
        return CalcUnit
        
    def SpuManagement(self, JycList):
        print('开始验证SPU管理')
        #查询创建得SPU是否存在
        endTime = time.time()+90
        while True:
            if time.time() < endTime:
                url = self.host+'/sysback/finish/spu/mgr/getSpuList?menuId=252&buttonId=2'
                data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\""+JycList['spuNo']+"\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
                try:
                    res = requests.post(url, headers=self.json_header, json=data).json()
                except Exception as e:
                    assert False, '接口请求失败, {}\n{}'.format(url, e)
                # print('==========================')
                # print(JycList['spuNo'])
                # print(res)
                time.sleep(3)
                if res['retData']['results'] != []:
                    assert res['retData']['results'][0]['spuNo'] == JycList['spuNo'], 'url : {} \n 入参 : {} \n 结果 : {} \n 查询Spu信息失败 \n SpunNo: {}'.format(url, data, res['retMessage'], JycList['spuNo'])
                    print('查询成功\nSpuNo: {} '.format(JycList['spuNo']))
                    break
            else:
                # print('请求失败,请检查spu准入是否完成 \nspuNo:{} '.format(JycList['spuNo']))
                assert False, '查询失败,请检查spu准入是否完成! \nspuNo:{} '.format(JycList['spuNo'])

        # 验证是否能够修改Spu, 从SPU查看页面点击修改
        url = self.host + '/sysback/spu/query/checkPerm?spuNo={}&menuId=252&buttonId=148'.format(JycList['spuNo'])
        data = {"spuNo": "{}".format(JycList['spuNo'])}
        try:
            res = requests.post(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '成功', 'url : {} \n 入参 : {} \n 结果 : {} \n 修改Spu失败'.format(url, data, res['retMessage'])

        ######################################## 后续等姜完善后再进行调试 ###########################
        # 修改Spu基本信息
        url = self.host + '/sysback/update/product/basicinfo/queryBasicInfoListFromSpu?menuId=252&buttonId=148'
        data = {'productKey':"{}".format(JycList['productUuid'])}
        try:
            res = requests.post(url, headers=self.form_header, data = data ).json()
        except Exception as e:
            assert False, '修改基本信息，接口请求失败\nurl:{}\ndata:{}\nexception:{}'.format(url, data, e)

        assert res['retStatus'] == '1', '修改基本信息，获取数据失败\nurl:{}\ndata:{}\nres:{}'.format(url, data, res)
        print('修改基本信息，获取数据成功')
        # for i in res['retData'][0]['attrList']:
        #     assert i['attrName'] == '', '' 啊
        # 判断Spu基本信息是否正确
        assert res['retData'][0]['attrList'] !=[],'url : {} \n 入参 : {} \n 结果 : {} \n 基础属性获取失败'.format(url , data , res['retMessage'])
        assert res['retData'][0]['spuNo'] == JycList['spuNo'],'spuNO 不正确，不符合创建时的 Spu, 创建时的 Spu : {}, 修改时的 Spu : {}'.format(JycList['spuNo'], res['redata'][0]['spuNo'])
        assert res['retData'][0]['productUuid'] == JycList['productUuid'] ,'productUuid 不正确，不符合创建时的 productUuid, 创建时的 productUuid : {}, 修改时的 productUuid : {}'.format(JycList['productUuid'], res['redata'][0]['productUuid'])
        # # 循环对比 属性原值和页面获取的值是否一致 ？？？ 需要后续修改
        # for ii in  res['retData'][0]['attrList']:
        #     assert ii['valueName'] == self.getString()[2] ,'原值 不正确，不符合创建时的 原值, 创建时的 原值 : {}, 修改时的 原值 : {}'.format(self.getString()[2],res['redata'][0]['valueName'])
        #
        # 修改基本信息属性值
        for i in res['retData'][0]['attrList']:
            # print (i)
            if i['attrType'] == '01':
                i['valueNameUpdate'] = self.getString(7)
                print('获取随机字符串成功')

            if i['attrType'] == '02':
                # print (i['allValueOptions'][random.randint(0,len(i['allValueOptions'])-1)]['optionHtml'])
                i['valueNameUpdate'] = i['allValueOptions'][random.randint(0, len(i['allValueOptions'])-1)]['optionHtml']
        NotspecList = res['retData'][0]['attrList']

        # 修改Spu信息-暂存
        url = self.host + '/sysback/update/product/basicinfo/saveBasicInfo?menuId=252&buttonId=148'
        data = {"inputList": [{"productKey": ""+JycList['productUuid']+"", "notSpecList":NotspecList}]}
        try:
            res = requests.post(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        # 判断是否有单据暂存，如果有就获取单据号重新请求
        Record = res['retData']['recordNo']
        newdata = {"recordNo": ""+Record+"", "inputList": [{"productKey": ""+JycList['productUuid']+"", "notSpecList": NotspecList}]}
        try:
            res = requests.post(url, headers=self.json_header, json=newdata).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retStatus'] == '1', 'url : {} \n 入参 : {} \n 结果: {} \n 暂存失败'.format(url , data , res['retMessage'])

        # 修改Spu信息-提交
        url = self.host + '/sysback/update/product/basicinfo/commitBasicInfo?recordNo={}'.format(Record)
        data = {}
        try:
            res = requests.post(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '修改基本信息提交失败, url: {} \n ,结果: {} '.format(url, res['retMessage'])
        assert res['retData']['commitState'] == 'COMMIT', '修改基本信息提交失败, url: {} \n ,结果: {} '.format(url, res['retMessage'])

        # 验证提交Spu数据是否生效
        url = self.host + '/sysback/update/product/basicinfo/queryBasicInfoListFromSpu?menuId=252&buttonId=148' #.format(JycList['spuNo'])
        data = {"productKey": "{}".format(JycList['productUuid'])}
        try:
            res = requests.post(url, headers=self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retData'][0]['spuNo'] == JycList['spuNo'], 'spuNo 不正确 原SpuNo:{} \n 现SpuNo: {}'.format(JycList['spuNo'], res['retData']['spuNo'])
        # for i,j in res['retData'][0]['attrList'],NotspecList:
        #     print('现值: {} '.format(i['valueNameUpdate']))
        #     print('原值: {} '.format(j['valueNameUpdata']))
        # i['valueNameUpdate'] == j['valueNameUpdata']

        print('Spu查看页面详情-商品基本信息')
        url = self.host + '/sysback/finish/spu/mgr/getSpuList?menuId=252&buttonId=2'
        data = {"nowPage":1 ,"pageShow":10,"searchParam":"[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\""+ JycList['spuNo'] +"\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
        try:
            res = requests.post(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        # print(res)
        assert res['retMessage'] == '', 'url : {} \n 入参 : {} \n 结果 : {} \n 获取Spu信息失败'.format(url, data, res['retMessage'])
        assert res['retData']['results'][0]['categoryPath'] != '','url : {} \n 入参 : {} \n 结果 : {} \n 缺少分类信息'.format(url , data , res['retMessage'])
        assert res['retData']['results'][0]['productName'] == JycList['productName'],'url : {} \n 入参 : {} \n 结果 : {} \n 商品名称错误 \n 原商品名称: {} \n 现商品名称: {}'.format(url, data, res['retMessage'], JycList['productName'], res['retData']['results'][0]['productName'])
        assert res['retData']['results'][0]['productTypeStr'] == JycList['productTypeStr'], 'url : {} \n 入参 : {} \n 结果 : {} \n 商品类型错误 \n 原商品名称: {} \n 现商品名称: {}'.format(url, data, res['retMessage'], JycList['productTypeStr'], res['retData']['results'][0]['productTypeStr'])
        assert res['retData']['results'][0]['brandName'] == JycList['brandName'],'url : {} \n 入参 : {} \n 结果 : {} \n 品牌信息错误 \n 原品牌名称: {} \n 现品牌名称: {} '.format(url, data, res['retMessage'], JycList['brandName'], res['retData']['results'][0]['brandName'])

        # Spu查看详情
        uUid = res['retData']['results'][0]['uuid']
        url = self.host + '/sysback/finish/spu/detail/toSpuDetailStep1?productUuid={}&menuId=252&buttonId=148'.format(uUid)
        dataa = {'productUuid': uUid}
        try:
            res = requests.post(url, headers=self.json_header, json=dataa).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)

        #品类信息
        # 执行判断原值与新增时候的值是否一致
        assert res['retMessage'] == '', 'url : {} \n 入参 : {} \n 结果 : {} \n 查询Spu信息失败'.format(url, data,res['retMessage'])
        assert res['retData']['currentCategoryStr'] != '', 'url : {} \n 入参 : {} \n 结果 : {} \n 四级分类为空\n 原四级分类 : {} ' .format(url, data, res['retMessage'],res['retData']['currentCategoryStr'])
        assert res['retData']['arch']['productTypeStr'] == JycList['productTypeStr'], 'url : {} \n 入参 : {} \n 结果 : {} \n 商品类型不正确 \n 原商品类型 : {} \n 现商品类型 : {} ' .format(url, data, res['retMessage'], JycList['productTypeStr'], res['retData']['arch']['productTypeStr'])
        assert res['retData']['arch']['brandName'] == JycList['brandName'],'url : {} \n 入参 : {} \n 结果 : {} \n 品牌不正确 \n 原商品品牌 : {} \n 现商品品牌 : {} ' .format(url, data, res['retMessage'], JycList['brandName'], res['retData']['arch']['brandName'])
        assert res['retData']['arch']['addPriceTypeStr'] == JycList['addPriceTypeStr'], 'url : {} \n 入参 : {} \n 结果 : {} \n 加价类型不正确 \n 原加价类型 : {} \n 现加价类型 : {} ' .format(url, data, res['retMessage'], JycList['addPriceTypeStr'], res['retData']['arch']['addPriceTypeStr'])
        assert res['retData']['arch']['isPurchaseMultiUnitStr'] != '' , 'url : {} \n 入参 : {} \n 结果 : {} \n 采购多计量不正确 \n 原采购多计量 : {} '.format(url, data, res['retMessage'], res['retData']['arch']['isPurchaseMultiUnitStr'])
        assert res['retData']['arch']['isSaleMultiUnitStr'] != '', 'url : {} \n 入参 : {} \n 结果 : {} \n 采销多计量不正确 \n 原采销多计量 : {}  '.format(url, data, res['retMessage'], res['retData']['arch']['isSaleMultiUnitStr'])
        assert res['retData']['arch']['mainUnitName'] == JycList['mainUnitName'], 'url : {} \n 入参 : {} \n 结果 : {} \n 主计量单位不正确 \n 原主计量单位 : {} \n 现主计量单位 : {} '.format(url, data, res['retMessage'], JycList['mainUnitName'], res['retData']['arch']['mainUnitName'])
        assert res['retData']['arch']['mainUnitDecimals'] == str(JycList['mainUnitdecimal']), 'url : {} \n 入参 : {} \n 结果 : {} \n 主计量单位小数位不正确 \n 原主计量单位小数位 : {} \n 现主计量单位小数位 : {} '.format(url, data, res['retMessage'], JycList['mainUnitdecimal'], res['retData']['arch']['mainUnitDecimals'])
        # #############################后续调整##############################
        # assert res['retData']['arch']['assistUnitName'] == '', 'url : {} \n 入参 : {} \n 结果 : {} \n 辅计量单位不正确 \n 原辅计量单位 : {} \n 现辅计量单位 : {} '.format(url, data, res['retMessage'], assistUnitName, res['retData']['arch']['assistUnitName'])
        # assert res['retData']['arch']['assistUnitDecimals'] == '', 'url : {} \n 入参 : {} \n 结果 : {} \n 辅计量单位小数位不正确 \n 原辅计量单位小数位 : {} \n 现辅计量单位小数位 : {} '.format(url, data, res['retMessage'], assistUnitDecimals, res['retData']['arch']['assistUnitDecimals'])
        # assert res['retData']['existingPackageList'][0]['saleRestrictStr'] == '', 'url : {} \n 入参 : {} \n 结果 : {} \n 销售限制类型不正确 \n 原销售限制类型 : {} \n 现销售限制类型 : {} '.format(url, data, res['retMessage'], saleRestrictStr, res['retData']['existingPackageList'][0]['saleRestrictStr'])
        # ##################################################################

        # Spu查看页面详情-销售价格信息
        url = self.host + '/sysback/salepricesku/getSalePriceByProductUuid?productUuid={}&menuId=252&buttonId=2'.format(JycList['productUuid'])
        data = {'productUuid':JycList['productUuid']}
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        # 拼接完整的品牌名称  包含厂商名称
        productName =JycList['brandName']+' '+JycList['productName']
        # 判断页面的值是否与新增时候的值一致
        assert res['retData']['salePriceTopInfoOutput']['productName'] == productName, 'url : {} \n 入参 : {} \n 结果 : {} \n 商品名称不正确 \n 原辅商品名称 : {} \n 现商品名称 : {} '.format(url, data, res['retMessage'], productName, res['retData']['salePriceTopInfoOutput']['productName'])
        # # 是否敏感后续姜传值，本期不管
        # assert res['retData']['salePriceTopInfoOutput']['isPriceSensitive'] == isPriceSensitive, 'url : {} \n 入参 : {} \n 结果 : {} \n 是否敏感不正确 \n 是否敏感原值 : {} \n 是否敏感现值 : {} '.format(url, data, res['retMessage'], isPriceSensitive, res['retData']['salePriceTopInfoOutput']['isPriceSensitive'])
        # # ##########################
        assert res['retData']['salePriceTopInfoOutput']['manageArea'] == JycList['manage_area_ch'], 'url : {} \n 入参 : {} \n 结果 : {} \n 管理区域不正确 \n 原管理区域 : {} \n 现管理区域 : {} '.format(url, data, res['retMessage'], JycList['manage_area_ch'], res['retData']['salePriceTopInfoOutput']['manageArea'])
        # 价格类型后续姜传值，本期不管
        # assert res['retData']['salePriceTopInfoOutput']['saleTypeStr'] == saleTypeStr, 'url : {} \n 入参 : {} \n 结果 : {} \n 价格类型不正确 \n 原价格类型 : {} \n 现价格类型 : {} '.format(url, data, res['retMessage'], saleTypeStr, res['retData']['salePriceTopInfoOutput']['saleTypeStr'])
        # ##########################
        # assert res['retData']['salepriceList'][0]['mainUnitPrice'] == JycList['mainUnitCostPrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 成本价不正确 \n 原成本价 : {} \n 现成本价 : {} '.format(url, data, res['retMessage'], JycList['mainUnitCostPrice'], res['retData']['salepriceList'][0]['mainUnitPrice'])
        assert res['retData']['salepriceList'][0]['salePrice'] == JycList['salePrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 售价不正确 \n 原售价 : {} \n 现售价 : {} '.format(url, data, res['retMessage'], JycList['salePrice'], res['retData']['salepriceList'][0]['salePrice'])
        # # 分销价后续姜传值，本期不管
        # assert res['retData']['salepriceList'][0]['cashDistribMoney'] == cashDistribMoney, 'url : {} \n 入参 : {} \n 结果 : {} \n 分销价不正确 \n 原分销价 : {} \n 现分销价 : {} '.format(url, data, res['retMessage'], cashDistribMoney, res['retData']['salepriceList'][0]['cashDistribMoney'])
        # # #########################
        assert res['retData']['salepriceList'][0]['cashPrice'] == JycList['cashPrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 现金价不正确 \n 原现金价 : {} \n 现现金价 : {} '.format(url, data, res['retMessage'], JycList['cashPrice'], res['retData']['salepriceList'][0]['cashPrice'])
        assert res['retData']['salepriceList'][0]['limitShowPrice'] == JycList['limitShowPrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 限制展示价不正确 \n 原限制展示价 : {} \n 现限制展示价 : {} '.format(url, data, res['retMessage'], JycList['limitShowPrice'], res['retData']['salepriceList'][0]['limitShowPrice'])
        assert res['retData']['salepriceList'][0]['limitTradePrice'] == round(JycList['limitTradePrice'],2), 'url : {} \n 入参 : {} \n 结果 : {} \n 限制交易价不正确 \n 原限制交易价 : {} \n 现限制交易价 : {} '.format(url, data, res['retMessage'], JycList['limitTradePrice'], res['retData']['salepriceList'][0]['limitTradePrice'])

        # Spu查看页面详情-图文介绍
        url = self.host + '/sysback/productinfo/getPicInfoByProductUuid?menuId=252&buttonId=2&productUuid={}'.format(uUid)
        data = {}
        try:
            res = requests.get(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        # 主图 等后续姜传值
        assert res['retData']['mainImage']['trimmingKey'] != '', 'url : {} \n 结果 : {}主图不存在'.format(url, res['retMessage'])


        print('商品类型查询')
        url = self.host + '/sysback/finish/spu/mgr/getSpuList?menuId=252&buttonId=2'
        rdlist = ['01', '02', '03', '04', '05', '08']
        data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\""+ str(sample(rdlist, 1))[2:4] +"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
        try:
            res = requests.post(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '', 'url : {} \n 入参 : {} \n 结果 : {} \n 商品类型查询失败'.format(url, data, res['retMessage'])
        print('验证SPU管理结束')

    def SkuManagement(self, JycList):
        print('开始验证SKU管理')
        # skuNo 查询
        endTime = time.time() + 90
        while True:
            if time.time() < endTime:
                url = self.host + '/sysback/finish/sku/list/getSkuListForSkuManage?menuId=253&buttonId=2'
                data ={"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"Like\"},{\"name\":\"skuNo\",\"value\":\""+JycList['skuNo']+"\"},{\"name\":\"skuNo_q\",\"value\":\"Like\"},{\"name\":\"productName\",\"value\":\"\"},{\"name\":\"productName_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
                try:
                    res = requests.post(url, headers=self.json_header, json=data).json()
                except Exception as e:
                    assert False, '接口请求失败, {}\n{}'.format(url, e)
                print('获取数据失败,重试ing.....')
                time.sleep(9)
                if res['retData']['results'] != []:
                    print('获取数据成功')
                    assert res['retData']['results'][0]['skuCode'] == JycList['skuNo'], 'url : {} \n 入参 : {} \n 结果 : {} \n 查询Spu信息失败'.format(url, data, res['retMessage'])
                    break
            else:
                assert False, '请求失败,请检查sku准入是否完成! \nskuNo:{} '.format(JycList['skuNo'])
        # sku 管理信息
        print('开始对比Sku管理信息数据')
        url = self.host + '/sysback/update/product/allmanaging/queryAllManagingListFromSpu?menuId=253&buttonId=148'
        data = {"productKey": ""+JycList['productUuid']+""}
        try:
            res = requests.post(url, headers=self.form_header, data=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        #比对Sku管理区域
        assert res['retData'][0]['manageList'][0]['valueName'] == JycList['manage_area_ch'], 'url : {} \n 入参 : {} \n 结果 : {} \n sku管理区域不同 \n 管理区域原值: {} \n 管理区域现值: {}'.format(url, data, res['retMessage'], JycList['manage_area_ch'], res['retData'][0]['manageList'][0]['valueName'])
        # 对比合作模式
        assert res['retData'][0]['manageList'][1]['valueName'] == JycList['manage_cooperation'], 'url : {} \n 入参 : {} \n 结果 : {} \n sku合作模式不同 \n 合作模式原值: {} \n 合作模式现值: {}'.format(url, data, res['retMessage'], JycList['manage_cooperation'], res['retData'][0]['manageList'][1]['valueName'])
        # 对比经营模式
        assert res['retData'][0]['manageList'][2]['valueName'] == JycList['manage_dealmode'], 'url : {} \n 入参: {} \n 结果: {} \n 经营模式不同\n 经营模式原值: {} \n 经营模式现值: {}'.format(url, data, res['retMessage'], JycList['manage_dealmode'], res['retData'][0]['manageList'][2]['valueName'])
        # 对比包装清单
        assert res['retData'][0]['manageList'][3]['valueName'] == JycList['manage_packlist'], 'url : {} \n 入参: {} \n 结果: {} \n 包装清单不同\n 包装清单原值: {} \n 包装清单现值: {}'.format(url, data, res['retMessage'], JycList['manage_packlist'], res['retData'][0]['manageList'][3]['valueName'])
        # 对比售价管理周期
        assert res['retData'][0]['manageList'][4]['valueName'] == JycList['manage_sellmanageperiod'], 'url : {} \n 入参: {} \n 结果: {} \n 售价管理周期不同\n 售价管理周期原值: {} \n 售价管理周期现值: {}'.format(url, data, res['retMessage'], JycList['manage_sellmanageperiod'], res['retData'][0]['manageList'][4]['valueName'])
        # 对比档次外部定位
        assert res['retData'][0]['manageList'][5]['valueName'] == JycList['manage_outpos'], 'url : {} \n 入参: {} \n 结果: {} \n 档次外部定位不同\n 档次外部定位原值: {} \n 档次外部定位现值: {}'.format(url, data, res['retMessage'], JycList['manage_outpos'], res['retData'][0]['manageList'][5]['valueName'])
        # 对比档次内部定位
        assert res['retData'][0]['manageList'][6]['valueName'] == JycList['manage_inpos'], 'url : {} \n 入参: {} \n 结果: {} \n 档次内部定位不同\n 档次内部定位原值: {} \n 档次内部定位现值: {}'.format(url, data, res['retMessage'], JycList['manage_inpos'], res['retData'][0]['manageList'][6]['valueName'])
        # 对比囤货期
        assert res['retData'][0]['manageList'][7]['valueName'] == JycList['manage_stock_period'], 'url : {} \n 入参: {} \n 结果: {} \n 囤货期不同\n 囤货期原值: {} \n 囤货期现值: {}'.format(url, data, res['retMessage'], JycList['manage_stock_period'], res['retData'][0]['manageList'][7]['valueName'])
        # 对比是否季节性商品
        assert res['retData'][0]['manageList'][8]['valueName'] == JycList['manage_season_product'], 'url : {} \n 入参: {} \n 结果: {} \n 是否季节性商品不同\n 是否季节性商品原值: {} \n 是否季节性商品现值: {}'.format(url, data, res['retMessage'], JycList['manage_season_product'], res['retData'][0]['manageList'][8]['valueName'])
        # 对比下架期
        assert res['retData'][0]['manageList'][9]['valueName'] == JycList['manage_soldout_period'], 'url : {} \n 入参: {} \n 结果: {} \n 下架期不同\n 下架期原值: {} \n 下架期现值: {}'.format(url, data, res['retMessage'], JycList['manage_soldout_period'], res['retData'][0]['manageList'][9]['valueName'])
        # 对比售卖平台
        assert res['retData'][0]['marketingList'][0]['valueUuid'] == JycList['marketing_saleplat'], 'url : {} \n 入参: {} \n 结果: {} \n 售卖平台不同\n 售卖平台原值: {} \n 售卖平台现值: {}'.format(url, data, res['retMessage'], JycList['marketing_saleplat'], res['retData'][0]['marketingList'][0]['valueName'])
        # 对比归类名称
        assert res['retData'][0]['taxList'][0]['valueName'] == JycList['tax_classify'], 'url : {} \n 入参: {} \n 结果: {} \n 归类名称不同\n 归类名称原值: {} \n 归类名称现值: {}'.format(url, data, res['retMessage'], JycList['tax_classify'], res['retData'][0]['taxList'][0]['valueName'])
        #########################
        # 对比税类代码  后续姜提供
        #assert res['retData'][0]['taxList'][1]['valueName'] != '', 'url : {} \n 入参: {} \n 结果: {} \n 税类代码为空\n '.format(url, data, res['retMessage'])
        #########################
        # 对比销售税类  后续姜提供
        #assert res['retData'][0]['taxList'][2]['valueName'] != '', 'url : {} \n 入参: {} \n 结果: {} \n 销售税类为空\n '.format(url, data, res['retMessage'])
        #########################
        print('对比sku管理信息数据结束')

        ###########################################################
        print('开始对比管理信息模板')
        # 获取暂存时需要的入参 取上次请求的json作为入参
        hrDepartmentNumber = res['retData'][0]['authDepartments'][0]['hrDepartmentNumber']
        hrDepartmentName = res['retData'][0]['authDepartments'][0]['hrDepartmentName']
        authDepartments = res['retData'][0]['authDepartments']
        logisticsList = res['retData'][0]['logisticsList']
        manageList = res['retData'][0]['manageList']
        marketingList = res['retData'][0]['marketingList']
        taxList = res['retData'][0]['taxList']
        thirdPlatList = list()

        # 修改页面数据 传入json 做为暂存提交时的数据
        # 修改管理区域
        randAreaNum = randint(0, len(manageList[0]['allValueOptions']) - 1)
        manageList[0]['valueNameUpdate'] = manageList[0]['allValueOptions'][randAreaNum]['optionHtml']
        manageList[0]['valueUuidUpdate'] = manageList[0]['allValueOptions'][randAreaNum]['optionValue']
        # 修改合作模式
        randCooperNum = randint(0, len(manageList[1]['allValueOptions']) - 1)
        manageList[1]['valueNameUpdate'] = manageList[1]['allValueOptions'][randCooperNum]['optionHtml']
        manageList[1]['valueUuidUpdate'] = manageList[1]['allValueOptions'][randCooperNum]['optionValue']
        # 修改经营模式
        randDealmodeNum = randint(0, len(manageList[2]['allValueOptions']) - 1)
        manageList[2]['valueNameUpdate'] = manageList[2]['allValueOptions'][randDealmodeNum]['optionHtml']
        manageList[2]['valueUuidUpdate'] = manageList[2]['allValueOptions'][randDealmodeNum]['optionValue']
        # 修改包装清单
        manageList[3]['valueNameUpdate'] = self.getString(7)  # 预发布
        # 修改售价管理周期
        randSellCycleNum = randint(0, len(manageList[4]['allValueOptions']) - 1)
        manageList[4]['valueNameUpdate'] = manageList[4]['allValueOptions'][randSellCycleNum]['optionHtml']
        manageList[4]['valueUuidUpdate'] = manageList[4]['allValueOptions'][randSellCycleNum]['optionValue']
        # 修改档次外部定位
        randOutposNum = randint(0, len(manageList[5]['allValueOptions']) - 1)
        manageList[5]['valueNameUpdate'] = manageList[5]['allValueOptions'][randOutposNum]['optionHtml']
        manageList[5]['valueUuidUpdate'] = manageList[5]['allValueOptions'][randOutposNum]['optionValue']
        # 修改档次内部定位
        randInposNum = randint(0, len(manageList[6]['allValueOptions']) - 1)
        manageList[6]['valueNameUpdate'] = manageList[6]['allValueOptions'][randInposNum]['optionHtml']
        manageList[6]['valueUuidUpdate'] = manageList[6]['allValueOptions'][randInposNum]['optionValue']
        # 修改囤货期
        randStockCycleNum = randint(0, len(manageList[7]['allValueOptions']) - 1)
        manageList[7]['valueNameUpdate'] = manageList[7]['allValueOptions'][randStockCycleNum]['optionHtml']
        manageList[7]['valueUuidUpdate'] = manageList[7]['allValueOptions'][randStockCycleNum]['optionValue']
        # 修改是否季节性商品
        randSeasonNum = randint(0, len(manageList[8]['allValueOptions']) - 1)
        manageList[8]['valueNameUpdate'] = manageList[8]['allValueOptions'][randSeasonNum]['optionHtml']
        manageList[8]['valueUuidUpdate'] = manageList[8]['allValueOptions'][randSeasonNum]['optionValue']
        # 修改下架期
        randSoldoutNum = randint(0, len(manageList[9]['allValueOptions']) - 1)
        manageList[9]['valueNameUpdate'] = manageList[9]['allValueOptions'][randSoldoutNum]['optionHtml']
        manageList[9]['valueUuidUpdate'] = manageList[9]['allValueOptions'][randSoldoutNum]['optionValue']
        # 修改售卖平台
        randSaleChannelNum = randint(0, len(marketingList[0]['allValueOptions']) - 1)
        marketingList[0]['valueNameUpdate'] = marketingList[0]['allValueOptions'][randSaleChannelNum]['optionHtml']
        marketingList[0]['valueUuidUpdate'] = marketingList[0]['allValueOptions'][randSaleChannelNum]['optionValue']
        # 修改归类名称
        randTaxNamelNum = randint(0, len(taxList[0]['allValueOptions']) - 1)
        taxList[0]['valueNameUpdate'] = taxList[0]['allValueOptions'][randTaxNamelNum]['optionHtml']
        taxList[0]['valueUuidUpdate'] = taxList[0]['allValueOptions'][randTaxNamelNum]['optionValue']
        #修改存储属性
        randStorageNum = randint(0, len(logisticsList[3]['allValueOptions']) - 1)
        logisticsList[3]['valueNameUpdate'] = logisticsList[3]['allValueOptions'][randStorageNum]['optionHtml']
        logisticsList[3]['valueUuidUpdate'] = logisticsList[3]['allValueOptions'][randStorageNum]['optionValue']
        #修改存量属性
        randStockNum = randint(0, len(logisticsList[4]['allValueOptions']) - 1)
        logisticsList[4]['valueNameUpdate'] = logisticsList[4]['allValueOptions'][randStockNum]['optionHtml']
        logisticsList[4]['valueUuidUpdate'] = logisticsList[4]['allValueOptions'][randStockNum]['optionValue']

        # 设置暂存的Url
        url2 = self.host + '/sysback/update/product/allmanaging/saveAllManaging?menuId=253&buttonId=148'
        self.json_header['Authorization'] = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhZG1pbiIsInNjb3BlIjpbImFsbCJdLCJleHAiOjE2MjA4MDU5MTYsImF1dGhvcml0aWVzIjpbImFhIl0sImp0aSI6ImJjYzkwNDBkLTA0NTMtNDg5ZS1iMTM5LWEzZGU2MjQzZmJlMyIsImNsaWVudF9pZCI6ImFkbWluIiwidG9rZW4iOiJsb2dpbl90b2tlbl9hYmMzMjNjNmQwZWY0YTg2OWVhYjg0NjZmMTQ5MDgwNiJ9.GGr40pJ6GuZYkoeYPrFwJJDMAcmAnbzV1z8E3siyjtMM-AMkJA8RxeMz0k457o7WTGdHmGKprSjxll0n4dEfaUusHqRWqnZ9ApDyMqwmL_3DE6hieDpd09-ScpTZ2Ptl8JFOrSws7aT7q8W4QMUvhFA501bV8rMLGWyXkWWFIz6fzRbS7_pNJzogk1a8UfYAqjw25Mvh5XyEjvCpi0szty-VFPeWDTNfuQavQ0oQ68Cfra3K0Wa_ZsoTzeLVOoXSZgLx7iEMQhGHLGvPRAmv15QZfbUeCPKIbYK1o9IvjEIM2v-aEKMSOX8OdLSUgnaBd-IFu3dRFuXP2_5G0D1uvQ'
        data2 = {"inputList": [{"productKey": JycList['productUuid'],
                               "thirdPlatList": thirdPlatList,
                                "authDepartments": authDepartments,
                                "manageList": manageList,
                                "marketingList": marketingList,
                                "taxList": taxList,
                                "logisticsList": logisticsList
                                }]}
        # 获取 入参json 后续对比数据用
        TestData = data2
        try:
            res = requests.post(url2, headers=self.json_header, json=data2).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '', '请求报错,url: {}\n入参: {}\n结果: {}'.format(url, data2, res['retMessage'])
        Record = res['retData']['recordNo']
        assert res['retData']['commitState'] == 'NOT', 'url : {} \n 入参: {} \n 结果: {} \n 暂存失败\n '.format(url, data, res['retMessage'])
        assert res['retData']['recordNo'] != '', 'url : {} \n 入参: {} \n 结果: {} \n 修改管理信息暂存失败 \n '.format(url, data, res['retMessage'])
        print('暂存修改的Sku结束')

        # 提交暂存的内容
        print ('开始提交暂存内容')
        url = self.host + '/sysback/update/product/allmanaging/commitAllManaging?recordNo={}&menuId=253&buttonId=148'.format(Record)
        data = [{"authDepartments":[{"hrDepartmentNumber":""+hrDepartmentNumber+"","hrDepartmentName":""+hrDepartmentName+""}]}]
        try:
            res = requests.post(url, headers=self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        # print(res)
        # print(res['retData']['commitStateStr'])
        assert res['retData']['commitStateStr'] != '', 'url : {} \n 入参: {} \n 结果: {} \n 修改管理信息提交失败，暂存失败 \n '.format(url, data, res['retMessage'])
        assert res['retData']['recordNo'] == Record, 'url : {} \n 入参: {} \n 结果: {} \n 暂存与提交单据号不相符 \n 原单据号: {} \n 现单据号: {} '.format(url, data, res['retMessage'], Record, res['retData']['recordNo'])
        print('提交暂存内容结束')

        # 验证提交数据是否正确
        print('验证数据开始')
        url = self.host + '/sysback/update/product/allmanaging/queryAllManagingListFromSpu?menuId=253&buttonId=148'
        data = {"productKey": JycList['productUuid']}
        try:
            res = requests.post(url, headers=self.form_header, data=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        # 对比提交数据和现在数据是否一致
        print('对比Sku管理区域')
        assert res['retData'][0]['manageList'][0]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][0]['valueNameUpdate'], 'url : {} \n 入参 : {} \n 结果 : {} \n sku管理区域不同 \n 管理区域原值: {} \n 管理区域现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][0]['valueNameUpdate'], res['retData'][0]['manageList'][0]['valueName'])
        # 对比合作模式
        assert res['retData'][0]['manageList'][1]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][1]['valueNameUpdate'], 'url : {} \n 入参 : {} \n 结果 : {} \n sku合作模式不同 \n 合作模式原值: {} \n 合作模式现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][1]['valueNameUpdate'], res['retData'][0]['manageList'][1]['valueName'])
        # 对比经营模式
        assert res['retData'][0]['manageList'][2]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][2]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 经营模式不同\n 经营模式原值: {} \n 经营模式现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][2]['valueNameUpdate'], res['retData'][0]['manageList'][2]['valueName'])
        # 对比包装清单
        assert res['retData'][0]['manageList'][3]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][3]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 包装清单不同\n 包装清单原值: {} \n 包装清单现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][3]['valueNameUpdate'], res['retData'][0]['manageList'][3]['valueName'])
        # 对比售价管理周期
        assert res['retData'][0]['manageList'][4]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][4]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 售价管理周期不同\n 售价管理周期原值: {} \n 售价管理周期现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][4]['valueNameUpdate'], res['retData'][0]['manageList'][4]['valueName'])
        # 对比档次外部定位
        assert res['retData'][0]['manageList'][5]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][5]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 档次外部定位不同\n 档次外部定位原值: {} \n 档次外部定位现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][5]['valueNameUpdate'], res['retData'][0]['manageList'][5]['valueName'])
        # 对比档次内部定位
        assert res['retData'][0]['manageList'][6]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][6]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 档次内部定位不同\n 档次内部定位原值: {} \n 档次内部定位现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][6]['valueNameUpdate'], res['retData'][0]['manageList'][6]['valueName'])
        # 对比囤货期
        assert res['retData'][0]['manageList'][7]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][7]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 囤货期不同\n 囤货期原值: {} \n 囤货期现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][7]['valueNameUpdate'], res['retData'][0]['manageList'][7]['valueName'])
        # 对比是否季节性商品
        assert res['retData'][0]['manageList'][8]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][8]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 是否季节性商品不同\n 是否季节性商品原值: {} \n 是否季节性商品现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][8]['valueNameUpdate'], res['retData'][0]['manageList'][8]['valueName'])
        # 对比下架期
        assert res['retData'][0]['manageList'][9]['valueNameUpdate'] == TestData['inputList'][0]['manageList'][9]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 下架期不同\n 下架期原值: {} \n 下架期现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['manageList'][9]['valueNameUpdate'], res['retData'][0]['manageList'][9]['valueName'])
        # 对比售卖平台
        assert res['retData'][0]['marketingList'][0]['valueNameUpdate'] == TestData['inputList'][0]['marketingList'][0]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 售卖平台不同\n 售卖平台原值: {} \n 售卖平台现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['marketingList'][0]['valueNameUpdate'], res['retData'][0]['marketingList'][0]['valueName'])
        # 对比归类名称
        assert res['retData'][0]['taxList'][0]['valueNameUpdate'] == TestData['inputList'][0]['taxList'][0]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 归类名称不同\n 归类名称原值: {} \n 归类名称现值: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['taxList'][0]['valueNameUpdate'], res['retData'][0]['taxList'][0]['valueName'])
        # 对比税类代码
        assert res['retData'][0]['taxList'][1]['valueNameUpdate'] == TestData['inputList'][0]['taxList'][1]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 税类代码不同\n 原税类代码: {} \n 现税类代码: {} '.format(url, data, res['retMessage'], TestData['inputList'][0]['taxList'][1]['valueNameUpdate'],res['retData'][0]['taxList'][1]['valueName'])
        # 对比销售税类
        assert res['retData'][0]['taxList'][2]['valueNameUpdate'] == TestData['inputList'][0]['taxList'][2]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 销售税类不同\n 原销售税类: {} \n 现销售税类: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['taxList'][2]['valueNameUpdate'],res['retData'][0]['taxList'][2]['valueName'])
        # 对比存储属性
        assert res['retData'][0]['logisticsList'][3]['valueNameUpdate'] == TestData['inputList'][0]['logisticsList'][3]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 存储属性不同\n 原存储属性: {} \n 现存储属性: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['logisticsList'][3]['valueNameUpdate'], res['retData'][0]['logisticsList'][3]['valueName'])
        # 对比存量属性
        assert res['retData'][0]['logisticsList'][4]['valueNameUpdate'] == TestData['inputList'][0]['logisticsList'][4]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 存量属性不同\n 原存量属性: {} \n 现存量属性: {}'.format(url, data, res['retMessage'], TestData['inputList'][0]['logisticsList'][4]['valueNameUpdate'], res['retData'][0]['logisticsList'][4]['valueName'])
        print('验证数据结束')
        print('对比管理信息模板结束')
        #
        print('======================开始核对SKU信息模板=======================')
        # 修改SKU信息
        url = self.host + '/sysback/update/product/package/queryPackageListFromSku?menuId=253&buttonId=148'
        data = {"skuNo": JycList['skuNo']}
        try:
            res = requests.post(url, headers=self.form_header, data=data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)

        assert res['retData'][0]['safetyRate'] == str(JycList['safetyRate']), 'url: {} \n 入参: {}\n 结果: {}\n 安全率/金额不正确 \n 原安全率/金额: {} \n 现安全率/金额: {} '.format(url, data, res['retMessage'], JycList['safetyRate'], res['retData'][0]['safetyRate'])
        assert res['retData'][0]['barcode'] == JycList['barcode'], 'url: {} \n 入参: {}\n 结果: {}\n 国际条形码不正确 \n 原国际条形码: {} \n 现国际条形码: {} '.format(url, data, res['retMessage'], JycList['barcode'], res['retData'][0]['barcode'])
        assert res['retData'][0]['saleMin'] == str(JycList['saleMin']), 'url: {} \n 入参: {}\n 结果: {}\n 最小起售量不正确 \n 原最小起售量: {} \n 现最小起售量: {} '.format(url, data, res['retMessage'], JycList['saleMin'], res['retData'][0]['saleMin'])
        assert res['retData'][0]['saleRestrict'] != '','url: {} \n 入参: {}\n 结果: {}\n 销售限制类型不正确'.format(url, data, res['retMessage'])
        assert res['retData'][0]['pieceInfo'] == JycList['pieceInfo'], 'url: {} \n 入参: {}\n 结果: {}\n 件装数量不正确 \n 原件装数量: {} \n 现件装数量: {} '.format(url, data, res['retMessage'], JycList['pieceInfo'], res['retData'][0]['pieceInfo'])
        assert res['retData'][0]['packageLayers'] == JycList['packageLayers'], 'url: {} \n 入参: {}\n 结果: {}\n 层数不正确 \n 原层数: {} \n 现层数: {} '.format(url, data, res['retMessage'], JycList['packageLayers'], res['retData'][0]['packageLayers'])
        assert res['retData'][0]['singlePackageUnit'] != '', 'url: {} \n 入参: {}\n 结果: {}\n 单品包装单位为空 '.format(url, data, res['retMessage'])
        assert res['retData'][0]['singlePackageCount'] == str(JycList['singlePackageCount']), 'url: {} \n 入参: {}\n 结果: {}\n 单品包装数量不正确 \n 原单品包装数量: {} \n 现单品包装数量: {} '.format(url, data, res['retMessage'], JycList['singlePackageCount'], res['retData'][0]['singlePackageCount'])
        assert float(res['retData'][0]['singleEdge1']) == JycList['singleEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 单品最长边不正确 \n 原单品最长边: {} \n 现单品最长边: {} '.format(url, data, res['retMessage'], JycList['singleEdge1'], res['retData'][0]['singleEdge1'])
        assert float(res['retData'][0]['singleEdge2']) == JycList['singleEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 单品次长边不正确 \n 原单品次长边: {} \n 现单品次长边: {} '.format(url, data, res['retMessage'], JycList['singleEdge2'], res['retData'][0]['singleEdge2'])
        assert float(res['retData'][0]['singleEdge3']) == JycList['singleEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 单品最短边不正确 \n 原单品最短边: {} \n 现单品最短边: {} '.format(url, data, res['retMessage'], JycList['singleEdge3'], res['retData'][0]['singleEdge3'])
        assert float(res['retData'][0]['singleVolume']) == JycList['singleVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 单品体积不正确 \n 原单品体积: {} \n 现单品体积: {} '.format(url, data, res['retMessage'], JycList['singleVolume'], res['retData'][0]['singleVolume'])
        assert float(res['retData'][0]['singleWeight']) == JycList['singleWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 单品重量不正确 \n 原单品重量: {} \n 现单品重量: {} '.format(url, data, res['retMessage'], JycList['singleWeight'], res['retData'][0]['singleWeight'])
        assert res['retData'][0]['onePackageUnit'] == JycList['onePackageUnit'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装单位不正确 \n 原一层包装单位: {} \n 现一层包装单位: {} '.format(url, data, res['retMessage'], JycList['onePackageUnit'], res['retData'][0]['onePackageUnit'])
        assert res['retData'][0]['onePackageCount'] == str(JycList['onePackageCount']), 'url: {} \n 入参: {}\n 结果: {}\n 一层包装数量不正确 \n 原一层包装数量: {} \n 现一层包装数量: {} '.format(url, data, res['retMessage'], JycList['onePackageCount'], res['retData'][0]['onePackageCount'])
        assert float(res['retData'][0]['oneEdge1']) == JycList['oneEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 一层最长边不正确 \n 原一层最长边: {} \n 现一层最长边: {} '.format(url, data, res['retMessage'], JycList['oneEdge1'], res['retData'][0]['oneEdge1'])
        assert float(res['retData'][0]['oneEdge2']) == JycList['oneEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 一层次长边不正确 \n 原一层次长边: {} \n 现一层次长边: {} '.format(url, data, res['retMessage'], JycList['oneEdge2'], res['retData'][0]['oneEdge2'])
        assert float(res['retData'][0]['oneEdge3']) == JycList['oneEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 一层最短边不正确 \n 原一层最短边: {} \n 现一层最短边: {} '.format(url, data, res['retMessage'], JycList['oneEdge3'], res['retData'][0]['oneEdge3'])
        assert float(res['retData'][0]['oneVolume']) == JycList['oneVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 一层体积不正确 \n 原一层体积: {} \n 现一层体积: {} '.format(url, data, res['retMessage'], JycList['oneVolume'], res['retData'][0]['oneVolume'])
        assert float(res['retData'][0]['oneWeight']) == JycList['oneWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 一层重量不正确 \n 原一层重量: {} \n 现一层重量: {} '.format(url, data, res['retMessage'], JycList['oneWeight'], res['retData'][0]['oneWeight'])
        assert res['retData'][0]['twoPackageUnit'] == JycList['twoPackageUnit'], 'url: {} \n 入参: {}\n 结果: {}\n 二层包装单位不正确 \n 原二层包装单位: {} \n 现二层包装单位: {} '.format(url, data, res['retMessage'], JycList['twoPackageUnit'], res['retData'][0]['twoPackageUnit'])
        assert res['retData'][0]['twoPackageCount'] == str(JycList['twoPackageCount']), 'url: {} \n 入参: {}\n 结果: {}\n 二层包装数量不正确 \n 原二层包装数量: {} \n 现二层包装数量: {} '.format(url, data, res['retMessage'], JycList['twoPackageCount'], res['retData'][0]['twoPackageCount'])
        assert float(res['retData'][0]['twoEdge1']) == JycList['twoEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 二层最长边不正确 \n 原二层最长边: {} \n 现二层最长边: {} '.format(url, data, res['retMessage'], JycList['twoEdge1'], res['retData'][0]['twoEdge1'])
        assert float(res['retData'][0]['twoEdge2']) == JycList['twoEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 二层次长边不正确 \n 原二层次长边: {} \n 现二层次长边: {} '.format(url, data, res['retMessage'], JycList['twoEdge2'], res['retData'][0]['twoEdge2'])
        assert float(res['retData'][0]['twoEdge3']) == JycList['twoEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 二层最短边不正确 \n 原二层最短边: {} \n 现二层最短边: {} '.format(url, data, res['retMessage'], JycList['twoEdge3'], res['retData'][0]['twoEdge3'])
        assert float(res['retData'][0]['twoVolume']) == JycList['twoVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 二层体积不正确 \n 原二层体积: {} \n 现二层体积: {} '.format(url, data, res['retMessage'], JycList['twoVolume'], res['retData'][0]['twoVolume'])
        assert float(res['retData'][0]['twoWeight']) == JycList['twoWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 二层重量不正确 \n 原二层重量: {} \n 现二层重量: {} '.format(url, data, res['retMessage'], JycList['twoWeight'], res['retData'][0]['twoWeight'])
        assert res['retData'][0]['threePackageUnit'] == JycList['threePackageUnit'], 'url: {} \n 入参: {}\n 结果: {}\n 三层包装单位不正确 \n 原三层包装单位: {} \n 现三层包装单位: {} '.format(url, data, res['retMessage'], JycList['threePackageUnit'], res['retData'][0]['threePackageUnit'])
        assert res['retData'][0]['threePackageCount'] == str(JycList['threePackageCount']), 'url: {} \n 入参: {}\n 结果: {}\n 三层包装数量不正确 \n 原三层包装数量: {} \n 现三层包装数量: {} '.format(url, data, res['retMessage'], JycList['threePackageCount'], res['retData'][0]['threePackageCount'])
        assert float(res['retData'][0]['threeEdge1']) == JycList['threeEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 三层最长边不正确 \n 原三层最长边: {} \n 现三层最长边: {} '.format(url, data, res['retMessage'], JycList['threeEdge1'], res['retData'][0]['threeEdge1'])
        assert float(res['retData'][0]['threeEdge2']) == JycList['threeEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 三层次长边不正确 \n 原三层次长边: {} \n 现三层次长边: {} '.format(url, data, res['retMessage'], JycList['threeEdge2'], res['retData'][0]['threeEdge2'])
        assert float(res['retData'][0]['threeEdge3']) == JycList['threeEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 三层最短边不正确 \n 原三层最短边: {} \n 现三层最短边: {} '.format(url, data, res['retMessage'], JycList['threeEdge3'], res['retData'][0]['threeEdge3'])
        assert float(res['retData'][0]['threeVolume']) == JycList['threeVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 三层体积不正确 \n 原三层体积: {} \n 现三层体积: {} '.format(url, data, res['retMessage'], JycList['threeVolume'], res['retData'][0]['threeVolume'])
        assert float(res['retData'][0]['threeWeight']) == JycList['threeWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 三层重量不正确 \n 原三层重量: {} \n 现三层重量: {} '.format(url, data, res['retMessage'], JycList['threeWeight'], res['retData'][0]['threeWeight'])
        print('======================核对SKU修改数据结束=======================')

        print('======================修改SKU各属性数据======================')
        #修改SKU信息
        url = self.host +'/sysback/update/product/package/queryPackageListFromSku?menuId=253&buttonId=148'
        reuqestsdata = {'skuNo': JycList['skuNo']}
        try:
            res = requests.post(url, headers=self.form_header, data=reuqestsdata).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        data = res['retData'][0]
        data['productKey'] = JycList['spuNo']
        data['safetyRateUpdate'] = randint(1, 20)
        data['barcodeUpdate'] = self.getString(8)
        data['saleMinUpdate'] = round(uniform(1, 100), 2)
        data['saleRestrictUpdate'] = randint(1, 2)
        data['pieceInfoUpdate'] = self.getString(8)
        # 生成层数列表 随机选择
        packageLayersList = ['THREE', 'TWO', 'ONE', 'SINGLE']
        data['packageLayersUpdate'] = sample(packageLayersList, 1)[0]
        #判断层数，更具实际层数赋值
        if data['packageLayersUpdate'] == 'SINGLE':
            data['singlePackageUnitUpdate'] = data['singlePackageUnit']
            data['singlePackageCountUpdate'] = randint(1, 20)
            data['singleEdge1Update'] = round(uniform(1, 100), 2)
            data['singleEdge2Update'] = round(uniform(1, 100), 2)
            data['singleEdge3Update'] = round(uniform(1, 100), 2)
            data['singleWeightUpdate'] = round(uniform(1, 100), 2)
            data['singleVolumeUpdate'] = (float(data['singleEdge1Update']) * float(data['singleEdge2Update']) * float(data['singleEdge3Update'])) / 1000000

        elif data['packageLayersUpdate'] == 'ONE':
            data['singlePackageUnitUpdate'] = data['singlePackageUnit']
            data['singlePackageCountUpdate'] = randint(1, 20)  #单品及一层赋值
            data['singleEdge1Update'] = round(uniform(1, 100), 2)
            data['singleEdge2Update'] = round(uniform(1, 100), 2)
            data['singleEdge3Update'] = round(uniform(1, 100), 2)
            data['singleWeightUpdate'] = round(uniform(1, 100), 2)
            data['singleVolumeUpdate'] = (float(data['singleEdge1Update']) * float(data['singleEdge2Update']) * float(data['singleEdge3Update'])) / 1000000

            data['onePackageUnitUpdate'] = self.GetCalcUnit() #需要获取层一计量单位
            data['onePackageCountUpdate'] = randint(1, 20)
            data['oneEdge1Update'] = round(uniform(1, 100), 2)
            data['oneEdge2Update'] = round(uniform(1, 100), 2)
            data['oneEdge3Update'] = round(uniform(1, 100), 2)
            data['oneWeightUpdate'] = round(uniform(1, 100), 2)
            data['oneVolumeUpdate'] = (float(data['oneEdge1Update']) * float(data['oneEdge2Update']) * float(data['oneEdge3Update'])) / 1000000

        elif data['packageLayersUpdate'] == 'TWO':
            data['singlePackageUnitUpdate'] = data['singlePackageUnit']
            data['singlePackageCountUpdate'] = randint(1, 20)   #单品、一层、二层赋值
            data['singleEdge1Update'] = round(uniform(1, 100), 2)
            data['singleEdge2Update'] = round(uniform(1, 100), 2)
            data['singleEdge3Update'] = round(uniform(1, 100), 2)
            data['singleWeightUpdate'] = round(uniform(1, 100), 2)
            data['singleVolumeUpdate'] = (float(data['singleEdge1Update']) * float(data['singleEdge2Update']) * float(data['singleEdge3Update'])) / 1000000

            data['onePackageUnitUpdate'] = self.GetCalcUnit()  #需要获取层一计量单位
            data['onePackageCountUpdate'] = randint(1, 20)
            data['oneEdge1Update'] = round(uniform(1, 100), 2)
            data['oneEdge2Update'] = round(uniform(1, 100), 2)
            data['oneEdge3Update'] = round(uniform(1, 100), 2)
            data['oneWeightUpdate'] = round(uniform(1, 100), 2)
            data['oneVolumeUpdate'] = (float(data['oneEdge1Update']) * float(data['oneEdge2Update']) * float(data['oneEdge3Update'])) / 1000000

            data['twoPackageUnitUpdate'] =self.GetCalcUnit() #需要获取二层计量单位
            data['twoPackageCountUpdate'] = randint(1, 20)
            data['twoEdge1Update'] = round(uniform(1, 100), 2)
            data['twoEdge2Update'] = round(uniform(1, 100), 2)
            data['twoEdge3Update'] = round(uniform(1, 100), 2)
            data['twoWeightUpdate'] = round(uniform(1, 100), 2)
            data['twoVolumeUpdate'] = (float(data['twoEdge1Update']) * float(data['twoEdge2Update']) * float(data['twoEdge3Update'])) / 1000000

        elif data['packageLayersUpdate'] == 'THREE':
            data['singlePackageUnitUpdate'] = data['singlePackageUnit']
            data['singlePackageCountUpdate'] = randint(1, 20)   #单品、一层、二层赋值
            data['singleEdge1Update'] = round(uniform(1, 100), 2)
            data['singleEdge2Update'] = round(uniform(1, 100), 2)
            data['singleEdge3Update'] = round(uniform(1, 100), 2)
            data['singleWeightUpdate'] = round(uniform(1, 100), 2)
            data['singleVolumeUpdate'] = (float(data['singleEdge1Update']) * float(data['singleEdge2Update']) * float(data['singleEdge3Update'])) / 1000000

            data['onePackageUnitUpdate'] = self.GetCalcUnit()  #需要获取层一计量单位
            data['onePackageCountUpdate'] = randint(1, 20)
            data['oneEdge1Update'] = round(uniform(1, 100), 2)
            data['oneEdge2Update'] = round(uniform(1, 100), 2)
            data['oneEdge3Update'] = round(uniform(1, 100), 2)
            data['oneWeightUpdate'] = round(uniform(1, 100), 2)
            data['oneVolumeUpdate'] = (float(data['oneEdge1Update']) * float(data['oneEdge2Update']) * float(data['oneEdge3Update'])) / 1000000

            data['twoPackageUnitUpdate'] = self.GetCalcUnit() #需要获取二层计量单位
            data['twoPackageCountUpdate'] = randint(1, 20)
            data['twoEdge1Update'] = round(uniform(1, 100), 2)
            data['twoEdge2Update'] = round(uniform(1, 100), 2)
            data['twoEdge3Update'] = round(uniform(1, 100), 2)
            data['twoWeightUpdate'] = round(uniform(1, 100), 2)
            data['twoVolumeUpdate'] = (float(data['twoEdge1Update']) * float(data['twoEdge2Update']) * float(data['twoEdge3Update'])) / 1000000

            data['threePackageUnitUpdate'] = self.GetCalcUnit() #需要获取二层计量单位
            data['threePackageCountUpdate'] = randint(1, 20)
            data['threeEdge1Update'] = round(uniform(1, 100), 2)
            data['threeEdge2Update'] = round(uniform(1, 100), 2)
            data['threeEdge3Update'] = round(uniform(1, 100), 2)
            data['threeWeightUpdate'] = round(uniform(1, 100), 2)
            data['threeVolumeUpdate'] = (float(data['threeEdge1Update']) * float(data['threeEdge2Update']) * float(data['threeEdge3Update'])) / 1000000

        else:
            assert data['packageLayersUpdate'] != '', '层数数据异常, 层数值为: {}'.format(data['packageLayersUpdate'])
        # 暂存用 URL
        SaveUrl = self.host + '/sysback/update/product/package/savePackage?menuId=253&buttonId=148'
        # 拼接暂存用 data
        listData = list()
        listData.append(data)
        SaveData = {'inputList': listData, 'recordNo': ''}
        # print('====================================')
        # print(SaveData)
        # print('====================================')
        print('执行暂存开始')
        try:
            SaveRes = requests.post(SaveUrl, headers=self.json_header, json=SaveData).json()
            # print(SaveRes)
            RecordCommit = SaveRes['retData']['recordNo']
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '', '暂存失败\n{}'.format(res['retMessage'])
        assert SaveRes['retData']['commitState'] == 'NOT', '暂存失败 \n, 请检查入参: {} '.format(SaveData)
        print('执行暂存成功')
        # 提交
        print('执行提交开始')
        print(listData)
        CommitUrl = self.host + '/sysback/update/product/package/commitPackage?recordNo={}&menuId=253&buttonId=148'.format(RecordCommit)
        CommitData = listData
        # 执行提交
        try:
            CommitRes = requests.post(CommitUrl, headers=self.json_header, json=CommitData).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        # print(CommitRes)
        assert CommitRes['retData']['commitState'] == 'COMMIT', '提交失败 \n, 请检查入参: {} '.format(CommitData)
        print('执行提交成功')

        # 验证数据是否与提交的一致
        CheckUrl = self.host + '/sysback/update/product/package/queryPackageListFromSku?menuId=253&buttonId=148'
        CheckData = {'skuNo': JycList['skuNo']}
        try:
            res = requests.post(CheckUrl, headers=self.form_header, data=CheckData).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        print('======================核对SKU提交数据开始=======================')
        assert res['retData'][0]['safetyRateUpdate'] == str(data['safetyRateUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 安全率/金额不正确 \n 提交的安全率/金额: {} \n 现安全率/金额: {} '.format(url, data, res['retMessage'], data['safetyRateUpdate'], res['retData'][0]['safetyRateUpdate'])
        assert res['retData'][0]['barcodeUpdate'] == data['barcodeUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 国际条形码不正确 \n 提交的国际条形码: {} \n 现国际条形码: {} '.format(url, data, res['retMessage'], data['barcodeUpdate'], res['retData'][0]['barcodeUpdate'])
        assert res['retData'][0]['saleMinUpdate'] == str(data['saleMinUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 最小起售量不正确 \n 提交的最小起售量: {} \n 现最小起售量: {} '.format(url, data, res['retMessage'], data['saleMinUpdate'], res['retData'][0]['saleMinUpdate'])
        assert res['retData'][0]['saleRestrictUpdate'] == str(data['saleRestrictUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 销售限制类型不正确 \n 提交的销售限制类型: {} \n 现销售限制类型: {} '.format(url, data, res['retMessage'], data['saleRestrictUpdate'], res['retData'][0]['saleRestrictUpdate'])
        assert res['retData'][0]['pieceInfoUpdate'] == data['pieceInfoUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 件装数量不正确 \n 提交的件装数量: {} \n 现件装数量: {} '.format(url, data, res['retMessage'], data['pieceInfoUpdate'], res['retData'][0]['pieceInfoUpdate'])
        assert res['retData'][0]['packageLayersUpdate'] == data['packageLayersUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 层数不正确 \n 提交层数: {} \n 现层数: {} '.format(url, data, res['retMessage'], data['packageLayersUpdate'], res['retData'][0]['packageLayersUpdate'])
        assert res['retData'][0]['singlePackageUnitUpdate'] == data['singlePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 单品包装单位不正确 \n 提交单品包装单位: {} \n 现单品包装单位: {} '.format(url, data, res['retMessage'], data['singlePackageUnitUpdate'], res['retData'][0]['singlePackageUnitUpdate'])
        assert res['retData'][0]['singlePackageCountUpdate'] == str(data['singlePackageCountUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 单品包装数量不正确 \n 提交的单品包装数量: {} \n 现单品包装数量: {} '.format(url, data, res['retMessage'], data['singlePackageCountUpdate'], res['retData'][0]['singlePackageCountUpdate'])
        assert res['retData'][0]['singleEdge1Update'] == str(data['singleEdge1Update']), 'url: {} \n 入参: {}\n 结果: {}\n 单品最长边不正确 \n 提交的单品最长边: {} \n 现单品最长边: {} '.format(url, data, res['retMessage'], data['singleEdge1Update'], res['retData'][0]['singleEdge1Update'])
        assert res['retData'][0]['singleEdge2Update'] == str(data['singleEdge2Update']), 'url: {} \n 入参: {}\n 结果: {}\n 单品次长边不正确 \n 提交的单品次长边: {} \n 现单品次长边: {} '.format(url, data, res['retMessage'], data['singleEdge2Update'], res['retData'][0]['singleEdge2Update'])
        assert res['retData'][0]['singleEdge3Update'] == str(data['singleEdge3Update']), 'url: {} \n 入参: {}\n 结果: {}\n 单品最短边不正确 \n 提交的单品最短边: {} \n 现单品最短边: {} '.format(url, data, res['retMessage'], data['singleEdge3Update'], res['retData'][0]['singleEdge3Update'])
        assert res['retData'][0]['singleVolumeUpdate'] == str(data['singleVolumeUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 单品体积不正确 \n 提交的单品体积: {} \n 现单品体积: {} '.format(url, data, res['retMessage'], data['singleVolumeUpdate'], res['retData'][0]['singleVolumeUpdate'])
        assert res['retData'][0]['singleWeightUpdate'] == str(data['singleWeightUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 单品重量不正确 \n 提交的单品重量: {} \n 现单品重量: {} '.format(url, data, res['retMessage'], data['singleWeightUpdate'], res['retData'][0]['singleWeightUpdate'])
        if res['retData'][0]['packageLayersUpdate'] == 'ONE':
            assert res['retData'][0]['onePackageUnitUpdate'] == data['onePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装单位不正确 \n 提交的一层包装单位: {} \n 现一层包装单位: {} '.format(url, data, res['retMessage'], data['onePackageUnitUpdate'], res['retData'][0]['onePackageUnitUpdate'])
            assert res['retData'][0]['onePackageCountUpdate'] == str(data['onePackageCountUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层包装数量不正确 \n 提交的一层包装数量: {} \n 现一层包装数量: {} '.format(url, data, res['retMessage'], data['onePackageCountUpdate'], res['retData'][0]['onePackageCountUpdate'])
            assert res['retData'][0]['oneEdge1Update'] == str(data['oneEdge1Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层最长边不正确 \n 提交的一层最长边: {} \n 现一层最长边: {} '.format(url, data, res['retMessage'], data['oneEdge1Update'], res['retData'][0]['oneEdge1Update'])
            assert res['retData'][0]['oneEdge2Update'] == str(data['oneEdge2Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层次长边不正确 \n 提交的一层次长边: {} \n 现一层次长边: {} '.format(url, data, res['retMessage'], data['oneEdge2Update'], res['retData'][0]['oneEdge2Update'])
            assert res['retData'][0]['oneEdge3Update'] == str(data['oneEdge3Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层最短边不正确 \n 提交的一层最短边: {} \n 现一层最短边: {} '.format(url, data, res['retMessage'], data['oneEdge3Update'], res['retData'][0]['oneEdge3Update'])
            assert res['retData'][0]['oneVolumeUpdate'] == str(data['oneVolumeUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层体积不正确 \n 提交的一层体积: {} \n 现一层体积: {} '.format(url, data, res['retMessage'], data['oneVolumeUpdate'], res['retData'][0]['oneVolumeUpdate'])
            assert res['retData'][0]['oneWeightUpdate'] == str(data['oneWeightUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层重量不正确 \n 提交的一层重量: {} \n 现一层重量: {} '.format(url, data, res['retMessage'], data['oneWeightUpdate'], res['retData'][0]['oneWeightUpdate'])
        elif res['retData'][0]['packageLayersUpdate'] == 'TWO':
            assert res['retData'][0]['onePackageUnitUpdate'] == data['onePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装单位不正确 \n 提交的一层包装单位: {} \n 现一层包装单位: {} '.format(url, data, res['retMessage'], data['onePackageUnitUpdate'], res['retData'][0]['onePackageUnitUpdate'])
            assert res['retData'][0]['onePackageCountUpdate'] == str(data['onePackageCountUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层包装数量不正确 \n 提交的一层包装数量: {} \n 现一层包装数量: {} '.format(url, data, res['retMessage'], data['onePackageCountUpdate'], res['retData'][0]['onePackageCountUpdate'])
            assert res['retData'][0]['oneEdge1Update'] == str(data['oneEdge1Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层最长边不正确 \n 提交的一层最长边: {} \n 现一层最长边: {} '.format(url, data, res['retMessage'], data['oneEdge1Update'], res['retData'][0]['oneEdge1Update'])
            assert res['retData'][0]['oneEdge2Update'] == str(data['oneEdge2Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层次长边不正确 \n 提交的一层次长边: {} \n 现一层次长边: {} '.format(url, data, res['retMessage'], data['oneEdge2Update'], res['retData'][0]['oneEdge2Update'])
            assert res['retData'][0]['oneEdge3Update'] == str(data['oneEdge3Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层最短边不正确 \n 提交的一层最短边: {} \n 现一层最短边: {} '.format(url, data, res['retMessage'], data['oneEdge3Update'], res['retData'][0]['oneEdge3Update'])
            assert res['retData'][0]['oneVolumeUpdate'] == str(data['oneVolumeUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层体积不正确 \n 提交的一层体积: {} \n 现一层体积: {} '.format(url, data, res['retMessage'], data['oneVolumeUpdate'], res['retData'][0]['oneVolumeUpdate'])
            assert res['retData'][0]['oneWeightUpdate'] == str(data['oneWeightUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层重量不正确 \n 提交的一层重量: {} \n 现一层重量: {} '.format(url, data, res['retMessage'], data['oneWeightUpdate'], res['retData'][0]['oneWeightUpdate'])
            assert res['retData'][0]['twoPackageUnitUpdate'] == data['twoPackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 二层包装单位不正确 \n 提交的二层包装单位: {} \n 现二层包装单位: {} '.format(url, data, res['retMessage'], data['twoPackageUnitUpdate'], res['retData'][0]['twoPackageUnitUpdate'])
            assert res['retData'][0]['twoPackageCountUpdate'] == str(data['twoPackageCountUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 二层包装数量不正确 \n 提交的二层包装数量: {} \n 现二层包装数量: {} '.format(url, data, res['retMessage'], data['twoPackageCountUpdate'], res['retData'][0]['twoPackageCountUpdate'])
            assert res['retData'][0]['twoEdge1Update'] == str(data['twoEdge1Update']), 'url: {} \n 入参: {}\n 结果: {}\n 二层最长边不正确 \n 提交的二层最长边: {} \n 现二层最长边: {} '.format(url, data, res['retMessage'], data['twoEdge1Update'], res['retData'][0]['twoEdge1Update'])
            assert res['retData'][0]['twoEdge2Update'] == str(data['twoEdge2Update']), 'url: {} \n 入参: {}\n 结果: {}\n 二层次长边不正确 \n 提交的二层次长边: {} \n 现二层次长边: {} '.format(url, data, res['retMessage'], data['twoEdge2Update'], res['retData'][0]['twoEdge2Update'])
            assert res['retData'][0]['twoEdge3Update'] == str(data['twoEdge3Update']), 'url: {} \n 入参: {}\n 结果: {}\n 二层最短边不正确 \n 提交的二层最短边: {} \n 现二层最短边: {} '.format(url, data, res['retMessage'], data['twoEdge3Update'], res['retData'][0]['twoEdge3Update'])
            assert res['retData'][0]['twoVolumeUpdate'] == str(data['twoVolumeUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 二层体积不正确 \n 提交的二层体积: {} \n 现二层体积: {} '.format(url, data, res['retMessage'], data['twoVolumeUpdate'], res['retData'][0]['twoVolumeUpdate'])
            assert res['retData'][0]['twoWeightUpdate'] == str(data['twoWeightUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 二层重量不正确 \n 提交的二层重量: {} \n 现二层重量: {} '.format(url, data, res['retMessage'], data['twoWeightUpdate'], res['retData'][0]['twoWeightUpdate'])
        elif res['retData'][0]['packageLayersUpdate'] == 'THREE':
            assert res['retData'][0]['onePackageUnitUpdate'] == data['onePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装单位不正确 \n 提交的一层包装单位: {} \n 现一层包装单位: {} '.format(url, data, res['retMessage'], data['onePackageUnitUpdate'], res['retData'][0]['onePackageUnitUpdate'])
            assert res['retData'][0]['onePackageCountUpdate'] == str(data['onePackageCountUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层包装数量不正确 \n 提交的一层包装数量: {} \n 现一层包装数量: {} '.format(url, data, res['retMessage'], data['onePackageCountUpdate'], res['retData'][0]['onePackageCountUpdate'])
            assert res['retData'][0]['oneEdge1Update'] == str(data['oneEdge1Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层最长边不正确 \n 提交的一层最长边: {} \n 现一层最长边: {} '.format(url, data, res['retMessage'], data['oneEdge1Update'], res['retData'][0]['oneEdge1Update'])
            assert res['retData'][0]['oneEdge2Update'] == str(data['oneEdge2Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层次长边不正确 \n 提交的一层次长边: {} \n 现一层次长边: {} '.format(url, data, res['retMessage'], data['oneEdge2Update'], res['retData'][0]['oneEdge2Update'])
            assert res['retData'][0]['oneEdge3Update'] == str(data['oneEdge3Update']), 'url: {} \n 入参: {}\n 结果: {}\n 一层最短边不正确 \n 提交的一层最短边: {} \n 现一层最短边: {} '.format(url, data, res['retMessage'], data['oneEdge3Update'], res['retData'][0]['oneEdge3Update'])
            assert res['retData'][0]['oneVolumeUpdate'] == str(data['oneVolumeUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层体积不正确 \n 提交的一层体积: {} \n 现一层体积: {} '.format(url, data, res['retMessage'], data['oneVolumeUpdate'], res['retData'][0]['oneVolumeUpdate'])
            assert res['retData'][0]['oneWeightUpdate'] == str(data['oneWeightUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 一层重量不正确 \n 提交的一层重量: {} \n 现一层重量: {} '.format(url, data, res['retMessage'], data['oneWeightUpdate'], res['retData'][0]['oneWeightUpdate'])
            assert res['retData'][0]['twoPackageUnitUpdate'] == data['twoPackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 二层包装单位不正确 \n 提交的二层包装单位: {} \n 现二层包装单位: {} '.format(url, data, res['retMessage'], data['twoPackageUnitUpdate'], res['retData'][0]['twoPackageUnitUpdate'])
            assert res['retData'][0]['twoPackageCountUpdate'] == str(data['twoPackageCountUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 二层包装数量不正确 \n 提交的二层包装数量: {} \n 现二层包装数量: {} '.format(url, data, res['retMessage'], data['twoPackageCountUpdate'], res['retData'][0]['twoPackageCountUpdate'])
            assert res['retData'][0]['twoEdge1Update'] == str(data['twoEdge1Update']), 'url: {} \n 入参: {}\n 结果: {}\n 二层最长边不正确 \n 提交的二层最长边: {} \n 现二层最长边: {} '.format(url, data, res['retMessage'], data['twoEdge1Update'], res['retData'][0]['twoEdge1Update'])
            assert res['retData'][0]['twoEdge2Update'] == str(data['twoEdge2Update']), 'url: {} \n 入参: {}\n 结果: {}\n 二层次长边不正确 \n 提交的二层次长边: {} \n 现二层次长边: {} '.format(url, data, res['retMessage'], data['twoEdge2Update'], res['retData'][0]['twoEdge2Update'])
            assert res['retData'][0]['twoEdge3Update'] == str(data['twoEdge3Update']), 'url: {} \n 入参: {}\n 结果: {}\n 二层最短边不正确 \n 提交的二层最短边: {} \n 现二层最短边: {} '.format(url, data, res['retMessage'], data['twoEdge3Update'], res['retData'][0]['twoEdge3Update'])
            assert res['retData'][0]['twoVolumeUpdate'] == str(data['twoVolumeUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 二层体积不正确 \n 提交的二层体积: {} \n 现二层体积: {} '.format(url, data, res['retMessage'], data['twoVolumeUpdate'], res['retData'][0]['twoVolumeUpdate'])
            assert res['retData'][0]['twoWeightUpdate'] == str(data['twoWeightUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 二层重量不正确 \n 提交的二层重量: {} \n 现二层重量: {} '.format(url, data, res['retMessage'], data['twoWeightUpdate'], res['retData'][0]['twoWeightUpdate'])
            assert res['retData'][0]['threePackageUnitUpdate'] == data['threePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 三层包装单位不正确 \n 提交的三层包装单位: {} \n 现三层包装单位: {} '.format(url, data, res['retMessage'], data['threePackageUnitUpdate'], res['retData'][0]['threePackageUnitUpdate'])
            assert res['retData'][0]['threePackageCountUpdate'] == str(data['threePackageCountUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 三层包装数量不正确 \n 提交的三层包装数量: {} \n 现三层包装数量: {} '.format(url, data, res['retMessage'], data['threePackageCountUpdate'], res['retData'][0]['threePackageCountUpdate'])
            assert res['retData'][0]['threeEdge1Update'] == str(data['threeEdge1Update']), 'url: {} \n 入参: {}\n 结果: {}\n 三层最长边不正确 \n 提交的三层最长边: {} \n 现三层最长边: {} '.format(url, data, res['retMessage'], data['threeEdge1Update'], res['retData'][0]['threeEdge1Update'])
            assert res['retData'][0]['threeEdge2Update'] == str(data['threeEdge2Update']), 'url: {} \n 入参: {}\n 结果: {}\n 三层次长边不正确 \n 提交的三层次长边: {} \n 现三层次长边: {} '.format(url, data, res['retMessage'], data['threeEdge2Update'], res['retData'][0]['threeEdge2Update'])
            assert res['retData'][0]['threeEdge3Update'] == str(data['threeEdge3Update']), 'url: {} \n 入参: {}\n 结果: {}\n 三层最短边不正确 \n 提交的三层最短边: {} \n 现三层最短边: {} '.format(url, data, res['retMessage'], data['threeEdge3Update'], res['retData'][0]['threeEdge3Update'])
            assert res['retData'][0]['threeVolumeUpdate'] == str(data['threeVolumeUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 三层体积不正确 \n 提交的三层体积: {} \n 现三层体积: {} '.format(url, data, res['retMessage'], data['threeVolumeUpdate'], res['retData'][0]['threeVolumeUpdate'])
            assert res['retData'][0]['threeWeightUpdate'] == str(data['threeWeightUpdate']), 'url: {} \n 入参: {}\n 结果: {}\n 三层重量不正确 \n 提交的三层重量: {} \n 现三层重量: {} '.format(url, data, res['retMessage'], data['threeWeightUpdate'], res['retData'][0]['threeWeightUpdate'])
        else:
            assert False, '包装层数信息异常: {}'.format(res['retData'][0]['packageLayersUpdate'])
        print('======================核对SKU提交数据结束=======================')
        print('验证SKU管理完成')

    def SupplyInfoQuerry(self, comParison):
        print('开始验证供货信息查询数据')
        # 查询创建得SPU是否存在
        endTime = time.time() + 90
        calc = 1
        total = 30
        while True:
            if time.time() < endTime:
                url = self.host + '/sysback/supplyarea/getSupplySaleAreaProudctListInner?menuId=281&buttonId=2'
                data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"categoryName\",\"value\":\"\"},{\"name\":\"productName\",\"value\":\"\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"skuNo\",\"value\":\"" +comParison['skuNo'] + "\"},{\"name\":\"supplierCode\",\"value\":\"\"},{\"name\":\"supplierName\",\"value\":\"\"},{\"name\":\"saleAreaName\",\"value\":\"\"},{\"name\":\"saleProvinceName\",\"value\":\"\"},{\"name\":\"categoryName_q\",\"value\":\"Like\"},{\"name\":\"productName_q\",\"value\":\"Like\"},{\"name\":\"brandName_q\",\"value\":\"Like\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"skuNo_q\",\"value\":\"EQ\"},{\"name\":\"supplierCode_q\",\"value\":\"EQ\"},{\"name\":\"supplierName_q\",\"value\":\"Like\"},{\"name\":\"saleAreaName_q\",\"value\":\"Like\"},{\"name\":\"saleProvinceName_q\",\"value\":\"Like\"}]", "sortName": "", "sortType": ""}
                try:
                    res = requests.post(url, headers=self.json_header, json=data).json()
                except Exception as e:
                    assert False, '接口请求失败, {}\n{}'.format(url, e)
                assert res['retMessage'] == '', '查询供货信息报错:\n{}'.format(res['retMessage'])
                time.sleep(3)
                if res['retData']['results'] != []:
                    assert res['retData']['totalNum'] != '', 'url : {} \n 入参 : {} \n 结果 : {} \n 供货信息未查询到sku信息 \n SkunNo: {}'.format(url, data, res['retMessage'], comParison['skuNo'])
                    print('查询供货信息成功\nSkuNo: {} '.format(comParison['skuNo']))
                    break
                print('查询供货信息失败,重新尝试请求{}/{}'.format(calc, total))
                calc += 1
            else:
                assert False, '查询供货信息失败,请检查sku准入是否完成! \nskuNo:{} '.format(comParison['skuNo'])

        for i in res['retData']['results']:
            assert i['brandName'] == comParison['brandName'], 'url: {}\n入参: {}\n结果: {}\n品牌名称不相同\n原品牌名称: {}\n现品牌名称: {}'.format(url, data, res['retMessage'], comParison['brandName'], i['brandName'])
            assert i['supplierCode'] == '11297', 'url: {}\n入参: {}\n结果: {}\n供应商编码不相同\n原供应商编码: {}\n现供应商编码: {}'.format(url, data, res['retMessage'], comParison['supplierCode'], i['supplierCode'])
            # assert i['specDetailStr'] == str(comParison['specDetailStr']), 'url: {}\n入参: {}\n结果: {}\n商品规格不相同\n原商品规格: {}\n现商品规格: {}'.format(url, data, res['retMessage'], comParison['specDetailStr'], i['specDetailStr'])
            assert i['specDetailStr'] != '', 'url: {}\n入参: {}\n结果: {}\n商品规格为空'.format(url, data, res['retMessage'])
            assert set(i['saleAreaCodes']) == set(comParison['saleAreaCode']), 'url: {}\n入参: {}\n结果: {}\n销售区域不相同\n原销售区域: {}\n现销售区域: {}'.format(url, data, res['retMessage'], comParison['saleAreaCode'], i['saleAreaCodes'])
            assert i['mainUnit'] == str(comParison['mainUnitName']), 'url: {}\n入参: {}\n结果: {}\n主计量单位不相同\n原主计量单位: {}\n现主计量单位: {}'.format(url, data, res['retMessage'], comParison['mainUnitId'], i['mainUnitId'])
            assert i['purchasePriceType'] == str(comParison['purchasePriceType']), 'url: {}\n入参: {}\n结果: {}\n进价类型不相同\n原进价类型: {}\n现进价类型: {}'.format(url, data, res['retMessage'], comParison['purchasePriceType'], i['purchasePriceType'])
            assert i['salepriceSkuDTO']['addPriceTypeName'] == str(comParison['addPriceTypeStr']), 'url: {}\n入参: {}\n结果: {}\n加价类型不相同\n原加价类型: {}\n现加价类型: {}'.format(url, data, res['retMessage'], comParison['addPriceTypeStr'], i['salepriceSkuDTO']['addPriceTypeName'])

            # 加逻辑判断，根据姜提供的集合判断是否有参照
            # 将传过来的参照城市信息转成列表
            tempSelf = list(comParison['tempSelf'])
            tempOther = list(comParison['tempOther'])
            for i in res['retData']['results']:
                if i['templateCityUuid'] in tempSelf:
                    assert int(i['mainPurchasePrice']) == comParison['mainPurchasePrice'], 'url: {}\n入参: {}\n结果: {}\n主计量进价不相同\n原主计量进价: {}\n现主计量进价: {}'.format(url, data, res['retMessage'], comParison['mainPurchasePrice'], i['salepriceSkuDTO']['mainUnitPrice'])
                    assert int(i['salepriceSkuDTO']['mainUnitPrice']) == comParison['mainUnitCostPrice'], 'url: {}\n入参: {}\n结果: {}\n主计量成本价不相同\n原主计量成本价: {}\n现主计量成本价: {}'.format(url, data, res['retMessage'], comParison['mainUnitCostPrice'], int(i['salepriceSkuDTO']['mainUnitPrice']))
                    assert int(i['salepriceSkuDTO']['salePrice']) == int(comParison['salePrice']), 'url: {}\n入参: {}\n结果: {}\n主计量售价不相同\n原主计量售价: {}\n现主计量售价: {}'.format(url, data, res['retMessage'], comParison['salePrice'], i['salepriceSkuDTO']['mainUnitPrice'])
                elif i['templateCityUuid'] in tempOther:
                    assert int(i['mainPurchasePrice']) == comParison['mainPurchasePrice'], 'url: {}\n入参: {}\n结果: {}\n主计量进价不相同\n原主计量进价: {}\n现主计量进价: {}'.format(url, data, res['retMessage'], comParison['mainPurchasePrice'], i['salepriceSkuDTO']['mainUnitPrice'])
                    assert int(i['salepriceSkuDTO']['mainUnitPrice']) == comParison['mainUnitCostPrice'], 'url: {}\n入参: {}\n结果: {}\n主计量成本价不相同\n原主计量成本价: {}\n现主计量成本价: {}'.format(url, data, res['retMessage'], comParison['mainUnitCostPrice'], int(i['salepriceSkuDTO']['mainUnitPrice']))
                    assert int(i['salepriceSkuDTO']['salePrice'])*2 == int(comParison['salePrice']), 'url: {}\n入参: {}\n结果: {}\n主计量售价不相同\n原主计量售价: {}\n现主计量售价: {}'.format(url, data, res['retMessage'], comParison['salePrice'], int(i['salepriceSkuDTO']['mainUnitPrice'])*2)
                else:
                    assert False, '获取参照数据异常\n参照自己: {}\n参照别人: {}\n当前参照数据:\nskuNo: {}\n销售省: {}\n参照区域: {}'.format(comParison['tempSelf'], comParison['tempOther'], comParison['skuNo'], i['saleProvinceUuid'], i['templateCityUuid'])
        print('验证供货信息查询数据结束')

        # print('=====================================')
        # print(comParison['tempSelf'])
        # print('=====================================')
        # print(comParison['tempOther'])