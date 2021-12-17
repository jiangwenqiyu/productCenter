import sys
import requests
import makeProduct
from environmentConfig import LoginInfo
import alterProductPrice
import alterProductBasicInfo
import viewProduct
import ImportantPointTest



def run_flow(env):
    # obj = makeProduct.MakePro()
    # info = obj.run()
    # print(info)  ttt
    print('-----------------------------------------------------------')
    print('-----------------------------------------------------------')
    print('开始流程测试')

    obj_makeProduct = makeProduct.MakePro()   # 制作商品
    obj_view = viewProduct.ProductManagement()      # 查看并修改
    obj_alterPrice = alterProductPrice.changePrice()   # 修改价格，进价、参照、售价、售价类型、价格组
    obj_alterBasic = alterProductBasicInfo.BasicInfo()    # 修改表单

    try:
        info = obj_makeProduct.run()
        print(info)
        obj_view.run(info)
        obj_alterPrice.run(info)
        obj_alterBasic.run(info)
    except Exception as e:
        word = '测试环境:{}\n{}'.format(env,e)
        data = {'text':{'content':'{}'.format(word)},
                'msgtype':'text'
                }
        res = requests.post(LoginInfo.dingToken, json=data).json()
        assert res['errmsg'] == 'ok', '钉钉报警失败'
        return


def run_single(env):
    print('-----------------------------------------------------------')
    print('-----------------------------------------------------------')
    print('开始单点测试')

    obj = ImportantPointTest.Test()

    try:
        obj.run()
    except Exception as e:
        word = '测试环境:{}\n{}'.format(env,e)
        data = {'text':{'content':'{}'.format(word)},
                'msgtype':'text'
                }
        res = requests.post(LoginInfo.dingToken, json=data).json()
        assert res['errmsg'] == 'ok', '钉钉报警失败'
        return


def main():
    LoginInfo.dingToken = sys.argv[2]
    # LoginInfo.dingToken = 'https://oapi.dingtalk.com/robot/send?access_token=e68f44036d2948f7942fc1d4ee10bb8718e42545f87dac2b324b6e7ced94351a'
    # a = 't4'
    if sys.argv[1] == 't4':
        print('测试环境:t4')
        LoginInfo.host = LoginInfo.t4_host
        LoginInfo.token = LoginInfo.t4_token
        LoginInfo.cate = LoginInfo.t4_cate
        LoginInfo.form_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
        LoginInfo.json_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
    else:
        print('测试环境:仿真')
        LoginInfo.host = LoginInfo.fangzhen_host
        LoginInfo.token = LoginInfo.fangzhen_token
        LoginInfo.cate = LoginInfo.fangzhen_cate
        LoginInfo.form_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
        LoginInfo.json_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)


    run_flow(sys.argv[2])
    run_single(sys.argv[2])


if __name__ == '__main__':
    main()




