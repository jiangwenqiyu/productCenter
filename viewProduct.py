import requests
from environmentConfig import LoginInfo
import time
import random
from random import randint,random,uniform,sample
from makeProduct import CommonFunction
import re

class ProductManagement(LoginInfo):
    def run(self, JycList):
        # self.makeProduct('30418')   # pre
        self.SpuManagement(JycList)  #已完成
        self.SkuManagement(JycList)  #已完成
        
    def SpuManagement(self, JycList):
        print('开始验证SPU管理')
        #查询创建得SPU是否存在
        endTime = time.time()+90
        while True:
            if time.time() < endTime:
                url = self.host+'/sysback/finish/spu/mgr/getSpuList?menuId=252&buttonId=2'
                data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\""+JycList['spuNo']+"\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
                res = requests.post(url, headers=self.json_header, json=data).json()
                # print('==========================')
                # print(JycList['spuNo'])
                # print(res)
                time.sleep(3)
                if res['retData']['results'] != []:
                    assert res['retData']['results'][0]['spuNo'] == JycList['spuNo'], 'url : {} \n 入参 : {} \n 结果 : {} \n 查询Spu信息失败 \n SpunNo: {}'.format(url, data, res['retMessage'], JycList['spuNo'])
                    print('查询成功')
                    break
            else:
                # print('请求失败,请检查spu准入是否完成 \nspuNo:{} '.format(JycList['spuNo']))
                assert False, '查询失败,请检查spu准入是否完成! \nspuNo:{} '.format(JycList['spuNo'])

        # 验证是否能够修改Spu, 从SPU查看页面点击修改
        url = self.host + '/sysback/spu/query/checkPerm?spuNo={}&menuId=252&buttonId=148'.format(JycList['spuNo'])
        data = {"spuNo": "{}".format(JycList['spuNo'])}
        res = requests.post(url, headers=self.json_header, json=data).json()
        assert res['retMessage'] == '成功', 'url : {} \n 入参 : {} \n 结果 : {} \n 修改Spu失败'.format(url, data, res['retMessage'])

        ######################################## 后续等姜完善后再进行调试 ###########################
        # 修改Spu基本信息
        url = self.host + 'sysback/update/product/basicinfo/queryBasicInfoListFromSpu?menuId=252&buttonId=148'
        data = {'productKey':"{}".format(JycList['productUuid'])}
        try:
            res = requests.post(url, headers=self.form_header, data=data ).json()
        except Exception as e:
            assert False, '修改基本信息，接口请求失败\nurl:{}\ndata:{}\nexception:{}'.format(url, data, e)

        assert res['retStatus'] == '1', '修改基本信息，获取数据失败\nurl:{}\ndata:{}\nres:{}'.format(url, data, res)
        print('修改基本信息，获取数据成功')
        # for i in res['retData'][0]['attrList']:
        #     assert i['attrName'] == '', ''
        # # 判断Spu基本信息是否正确
        # assert res['retData'][0]['attrList'] !=[],'url : {} \n 入参 : {} \n 结果 : {} \n 基础属性获取失败'.format(url , data , res['retMessage'])
        # assert res['redata'][0]['spuNo'] == JycList['spuNo'],'spuNO 不正确，不符合创建时的 Spu, 创建时的 Spu : {}, 修改时的 Spu : {}'.format(JycList['spuNo'], res['redata'][0]['spuNo'])
        # assert res['redata'][0]['productUuid'] == JycList['productUuid'] ,'productUuid 不正确，不符合创建时的 productUuid, 创建时的 productUuid : {}, 修改时的 productUuid : {}'.format(JycList['productUuid'], res['redata'][0]['productUuid'])
        # # 循环对比 属性原值和页面获取的值是否一致 ？？？ 需要后续修改
        # for ii in  res['retData'][0]['attrList']:
        #     assert ii['valueName'] == CommonFunction.getString()[2] ,'原值 不正确，不符合创建时的 原值, 创建时的 原值 : {}, 修改时的 原值 : {}'.format(CommonFunction.getString()[2],res['redata'][0]['valueName'])
        #
        # 修改基本信息属性值
        for i in res['retData'][0]['attrList']:
            # print (i)
            if i['attrType'] == '01':
                i['valueNameUpdate'] = CommonFunction.getString(7)

            if i['attrType'] == '02':
                # print (i['allValueOptions'][random.randint(0,len(i['allValueOptions'])-1)]['optionHtml'])
                i['valueNameUpdate'] = i['allValueOptions'][random.randint(0, len(i['allValueOptions'])-1)]['optionHtml']
        NotspecList = res['retData'][0]['attrList']

        # 修改Spu信息-暂存
        url = self.host + '/sysback/update/product/basicinfo/saveBasicInfo?menuId=252&buttonId=148'
        data = {"inputList": [{"productKey": ""+JycList['productUuid']+"", "notSpecList":NotspecList}]}

        res = requests.post(url, headers=self.json_header, json=data).json()
        # 判断是否有单据暂存，如果有就获取单据号重新请求
        if re.findall(r'查到该商品存在进行中的单据', res['retMessage']):
            Record = re.findall(r'(RECORD.*?)]', res['retMessage'])[0]
        newdata= {"recordNo": ""+Record+"", "inputList": [{"productKey": ""+JycList['productUuid']+"", "notSpecList": NotspecList}]}

        res = requests.post(url, headers=self.json_header, json=newdata).json()

        assert res['retStatus'] == '1','url : {} \n 入参 : {} \n 结果: {} \n 暂存失败'.format(url , data , res['retMessage'])

        # 修改Spu信息-提交
        url = self.host + '/sysback/update/product/basicinfo/commitBasicInfo?recordNo={}'.format(Record)
        data = {}
        res = requests.post(url, headers=self.json_header, json=data).json()
        assert res['retStatus'] == '1', '修改基本信息提交失败, url: {} \n ,结果: {} '.format(url, res['retMessage'])
        assert res['retData']['commitState'] == 'COMMIT', '修改基本信息提交失败, url: {} \n ,结果: {} '.format(url, res['retMessage'])

        # 验证提交Spu数据是否生效
        url = self.host + '/sysback/update/product/basicinfo/queryBasicInfoListFromSpu?menuId=252&buttonId=148' #.format(JycList['spuNo'])
        data = {"productKey": "{}".format(JycList['productUuid'])}
        res = requests.post(url, headers=self.form_header, data = data).json()
        assert res['retData'][0]['attrList']['spuNo'] == JycList['spuNo'], 'spuNo 不正确 原SpuNo:{} \n 现SpuNo: {}'.format(JycList['spuNo'], res['retData'][0]['attrList']['spuNo'])
        # for i,j in res['retData'][0]['attrList'],NotspecList:
        #     print('现值: {} '.format(i['valueNameUpdate']))
        #     print('原值: {} '.format(j['valueNameUpdata']))
            # i['valueNameUpdate'] == j['valueNameUpdata']

        # Spu查看页面详情-商品基本信息
        url = self.host + '/sysback/finish/spu/mgr/getSpuList?menuId=252&buttonId=2'
        data = {"nowPage":1 ,"pageShow":10,"searchParam":"[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\""+ JycList['spuNo'] +"\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
        res = requests.post(url, headers=self.json_header, json=data).json()
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
        res = requests.post(url, headers=self.json_header, json=dataa).json()

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
        res = requests.post(url, headers = self.json_header, json=data).json()
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
        assert res['retData']['salepriceList'][0]['mainUnitPrice'] == JycList['mainUnitCostPrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 成本价不正确 \n 原成本价 : {} \n 现成本价 : {} '.format(url, data, res['retMessage'], JycList['mainUnitCostPrice'], res['retData']['salepriceList'][0]['mainUnitPrice'])
        assert res['retData']['salepriceList'][0]['salePrice'] == JycList['salePrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 售价不正确 \n 原售价 : {} \n 现售价 : {} '.format(url, data, res['retMessage'], JycList['salePrice'], res['retData']['salepriceList'][0]['salePrice'])
        # # 分销价后续姜传值，本期不管
        # assert res['retData']['salepriceList'][0]['cashDistribMoney'] == cashDistribMoney, 'url : {} \n 入参 : {} \n 结果 : {} \n 分销价不正确 \n 原分销价 : {} \n 现分销价 : {} '.format(url, data, res['retMessage'], cashDistribMoney, res['retData']['salepriceList'][0]['cashDistribMoney'])
        # # #########################
        assert res['retData']['salepriceList'][0]['cashPrice'] == JycList['cashPrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 现金价不正确 \n 原现金价 : {} \n 现现金价 : {} '.format(url, data, res['retMessage'], JycList['cashPrice'], res['retData']['salepriceList'][0]['cashPrice'])
        assert res['retData']['salepriceList'][0]['limitShowPrice'] == JycList['limitShowPrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 限制展示价不正确 \n 原限制展示价 : {} \n 现限制展示价 : {} '.format(url, data, res['retMessage'], JycList['limitShowPrice'], res['retData']['salepriceList'][0]['limitShowPrice'])
        assert res['retData']['salepriceList'][0]['limitTradePrice'] == JycList['limitTradePrice'], 'url : {} \n 入参 : {} \n 结果 : {} \n 限制交易价不正确 \n 原限制交易价 : {} \n 现限制交易价 : {} '.format(url, data, res['retMessage'], JycList['limitTradePrice'], res['retData']['salepriceList'][0]['limitTradePrice'])



        # Spu查看页面详情-图文介绍
        url = self.host + '/sysback/productinfo/getPicInfoByProductUuid?menuId=252&buttonId=2&productUuid={}'.format(uUid)
        data = {}
        res = requests.get(url, headers=self.json_header, json=data).json()
        # 主图 等后续姜传值
        assert res['retData']['mainImage']['trimmingKey'] != '', 'url : {} \n 结果 : {}主图不存在'.format(url, res['retMessage'])


        # 商品类型查询
        url = self.host + 'sysback/finish/spu/mgr/getSpuList?menuId=252&buttonId=2'
        rdlist = ['01', '02', '03', '04', '05', '08']
        data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"EQ\"},{\"name\":\"productNameFinal\",\"value\":\"\"},{\"name\":\"productNameFinal_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\""+ str(random.sample(rdlist, 1))[2:4] +"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
        res = requests.post(url, headers=self.json_header, json=data).json()
        assert res['retData']['results'] != [], 'url : {} \n 入参 : {} \n 结果 : {} \n 商品类型查询失败'.format(url, data, res['retMessage'])
        print('验证SPU管理结束')


    def SkuManagement(self, JycList):
        print('开始验证SKU管理')
        # skuNo 查询
        endTime = time.time() + 90
        while True:
            if time.time() < endTime:
                url = self.host + '/sysback/finish/sku/list/getSkuListForSkuManage?menuId=253&buttonId=2'
                data ={"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"Like\"},{\"name\":\"skuNo\",\"value\":\""+JycList['skuNo']+"\"},{\"name\":\"skuNo_q\",\"value\":\"Like\"},{\"name\":\"productName\",\"value\":\"\"},{\"name\":\"productName_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
                res = requests.post(url, headers=self.json_header, json=data).json()
                print(res)
                time.sleep(9)
                if res['retData']['results'] != []:
                    assert res['retData']['results'][0]['skuCode'] == JycList['skuNo'], 'url : {} \n 入参 : {} \n 结果 : {} \n 查询Spu信息失败'.format(url, data, res['retMessage'])
                    break
            else:
                # url = self.host + '/sysback/finish/sku/list/getSkuListForSkuManage?menuId=253&buttonId=2'
                # data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"productAddState\",\"value\":\"\"},{\"name\":\"productAddState_q\",\"value\":\"EQ\"},{\"name\":\"categoryPath\",\"value\":\"\"},{\"name\":\"categoryPath_q\",\"value\":\"Like\"},{\"name\":\"categoryUuid\",\"value\":\"\"},{\"name\":\"categoryUuid_q\",\"value\":\"Like\"},{\"name\":\"spuNo\",\"value\":\"\"},{\"name\":\"spuNo_q\",\"value\":\"Like\"},{\"name\":\"skuNo\",\"value\":\"" +JycList['skuNo'] + "\"},{\"name\":\"skuNo_q\",\"value\":\"Like\"},{\"name\":\"productName\",\"value\":\"\"},{\"name\":\"productName_q\",\"value\":\"Like\"},{\"name\":\"productType\",\"value\":\"\"},{\"name\":\"productType_q\",\"value\":\"EQ\"},{\"name\":\"brandName\",\"value\":\"\"},{\"name\":\"brandName_q\",\"value\":\"Like\"}]","sortName": "", "sortType": ""}
                # res = requests.post(url, headers=self.json_header, json=data).json()
                # print(res)
                assert False, '请求失败,请检查sku准入是否完成! \nskuNo:{} '.format(JycList['skuNo'])
        # sku 管理信息
        # print('开始对比数据')
        url = self.host + '/sysback/update/product/allmanaging/queryAllManagingListFromSpu?menuId=253&buttonId=148'
        data = {"productKey": ""+JycList['productUuid']+""}
        res = requests.post(url, headers=self.form_header, data=data).json()
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
        assert res['retData'][0]['marketingList'][0]['valueName'] == JycList['marketing_saleplat'], 'url : {} \n 入参: {} \n 结果: {} \n 售卖平台不同\n 售卖平台原值: {} \n 售卖平台现值: {}'.format(url, data, res['retMessage'], JycList['marketing_saleplat'], res['retData'][0]['marketingList'][0]['valueName'])
        # 对比归类名称
        assert res['retData'][0]['taxList'][0]['valueName'] == JycList['tax_classify'], 'url : {} \n 入参: {} \n 结果: {} \n 归类名称不同\n 归类名称原值: {} \n 归类名称现值: {}'.format(url, data, res['retMessage'], JycList['tax_classify'], res['retData'][0]['taxList'][0]['valueName'])
        #########################
        # 对比税类代码  后续姜提供
        #assert res['retData'][0]['taxList'][1]['valueName'] != '', 'url : {} \n 入参: {} \n 结果: {} \n 税类代码为空\n '.format(url, data, res['retMessage'])
        #########################
        # 对比销售税类  后续姜提供
        #assert res['retData'][0]['taxList'][2]['valueName'] != '', 'url : {} \n 入参: {} \n 结果: {} \n 销售税类为空\n '.format(url, data, res['retMessage'])
        #########################
        # print('对比数据结束')

        # 暂存修改的Sku
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
        manageList[3]['valueNameUpdate'] = CommonFunction.getString(7)  # 预发布
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
        res = requests.post(url2, headers=self.json_header, json=data2, verify=False).json()
        # 获取 入参json 后续对比数据用
        TestData = data2
        Record = res['retData']['recordNo']
        assert res['retData']['commitState'] == 'NOT', 'url : {} \n 入参: {} \n 结果: {} \n 暂存失败\n '.format(url, data, res['retMessage'])
        assert res['retData']['recordNo'] != '','url : {} \n 入参: {} \n 结果: {} \n 修改管理信息暂存失败 \n '.format(url, data, res['retMessage'])

        # 提交暂存的内容
        # print ('开始对比提交值和现值是否一致')
        url = self.host + '/sysback/update/product/allmanaging/commitAllManaging?recordNo={}&menuId=253&buttonId=148'.format(Record)
        data = [{"authDepartments":[{"hrDepartmentNumber":""+hrDepartmentNumber+"","hrDepartmentName":""+hrDepartmentName+""}]}]
        res = requests.post(url, headers=self.json_header, json=data).json()
        # print(res)
        # print(res['retData']['commitStateStr'])
        assert res['retData']['commitStateStr'] != '', 'url : {} \n 入参: {} \n 结果: {} \n 修改管理信息提交失败，暂存失败 \n '.format(url, data, res['retMessage'])
        assert res['retData']['recordNo'] == Record, 'url : {} \n 入参: {} \n 结果: {} \n 暂存与提交单据号不相符 \n 原单据号: {} \n 现单据号: {} '.format(url, data, res['retMessage'], Record, res['retData']['recordNo'])

        # 验证提交数据是否正确
        url = self.host + '/sysback/update/product/allmanaging/queryAllManagingListFromSpu?menuId=253&buttonId=148'
        data = {"productKey": "" + JycList['productUuid'] + ""}
        res = requests.post(url, headers=self.form_header, data=data).json()
        # 对比提交数据和现在数据是否一致
        #比对Sku管理区域
        assert res['retData'][0]['manageList'][0]['valueName'] == TestData['retData'][0]['manageList'][0]['valueNameUpdate'], 'url : {} \n 入参 : {} \n 结果 : {} \n sku管理区域不同 \n 管理区域原值: {} \n 管理区域现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][0]['valueNameUpdate'], res['retData'][0]['manageList'][0]['valueName'])
        # 对比合作模式
        assert res['retData'][0]['manageList'][1]['valueName'] == TestData['retData'][0]['manageList'][1]['valueNameUpdate'], 'url : {} \n 入参 : {} \n 结果 : {} \n sku合作模式不同 \n 合作模式原值: {} \n 合作模式现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][1]['valueNameUpdate'], res['retData'][0]['manageList'][1]['valueName'])
        # 对比经营模式
        assert res['retData'][0]['manageList'][2]['valueName'] == TestData['retData'][0]['manageList'][2]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 经营模式不同\n 经营模式原值: {} \n 经营模式现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][2]['valueNameUpdate'], res['retData'][0]['manageList'][2]['valueName'])
        # 对比包装清单
        assert res['retData'][0]['manageList'][3]['valueName'] == TestData['retData'][0]['manageList'][3]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 包装清单不同\n 包装清单原值: {} \n 包装清单现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][3]['valueNameUpdate'], res['retData'][0]['manageList'][3]['valueName'])
        # 对比售价管理周期
        assert res['retData'][0]['manageList'][4]['valueName'] == TestData['retData'][0]['manageList'][4]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 售价管理周期不同\n 售价管理周期原值: {} \n 售价管理周期现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][4]['valueNameUpdate'], res['retData'][0]['manageList'][4]['valueName'])
        # 对比档次外部定位
        assert res['retData'][0]['manageList'][5]['valueName'] == TestData['retData'][0]['manageList'][5]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 档次外部定位不同\n 档次外部定位原值: {} \n 档次外部定位现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][5]['valueNameUpdate'], res['retData'][0]['manageList'][5]['valueName'])
        # 对比档次内部定位
        assert res['retData'][0]['manageList'][6]['valueName'] == TestData['retData'][0]['manageList'][6]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 档次内部定位不同\n 档次内部定位原值: {} \n 档次内部定位现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][6]['valueNameUpdate'], res['retData'][0]['manageList'][6]['valueName'])
        # 对比囤货期
        assert res['retData'][0]['manageList'][7]['valueName'] == TestData['retData'][0]['manageList'][7]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 囤货期不同\n 囤货期原值: {} \n 囤货期现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][7]['valueNameUpdate'], res['retData'][0]['manageList'][7]['valueName'])
        # 对比是否季节性商品
        assert res['retData'][0]['manageList'][8]['valueName'] == TestData['retData'][0]['manageList'][8]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 是否季节性商品不同\n 是否季节性商品原值: {} \n 是否季节性商品现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][8]['valueNameUpdate'], res['retData'][0]['manageList'][8]['valueName'])
        # 对比下架期
        assert res['retData'][0]['manageList'][9]['valueName'] == TestData['retData'][0]['manageList'][9]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 下架期不同\n 下架期原值: {} \n 下架期现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['manageList'][9]['valueNameUpdate'], res['retData'][0]['manageList'][9]['valueName'])
        # 对比售卖平台
        assert res['retData'][0]['marketingList'][0]['valueName'] == TestData['retData'][0]['marketingList'][0]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 售卖平台不同\n 售卖平台原值: {} \n 售卖平台现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['marketingList'][0]['valueNameUpdate'], res['retData'][0]['marketingList'][0]['valueName'])
        # 对比归类名称
        assert res['retData'][0]['taxList'][0]['valueName'] == TestData['retData'][0]['taxList'][0]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 归类名称不同\n 归类名称原值: {} \n 归类名称现值: {}'.format(url, data, res['retMessage'], TestData['retData'][0]['taxList'][0]['valueNameUpdate'], res['retData'][0]['taxList'][0]['valueName'])
        # 对比税类代码
        assert res['retData'][0]['taxList'][1]['valueName'] == TestData['retData'][0]['taxList'][1]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 税类代码不同\n 原税类代码: {} \n 现税类代码: {} '.format(url, data, res['retMessage'], TestData['retData'][0]['taxList'][1]['valueNameUpdate'],res['retData'][0]['taxList'][1]['valueName'])
        # 对比销售税类
        assert res['retData'][0]['taxList'][2]['valueName'] == TestData['retData'][0]['taxList'][2]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 销售税类不同\n 原销售税类: {} \n 现销售税类: {}'.format(url, data, res['retMessage'],TestData['retData'][0]['taxList'][2]['valueNameUpdate'],res['retData'][0]['taxList'][2]['valueName'])
        # 对比存储属性
        assert res['retData'][0]['logisticsList'][3]['valueName'] == TestData['retData'][0]['logisticsList'][3]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 存储属性不同\n 原存储属性: {} \n 现存储属性: {}'.format(url, data, res['retMessage'],TestData['retData'][0]['logisticsList'][3]['valueNameUpdate'], res['retData'][0]['logisticsList'][3]['valueName'])
        # 对比存量属性
        assert res['retData'][0]['logisticsList'][4]['valueName'] == TestData['retData'][0]['logisticsList'][4]['valueNameUpdate'], 'url : {} \n 入参: {} \n 结果: {} \n 存量属性不同\n 原存量属性: {} \n 现存量属性: {}'.format(url, data, res['retMessage'],TestData['retData'][0]['logisticsList'][4]['valueNameUpdate'], res['retData'][0]['logisticsList'][4]['valueName'])
        # print('对比提交值和现值结束')
        #
        # print('======================核对SKU修改数据开始=======================')
        # 修改SKU信息
        url = self.host + '/sysback/update/product/package/queryPackageListFromSpu?menuId=252&buttonId=148'
        data = {"productKey": ""+JycList['productUuid']+""}
        res = requests.post(url, headers=self.json_header, json=data).json()
        assert res['retData'][0]['safetyRate'] == JycList['safetyRate'], 'url: {} \n 入参: {}\n 结果: {}\n 安全率/金额不正确 \n 原安全率/金额: {} \n 现安全率/金额: {} '.format(url, data, res['retMessage'], JycList['safetyRate'], res['retData'][0]['safetyRate'])
        assert res['retData'][0]['barcode'] == JycList['barcode'], 'url: {} \n 入参: {}\n 结果: {}\n 国际条形码不正确 \n 原国际条形码: {} \n 现国际条形码: {} '.format(url, data, res['retMessage'], JycList['barcode'], res['retData'][0]['barcode'])
        assert res['retData'][0]['saleMin'] == JycList['saleMin'], 'url: {} \n 入参: {}\n 结果: {}\n 最小起售量不正确 \n 原最小起售量: {} \n 现最小起售量: {} '.format(url, data, res['retMessage'], JycList['saleMin'], res['retData'][0]['saleMin'])
        assert res['retData'][0]['saleRestrict'] != '','url: {} \n 入参: {}\n 结果: {}\n 销售限制类型不正确'.format(url, data, res['retMessage'])
        assert res['retData'][0]['pieceInfo'] == JycList['pieceInfo'], 'url: {} \n 入参: {}\n 结果: {}\n 件装数量不正确 \n 原件装数量: {} \n 现件装数量: {} '.format(url, data, res['retMessage'], JycList['pieceInfo'], res['retData'][0]['pieceInfo'])
        assert res['retData'][0]['packageLayers'] == JycList['packageLayers'], 'url: {} \n 入参: {}\n 结果: {}\n 层数不正确 \n 原层数: {} \n 现层数: {} '.format(url, data, res['retMessage'], JycList['packageLayers'], res['retData'][0]['packageLayers'])
        assert res['retData'][0]['singlePackageUnit'] != '', 'url: {} \n 入参: {}\n 结果: {}\n 单品包装单位为空 '.format(url, data, res['retMessage'])
        assert res['retData'][0]['singlePackageCount'] == JycList['singlePackageCount'], 'url: {} \n 入参: {}\n 结果: {}\n 单品包装数量不正确 \n 原单品包装数量: {} \n 现单品包装数量: {} '.format(url, data, res['retMessage'], JycList['singlePackageCount'], res['retData'][0]['singlePackageCount'])
        assert res['retData'][0]['singleEdge1'] == JycList['singleEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 单品最长边不正确 \n 原单品最长边: {} \n 现单品最长边: {} '.format(url, data, res['retMessage'], JycList['singleEdge1'], res['retData'][0]['singleEdge1'])
        assert res['retData'][0]['singleEdge2'] == JycList['singleEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 单品次长边不正确 \n 原单品次长边: {} \n 现单品次长边: {} '.format(url, data, res['retMessage'], JycList['singleEdge2'], res['retData'][0]['singleEdge2'])
        assert res['retData'][0]['singleEdge3'] == JycList['singleEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 单品最短边不正确 \n 原单品最短边: {} \n 现单品最短边: {} '.format(url, data, res['retMessage'], JycList['singleEdge3'], res['retData'][0]['singleEdge3'])
        assert res['retData'][0]['singleVolume'] == JycList['singleVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 单品体积不正确 \n 原单品体积: {} \n 现单品体积: {} '.format(url, data, res['retMessage'], JycList['singleVolume'], res['retData'][0]['singleVolume'])
        assert res['retData'][0]['singleWeight'] == JycList['singleWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 单品重量不正确 \n 原单品重量: {} \n 现单品重量: {} '.format(url, data, res['retMessage'], JycList['singleWeight'], res['retData'][0]['singleWeight'])
        assert res['retData'][0]['onePackageUnit'] == JycList['onePackageUnit'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装单位不正确 \n 原一层包装单位: {} \n 现一层包装单位: {} '.format(url, data, res['retMessage'], JycList['onePackageUnit'], res['retData'][0]['onePackageUnit'])
        assert res['retData'][0]['onePackageCount'] == JycList['onePackageCount'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装数量不正确 \n 原一层包装数量: {} \n 现一层包装数量: {} '.format(url, data, res['retMessage'], JycList['onePackageCount'], res['retData'][0]['onePackageCount'])
        assert res['retData'][0]['oneEdge1'] == JycList['oneEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 一层最长边不正确 \n 原一层最长边: {} \n 现一层最长边: {} '.format(url, data, res['retMessage'], JycList['oneEdge1'], res['retData'][0]['oneEdge1'])
        assert res['retData'][0]['oneEdge2'] == JycList['oneEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 一层次长边不正确 \n 原一层次长边: {} \n 现一层次长边: {} '.format(url, data, res['retMessage'], JycList['oneEdge2'], res['retData'][0]['oneEdge2'])
        assert res['retData'][0]['oneEdge3'] == JycList['oneEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 一层最短边不正确 \n 原一层最短边: {} \n 现一层最短边: {} '.format(url, data, res['retMessage'], JycList['oneEdge3'], res['retData'][0]['oneEdge3'])
        assert res['retData'][0]['oneVolume'] == JycList['oneVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 一层体积不正确 \n 原一层体积: {} \n 现一层体积: {} '.format(url, data, res['retMessage'], JycList['oneVolume'], res['retData'][0]['oneVolume'])
        assert res['retData'][0]['oneWeight'] == JycList['oneWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 一层重量不正确 \n 原一层重量: {} \n 现一层重量: {} '.format(url, data, res['retMessage'], JycList['oneWeight'], res['retData'][0]['oneWeight'])
        assert res['retData'][0]['twoPackageUnit'] == JycList['twoPackageUnit'], 'url: {} \n 入参: {}\n 结果: {}\n 二层包装单位不正确 \n 原二层包装单位: {} \n 现二层包装单位: {} '.format(url, data, res['retMessage'], JycList['twoPackageUnit'], res['retData'][0]['twoPackageUnit'])
        assert res['retData'][0]['twoPackageCount'] == JycList['twoPackageCount'], 'url: {} \n 入参: {}\n 结果: {}\n 二层包装数量不正确 \n 原二层包装数量: {} \n 现二层包装数量: {} '.format(url, data, res['retMessage'], JycList['twoPackageCount'], res['retData'][0]['twoPackageCount'])
        assert res['retData'][0]['twoEdge1'] == JycList['twoEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 二层最长边不正确 \n 原二层最长边: {} \n 现二层最长边: {} '.format(url, data, res['retMessage'], JycList['twoEdge1'], res['retData'][0]['twoEdge1'])
        assert res['retData'][0]['twoEdge2'] == JycList['twoEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 二层次长边不正确 \n 原二层次长边: {} \n 现二层次长边: {} '.format(url, data, res['retMessage'], JycList['twoEdge2'], res['retData'][0]['twoEdge2'])
        assert res['retData'][0]['twoEdge3'] == JycList['twoEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 二层最短边不正确 \n 原二层最短边: {} \n 现二层最短边: {} '.format(url, data, res['retMessage'], JycList['twoEdge3'], res['retData'][0]['twoEdge3'])
        assert res['retData'][0]['twoVolume'] == JycList['twoVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 二层体积不正确 \n 原二层体积: {} \n 现二层体积: {} '.format(url, data, res['retMessage'], JycList['twoVolume'], res['retData'][0]['twoVolume'])
        assert res['retData'][0]['twoWeight'] == JycList['twoWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 二层重量不正确 \n 原二层重量: {} \n 现二层重量: {} '.format(url, data, res['retMessage'], JycList['twoWeight'], res['retData'][0]['twoWeight'])
        assert res['retData'][0]['threePackageUnit'] == JycList['threePackageUnit'], 'url: {} \n 入参: {}\n 结果: {}\n 三层包装单位不正确 \n 原三层包装单位: {} \n 现三层包装单位: {} '.format(url, data, res['retMessage'], JycList['threePackageUnit'], res['retData'][0]['threePackageUnit'])
        assert res['retData'][0]['threePackageCount'] == JycList['threePackageCount'], 'url: {} \n 入参: {}\n 结果: {}\n 三层包装数量不正确 \n 原三层包装数量: {} \n 现三层包装数量: {} '.format(url, data, res['retMessage'], JycList['threePackageCount'], res['retData'][0]['threePackageCount'])
        assert res['retData'][0]['threeEdge1'] == JycList['threeEdge1'], 'url: {} \n 入参: {}\n 结果: {}\n 三层最长边不正确 \n 原三层最长边: {} \n 现三层最长边: {} '.format(url, data, res['retMessage'], JycList['threeEdge1'], res['retData'][0]['threeEdge1'])
        assert res['retData'][0]['threeEdge2'] == JycList['threeEdge2'], 'url: {} \n 入参: {}\n 结果: {}\n 三层次长边不正确 \n 原三层次长边: {} \n 现三层次长边: {} '.format(url, data, res['retMessage'], JycList['threeEdge2'], res['retData'][0]['threeEdge2'])
        assert res['retData'][0]['threeEdge3'] == JycList['threeEdge3'], 'url: {} \n 入参: {}\n 结果: {}\n 三层最短边不正确 \n 原三层最短边: {} \n 现三层最短边: {} '.format(url, data, res['retMessage'], JycList['threeEdge3'], res['retData'][0]['threeEdge3'])
        assert res['retData'][0]['threeVolume'] == JycList['threeVolume'], 'url: {} \n 入参: {}\n 结果: {}\n 三层体积不正确 \n 原三层体积: {} \n 现三层体积: {} '.format(url, data, res['retMessage'], JycList['threeVolume'], res['retData'][0]['threeVolume'])
        assert res['retData'][0]['threeWeight'] == JycList['threeWeight'], 'url: {} \n 入参: {}\n 结果: {}\n 三层重量不正确 \n 原三层重量: {} \n 现三层重量: {} '.format(url, data, res['retMessage'], JycList['threeWeight'], res['retData'][0]['threeWeight'])
        # print('======================核对SKU修改数据结束=======================')
        #
        # print('======================核对SKU各属性数据======================')
        #修改SKU信息
        url = self.host +'/sysback/update/product/package/queryPackageListFromSku?menuId=253&buttonId=148'
        reuqestsdata = {'skuNo': JycList['skuNo']}
        res = requests.post(url, headers=self.json_header, json=reuqestsdata).json()
        data = res['retData'][0]
        data['safetyRateUpdate'] = randint(1, 20)
        data['barcodeUpdate'] = CommonFunction.getString(8)
        data['saleMinUpdate'] = round(uniform(1, 100), 2)
        data['saleRestrictUpdate'] = randint(1, 2)
        data['pieceInfoUpdate'] = CommonFunction.getString(8)
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
        SaveData ={'inputList': [data]}
        # 执行暂存
        SaveRes = requests.post(SaveUrl, headers=self.json_header, json=SaveData).json()
        # print(SaveRes)
        assert SaveRes['retData']['commitState'] == 'NOT', '暂存失败 \n, 请检查入参: {} '.format(SaveData)

        # 提交
        CommitUrl = self.host + '/sysback/update/product/package/commitPackage?recordNo={}&menuId=253&buttonId=148'.format(Record)
        CommitData = {[data]}
        # 执行提交
        CommitRes = requests.post(CommitUrl, headers=self.json_header, json=CommitData).json()
        # print(CommitRes)
        assert CommitRes['retData']['commitState'] == 'COMMIT', '提交失败 \n, 请检查入参: {} '.format(CommitData)

        # 验证数据是否与提交的一致
        CheckUrl = self.host + '/sysback/update/product/package/queryPackageListFromSku?menuId=253&buttonId=148'
        CheckData = {'skuNo': JycList['skuNo']}
        res = requests.post(CheckUrl, headers=self.form_header, data=CheckData).json()
        # print(res)
        # print('======================核对SKU提交数据开始=======================')
        assert res['retData'][0]['safetyRate'] == data['safetyRateUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 安全率/金额不正确 \n 提交的安全率/金额: {} \n 现安全率/金额: {} '.format(url, data, res['retMessage'], data['safetyRateUpdate'], res['retData'][0]['safetyRate'])
        assert res['retData'][0]['barcode'] == data['barcodeUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 国际条形码不正确 \n 提交的国际条形码: {} \n 现国际条形码: {} '.format(url, data, res['retMessage'], data['barcodeUpdate'], res['retData'][0]['barcode'])
        assert res['retData'][0]['saleMin'] == data['saleMinUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 最小起售量不正确 \n 提交的最小起售量: {} \n 现最小起售量: {} '.format(url, data, res['retMessage'], data['saleMinUpdate'], res['retData'][0]['saleMin'])
        assert res['retData'][0]['saleRestrict'] == data['saleRestrictUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 销售限制类型不正确 \n 提交的销售限制类型: {} \n 现销售限制类型: {} '.format(url, data, res['retMessage'], data['saleRestrictUpdate'], res['retData'][0]['saleRestrict'])
        assert res['retData'][0]['pieceInfo'] == data['pieceInfoUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 件装数量不正确 \n 提交的件装数量: {} \n 现件装数量: {} '.format(url, data, res['retMessage'], data['pieceInfoUpdate'], res['retData'][0]['pieceInfo'])
        assert res['retData'][0]['packageLayers'] == data['packageLayersUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 层数不正确 \n 提交层数: {} \n 现层数: {} '.format(url, data, res['retMessage'], data['packageLayersUpdate'], res['retData'][0]['packageLayers'])
        assert res['retData'][0]['singlePackageUnit'] == data['singlePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 单品包装单位不正确 \n 提交单品包装单位: {} \n 现单品包装单位: {} '.format(url, data, res['retMessage'], data['singlePackageUnitUpdate'], res['retData'][0]['singlePackageUnit'])
        assert res['retData'][0]['singlePackageCount'] == data['singlePackageCountUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 单品包装数量不正确 \n 提交的单品包装数量: {} \n 现单品包装数量: {} '.format(url, data, res['retMessage'], data['singlePackageCountUpdate'], res['retData'][0]['singlePackageCount'])
        assert res['retData'][0]['singleEdge1'] == data['singleEdge1Update'], 'url: {} \n 入参: {}\n 结果: {}\n 单品最长边不正确 \n 提交的单品最长边: {} \n 现单品最长边: {} '.format(url, data, res['retMessage'], data['singleEdge1Update'], res['retData'][0]['singleEdge1'])
        assert res['retData'][0]['singleEdge2'] == data['singleEdge2Update'], 'url: {} \n 入参: {}\n 结果: {}\n 单品次长边不正确 \n 提交的单品次长边: {} \n 现单品次长边: {} '.format(url, data, res['retMessage'], data['singleEdge2Update'], res['retData'][0]['singleEdge2'])
        assert res['retData'][0]['singleEdge3'] == data['singleEdge3Update'], 'url: {} \n 入参: {}\n 结果: {}\n 单品最短边不正确 \n 提交的单品最短边: {} \n 现单品最短边: {} '.format(url, data, res['retMessage'], data['singleEdge3Update'], res['retData'][0]['singleEdge3'])
        assert res['retData'][0]['singleVolume'] == data['singleVolumeUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 单品体积不正确 \n 提交的单品体积: {} \n 现单品体积: {} '.format(url, data, res['retMessage'], data['singleVolumeUpdate'], res['retData'][0]['singleVolume'])
        assert res['retData'][0]['singleWeight'] == data['singleWeightUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 单品重量不正确 \n 提交的单品重量: {} \n 现单品重量: {} '.format(url, data, res['retMessage'], data['singleWeightUpdate'], res['retData'][0]['singleWeight'])
        assert res['retData'][0]['onePackageUnit'] == data['onePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装单位不正确 \n 提交的一层包装单位: {} \n 现一层包装单位: {} '.format(url, data, res['retMessage'], data['onePackageUnitUpdate'], res['retData'][0]['onePackageUnit'])
        assert res['retData'][0]['onePackageCount'] == data['onePackageCountUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 一层包装数量不正确 \n 提交的一层包装数量: {} \n 现一层包装数量: {} '.format(url, data, res['retMessage'], data['onePackageCountUpdate'], res['retData'][0]['onePackageCount'])
        assert res['retData'][0]['oneEdge1'] == data['oneEdge1Update'], 'url: {} \n 入参: {}\n 结果: {}\n 一层最长边不正确 \n 提交的一层最长边: {} \n 现一层最长边: {} '.format(url, data, res['retMessage'], data['oneEdge1Update'], res['retData'][0]['oneEdge1'])
        assert res['retData'][0]['oneEdge2'] == data['oneEdge2Update'], 'url: {} \n 入参: {}\n 结果: {}\n 一层次长边不正确 \n 提交的一层次长边: {} \n 现一层次长边: {} '.format(url, data, res['retMessage'], data['oneEdge2Update'], res['retData'][0]['oneEdge2'])
        assert res['retData'][0]['oneEdge3'] == data['oneEdge3Update'], 'url: {} \n 入参: {}\n 结果: {}\n 一层最短边不正确 \n 提交的一层最短边: {} \n 现一层最短边: {} '.format(url, data, res['retMessage'], data['oneEdge3Update'], res['retData'][0]['oneEdge3'])
        assert res['retData'][0]['oneVolume'] == data['oneVolumeUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 一层体积不正确 \n 提交的一层体积: {} \n 现一层体积: {} '.format(url, data, res['retMessage'], data['oneVolumeUpdate'], res['retData'][0]['oneVolume'])
        assert res['retData'][0]['oneWeight'] == data['oneWeightUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 一层重量不正确 \n 提交的一层重量: {} \n 现一层重量: {} '.format(url, data, res['retMessage'], data['oneWeightUpdate'], res['retData'][0]['oneWeight'])
        assert res['retData'][0]['twoPackageUnit'] == data['twoPackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 二层包装单位不正确 \n 提交的二层包装单位: {} \n 现二层包装单位: {} '.format(url, data, res['retMessage'], data['twoPackageUnitUpdate'], res['retData'][0]['twoPackageUnit'])
        assert res['retData'][0]['twoPackageCount'] == data['twoPackageCountUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 二层包装数量不正确 \n 提交的二层包装数量: {} \n 现二层包装数量: {} '.format(url, data, res['retMessage'], data['twoPackageCountUpdate'], res['retData'][0]['twoPackageCount'])
        assert res['retData'][0]['twoEdge1'] == data['twoEdge1Update'], 'url: {} \n 入参: {}\n 结果: {}\n 二层最长边不正确 \n 提交的二层最长边: {} \n 现二层最长边: {} '.format(url, data, res['retMessage'], data['twoEdge1Update'], res['retData'][0]['twoEdge1'])
        assert res['retData'][0]['twoEdge2'] == data['twoEdge2Update'], 'url: {} \n 入参: {}\n 结果: {}\n 二层次长边不正确 \n 提交的二层次长边: {} \n 现二层次长边: {} '.format(url, data, res['retMessage'], data['twoEdge2Update'], res['retData'][0]['twoEdge2'])
        assert res['retData'][0]['twoEdge3'] == data['twoEdge3Update'], 'url: {} \n 入参: {}\n 结果: {}\n 二层最短边不正确 \n 提交的二层最短边: {} \n 现二层最短边: {} '.format(url, data, res['retMessage'], data['twoEdge3Update'], res['retData'][0]['twoEdge3'])
        assert res['retData'][0]['twoVolume'] == data['twoVolumeUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 二层体积不正确 \n 提交的二层体积: {} \n 现二层体积: {} '.format(url, data, res['retMessage'], data['twoVolumeUpdate'], res['retData'][0]['twoVolume'])
        assert res['retData'][0]['twoWeight'] == data['twoWeightUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 二层重量不正确 \n 提交的二层重量: {} \n 现二层重量: {} '.format(url, data, res['retMessage'], data['twoWeightUpdate'], res['retData'][0]['twoWeight'])
        assert res['retData'][0]['threePackageUnit'] == data['threePackageUnitUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 三层包装单位不正确 \n 提交的三层包装单位: {} \n 现三层包装单位: {} '.format(url, data, res['retMessage'], data['threePackageUnitUpdate'], res['retData'][0]['threePackageUnit'])
        assert res['retData'][0]['threePackageCount'] == data['threePackageCountUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 三层包装数量不正确 \n 提交的三层包装数量: {} \n 现三层包装数量: {} '.format(url, data, res['retMessage'], data['threePackageCountUpdate'], res['retData'][0]['threePackageCount'])
        assert res['retData'][0]['threeEdge1'] == data['threeEdge1Update'], 'url: {} \n 入参: {}\n 结果: {}\n 三层最长边不正确 \n 提交的三层最长边: {} \n 现三层最长边: {} '.format(url, data, res['retMessage'], data['threeEdge1Update'], res['retData'][0]['threeEdge1'])
        assert res['retData'][0]['threeEdge2'] == data['threeEdge2Update'], 'url: {} \n 入参: {}\n 结果: {}\n 三层次长边不正确 \n 提交的三层次长边: {} \n 现三层次长边: {} '.format(url, data, res['retMessage'], data['threeEdge2Update'], res['retData'][0]['threeEdge2'])
        assert res['retData'][0]['threeEdge3'] == data['threeEdge3Update'], 'url: {} \n 入参: {}\n 结果: {}\n 三层最短边不正确 \n 提交的三层最短边: {} \n 现三层最短边: {} '.format(url, data, res['retMessage'], data['threeEdge3Update'], res['retData'][0]['threeEdge3'])
        assert res['retData'][0]['threeVolume'] == data['threeVolumeUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 三层体积不正确 \n 提交的三层体积: {} \n 现三层体积: {} '.format(url, data, res['retMessage'], data['threeVolumeUpdate'], res['retData'][0]['threeVolume'])
        assert res['retData'][0]['threeWeight'] == data['threeWeightUpdate'], 'url: {} \n 入参: {}\n 结果: {}\n 三层重量不正确 \n 提交的三层重量: {} \n 现三层重量: {} '.format(url, data, res['retMessage'], data['threeWeightUpdate'], res['retData'][0]['threeWeight'])
        # print('======================核对SKU提交数据结束=======================')
        print('验证SKU管理结束')


    def GetCalcUnit(self):
        CalcUnitList = list()
        url = self.host + '/sysback/unit/baseQueryList?menuId=253&buttonId=148'
        data = {"nowPage": 1, "pageShow": 10, "searchParam": "[{\"name\":\"unitName\",\"value\":\"\"},{\"name\":\"unitName_q\",\"value\":\"Like\"}]"}
        res = requests.post(url, headers=self.json_header, json=data).json()
        data['pageShow'] = res['retData']['totalNum']
        res = requests.post(url, headers=self.json_header, json=data).json()
        for i in res['retData']['results']:
            CalcUnitList.append(i['unitName'])

        CalcUnit = sample(CalcUnitList, 1)[0]
        # print(CalcUnit)
        return CalcUnit


