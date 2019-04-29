import requests
from requests.exceptions import RequestException
import re
import xlwt
from urllib.parse import urlencode
import time


def get_url(keyword, number_two):
    '''
        获取关键字的链接
        :param keyword:    关键字
        :param number_two:    不同的数值对应不同的页码，淘宝上第一页为0 ，第二页为44
                               第三页为88.。。。
        :return:   不同页码的链接
    '''
    data = {
        'ie': 'utf8',
        'initiative_id': 'staobaoz_20180830',
        'stats_click': 'search_radio_all:1',
        'js': '1',
        'imgfile': ' ',
        'q': keyword,
        'suggest': 'history_3',
        '_input_charset': 'utf - 8',
        'wq': ' ',
        'suggest_query': ' ',
        'source': 'suggest',
        'bcoffset': '6',
        'ntoffset': '6',
        'p4ppushleft': '1, 48',
        's': number_two
    }
    url = r'https://s.taobao.com/search?' + urlencode(data)
    return url


def get_html(url):
    '''
       获取网页源码
       注:   字典header必须要，模拟浏览器访问，如果没有，可能无法获取真正的网页源码
       :param url:
       :return:
       '''
    header = {
        'authority': 's.taobao.com',
        'method': 'GET',
        'path': '/search?q=%E5%8D%8E%E4%B8%BA&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 't=36cb250100b52693b17ae64bc1bfdd70; cna=VyPnE24R+BkCATutHgrsC+PV; thw=cn; enc=a3RNml%2FS%2BsGExETuWVzeQtnku9tWlLTy8SAFpvYnh8dmn1LPXEmw5YZa%2Bp6MFnSuPtZGWzYPfymeYAg6dyDCnw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; miid=75000991625205136; _m_h5_tk=31112bbc02d3d787d370cfe5fd3623f7_1535451779885; _m_h5_tk_enc=6cf0675f1fcc9c93fc7919e3da3e79db; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; v=0; cookie2=34115b060c8e01bc8e9915cd17f750a4; _tb_token_=e761eedae8eae; JSESSIONID=C52D3D32676B70B8B9A15B9865025A9A; isg=BJubrzdiRKUI97i8-ww_luaHKv-pbq751j8AYI3YdhqxbLtOFUQQwryuAozHzAdq',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }  # 模拟浏览器访问
    response = requests.get(url, headers=header)
    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print("页面请求错误！")
        return None


def get_select(html, num_one):
    row = ['名称', '价格', '销量']
    reg_lect = r'"raw_title":"(.*?)"'  # 名称
    reg_com = re.compile(reg_lect)
    reg_lectlists = reg_com.findall(html, re.S)
    reg_price = r'"view_price":"(.*?)"'  # 价格
    reg_com_pri = re.compile(reg_price)
    reg_pricelists = reg_com_pri.findall(html, re.S)
    reg_sale = r'"view_sales":"(.*?)"'  # 销量
    reg_com_sale = re.compile(reg_sale)
    reg_salelists = reg_com_sale.findall(html, re.S)
    for num in range(3):
        sheet1.write(0, num, row[num])  # 向excel表格里写入名称，价格等信息
    infor_taobao = zip(reg_lectlists, reg_pricelists, reg_salelists)
    infor_taobaos = list(infor_taobao)
    print(infor_taobaos)
    for huawei in infor_taobaos:
        sheet1.write(num_one, 0, huawei[0])
        sheet1.write(num_one, 1, huawei[1])
        sheet1.write(num_one, 2, huawei[2])
        num_one += 1
    print(num_one)
    num_two = num_one
    inforfiile.save('华为手机信息.xls')
    return num_two


if __name__ == '__main__':
    number = 0
    num_one = 1
    inforfiile = xlwt.Workbook()  # 创建excel表格
    sheet1 = inforfiile.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet1
    while number < 397:
        url = get_url('华为', number)
        print(url)
        html = get_html(url)
        number_one = get_select(html, num_one)
        num_one = number_one
        number += 44
        time.sleep(1)
