from environmentConfig import LoginInfo
import requests





class Test(LoginInfo):
    # 参照比例
    def templateRate(self):
        # LoginInfo.json_header['cookie'] = 'uc_token=e957c609b1554018ae97fe1dc86e9cf1'
        # LoginInfo.host = 'http://product.pre.xinfangsheng.com'

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
            assert False, assert_word





    def run(self):
        self.templateRate()

# Test().run()