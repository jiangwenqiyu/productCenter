import sys
import requests
import makeProduct
from environmentConfig import LoginInfo
import alterProductPrice
import alterProductBasicInfo
import viewProduct
import ImportantPointTest
import threading



def run_flow(env):
    print('-----------------------------------------------------------')
    print('-----------------------------------------------------------')
    print('开始流程测试')
    global flow_flag

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
        assert False, '流程测试结束, 未发现异常'
    except Exception as e:
        flow_flag = False
        word = '测试环境:{}\n{}'.format(env,e)
        data = {'text':{'content':'{}'.format(word)},
                'msgtype':'text'
                }
        res = requests.post(LoginInfo.dingToken, json=data).json()
        assert res['errmsg'] == 'ok', '钉钉报警失败\n{}'.format(res)
        return


def run_single(env):
    print('-----------------------------------------------------------')
    print('-----------------------------------------------------------')
    print('开始单点测试')
    global single_flag

    obj = ImportantPointTest.Test()
    testContent = '1.修改进价,所有城市进价+1\n2.对比进价单据原值与现值\n3.判断是否应生成售价单据\n4.判断售价单据中原值现值价格是否正确\n5.判断售价单据中未被影响的售价，原值现值是否一直\n6.对比cityPrice售价单据是否生效'
    try:
        obj.run()
        assert False, '单点测试结束，未发现异常'
    except Exception as e:
        single_flag = False
        word = '测试环境:{}\n{}'.format(env,e)
        data = {'text':{'content':'{}'.format(word)},
                'msgtype':'text'
                }
        res = requests.post(LoginInfo.dingToken, json=data).json()
        assert res['errmsg'] == 'ok', '钉钉报警失败\n{}'.format(res)
        return


flow_flag = True
single_flag = True
def main():
    LoginInfo.dingToken = sys.argv[2]
    environ = sys.argv[1]

    # LoginInfo.dingToken = 'https://oapi.dingtalk.com/robot/send?access_token=f7acf4dbf372ecedb2a93113aebf6eee6d8278de40599279f59a2774c5566ef5'
    # environ = 't4'

    if environ == 't4':
        print('测试环境:t4')
        LoginInfo.host = LoginInfo.t4_host
        LoginInfo.cityPrice = LoginInfo.t4_cityPrice
        LoginInfo.token = LoginInfo.t4_token
        LoginInfo.cate = LoginInfo.t4_cate
        LoginInfo.form_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
        LoginInfo.json_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
    else:
        print('测试环境:仿真')
        LoginInfo.host = LoginInfo.fangzhen_host
        LoginInfo.cityPrice = LoginInfo.fangzhen_cityPrice
        LoginInfo.token = LoginInfo.fangzhen_token
        LoginInfo.cate = LoginInfo.fangzhen_cate
        LoginInfo.form_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)
        LoginInfo.json_header['cookie'] = 'uc_token={}'.format(LoginInfo.token)


    t1 = threading.Thread(target=run_flow, args=(environ, ))
    t2 = threading.Thread(target=run_single, args=(environ, ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


    if flow_flag and single_flag:
        print('测试结束, 全程未发现错误')
    elif flow_flag==True and single_flag==False:
        print('测试结束, 单点测试发生错误')
    elif flow_flag==False and single_flag==True:
        print('测试结束, 流程测试发生错误')
    else:
        print('测试结束, 流程发生错误, 单点发生错误')


if __name__ == '__main__':
    main()




