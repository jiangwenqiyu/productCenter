import requests
import pymysql
import xlsxwriter
import time
import datetime
import cx_Oracle

host = 'http://product.pre.xinfangsheng.com'   # 线上  http://product.xinfangsheng.com   t4  http://product.t4.xinfangsheng.com  仿真  http://product.pre.xinfangsheng.com
login_host = 'http://ssoin.pre.fsyuncai.com'   # 线上  http://ssoin.fsyuncai.com         t4  http://ssoin.test.xinfangsheng.com  仿真  http://ssoin.pre.fsyuncai.com

my_host = '172.19.2.184'      # 线上  192.168.0.184   t4  192.168.0.31   仿真    172.19.2.184
my_port = 3306                 # 线上  3306   t4  3307    仿真   3306
my_user = 'PRE_W'              # 线上  srm_r  t4  usercenter   仿真    PRE_W
my_password = 'ETezPf+W4QA9S1Yq'    # 线上  oK8De5Xz5u+NbZe1  t4 usercenter123!    仿真   ETezPf+W4QA9S1Yq
database = 'xfs_product_pre'       # 线上  xfs_product   t4 xfs_product_70w     仿真   xfs_product_pre


def getCur():

    con = pymysql.connect(host = my_host, port = my_port, user = my_user, password = my_password, database = database)
    cur = con.cursor()
    return cur, con


def getOra():
    con = cx_Oracle.connect('SUPPLIER/SUPPLIER@172.19.2.145/XFS')   # 仿真
    cur = con.cursor()
    return cur, con


def getsku():
    cur, con = getCur()
    sql = ''' select s.skuNo from product_sku s where s.oper = '-1' '''
    cur.execute(sql)
    data = cur.fetchall()
    skus = []
    for i in data:
        skus.append(i[0])
    cur.close()
    con.close()
    return skus


def productInfo(sku):
    sql = ''' select s.factoryFacePrice, s.templateCitySaleAreaNo, s.supplyUuid from product_supply_price s where s.skuNo = '{}' '''.format(sku)
    mycur, mycon = getCur()
    mycur.execute(sql)
    data = mycur.fetchall()
    for i in data:
        face = i[0]
        area = i[1]
        supply = i[2]
        oracleInfo(sku, face, area, supply)


def oracleInfo(sku, face, area, supplier):
    sql = ''' select jinjia.MJ1 from T_TJINFO jinjia
                inner join T_TJPRODUCT sku on sku.FID = jinjia.FPRODUCTID
                left join item.AREA area on area.AREA_ID = jinjia.FAREAID
                inner join T_SUPPLIERCONTRACT su on su.FSUPPLIERID = jinjia.FSUPPLIERID
                where sku.FNUMBER = '{}' and area.AREA_NUMBER = '{}' and su.FNUMBER = '{}' '''.format(sku, area, supplier)
    cur, con = getOra()
    cur.execute(sql)
    oface = cur.fetchone()[0]
    assert float(oface) == float(face), 'sku:{},商品中心:{},老数据:{},区域:{},供应商:{}'.format(sku, face, oface, area, supplier)


skus = getsku()
for sku in skus:
    try:
        productInfo(sku)
    except Exception as e:
        print(e)



