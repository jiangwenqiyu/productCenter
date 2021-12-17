import requests
from environmentConfig import LoginInfo
import datetime
import random
import time


class CommonFunction(LoginInfo):
    def __init__(self):
        super().__init__()
        # 用户信息
        self.user_id = ''    # 用户id
        self.orgId = ''      # 组织代码
        # 生成代码
        self.productType = ''     # 商品类型代码
        self.productTypeStr = ''  # 商品类型   中文
        self.brandName = ''    # 品牌名称
        self.productName = ''  # 商品名称
        self.helpCode = ''    # 助记码
        self.secondTitle = ''  # 副标题
        self.specName = ''     # 规格名称
        self.mainUnitName = ''     # 主计量单位名称  中文
        self.mainUnitId = ''       # 主计量单位id
        self.mainUnitdecimal = ''  # 主计量小数位
        self.secondUnitName = None     # 辅计量单位名称  中文
        self.secondUnitId = None       # 辅计量单位id
        self.secondUnitdecimal = None  # 辅计量小数位
        self.addPriceTypeStr = ''  # 加价类型  中文
        self.addPriceType = ''   # 1.金额   2.比例
        self.isPurchaseMultiUnit = ''  # 是否采购多计量   1 是  2否
        self.isSaleMultiUnit = ''   # 是否销售多计量
        self.productUuid = ''
        self.spuNo = ''
        self.skuNo = ''
        # 管理信息
        self.manage_area = ''        # 管理区域   uuid   1001
        self.manage_area_ch = ''    # 管理区域，中文
        self.logistics_store = ''      # 储存属性   中文集合
        self.manage_stock_period = ''    # 囤货期
        self.manage_soldout_period = ''    # 下架期
        self.manage_cooperation = ''    # 合作模式，必填
        self.manage_dealmode = ''    # 经营模式，必填
        self.manage_packlist = ''    # 包装清单，必填
        self.manage_sellmanageperiod = ''    # 售价管理周期，必填
        self.manage_outpos = ''     # 档次外部定位，必填
        self.manage_inpos = ''     # 档次内部定位，必填
        self.manage_season_product = ''     # 是否季节性商品
        self.marketing_saleplat = ''     # 售卖平台，必填
        self.tax_classify = ''      # 归类名，必填，中文
        # sku信息
        self.safetyRate = ''      # 安全率/金额
        self.barcode = ''  # 国际条形码
        self.saleMin = ''  # 最小起售量
        # 销售限制类型
        self.pieceInfo = ''  # 件装数量
        self.packageLayers = ''# 层数
        self.singlePackageCount = ''# 单品数量
        self.singleEdge1 = ''  # 单品最长边
        self.singleEdge2 = ''  # 单品次长边
        self.singleEdge3 = ''   # 单品最短边
        self.singleVolume = ''  # 单品体积
        self.singleWeight = ''   # 单品重量
        self.onePackageUnit = ''   # 一层包装单位
        self.onePackageCount = ''   # 一层数量
        self.oneEdge1 = ''   # 一层最长边
        self.oneEdge2 = ''   # 一层次长边
        self.oneEdge3 = ''   # 一层最短边
        self.oneVolume = ''  # 一层体积
        self.oneWeight = ''   # 一层重量
        self.twoPackageUnit = ''   # 二层包装单位
        self.twoPackageCount = ''   # 二层数量
        self.twoEdge1 = ''   # 二层最长边
        self.twoEdge2 = ''   # 二层次长边
        self.twoEdge3 = ''   # 二层最短边
        self.twoVolume = ''  # 二层体积
        self.twoWeight = ''   # 二层重量
        self.threePackageUnit = ''   # 三层包装单位
        self.threePackageCount = ''   # 三层数量
        self.threeEdge1 = ''   # 三层最长边
        self.threeEdge2 = ''   # 三层次长边
        self.threeEdge3 = ''   # 三层最短边
        self.threeVolume = ''  # 三层体积
        self.threeWeight = ''   # 三层重量
        # 供货信息   被参照城市 都是北京,比例  2
        self.purchasePriceType = ''  # 进价类型   1  统一  2 区域
        self.saleAreaCode = '' # 销售区域   区域编码字符串  101,102
        self.tempSelf = set()  # 参照自己的城市,集合
        self.tempOther = set()  # 参照别人的城市，集合
        self.mainPurchasePrice = ''  # 进价
        self.factoryFacePrice = ''# 厂家面价
        self.purchasePriceNote = ''# 进价备注
        self.freightRatio = ''# 运费比例
        self.packRatio = ''# 包装比例
        self.processChargesRatio = ''# 加工费比例
        self.rebateRatio = ''# 返利折合比例
        self.mainUnitCostPrice = ''# 成本价

        self.areaCostPrice = list()   # 区域进价，价格信息


        # 售价信息
        self.cashPrice = ''  # 现金价
        self.distributePrice = ''  # 分销价
        self.salePrice = ''   # 售价
        self.saleFacePrice = ''  # 销售面价
        self.limitShowPrice = '' # 限制展示价
        self.limitTradePrice = ''  # 限制交易价

    # 获取随机字符串
    def getString(self, length):
        s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        temp = ''
        for i in range(length):
            temp += random.choice(s)
        return temp

    # 获取登录信息，管理区域
    def getLoginInfo(self):
        url = self.host + '/sysback/login/getLoginInfo?menuId=238&buttonId=1'
        try:
            res = requests.post(url, headers = self.json_header, json={}).json()
        except Exception as e:
            assert False, '获取登录信息，请求失败\nurl:{}\n{}'.format(url, e)
        assert res['retMessage'] == 'success', '登录失败\nurl:{}\nres:{}'.format(url, res)
        self.manage_area = res['retData']['hrAreaId']
        self.user_id = res['retData']['userId']
        self.orgId = res['retData']['hrDepartmentNumber']

    # 生成代码
    def generateCode(self, cateUuid, addPriceType, isSaleMultiUnit, isPurchaseMultiUnit):
        # 创建分类
        url = self.host + '/sysback/choose/category/createProductCategoryOper?menuId=238&buttonId=1'
        data = {'categoryUuid':cateUuid}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '', 'url:{}\n入参:{}\n结果:{}\n创建分类失败'.format(url,data,res['retMessage'])
        print('创建分类成功')

        # 获取分类信息
        url = self.host + '/sysback/addsingleproduct/basicinfo/toManualAddStep1?menuId=238&buttonId=1'
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '', 'url:{}\n入参:{}\n结果:{}\n获取分类信息失败'.format(url,data,res['retMessage'])
        print('获取分类信息成功')

        # 随机选择一个属性下的属性值
        templateUuid = res['retData']['templateUuid']
        attributeInfo = res['retData']['specList'][random.randint(0,len(res['retData']['specList']) - 1)]
        valueInfo = attributeInfo['values'][random.randint(0,len(attributeInfo['values'])-1)]
        self.specName = valueInfo['valueName']

        # 随机选择一个商品类型
        productTypeInfo = res['retData']['productTypeOptions'][random.randint(0,len(res['retData']['productTypeOptions']) - 1)]
        self.productType = productTypeInfo['optionValue']
        self.productTypeStr = productTypeInfo['optionHtml']

        # 随机选择一个品牌，然后判断厂家品牌影响力
        url = self.host + '/sysback/addsingleproduct/basicinfo/getPagerByBrandAndCategory?menuId=238&buttonId=1'
        data = {'nowPage':1,'pageShow':10,'brandName':'','categoryUuid':13000,'notInUuids':''}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '', 'url:{}\n入参:{}\n结果:{}\n获取品牌信息失败'.format(url,data,res['retMessage'])
        data['nowPage'] = random.randint(1,res['retData']['totalNum'])
        data['pageShow'] = 1
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        brandInfo = res['retData']['results'][0]
        if brandInfo['factoryInfluenceMore'] == '1':
            brandName = brandInfo['factoryBrandName']
        else:
            brandName = brandInfo['brandName']
        self.brandName = brandName

        # 商品名称
        name = '自动化测试商品{}'.format(str(int(time.time()*1000))[-5:])
        self.productName = name

        # 获取助记码，名称包含品牌
        url = self.host + '/sysback/addsingleproduct/basicinfo/getSpuHelpCode?menuId=238&buttonId=1'
        data = {"productNameType":"1","productName":name,"brandName":brandInfo['brandName']}
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retMessage'] == '', 'url:{}\n入参:{}\n结果:{}\n获取助记码失败'.format(url,data,res['retMessage'])
        helpCode = res['retData']['helpCode']
        self.helpCode = helpCode

        # 副标题
        self.secondTitle = self.getString(6)

        # 随机选择主计量单位
        url = self.host + '/sysback/unit/baseQueryList?menuId=238&buttonId=1'
        data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"unitName\",\"value\":\"\"},{\"name\":\"unitName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retMessage'] == '', 'url:{}\n入参:{}\n结果:{}\n获取主计量单位信息失败'.format(url,data,res['retMessage'])
        data['nowPage'] = random.randint(1,res['retData']['totalNum'])
        data['pageShow'] = 1
        try:
            res = requests.post(url, headers = self.json_header, json = data).json()
        except Exception as e:
            assert False, '获取计量单位信息失败, {}\n{}'.format(url, e)
        unitInfo = res['retData']['results'][0]
        self.mainUnitName = unitInfo['unitName']
        self.mainUnitId = unitInfo['uuid']
        self.mainUnitdecimal = unitInfo['decimalPlaces']

        # 辅计量单位
        self.isPurchaseMultiUnit = isPurchaseMultiUnit
        self.isSaleMultiUnit = isSaleMultiUnit
        if (isSaleMultiUnit == '1' and isPurchaseMultiUnit == '1') or (isSaleMultiUnit == '2' and isPurchaseMultiUnit == '1'):
            while True:
                url = self.host + '/sysback/unit/baseQueryList?menuId=238&buttonId=1'
                data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"unitName\",\"value\":\"\"},{\"name\":\"unitName_q\",\"value\":\"Like\"}]","sortName":"","sortType":""}
                try:
                    res = requests.post(url, headers = self.json_header, json=data).json()
                except Exception as e:
                    assert False, '接口请求失败,{}\n{}'.format(url, e)
                assert res['retMessage'] == '', 'url:{}\n入参:{}\n结果:{}\n获取辅计量单位信息失败'.format(url,data,res['retMessage'])
                data['nowPage'] = random.randint(1,res['retData']['totalNum'])
                data['pageShow'] = 1
                res = requests.post(url, headers = self.json_header, json = data).json()
                unitInfo = res['retData']['results'][0]
                if unitInfo['unitName'] == self.mainUnitName:
                    continue
                else:
                    self.secondUnitName = unitInfo['unitName']
                    self.secondUnitId = unitInfo['uuid']
                    self.secondUnitdecimal = unitInfo['decimalPlaces']
                    unitNo = unitInfo['unitNo']
                    break
        elif isSaleMultiUnit == '1' and isPurchaseMultiUnit == '2':
            assert False, '传参错误,销售多计量,采购必须是多计量'
        else:
            self.secondUnitName = None
            self.secondUnitId = None
            self.secondUnitdecimal = None

        # 加价类型
        if addPriceType == '1':
            self.addPriceType = '1'
            self.addPriceTypeStr = '固定金额'
        else:
            self.addPriceType = '2'
            self.addPriceTypeStr = '比例'

        # 生成代码
        url = self.host + '/sysback/addsingleproduct/basicinfo/generateCode?menuId=238&buttonId=1'
        data = {
            "categoryUuid": cateUuid,                             # 分类id
            "templateUuid": templateUuid,                         # 模板id
            "productType": self.productType,        # 商品类型
            "productTypeStr": self.productTypeStr,      # 商品类型中文
            "brandUuid": brandInfo['uuid'],                       # 品牌id
            "brandName": brandName,                               # 品牌名
            "brandseriesUuid": "",                                # 品牌系列id，都是空
            "brandseries": "",                                    # 品牌系列，都是空
            "specList": [],                                         # 规格详情,下边获取
            "notSpecList": [],                      # 非规格属性，都是空
            "basicManageList": [],                  # 基本管理信息，都是空
            "marketingList": [],                    # 都是空
            "taxList": [],                          # 都是空
            "logisticsList": [],                    # 都是空
            "sceneList": [
                {
                    "twoSceneName": "通用模块",
                    "twoSceneUuid": "10028"
                }
            ],
            "cityList": [],                       # 都是空
            "centralBuyState": '2',               # 是否集采
            "productName": self.productName,                  # productName
            "productNameType": "1",               # 名称包含品牌默认  1.包含   2.不包含   助记码也得改
            "helpCode": helpCode,                 # 助记码
            "addPriceType": addPriceType,                  # 加价类型
            "addPriceTypeStr": self.addPriceTypeStr,         # 加价类型
            "subtitle": self.secondTitle,                    # 副标题
            "isSaleMultiUnit": isSaleMultiUnit,               # 是否销售多计量
            "isPurchaseMultiUnit": isPurchaseMultiUnit,           # 是否采购多计量
            "mainUnit": self.mainUnitName,         # 主计量单位，中文
            "mainUnitDecimalsStr": self.mainUnitdecimal,   # 主计量单位小数位
            "mainUnitUuid": self.mainUnitId,     # 主计量单位id
            "tagList": [],
            "sideUnitList": []
        }
        # 规格信息
        specList = list()
        temp = dict()
        temp['attributeName'] = attributeInfo['attributeName']
        temp['attributeUuid'] = attributeInfo['attributeUuid']
        temp['helpCode'] = valueInfo['helpCode']
        temp['officialFlag'] = valueInfo['officialFlag']
        temp['selected'] = True
        temp['valueName'] = valueInfo['valueName']
        temp['valueUuid'] = valueInfo['valueUuid']

        specList.append(temp)
        data['specList'].append(specList)

        # 多计量信息
        if self.secondUnitName != None:
            temp = dict()
            if isSaleMultiUnit == '2' and isPurchaseMultiUnit == '1':
                scenario = '1'
            else:
                scenario = '2'
            temp['scenario'] = scenario
            temp['sideUnit'] = self.secondUnitName
            temp['sideUnitDecimalsStr'] = self.secondUnitdecimal
            temp['sideUnitNo'] = unitNo
            temp['sideUnitUuid'] = self.secondUnitId
            data['sideUnitList'].append(temp)

        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '生成代码失败\nurl:{}\ndata:{}\nres:{}'.format(url, data, res['retMessage'])
        standard = res['retData']['addState']['acceptanceAddState']
        qualification = res['retData']['addState']['qualificationAddState']
        self.productUuid = res['retData']['productUuid']
        self.spuNo = res['retData']['spuNo']
        self.skuNo = res['retData']['skuNoMap'][valueInfo['valueName']]
        print('生成代码成功')
        return self.productUuid, standard, qualification

    # 完善基本信息
    def basicInfo(self, productUuid):
        # 先获取商品分类都有哪些非规格属性
        url = self.host + '/sysback/prepare/commit/basicinfo/queryBasicInfo?productUuid={}&menuId=239&buttonId=2'.format(productUuid)
        try:
            res = requests.post(url, headers = self.json_header, json={}).json()
        except Exception as e:
            assert False, '接口请求失败, {}'.format(url, e)
        assert res['retMessage'] == '', 'url:{}\n入参:{}\n结果:{}\n完善基本信息失败'.format(url,data,res['retMessage'])
        assert res['retData']['main']['addPriceTypeStr'] == self.addPriceTypeStr, '完善基本信息， 加价类型不正确, {}, \nexp:{}\nfact:{}'.format(productUuid, self.addPriceTypeStr, res['retData']['main']['addPriceTypeStr'])
        assert res['retData']['main']['brandName'] == self.brandName, '完善基本信息， 品牌不正确, {}, \nexp:{}\nfact:{}'.format(productUuid, self.brandName, res['retData']['main']['brandName'])
        assert res['retData']['main']['manageArea'] == self.manage_area, '完善基本信息， 管理区域不正确, {}, \nexp:{}\nfact:{}'.format(productUuid, self.manage_area, res['retData']['main']['manageArea'])
        print('判断初始信息成功')

        # 如果是空，直接返回，自动已完善
        if res['retData']['attrList'] == []:
            return
        else:
            data = dict()
            data['notSpecList'] = []
            data['productUuid'] = productUuid

            for i in res['retData']['attrList']:
                temp = dict()

                if i['attrType'] == '01':   # 文本框
                    temp['attrInfo'] = i['attrUuid']
                    temp['officialFlag'] = i['officialFlag']
                    temp['valueInfo'] = self.getString(6)
                elif i['attrType'] == '02':   # 下拉框
                    temp['attrInfo'] = i['attrUuid']
                    temp['officialFlag'] = i['officialFlag']
                    temp['valueInfo'] = random.choice(i['allValueOptions'])['optionValue']
                elif i['attrType'] == '04':   # 多选框
                    temp['attrInfo'] = i['attrUuid']
                    temp['officialFlag'] = i['officialFlag']
                    s = ''
                    for x in i['allValueOptions']:
                        s += x['optionValue'] + ','
                    temp['valueInfo'] = s[0:-1]
                else:
                    assert False, '待准入维护基本信息，没有符合条件的属性类型， {}'.format(productUuid)

                data['notSpecList'].append(temp)

            url = self.host + '/sysback/prepare/commit/basicinfo/saveBasicInfo?menuId=239&buttonId=2'
            try:
                res = requests.post(url, headers = self.json_header, json=data).json()
            except Exception as e:
                assert False, '接口请求失败,{}\n{}'.format(url, e)
            assert res['retStatus'] == '1', '待准入完善基本信息失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
            print('完善成功')

    # 完善管理信息
    def manageInfo(self, productUuid):
        url = self.host + '/sysback/prepare/commit/allmanaging/queryAllManaging?productUuid={}&menuId=239&buttonId=2'.format(productUuid)
        res = requests.post(url, headers = self.json_header, json={}).json()
        assert res['retMessage'] == '', '待准入完善管理信息失败, {}\nurl:{}\nres:{},'.format(productUuid, url, res)
        assert res['retData']['manageList'][0]['valueUuid'] == self.manage_area, 'uuid:{},待准入管理区域不同'.format(productUuid)
        print('判断表头信息成功')

        # 完善所有字段，保存

        # 管理区域
        manage_area = res['retData']['manageList'][0]['valueUuid']   # 管理区域
        self.manage_area_ch = res['retData']['manageList'][0]['valueName']
        # 储存属性，随机选择五次,去重
        chucunName = set()
        chucunId = set()
        for i in range(5):
            obj = res['retData']['logisticsList'][3]['allValueOptions'][random.randint(0,8)]
            chucunName.add(obj['optionHtml'])
            chucunId.add(obj['optionValue'])
        w = ''
        if len(chucunId) == 1:
            w = list(chucunId)[0]
        else:
            for i in chucunId:
                w += i + ','
            w = w[0:-1]
        self.logistics_store = chucunName    # 储存属性，中文集合
        for i in res['retData']['manageList']:
            if i['attrName'] == '囤货期':
                # 囤货期
                obj = i['allValueOptions'][random.randint(0,11)]
                manage_stock_period = obj['optionValue']                 # 入参
                self.manage_stock_period = obj['optionHtml']   # 中文
            if i['attrName'] == '下架期':
                # 下架期
                obj = i['allValueOptions'][random.randint(0,11)]
                manage_soldout_period = obj['optionValue']               # 入参
                self.manage_soldout_period = obj['optionHtml'] # 中文
            if i['attrName'] == '合作模式':
                # 合作模式
                obj = i['allValueOptions'][random.randint(0,3)]
                manage_cooperation = obj['optionValue']                # 入参
                self.manage_cooperation = obj['optionHtml']  # 中文
            if i['attrName'] == '经营模式':
                # 经营模式
                obj = i['allValueOptions'][random.randint(0,2)]
                manage_dealmode = obj['optionValue']               # 入参
                self.manage_dealmode = obj['optionHtml']  # 中文
            if i['attrName'] == '包装清单':
                # 包装清单
                manage_packlist = self.getString(random.randint(3,8))   # 随机获取3到8位组合
                self.manage_packlist = manage_packlist
            if i['attrName'] == '售价管理周期':
                # 售价管理周期
                obj = i['allValueOptions'][random.randint(0,2)]
                manage_sellmanageperiod = obj['optionValue']        # 入参
                self.manage_sellmanageperiod = obj['optionHtml']   # 中文
            if i['attrName'] == '档次外部定位':
                # 档次外部定位
                obj = i['allValueOptions'][random.randint(0,4)]
                manage_outpos = obj['optionValue']        # 入参
                self.manage_outpos = obj['optionHtml']   # 中文
            if i['attrName'] == '档次内部定位':
                # 档次内部定位
                obj = i['allValueOptions'][random.randint(0,4)]
                manage_inpos = obj['optionValue']        # 入参
                self.manage_inpos = obj['optionHtml']   # 中文
            if i['attrName'] == '是否季节性商品':
                # 是否季节性商品
                obj = i['allValueOptions'][random.randint(0,1)]
                manage_season_product = obj['optionValue']        # 入参
                self.manage_season_product = obj['optionHtml']   # 中文
            # 售卖平台,暂时写死，签约平台
            marketing_saleplat = 'marketing_saleplat_signed'
            self.marketing_saleplat = 'optionHtml'

        # 归类信息
        assert len(res['retData']['taxList'][0]['allValueOptions'])>=1, '{},完善管理信息失败，没有归类'.format(productUuid)
        obj = res['retData']['taxList'][0]['allValueOptions'][random.randint(0,len(res['retData']['taxList'][0]['allValueOptions']) - 1)]
        tax_classify = obj['optionValue']    # 归类id
        url = self.host + '/sysback/addsingleproduct/basicinfo/getClassificationByUuid?uuid=10129&menuId=239&buttonId=2'
        data = {'uuid':tax_classify}
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retMessage'] == '', '{}, 完善管理信息时候，获取归类信息失败, \n{}'.format(productUuid, data)
        tax_code = res['retData']['taxCateNo']       # 税务代码
        tax_rate = res['retData']['taxRate']         # 税率
        self.tax_classify = obj['optionHtml']    # 归类中文名


        data = {
            "productUuid": productUuid,
            "logisticsList": [
                {
                    "attrUuid": "logistics_pack"
                },
                {
                    "attrUuid": "logistics_transport"
                },
                {
                    "attrUuid": "logistics_restrict"
                },
                {
                    "attrUuid": "logistics_store",
                    "valueInfo": w  # 储存属性
                },
                {
                    "attrUuid": "logistics_stock",
                    "valueInfo": "logistics_stock_none"
                }
            ],
            "manageList": [
                {
                    "attrUuid": "manage_area",   # 管理区域，自动代入的，不做更改
                    "valueInfo": manage_area
                },
                {
                    "attrUuid": "manage_stock_period",    # 囤货期
                    "valueInfo": manage_stock_period
                },
                {
                    "attrUuid": "manage_soldout_period",   # 下架期
                    "valueInfo": manage_soldout_period
                },
                {
                    "attrUuid": "manage_cooperation",    # 合作模式，必填
                    "valueInfo": manage_cooperation
                },
                {
                    "attrUuid": "manage_dealmode",     # 经营模式，必填
                    "valueInfo": manage_dealmode
                },
                {
                    "attrUuid": "manage_packlist",    # 包装清单，必填
                    "valueInfo": manage_packlist
                },
                {
                    "attrUuid": "manage_sellmanageperiod",    # 售价管理周期，必填
                    "valueInfo": manage_sellmanageperiod
                },
                {
                    "attrUuid": "manage_outpos",   # 档次外部定位，必填
                    "valueInfo": manage_outpos
                },
                {
                    "attrUuid": "manage_inpos",    # 档次内部定位，必填
                    "valueInfo": manage_inpos
                },
                {
                    "attrUuid": "manage_season_product",   # 是否季节性商品
                    "valueInfo": manage_season_product
                }
            ],
            "marketingList": [
                {
                    "attrUuid": "marketing_saleplat",     # 售卖平台，必填
                    "valueInfo": marketing_saleplat
                }
            ],
            "taxList": [
                {
                    "attrUuid": "tax_classify",    # 归类名称，必填
                    "valueInfo": tax_classify
                },
                {
                    "attrUuid": "tax_code",   # 带出来的
                    "valueInfo": tax_code
                },
                {
                    "attrUuid": "tax_rate",   # 带出来的
                    "valueInfo": tax_rate
                }
            ],
            "thirdPlatList": [],
            "cityList": []
        }

        url = self.host + '/sysback/prepare/commit/allmanaging/saveAllManaging?menuId=239&buttonId=2'
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retMessage'] == '', '{}, 完善管理信息失败, {}, \n{}'.format(productUuid, res['retMessage'], data)
        print('完善成功')

    # 完善sku信息
    def skuInfo(self, productUuid):
        url = self.host + '/sysback/prepare/commit/package/queryPackage?productUuid={}&menuId=239&buttonId=2'.format(productUuid)
        res = requests.post(url, headers = self.json_header, json={}).json()
        assert res['retMessage'] == '', '{}, 待准入完善sku信息失败, {}'.format(productUuid, res['retMessage'])
        assert res['retData']['main']['addPriceTypeStr'] == self.addPriceTypeStr, '{}, 完善sku信息加价类型不对'.format(productUuid)
        assert res['retData']['main']['brandName'] == self.brandName, '{}, 完善sku信息品牌不对'.format(productUuid)
        assert res['retData']['main']['manageArea'] == self.manage_area_ch, '{}, 完善sku信息管理区域不对'.format(productUuid)
        assert res['retData']['main']['productNameFinal'] == self.brandName + ' ' + self.productName, '{}, 完善sku信息名称不对,expect:{}, fact:{}'.format(productUuid, self.brandName + self.productName, res['retData']['main']['productNameFinal'])
        assert res['retData']['main']['productUuid'] == productUuid, '{}, 完善sku信息uuid不对'.format(productUuid)
        assert res['retData']['main']['spuNo'] == self.spuNo, '{}, 完善sku信息spu编码不对'.format(productUuid)
        assert res['retData']['packageList'][0]['specDetailStr'] == self.specName, '{}, 完善sku信息规格不对'.format(productUuid)
        assert res['retData']['packageList'][0]['singlePackageUnit'] == self.mainUnitName, '{}, 完善sku信息单品单位不对'.format(productUuid)
        print('判断表头信息成功')

        # 生成参数

        # 件装数量
        pieceInfo = self.getString(5)
        self.pieceInfo = pieceInfo
        # 国际条形码
        barcode = self.getString(10)
        self.barcode = barcode
        # 安全值
        safetyRate = random.randint(3, 6)
        self.safetyRate = safetyRate
        # 最小起售量
        saleMin = random.randint(1, 10)
        self.saleMin = saleMin
        # 层数
        packageLayers = 'THREE'
        self.packageLayers = packageLayers
        # 单品数量
        singlePackageCount = random.randint(1,10)
        self.singlePackageCount = singlePackageCount
        # 单品最长边
        singleEdge1 = round(random.randint(0, 10) + random.random(), 2)
        self.singleEdge1 = singleEdge1
        # 单品次长边
        singleEdge2 = round(random.randint(0, 10) + random.random(), 2)
        self.singleEdge2 = singleEdge2
        # 单品最短边
        singleEdge3 = round(random.randint(0, 10) + random.random(), 2)
        self.singleEdge3 = singleEdge3
        # 单品体积
        singleVolume = singleEdge1 * singleEdge2 * singleEdge3 * 0.000001
        self.singleVolume = singleVolume
        # 单品重量
        singleWeight = round(random.randint(0, 10) + random.random(), 2)
        self.singleWeight = singleWeight
        # 一层单位
        unit_url = self.host + '/sysback/unit/baseQueryList?menuId=239&buttonId=2'
        unit_data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"unitName\",\"value\":\"\"},{\"name\":\"unitName_q\",\"value\":\"Like\"}]"}
        unit_res = requests.post(unit_url, headers = self.json_header, json=unit_data).json()
        unit_data['pageShow'] = unit_res['retData']['totalNum']
        unit_res = requests.post(unit_url, headers = self.json_header, json=unit_data).json()
        while True:
            unitname = random.choice(unit_res['retData']['results'])['unitName']
            if unitname != self.mainUnitName:
                break
        onePackageUnit = unitname
        self.onePackageUnit = onePackageUnit
        # 一层数量
        onePackageCount = random.randint(1,10)
        self.onePackageCount = onePackageCount
        # 一层最长边
        oneEdge1 = round(random.randint(0, 10) + random.random(), 2)
        self.oneEdge1 = oneEdge1
        # 一层次长边
        oneEdge2 = round(random.randint(0, 10) + random.random(), 2)
        self.oneEdge2 = oneEdge2
        # 一层最短边
        oneEdge3 = round(random.randint(0, 10) + random.random(), 2)
        self.oneEdge3 = oneEdge3
        # 一层体积
        oneVolume = oneEdge1 * oneEdge2 * oneEdge3 * 0.000001
        self.oneVolume = oneVolume
        # 一层重量
        oneWeight = round(random.randint(0, 10) + random.random(), 2)
        self.oneWeight = oneWeight
        # 二层单位
        unit_url = self.host + '/sysback/unit/baseQueryList?menuId=239&buttonId=2'
        unit_data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"unitName\",\"value\":\"\"},{\"name\":\"unitName_q\",\"value\":\"Like\"}]"}
        unit_res = requests.post(unit_url, headers = self.json_header, json=unit_data).json()
        unit_data['pageShow'] = unit_res['retData']['totalNum']
        unit_res = requests.post(unit_url, headers = self.json_header, json=unit_data).json()
        while True:
            unitname = random.choice(unit_res['retData']['results'])['unitName']
            if unitname != self.mainUnitName and unitname != onePackageUnit:
                break
        twoPackageUnit = unitname
        self.twoPackageUnit = twoPackageUnit
        # 二层数量
        twoPackageCount = random.randint(1,10)
        self.twoPackageCount = twoPackageCount
        # 二层最长边
        twoEdge1 = round(random.randint(0, 10) + random.random(), 2)
        self.twoEdge1 = twoEdge1
        # 二层次长边
        twoEdge2 = round(random.randint(0, 10) + random.random(), 2)
        self.twoEdge2 = twoEdge2
        # 二层最短边
        twoEdge3 = round(random.randint(0, 10) + random.random(), 2)
        self.twoEdge3 = twoEdge3
        # 二层体积
        twoVolume = twoEdge1 * twoEdge2 * twoEdge3 * 0.000001
        self.twoVolume = twoVolume
        # 二层重量
        twoWeight = round(random.randint(0, 10) + random.random(), 2)
        self.twoWeight = twoWeight
        # 三层单位
        unit_url = self.host + '/sysback/unit/baseQueryList?menuId=239&buttonId=2'
        unit_data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"unitName\",\"value\":\"\"},{\"name\":\"unitName_q\",\"value\":\"Like\"}]"}
        unit_res = requests.post(unit_url, headers = self.json_header, json=unit_data).json()
        unit_data['pageShow'] = unit_res['retData']['totalNum']
        unit_res = requests.post(unit_url, headers = self.json_header, json=unit_data).json()
        while True:
            unitname = random.choice(unit_res['retData']['results'])['unitName']
            if unitname != self.mainUnitName and unitname != onePackageUnit and unitname != twoPackageUnit:
                break
        threePackageUnit = unitname
        self.threePackageUnit = threePackageUnit
        # 三层数量
        threePackageCount = random.randint(1,10)
        self.threePackageCount = threePackageCount
        # 三层最长边
        threeEdge1 = round(random.randint(0, 10) + random.random(), 2)
        self.threeEdge1 = threeEdge1
        # 三层次长边
        threeEdge2 = round(random.randint(0, 10) + random.random(), 2)
        self.threeEdge2 = threeEdge2
        # 三层最短边
        threeEdge3 = round(random.randint(0, 10) + random.random(), 2)
        self.threeEdge3 = threeEdge3
        # 三层体积
        threeVolume = threeEdge1 * threeEdge2 * threeEdge3 * 0.000001
        self.threeVolume = threeVolume
        # 三层重量
        threeWeight = round(random.randint(0, 10) + random.random(), 2)
        self.threeWeight = threeWeight



        # 构造提交参数
        data = {
            "productUuid": productUuid,
            "packageList": [{
                "productUuid": productUuid,
                "productNameFinal": res['retData']['main']['productNameFinal'],
                "brandName": res['retData']['main']['brandName'],
                "categoryPath": res['retData']['main']['categoryPath'],
                "spuNo": res['retData']['main']['spuNo'],
                "saleAttrInfo": res['retData']['main']['saleAttrInfo'],
                "manageArea": res['retData']['main']['manageArea'],
                "addPriceTypeStr": res['retData']['main']['addPriceTypeStr'],
                "skuNo": res['retData']['packageList'][0]['skuNo'],
                "specDetailStr": res['retData']['packageList'][0]['specDetailStr'],
                "packageLayers": packageLayers,
                "pieceInfo": pieceInfo,
                "barcode": barcode,
                "safetyRate": safetyRate,
                "saleMin": saleMin,
                "saleRestrict": "1",
                "packageLayersOptions": [
                    {
                    "optionValue": "SINGLE",
                    "optionHtml": "单品",
                    "selected": False
                    },
                    {
                        "optionValue": "ONE",
                        "optionHtml": "一层",
                        "selected": False
                    },
                    {
                        "optionValue": "TWO",
                        "optionHtml": "二层",
                        "selected": False
                    },
                    {
                        "optionValue": "THREE",
                        "optionHtml": "三层",
                        "selected": False
                    }
                ],
                "singlePackageUnit": res['retData']['packageList'][0]['singlePackageUnit'],
                "singlePackageCount": singlePackageCount,
                "singleEdge1":singleEdge1,
                "singleEdge2": singleEdge2,
                "singleEdge3": singleEdge3,
                "singleVolume": singleVolume,
                "singleWeight": singleWeight,
                "onePackageUnit": onePackageUnit,
                "onePackageCount": onePackageCount,
                "oneEdge1": oneEdge1,
                "oneEdge2": oneEdge2,
                "oneEdge3": oneEdge3,
                "oneVolume": oneVolume,
                "oneWeight": oneWeight,
                "twoPackageUnit": twoPackageUnit,
                "twoPackageCount": twoPackageCount,
                "twoEdge1": twoEdge1,
                "twoEdge2": twoEdge2,
                "twoEdge3": twoEdge3,
                "twoVolume": twoVolume,
                "twoWeight": twoWeight,
                "threePackageUnit": threePackageUnit,
                "threePackageCount": threePackageCount,
                "threeEdge1": threeEdge1,
                "threeEdge2": threeEdge2,
                "threeEdge3": threeEdge3,
                "threeVolume": threeVolume,
                "threeWeight": threeWeight
            }]
        }
        url = self.host + '/sysback/prepare/commit/package/savePackage?menuId=239&buttonId=2'
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retMessage'] == '', '{}, 待准入完善sku信息报错, {}\n{}'.format(productUuid, res['retMessage'], data)
        print('完善成功')

    # 完善供货信息, 单计量全国统一
    def supplyInfo(self, productUuid, purchasePriceType):
        self.purchasePriceType = purchasePriceType   # 进价类型  1 统一   2  区域
        if purchasePriceType != '1' and purchasePriceType != '2':
            assert False, '进价类型传参错误'

        # 验证表头
        url = self.host + '/sysback/supplyproductrel/getTopInfo?menuId=239&buttonId=2'
        data = {'productUuid':productUuid}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善供货信息，获取表头信息失败, {}\nres:{}'.format(productUuid, res)
        assert res['retData']['productName'] == self.brandName + ' ' + self.productName, '完善供货信息，获取表头信息失败, {}\nexp:{}, fact:{}'.format(productUuid, self.brandName + ' ' + self.productName, res['retData']['productName'])
        assert res['retData']['manageArea'] == self.manage_area_ch, '完善供货信息，获取表头信息失败, {}\nexp:{}, fact:{}'.format(productUuid, self.manage_area_ch, res['retData']['manageArea'])
        print('判断表头信息成功')

        # 获取销售区域
        url = self.host + '/sysback/supplyinfofromsrcm/getAllAreaFromScrm?menuId=239&buttonId=2'
        res = requests.post(url, headers = self.json_header).json()
        assert res['retMessage'] == 'success' and len(res['retData']) == 16, '完善供货信息，获取销售区域报错, url:{}\nres:{}'.format(url, res)
        areaName = ['北京区域','天津区域','重庆区域','陕西区域','河南区域','山东区域','广东区域','山西区域','湖南区域','江西区域','四川区域','湖北区域','江苏区域','浙江区域','安徽区域','云南区域']
        tempArea = set()
        print('销售区域信息获取成功')

        # 随机选择销售区域，必含北京
        for i in range(random.randint(0, 16)):
            tempArea.add(random.choice(areaName))
        tempArea.add('北京区域')
        areaObj = list()     # [{areaId: 100, areaCode: "101", areaName: "北京区域"}]
        for i in res['retData']:
            if i['areaName'] in tempArea:
                areaObj.append(i)
        print('销售区域选择完成')

        # 获取商品基础信息
        url = self.host + '/sysback/skuaudit/list/getAuditSkuByProduct?menuId=239&buttonId=147'
        data = {'productUuid':productUuid}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == '', '完善供货信息，获取商品信息失败\n{}'.format(res)
        assert res['retData'][0]['addPriceType'] == self.addPriceType and res['retData'][0]['addPriceTypeStr'] == self.addPriceTypeStr, '完善供货信息，加价类型不对\nexp:{}, fact:{}, spu:{}'.format(self.addPriceTypeStr, res['retData'][0]['addPriceTypeStr'], self.spuNo)
        assert res['retData'][0]['brandName'] == self.brandName, '完善供货信息，品牌不对\nexp:{}, fact:{}, spu:{}'.format(self.brandName, res['retData'][0]['brandName'], self.spuNo)
        assert res['retData'][0]['mainUnitStr'] == self.mainUnitName, '完善供货信息，计量单位不对\nexp:{}, fact:{}, spu:{}'.format(self.mainUnitName, res['retData'][0]['mainUnitStr'], self.spuNo)
        assert res['retData'][0]['productName'] == self.brandName + ' ' + self.productName, '完善供货信息，商品名称不对\nexp:{}, fact:{}, spu:{}'.format(self.brandName + ' ' + self.productName, res['retData'][0]['productName'], self.spuNo)
        assert res['retData'][0]['productTypeStr'] == self.productTypeStr, '完善供货信息，商品类型不对\nexp:{}, fact:{}, spu:{}'.format(self.productTypeStr, res['retData'][0]['productTypeStr'], self.spuNo)
        priceCommitParam = res['retData'][0]
        print('商品信息验证完成')
        # 提交时候用到的参数
        skuUuid = res['retData'][0]['skuUuid']
        skuHelpCode = res['retData'][0]['skuHelpCode']
        specDefault = res['retData'][0]['specDefault']
        specDetail = res['retData'][0]['specDetail']
        specDetailStr = res['retData'][0]['specDetailStr']
        # 获取供应商，只做断言，没别的用
        su_url = self.host + '/sysback/supplyinfofromsrcm/getSupplyPageFromScrm?menuId=239&buttonId=147'
        su_data = {'nowPage':1, 'pageShow':10, 'supplyName':''}
        su_res = requests.post(su_url, headers = self.form_header, data = su_data).json()
        assert su_res['retStatus'] == '1' and len(su_res['retData']['results']) == 10, '待准入完善供货信息，查询供应商失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, su_url, su_data, su_res)
        print('供应商信息获取成功')

        # 设置参照城市
        # 获取销售省和供货省，销售省-供货省，如果为空集则全部参照自己，否则需要设置参照，参照比例统一为2
        url = self.host + '/sysback/supplyinfofromsrcm/getSupplyCityByAreaCodes?menuId=239&buttonId=147'
        areaCode = ''
        for i in areaObj:
            areaCode += i['areaCode'] + ','
        saleAreaCode = areaCode[0:-1]
        self.saleAreaCode = saleAreaCode
        data['areaCode'] = saleAreaCode
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '设置参照城市,接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == 'success', '获取销售城市失败, {}\n{}'.format(productUuid, res['retMessage'])
        saleCityObj = res['retData']
        saleCityCode = set()
        for i in res['retData']:
            assert i['areaCode']!='' or i['areaCode']!=None, '完善供货信息，获取销售城市缺少区域编码, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            assert i['areaName']!='' or i['areaName']!=None, '完善供货信息，获取销售城市缺少区域名称, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            assert i['cityCode']!='' or i['cityCode']!=None, '完善供货信息，获取销售城市缺少城市编码, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            assert i['cityName']!='' or i['cityName']!=None, '完善供货信息，获取销售城市缺少城市名称, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            assert i['provinceCode']!='' or i['provinceCode']!=None, '完善供货信息，获取销售城市缺少省编码, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            assert i['provinceName']!='' or i['provinceName']!=None, '完善供货信息，获取销售城市缺少省名称, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            saleCityCode.add(i['cityCode'])

        url = self.host + '/sysback/supplyinfofromsrcm/getSupplyProvinceBySupplyNo?menuId=239&buttonId=147'
        data = {'supplierCode': '11297'}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '获取供货城市,接口请求失败, {}\n{}'.format(url, e)
        assert res['retMessage'] == 'success', '获取供货城市失败, {}\n{}'.format(productUuid, res['retMessage'])
        supplyCityCode = set()
        for i in res['retData']:
            assert i['cityCode'] != '' or i['cityCode'] != None, '完善供货信息，获取供货城市缺少编码, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            assert i['cityName'] != '' or i['cityName'] != None, '完善供货信息，获取供货城市缺少名称, {}\nurl:{}, data:{}, res:{}'.format(productUuid,url, data, res)
            supplyCityCode.add(i['cityCode'])

        # 保存，需要请求四个接口
        # 1.创建商品销售区域
        url = self.host + '/sysback/supplysaleareaproductrel/createRel?chooseAll=&menuId=239&buttonId=147'
        data = {'productUuid': productUuid, 'areaCodes':saleAreaCode}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善供货信息，创建销售区域失败, {}\nurl:{}, data:{}, res:{}'.format(productUuid, url, data, res)
        print('1.创建商品销售区域成功')

        # 2.供应商和sku关系
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        url = self.host + '/sysback/supplyskurel/batchCreateSupplySkuRel?batchState=prepareing&menuId=239&buttonId=147'
        data = []
        param = dict()
        param['addPriceType'] = self.addPriceType
        param['addPriceTypeStr'] = self.addPriceTypeStr
        param['areaNo'] = None
        param['auditState'] = None
        param['auditStateStr'] = None
        param['auditTime'] = None
        param['auditorName'] = None
        param['barcode'] = None
        param['brandName'] = self.brandName
        param['brandUuid'] = None
        param['brandseries'] = None
        param['buttonId'] = None
        param['cashDistribMoney'] = None
        param['cashPrice'] = None
        param['categoryName'] = None
        param['categoryNo'] = None
        param['categoryPath'] = None
        param['categoryProductType'] = None
        param['categoryUuid'] = None
        param['categoryUuid1'] = None
        param['categoryUuid2'] = None
        param['categoryUuid3'] = None
        param['categoryUuid4'] = None
        param['classificationName'] = None
        param['contractPrice'] = None
        param['costPrice'] = None
        param['costPriceTax'] = None
        param['createOpeTime'] = now
        param['createOper'] = self.user_id
        param['dealMode'] = None
        param['defaultTemplateCityName'] = "北京市"  # 默认参照城市，写死北京市
        param['defaultTemplateCityUuid'] = "110100"
        param['delFlag'] = 1
        param['edge1'] = None
        param['edge2'] = None
        param['edge3'] = None
        param['enableStatus'] = "1"
        param['enableStatusStr'] = "启用"
        param['enumTempProduct'] = None
        param['exchangeGoodsCondition'] = ""
        param['exchangeGoodsDay'] = 0
        param['exchangeGoodsStatus'] = ""
        param['factoryCode'] = ""
        param['factoryFacePrice'] = 0
        param['factoryName'] = ""
        param['helpCode'] = None
        param['hrAreaId'] = None
        param['hrDepartmentNumber'] = None
        param['isDelete'] = None
        param['isMainSupply'] = "1"
        param['isMetal'] = None
        param['isPriceSensitive'] = None
        param['isPurchaseMultiUnit'] = None
        param['isSaleMultiUnit'] = None
        param['limitShowPlatform'] = None
        param['limitShowPrice'] = None
        param['limitTradePrice'] = None
        param['loginUserId'] = None
        param['mainUnitDecimals'] = self.mainUnitdecimal
        param['mainUnitStr'] = self.mainUnitName
        param['mainUnitUuid'] = self.mainUnitId
        param['mapCondition'] = {}
        param['marketingAttr'] = None
        param['menuId'] = None
        param['minOrderGoodsNum'] = 0
        param['minReOrExNum'] = 0
        param['minSaleImperfectionsNum'] = 0
        param['opeTime'] = now
        param['oper'] = self.user_id
        param['operName'] = None
        param['operationNumber'] = None
        param['orderIndex'] = None
        param['orgId'] = self.orgId
        param['otherPromise'] = ""
        param['packageDetailList'] = None
        param['pieceInfo'] = None
        param['priceDecimals'] = None
        param['productAddState'] = None
        param['productAddStateStr'] = None
        param['productCurrent'] = None
        param['productManagerArea'] = None
        param['productName'] = self.brandName + ' ' + self.productName
        param['productPacking'] = ""
        param['productType'] = self.productType
        param['productTypeStr'] = self.productTypeStr
        param['productUuid'] = productUuid
        param['purchasePrice'] = 0
        if self.isPurchaseMultiUnit == '1':
            param['purchaseUnitDecimals'] = self.secondUnitdecimal
            param['purchaseUnitStr'] = self.secondUnitName
            param['purchaseUnitUuid'] = self.secondUnitId
        else:
            param['purchaseUnitDecimals'] = self.mainUnitdecimal
            param['purchaseUnitStr'] = self.mainUnitName
            param['purchaseUnitUuid'] = self.mainUnitId
        param['returnGoodsCondition'] = ""
        param['returnGoodsDay'] = 0
        param['returnGoodsStatus'] = ""
        param['rewardProgram'] = None
        param['safetyRate'] = None
        param['saleAttrInfo'] = None
        param['saleMin'] = None
        param['salePrice'] = None
        param['skuCount'] = None
        param['skuHelpCode'] = skuHelpCode
        param['skuId'] = None
        param['skuName'] = self.brandName + ' ' + self.productName + ' ' + self.specName
        param['skuNo'] = self.skuNo
        param['skuUuid'] = skuUuid
        param['sortName'] = "opeTime"
        param['sortType'] = "desc"
        param['specColorStr'] = ""
        param['specDefault'] = specDefault
        param['specDetail'] = specDetail
        param['specDetailStr'] = specDetailStr
        param['spuName'] = None
        param['spuNo'] = self.spuNo
        param['spuUuid'] = None
        param['state'] = "1"
        param['stateStr'] = "上架"
        param['supplierClaimState'] = "1"
        param['supplierClaimUuid'] = None
        param['supplierPriceClaimState'] = "1"
        param['supplierPriceClaimUuid'] = None
        param['supplyUuid'] = "11297"   # 供应商写死11297
        param['taxRate'] = None
        param['unitDecimals'] = self.mainUnitdecimal
        param['unitName'] = self.mainUnitName
        param['unitUuid'] = self.mainUnitId
        param['uuid'] = self.mainUnitId
        param['version'] = 0
        param['volume'] = None
        param['warrantyDay'] = 0
        param['warrantyStatus'] = ""
        param['weight'] = None
        data.append(param)
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善供货信息报错,{}\nurl:{}, data:{}, res:{}'.format(productUuid, url, data, res)
        print('2.供货关系维护成功')

        # 3.设置参照关系
        url = self.host + '/sysback/supplyarea/batchCreateSupplyArea?menuId=239&buttonId=2'
        tempSelf = supplyCityCode & saleCityCode   # 参照自己的城市代码
        tempOther = saleCityCode - supplyCityCode   # 需要设置参照的城市代码
        self.tempSelf = tempSelf
        self.tempOther = tempOther
        data = list()
        for i in saleCityObj:
            temp = dict()
            temp['buyPriceRatio'] = 1   # 进价参照比例
            temp['isMainSupply'] = 1   # 主供
            temp['isSupply'] = 1      # 供货
            temp['mainUnitStr'] = self.mainUnitName  # 计量单位
            temp['productUuid'] = productUuid


            if i['cityCode'] in tempSelf:   # 参照自己的
                temp['costPriceRatio'] = 1
                temp['saleAreaName'] = i['areaName']
                temp['saleAreaUuid'] = i['areaCode']   # 销售区域id
                temp['saleCityName'] = i['cityName']
                temp['saleCityUuid'] = i['cityCode']
                temp['saleProvinceName'] = i['provinceName']
                temp['saleProvinceUuid'] = i['provinceCode']
                temp['supplyUuid'] = '11297'
                temp['templateCityName'] = i['cityName']  # 参照城市名
                temp['templateCitySaleAreaName'] = i['areaName']      # 参照城市的销售区域名
                temp['templateCitySaleAreaNo'] = i['areaCode']
                temp['templateCityUuid'] = i['cityCode']

            elif i['cityCode'] in tempOther:    # 需要设置参照的, 成本比例都为  2
                temp['costPriceRatio'] = 2
                temp['saleAreaName'] = i['areaName']
                temp['saleAreaUuid'] = i['areaCode']   # 销售区域id
                temp['saleCityName'] = i['cityName']
                temp['saleCityUuid'] = i['cityCode']
                temp['saleProvinceName'] = i['provinceName']
                temp['saleProvinceUuid'] = i['provinceCode']
                temp['supplyUuid'] = '11297'
                temp['templateCityName'] = '北京市'  # 统一参照北京
                temp['templateCitySaleAreaName'] = '北京区域'      # 参照城市的销售区域名
                temp['templateCitySaleAreaNo'] = '101'
                temp['templateCityUuid'] = '110100'

            else:
                assert False,'即将设置的城市，既不在参照自己，也不在需要设置参照里, {}\ncode:{}, self:{}, other:{}'.format(productUuid, i['cityCode'], tempSelf, tempOther)
            data.append(temp)
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '待准入完善供货信息，提交参照信息报错，{}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
        print('3.参照关系提交成功')

        # 4.创建供货区域价格
        url = self.host + '/sysback/supplyareaprice/batchCreateSupplyAreaPrice?batchState=prepareing&menuId=239&buttonId=2'
        data = list()

        # 单计量
        if self.secondUnitName == None:
            # 全国统一
            if purchasePriceType == '1':
                if self.addPriceType == '1':

                    # priceCommitParam['supplyUuid'] = '11297'
                    # priceCommitParam['purchasePriceType'] = purchasePriceType
                    # priceCommitParam['processRateOrPrice'] = ''  # 加工比例或金额
                    # priceCommitParam['fujiliang'] = ''
                    # priceCommitParam['supplyUnit'] = ''
                    # priceCommitParam['mainUnitCostPrice'] = ''   # 主计量成本价
                    # priceCommitParam['rebateRatio'] = ''   # 返利折合比例
                    # priceCommitParam['isMainSupply'] = '1'
                    # priceCommitParam['templateCityUuid'] = '110100'
                    # priceCommitParam['mainPurchasePrice'] = ''    # 主计量进价
                    # priceCommitParam['rebateOrPrice'] = '11297'
                    # priceCommitParam['mainConvertRatio'] = '11297'
                    # priceCommitParam['processChargesRatio'] = '11297'
                    # priceCommitParam['factoryFacePrice'] = '11297'
                    # priceCommitParam['packRateOrPrice'] = '11297'
                    # priceCommitParam['zhugong'] = '11297'
                    # priceCommitParam['carriageRateOrPrice'] = '11297'
                    # priceCommitParam['packRatio'] = '11297'
                    # priceCommitParam['enterPriceType'] = '11297'
                    # priceCommitParam['supplyMainUnit'] = '11297'
                    # priceCommitParam['freightRatio'] = '11297'

                    # data.append(priceCommitParam)


                    # 先用老的
                    temp = dict()
                    self.mainPurchasePrice = random.randint(100, 200)  # 进价
                    self.factoryFacePrice = round(random.randint(0, 100) + random.random(), 2)   # 厂家面价
                    self.purchasePriceNote = self.getString(10)   # 进价备注
                    self.freightRatio = random.randint(0, 10)        # 运费折合比例
                    self.processChargesRatio = random.randint(0, 10)   # 加工折合比例
                    self.packRatio = random.randint(0, 10)       # 包装折合比例
                    self.rebateRatio = random.randint(0, 10)         # 返利折合比例
                    self.mainUnitCostPrice = self.mainPurchasePrice + self.freightRatio + self.processChargesRatio + self.packRatio - self.rebateRatio   # 成本价

                    temp['addPriceType'] = self.addPriceType
                    temp['mainPurchasePrice'] =  self.mainPurchasePrice  # 进价
                    temp['factoryFacePrice'] = self.factoryFacePrice   # 厂家面价
                    temp['purchasePriceNote'] = self.purchasePriceNote   # 进价备注
                    temp['freightRatio'] = self.freightRatio       # 运费折合比例
                    temp['processChargesRatio'] = self.processChargesRatio   # 加工折合比例
                    temp['packRatio'] = self.packRatio       # 包装折合比例
                    temp['rebateRatio'] = self.rebateRatio         # 返利折合比例
                    temp['isMainSupply'] = '1'    # 主供

                    temp['mainUnitCostPrice'] = self.mainUnitCostPrice   # 成本价
                    temp['mainUnitStr'] = self.mainUnitName      # 计量单位
                    temp['mainUnitUuid'] = ''   # 计量单位id，传空
                    temp['productUuid'] = productUuid
                    temp['purchasePrice'] = 0   # 进价，单计量直接是 0
                    temp['purchasePriceType'] = purchasePriceType   # 进价类型，1 统一  2 区域
                    temp['skuNo'] = self.skuNo
                    temp['specDetailStr'] = specDetailStr
                    temp['supplyUuid'] = '11297'
                    temp['templateCityUuid'] = '110100'
                    temp['unitName'] = self.mainUnitName
                    temp['mainConvertRatio'] = ''  # 主计量转换率
                    data.append(temp)

            # 区域
            else:
                pass


        # 多计量
        else:
            pass



        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '待准入完善供货信息，提交价格信息报错, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url,data, res)
        print('4.价格提交成功')

    # 完善售价，全国统一
    def salePriceInfo(self, productUuid):
        # 获取基本信息
        url = self.host + '/sysback/salepricesku/getTopAndSalepriceSkuList?menuId=239&buttonId=2'
        data = {'productUuid':productUuid,'saleType':1,'cityCode':''}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善售价，获取基本信息失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
        # 判断默认主城市够不够
        salePriceArea = set()
        for i in res['retData']['saleAreaList']:
            salePriceArea.add(i['areaCode'])
        costPriceArea = self.saleAreaCode.split(',')
        costPriceArea = set(costPriceArea)
        assert salePriceArea ^ costPriceArea == set(), '选择默认主城市时候，可选数量不符, {}\nexp:{}\nfact:{}'.format(productUuid, costPriceArea, salePriceArea)
        # 判断基本信息
        assert res['retData']['salePriceMainList'][0]['addPriceTypeName'] == self.addPriceTypeStr, '完善售价，加价类型不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.addPriceTypeStr, res['retData']['salePriceMainList'][0]['addPriceTypeName'])
        assert res['retData']['salePriceMainList'][0]['mainUnit'] == self.mainUnitName, '完善售价，主计量单位不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.mainUnitName, res['retData']['salePriceMainList'][0]['mainUnit'])
        assert res['retData']['salePriceMainList'][0]['productName'] == self.productName, '完善售价，商品名称不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.productName, res['retData']['salePriceMainList'][0]['productName'])
        assert res['retData']['salePriceMainList'][0]['productTypeStr'] == self.productTypeStr, '完善售价，商品类型不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.productTypeStr, res['retData']['salePriceMainList'][0]['productTypeStr'])
        assert res['retData']['salePriceMainList'][0]['spec'] == self.specName, '完善售价，主计量单位不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.specName, res['retData']['salePriceMainList'][0]['spec'])
        assert res['retData']['topInfo']['brandName'] == self.brandName, '完善售价，品牌不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.brandName, res['retData']['topInfo']['brandName'])
        assert res['retData']['topInfo']['manageArea'] == self.manage_area_ch, '完善售价，管理区域不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.manage_area_ch, res['retData']['topInfo']['manageArea'])
        assert res['retData']['topInfo']['productName'] == self.brandName + ' ' + self.productName, '完善售价，商品名称不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.brandName + ' ' + self.productName, res['retData']['topInfo']['productName'])
        assert res['retData']['topInfo']['supplyGoodsUnit'] == self.mainUnitName, '完善售价，计量单位不对,{}\nexp:{}\nfact:{}'.format(productUuid, self.mainUnitName, res['retData']['topInfo']['supplyGoodsUnit'])

        # 随机选择一个默认主城市, 获取成本
        cityObj = random.choice(res['retData']['saleAreaList'])
        url = self.host + '/sysback/salepricesku/batchCalculatePriceRow?menuId=239&buttonId=2'
        data = list()
        temp = dict()
        temp["addPriceType"] = self.addPriceType
        temp["addPriceTypeName"] = self.addPriceTypeStr
        temp["areaCode"] = cityObj['areaCode']
        temp["areaName"] = cityObj['areaName']
        temp["areaNo"] = None
        temp["backUnitCashPrice"] = None
        temp["backUnitDistribPrice"] = None
        temp["backUnitSalePrice"] = None
        temp["brandName"] = None
        temp["brandUuid"] = None
        temp["buttonId"] = None
        temp["cashAddRateOrMoney"] = None
        temp["cashBackUnitAddRateOrMoney"] = None
        temp["cashBackUnitBatchPrice"] = None
        temp["cashDistribMoney"] = None
        temp["cashPrice"] = None
        temp["categoryPath"] = None
        temp["categoryUuid"] = None
        temp["cityCode"] = cityObj['saleCityNo']
        temp["cityName"] = cityObj['saleCityName']
        temp["createOpeTime"] = None
        temp["createOper"] = None
        temp["delFlag"] = 1
        temp["distribCashDiffRateOrMoney"] = None
        temp["enumTxtInput"] = 0
        temp["exConverRate"] = None
        temp["facePrice2"] = None
        temp["groupName"] = "全国"
        temp["groupUuid"] = "-1"
        temp["hrAreaId"] = None
        temp["hrDepartmentNumber"] = None
        temp["isPriceSensitive"] = None
        temp["isSaleMultiUnit"] = "2"
        temp["lessAreaBidPrice"] = None
        temp["limitShowPrice"] = None
        temp["limitTradePrice"] = None
        temp["loginUserId"] = None
        temp["mainUnit"] = "立方米"
        temp["mainUnitCashPrice"] = None
        temp["mainUnitDistribPrice"] = None
        temp["mainUnitPrice"] = None
        temp["mainUnitSalePrice"] = None
        temp["mapCondition"] = {}
        temp["menuId"] = None
        temp["opeTime"] = None
        temp["oper"] = None
        temp["operationNumber"] = None
        temp["orgId"] = None
        temp["productName"] = self.productName
        temp["productTypeStr"] = self.productTypeStr
        temp["productUuid"] = productUuid
        temp["profit"] = None
        temp["provinceCode"] = None
        temp["provinceName"] = None
        temp["realBackUnitPrice"] = None
        temp["realCashPriceAddRate"] = None
        temp["realConverRate"] = None
        temp["realDistribPriceAddRate"] = None
        temp["realSalePriceAddRate"] = None
        temp["saleAddRateOrMoney"] = None
        temp["saleBackUnitAddRateOrMoney"] = None
        temp["saleBackUnitBatchPrice"] = None
        temp["salePrice"] = None
        temp["saleType"] = "1"
        temp["saleTypeName"] = "统一售价"
        temp["skuNo"] = self.skuNo
        temp["sortName"] = "opeTime"
        temp["sortType"] = "desc"
        temp["spec"] = self.specName
        temp["spuNo"] = None
        temp["theoryBackUnitPrice"] = None
        temp["theoryConverRate"] = None
        temp["uuid"] = None
        temp["version"] = 0
        data.append(temp)
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '选择默认主城市失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
        if cityObj['saleCityNo'] in self.tempOther:
            assert res['retData']['calculateResult'][0]['mainUnitPrice'] == self.mainUnitCostPrice*2, '完善售价，成本价代入不对, {}\nexp:{}\nfact:{}'.format(productUuid, self.mainUnitCostPrice*2, res['retData']['calculateResult'][0]['mainUnitPrice'])
        else:
            assert res['retData']['calculateResult'][0]['mainUnitPrice'] == self.mainUnitCostPrice, '完善售价，成本价代入不对, {}\nexp:{}\nfact:{}'.format(productUuid, self.mainUnitCostPrice, res['retData']['calculateResult'][0]['mainUnitPrice'])
        costPrice = res['retData']['calculateResult'][0]['mainUnitPrice']
        lessAreaBidPrice = res['retData']['calculateResult'][0]['lessAreaBidPrice']
        # 完善现金价, 销售面价，补成本价，全国最低价
        saleFacePrice = round(random.randint(10, 50) + random.random(), 2)
        self.saleFacePrice = saleFacePrice  # 销售面价
        data = temp
        cashPrice = costPrice + random.randint(10, 50)
        self.cashPrice = cashPrice   # 现金价
        data['cashPrice'] = cashPrice
        data['facePrice2'] = saleFacePrice
        data['lessAreaBidPrice'] = lessAreaBidPrice
        data['mainUnitPrice'] = costPrice
        url = self.host + '/sysback/salepricesku/calculatePriceRow?menuId=239&buttonId=2'
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善现金价失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
        # 完善分销价，补现金价加价率
        data['cashAddRateOrMoney'] = res['retData']['cashAddRateOrMoney']
        distributePrice = random.randint(int(costPrice) + 1, int(cashPrice)-1)
        self.distributePrice = distributePrice
        data['cashDistribMoney'] = distributePrice
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善分销价失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
        # 完善售价, 补分销价加价率
        data['distribCashDiffRateOrMoney'] = res['retData']['distribCashDiffRateOrMoney']
        salePrice = random.randint(int(cashPrice) + 1, int(cashPrice) + 100)
        self.salePrice = salePrice
        data['salePrice'] = salePrice
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善分销价失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
        # 补售价加价率，限制展示价，限制交易价
        data['saleAddRateOrMoney'] = res['retData']['saleAddRateOrMoney']
        limitShowPrice = round(random.randint(10,100) + random.random(), 2)
        limitTradePrice = limitShowPrice - round(random.randint(1,3) + random.random(), 2)
        self.limitShowPrice = limitShowPrice
        self.limitTradePrice = limitTradePrice
        data['limitShowPrice'] = limitShowPrice
        data['limitTradePrice'] = limitTradePrice

        # 准备提交
        data['productName'] = self.brandName + ' ' + self.productName
        data['profit'] = res['retData']['profit']
        data['realCashPriceAddRate'] = res['retData']['realCashPriceAddRate']
        data['realDistribPriceAddRate'] = res['retData']['realDistribPriceAddRate']
        data['realSalePriceAddRate'] = res['retData']['realSalePriceAddRate']
        data['saleAddRateOrMoney'] = res['retData']['saleAddRateOrMoney']
        data['enumTxtInput'] = res['retData']['enumTxtInput']
        final_data = dict()
        final_data['addPriceType'] = self.addPriceType
        final_data['areaType'] = '1'
        final_data['mainUnit'] = self.mainUnitName
        final_data['productUuid'] = productUuid
        final_data['salePriceMainList'] = [data]
        final_data['saleType'] = '1'
        data = {'t':final_data}
        url = self.host + '/sysback/salepricesku/createComplateSaleSku?menuId=239&buttonId=2'
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '完善售价信息，提交失败,{}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)

    # 完善图文介绍
    def picIntroduce(self, productUuid):
        mainPic = '/2021-11-30/FILE56879f981de24fc99b90dd7afb95e70f.jpg'
        multiPic = ['/2021-11-30/FILEe0fc3c45f9ca477baf3602aba2ba315c.jpg', '/2021-11-30/FILE5702ce2111674bb59fc9b04d3b7da48f.jpg', '/2021-11-30/FILE108eec15b0b34ff1aa4498270fec9813.jpg']
        data = dict()
        data['type'] = '1'
        data['recordNo'] = ''
        data['productUuid'] = productUuid
        data['skuImageUpdateList'] = []
        data['descriptionUpdate'] = {'appdescrition':'', 'currency':'1', 'description':''}
        data['mainImageUpdate'] = {'mainImageKey':'', 'saleVideoKey':'', 'trimmingKey':mainPic, 'videoKey':''}
        data['multiImageUpdateList'] = []
        for i in multiPic:
            calc = 10
            temp = dict()
            temp['basicImageKey'] = i
            temp['position'] = calc
            temp['trimming'] = 1
            calc += 1
            data['multiImageUpdateList'].append(temp)
        url = self.host + '/sysback/productinfoupdate/createProductPicInfo?menuId=239&buttonId=2'
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '待准入完善图片失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)

    # 完善验收标准
    def standardInfo(self, productUuid):
        url = self.host + '/sysback/prepare/commit/acceptance/queryAcceptance?productUuid={}&menuId=239&buttonId=2'.format(productUuid)
        try:
            res = requests.post(url, headers = self.json_header, json={}).json()
        except Exception as e:
            assert False, '待准入完善验收标准，请求失败,  url:{}, exception:{}'.format(url, e)
        assert res['retStatus'] == '1', '待准入维护验收标准，获取信息失败, {}\nurl:{}\nres:{}'.format(productUuid, url, res)
        assert res['retData']['main']['addPriceTypeStr'] == self.addPriceTypeStr, '待准入完善验收标准,加价类型显示不正确, {}\nexp:{}\nfact:{}'.format(productUuid, self.addPriceTypeStr, res['retData']['main']['addPriceTypeStr'])
        assert res['retData']['main']['manageArea'] == self.manage_area_ch, '待准入完善验收标准,管理区域显示不正确, {}\nexp:{}\nfact:{}'.format(productUuid, self.manage_area_ch, res['retData']['main']['manageArea'])
        assert res['retData']['main']['productNameFinal'] == self.brandName + ' ' + self.productName, '待准入完善验收标准,商品名称显示不正确, {}\nexp:{}\nfact:{}'.format(productUuid, self.brandName + ' ' + self.productName, res['retData']['main']['productNameFinal'])
        assert res['retData']['standardList'] != [], '待准入完善验收标准,缺少sku信息, {}\nurl:{}\nres:{}'.format(productUuid, url, res)


        data = dict()
        data['productUuid'] = self.productUuid
        data['acceptList'] = []

        for skuInfo in res['retData']['standardList']:
            temp_data = dict()
            temp_data['brandName'] = self.brandName
            temp_data['categoryPath'] = res['retData']['main']['categoryPath']
            temp_data['checkFrequency'] = random.randint(1, 10)
            temp_data['checkTime'] = '入库前'
            temp_data['productNameFinal'] = res['retData']['main']['productNameFinal']
            temp_data['productUuid'] = self.productUuid
            temp_data['skuNo'] = self.skuNo
            temp_data['specDetailStr'] = self.specName
            temp_data['spuNo'] = self.spuNo
            temp_data['itemList'] = []
            for item in skuInfo['itemList']:

                if item['isNeed'] == '1':   # 必填

                    item['checkCount'] = random.randint(1, 10)  # 验收次数
                    item['standardValue'] = self.getString(10)  # 标准值
                    item['checkMethod'] = self.getString(10)  # 验方法

                    if item['checkItemType'] == '1':    # 类型  1数值   2文本
                        item['upDiffValue'] = random.randint(1, 10)
                        item['downDiffValue'] = random.randint(1, 10)

                    elif item['checkItemType'] == '2':

                        pass

                    else:
                        assert False, '待准入维护验收标准,多了个类型, {}, {}'.format(item['checkItemType'], productUuid)

                temp_data['itemList'].append(item)

            data['acceptList'].append(temp_data)


        url = self.host + '/sysback/prepare/commit/acceptance/saveAcceptance?menuId=239&buttonId=2'
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '待准入完善验收标准失败, {}'.format(self.productUuid)

    # 完善资质信息
    def qualification(self, productUuid):
        url = self.host + '/sysback/prepare/commit/qualification/queryQualification?productUuid={}&menuId=239&buttonId=2'.format(productUuid)
        res = requests.post(url, headers = self.json_header, json={}).json()
        assert res['retStatus'] == '1', '待准入完善资质信息失败, {}'.format(productUuid)
        assert res['retData']['main']['addPriceTypeStr'] == self.addPriceTypeStr, '待准入完善资质信息，加价类型不对, {}\nexp:{}\nfact:{}'.format(productUuid, self.addPriceTypeStr, res['retData']['main']['addPriceTypeStr'])
        assert res['retData']['main']['brandName'] == self.brandName, '待准入完善资质信息，品牌不对, {}\nexp:{}\nfact:{}'.format(productUuid, self.brandName, res['retData']['main']['brandName'])
        assert res['retData']['main']['manageArea'] == self.manage_area_ch, '待准入完善资质信息，管理区域不对, {}\nexp:{}\nfact:{}'.format(productUuid, self.manage_area_ch, res['retData']['main']['manageArea'])
        assert res['retData']['main']['productNameFinal'] == self.brandName + ' ' + self.productName, '待准入完善资质信息，商品名称不对, {}\nexp:{}\nfact:{}'.format(productUuid, self.brandName + ' ' + self.productName, res['retData']['main']['productNameFinal'])

        for i in res['retData']['quaList']:
            if i['mustHave'] == '1':   # 1 必填   2  非必填
                # 随机选个资质
                url = self.host + '/sysback/qualification/getAuditNotRelByCondition?relUuid=2b32623daf34451f9e31764186e623ad&menuId=239&buttonId=2'
                data = {"nowPage":1,"pageShow":10,"searchParam":"[{\"name\":\"qualificationName\",\"value\":\"\"},{\"name\":\"qualificationName_q\",\"value\":\"Like\"},{\"name\":\"supplyName\",\"value\":\"\"},{\"name\":\"supplyName_q\",\"value\":\"Like\"},{\"name\":\"qualificationCate\",\"value\":\"1\"},{\"name\":\"qualificationCate_q\",\"value\":\"EQ\"}]","sortName":"","sortType":""}
                try:
                    res = requests.post(url, headers = self.json_header, json=data).json()
                except Exception as e:
                    assert False, '接口请求失败,{}\n{}'.format(url, e)
                assert res['retStatus'] == '1' and len(res['retData']['results']) != 0, '待准入维护资质，获取数据失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)
                q = random.choice(res['retData']['results'])

                # 创建资质与行的关系
                url = self.host + '/sysback/qualificationskuqualificationrel/createAuditRelate?menuId=239&buttonId=2'
                data = {'qualificationUuids':q['uuid'],'relUuid':i['uuid']}
                try:
                    res = requests.post(url, headers = self.form_header, data = data).json()
                except Exception as e:
                    assert False, '接口请求失败, {}\n{}'.format(url, e)
                assert res['retStatus'] == '1', '待准入维护资质，创建关系失败, {}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)

        # 保存
        url = self.host + '/sysback/prepare/commit/qualification/saveQualification?menuId=239&buttonId=2'
        data = {"productUuid":productUuid,"notSpecList":[]}
        try:
            res = requests.post(url, headers = self.json_header, json=data).json()
        except Exception as e:
            assert False, '接口请求失败,{}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '待准入维护资质信息，保存失败,{}\nurl:{}\ndata:{}\nres:{}'.format(productUuid, url, data, res)

    # 提交
    def commit(self, productUuid):
        url = self.host + '/sysback/prepare/list/commitByProduct?menuId=240&buttonId=2'
        data = {'productUuids':productUuid}
        try:
            res = requests.post(url, headers = self.form_header, data = data).json()
        except Exception as e:
            assert False, '接口请求失败, {}\n{}'.format(url, e)
        assert res['retStatus'] == '1', '准入提交失败,{}'.format(productUuid)

    # 返回参数
    def parameters(self):
        p = dict()
        p['user_id'] = self.user_id
        p['orgId'] = self.orgId
        p['productName'] = self.productName   # 商品名称
        p['specName'] = self.specName      # 规格名称
        p['brandName'] = self.brandName     # 品牌名称
        p['productType'] = self.productType      # 商品类型
        p['productTypeStr'] = self.productTypeStr   # 商品类型   中文
        p['mainUnitName'] = self.mainUnitName      # 主计量单位名称  中文
        p['mainUnitId'] = self.mainUnitId        # 主计量单位id  中文
        p['mainUnitdecimal'] = self.mainUnitdecimal   # 主计量小数位
        p['addPriceTypeStr'] = self.addPriceTypeStr   # 加价类型  中文
        p['addPriceType'] = self.addPriceType   #
        p['productUuid'] = self.productUuid
        p['spuNo'] = self.spuNo
        p['skuNo'] = self.skuNo
        p['manage_area'] = self.manage_area         # 管理区域   uuid   1001
        p['manage_area_ch'] = self.manage_area_ch     # 管理区域，中文
        p['logistics_store'] = self.logistics_store       # 储存属性   中文集合
        p['manage_stock_period'] = self.manage_stock_period     # 囤货期
        p['manage_soldout_period'] = self.manage_soldout_period     # 下架期
        p['manage_cooperation'] = self.manage_cooperation     # 合作模式，必填
        p['manage_dealmode'] = self.manage_dealmode     # 经营模式，必填
        p['manage_packlist'] = self.manage_packlist     # 包装清单，必填
        p['manage_sellmanageperiod'] = self.manage_sellmanageperiod     # 售价管理周期，必填
        p['manage_outpos'] = self.manage_outpos      # 档次外部定位，必填
        p['manage_inpos'] = self.manage_inpos      # 档次内部定位，必填
        p['manage_season_product'] = self.manage_season_product      # 是否季节性商品
        p['marketing_saleplat'] = self.marketing_saleplat      # 售卖平台，必填
        p['tax_classify'] = self.tax_classify       # 归类名，必填，中文
        p['safetyRate'] = self.safetyRate       # 安全率/金额
        p['barcode'] = self.barcode   # 国际条形码
        p['saleMin'] = self.saleMin   # 最小起售量
        p['pieceInfo'] = self.pieceInfo   # 件装数量
        p['packageLayers'] = self.packageLayers # 层数
        p['singlePackageCount'] = self.singlePackageCount # 单品数量
        p['singleEdge1'] = self.singleEdge1   # 单品最长边
        p['singleEdge2'] = self.singleEdge2   # 单品次长边
        p['singleEdge3'] = self.singleEdge3    # 单品最短边
        p['singleVolume'] = self.singleVolume   # 单品体积
        p['singleWeight'] = self.singleWeight    # 单品重量
        p['onePackageUnit'] = self.onePackageUnit    # 一层包装单位
        p['onePackageCount'] = self.onePackageCount    # 一层数量
        p['oneEdge1'] = self.oneEdge1    # 一层最长边
        p['oneEdge2'] = self.oneEdge2    # 一层次长边
        p['oneEdge3'] = self.oneEdge3    # 一层最短边
        p['oneVolume'] = self.oneVolume   # 一层体积
        p['oneWeight'] = self.oneWeight    # 一层重量
        p['twoPackageUnit'] = self.twoPackageUnit    # 二层包装单位
        p['twoPackageCount'] = self.twoPackageCount    # 二层数量
        p['twoEdge1'] = self.twoEdge1    # 二层最长边
        p['twoEdge2'] = self.twoEdge2    # 二层次长边
        p['twoEdge3'] = self.twoEdge3    # 二层最短边
        p['twoVolume'] = self.twoVolume   # 二层体积
        p['twoWeight'] = self.twoWeight    # 二层重量
        p['threePackageUnit'] = self.threePackageUnit    # 三层包装单位
        p['threePackageCount'] = self.threePackageCount    # 三层数量
        p['threeEdge1'] = self.threeEdge1    # 三层最长边
        p['threeEdge2'] = self.threeEdge2    # 三层次长边
        p['threeEdge3'] = self.threeEdge3    # 三层最短边
        p['threeVolume'] = self.threeVolume   # 三层体积
        p['threeWeight'] = self.threeWeight    # 三层重量
        p['saleAreaCode'] = self.saleAreaCode  # 销售区域   区域编码字符串  101,102
        p['purchasePriceType'] = self.purchasePriceType
        p['tempSelf'] = self.tempSelf   # 参照自己的城市,集合
        p['tempOther'] = self.tempOther   # 参照别人的城市，集合
        p['mainPurchasePrice'] = self.mainPurchasePrice   # 进价
        p['factoryFacePrice'] = self.factoryFacePrice # 厂家面价
        p['purchasePriceNote'] = self.purchasePriceNote # 进价备注
        p['freightRatio'] = self.freightRatio # 运费比例
        p['packRatio'] = self.packRatio # 包装比例
        p['processChargesRatio'] = self.processChargesRatio # 加工费比例
        p['rebateRatio'] = self.rebateRatio # 返利折合比例
        p['mainUnitCostPrice'] = self.mainUnitCostPrice # 成本价
        p['cashPrice'] = self.cashPrice   # 现金价
        p['distributePrice'] = self.distributePrice   # 分销价
        p['salePrice'] = self.salePrice    # 售价
        p['saleFacePrice'] = self.saleFacePrice   # 销售面价
        p['limitShowPrice'] = self.limitShowPrice  # 限制展示价
        p['limitTradePrice'] = self.limitTradePrice   # 限制交易价
        return p


class MakePro(CommonFunction):

    def run(self):
        print('\n*************************************************')
        print('获取登录信息:')
        self.getLoginInfo()

        print('\n*************************************************')
        print('生成代码:')
        productUuid, standard, qualification = self.generateCode(LoginInfo.cate, '1', '2', '2')

        print('\n*************************************************')
        print('完善基本信息:')
        self.basicInfo(productUuid)

        print('\n*************************************************')
        print('完善管理信息:')
        self.manageInfo(productUuid)

        print('\n*************************************************')
        print('完善sku信息:')
        self.skuInfo(productUuid)

        print('\n*************************************************')
        print('完善供货信息:')
        self.supplyInfo(productUuid, '1')

        print('\n*************************************************')
        print('完善售价:')
        self.salePriceInfo(productUuid)

        print('\n*************************************************')
        print('完善图文:')
        self.picIntroduce(productUuid)

        print('\n*************************************************')
        print('完善验收标准:')
        if standard != 'OK':
            self.standardInfo(productUuid)

        print('\n*************************************************')
        print('完善资质:')
        if qualification!= 'OK':
            self.qualification(productUuid)

        print('\n*************************************************')
        print('提交:')
        self.commit(productUuid)

        return self.parameters()









