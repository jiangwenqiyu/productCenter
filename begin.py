import sys
import requests
import makeProduct
from environmentConfig import LoginInfo
import alterProductPrice
import alterProductBasicInfo
import viewProduct



def run_flow(env):
    # obj = makeProduct.MakePro()
    # info = obj.run()
    # print(info)

    obj_makeProduct = makeProduct.MakePro()   # 制作商品
    obj_view = viewProduct.ProductManagement()      # 查看并修改
    obj_alterPrice = alterProductPrice.changeCostPrice()   # 修改价格，进价、参照、售价、售价类型、价格组
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
        res = requests.post(LoginInfo.test_dingToken, json=data).json()
        assert res['errmsg'] == 'ok', '钉钉报警失败'
        return




















def main():
    if sys.argv[1] == 't4':
        print('测试环境:t4')
        LoginInfo.host = LoginInfo.t4_host
        LoginInfo.token = LoginInfo.t4_token
        LoginInfo.form_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
        LoginInfo.json_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
    else:
        print('测试环境:仿真')
        LoginInfo.host = LoginInfo.fangzhen_host
        LoginInfo.token = LoginInfo.fangzhen_token
        LoginInfo.form_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
        LoginInfo.json_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)


    run_flow(sys.argv[1])


if __name__ == '__main__':
    main()




