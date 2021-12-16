import requests
import re
import pymysql


class Env():
    # 账号信息
    account = '2010368'
    password = 'xfs@1234'

    # 域名信息
    t4_host = 'http://product.t4.xinfangsheng.com'
    fangzhen_host = 'http://product.pre.xinfangsheng.com'
    host = ''   # 线上  http://product.xinfangsheng.com   t4  http://product.t4.xinfangsheng.com  仿真  http://product.pre.xinfangsheng.com

    # login_host = 'http://ssoin.pre.fsyuncai.com'   # 线上  http://ssoin.fsyuncai.com         t4  http://ssoin.test.xinfangsheng.com  仿真  http://ssoin.pre.fsyuncai.com

    # 数据库信息
    my_host = '172.19.2.184'      # 线上  192.168.0.184   t4  192.168.0.31   仿真    172.19.2.184
    my_port = 3306                 # 线上  3306   t4  3307    仿真   3306
    my_user = 'PRE_W'              # 线上  srm_r  t4  usercenter   仿真    PRE_W
    my_password = 'ETezPf+W4QA9S1Yq'    # 线上  oK8De5Xz5u+NbZe1  t4 usercenter123!    仿真   ETezPf+W4QA9S1Yq
    database = 'xfs_product_pre'       # 线上  xfs_product   t4 xfs_product_70w     仿真   xfs_product_pre

    # connect = pymysql.connect(host =my_host, port = my_port, user = my_user, password = my_password, database = database)
    # cur = connect.cursor()

    test_dingToken = 'https://oapi.dingtalk.com/robot/send?access_token=f7acf4dbf372ecedb2a93113aebf6eee6d8278de40599279f59a2774c5566ef5'

    form_header = {'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    json_header = {'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json;charset=UTF-8'}

    # token
    fangzhen_token = 'e957c609b1554018ae97fe1dc86e9cf1'
    t4_token = ''

    token = ''



class LoginInfo(Env):
    def __init__(self):
        pass

        # try:
        #     self.token = self.getToken(self.account, self.password)
        # except:
        #     assert False, '登录失败'

    def getToken(self, user, password):
        # 获取mtk
        url = self.login_host + '/login.php'
        data = {'backurl':self.host,
                'local':1,
                'is_sms_verify':'',
                'site':'uc',
                'username':user,
                'password':password}
        res = requests.post(url, headers = self.form_header, data = data).text
        pat = 'location.href = "(.*?)"'
        a = re.findall(pat, res)[0]
        pat = 'tk=(.*)'
        m_tk = re.findall(pat, a)[0]

        # 利用mtk获取token
        url = self.host + '/usercenter/web/login/login'
        header = {'Accept': 'application/json, text/plain, */*',
                  'Content-Type': 'application/json;charset=utf-8'}
        param = {'m_tk':m_tk}
        res = requests.get(url, headers = header, params = param).json()
        return res['data']['ucToken']







