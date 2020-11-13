import requests
import re
import time

#手套箱概率
prob = [0.00256, 0.00639, 0.03197, 0.15985, 0.79923]
#磨损度
cost_len = 5
cost = ['薪新出厂', '略有磨损', '久经沙场', '跛损不堪', '战痕累累']
cost_value = [0.07, 0.08, 0.23, 0.07, 0.55 ]


def readBoxData(box_list):
    file = open(" Glove_weapon_box.txt", 'r', encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        line.strip('\n')
        box_list.append(line.split())
    file.close()


def getHTMLText(url):
    kv = {
        'cookie':'',
        'user-agent': ''}
    try:
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilt, html, box_list, result):
    try:
        plt = re.findall(r'\"sell_min_price\"\: \"[\d\.]*\"', html)
        tlt = re.findall(r'\"name\"\: \".*?\"', html)
        # print('plt', plt)
        # print('tlt', tlt)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1].encode('utf-8').decode('unicode_escape'))
            print("Price and Title", price, title)
            str_title = str(title)
            float_price = float(price)
            for box_item in box_list:
                if str_title.find(box_item[1]) != -1 and str_title.find(box_item[2]) != -1:
                    for i in range(cost_len):
                        if str_title.find(cost[i]) != -1:
                            compute = cost_value[i] * prob[int(box_item[0])] * float_price
                            print(compute)
                            result = result + compute
            ilt.append([price, title])
            # print(result)
        print(result)
    except:
        print("")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    # 写入文件
    f = open('csgo_goods.txt', 'w', encoding='utf-8')
    f.write(tplt.format("序号", "价格", "商品名称"))
    f.write('\n')
    count = 0
    print(ilt)
    for g in ilt:
        count = count + 1
        # print(tplt.format(count, g[0], g[1]))
        tmp_str = str(count) + ' ' + str(g[0]) + ' ' + str(g[1])
        # print(tmp_str)
        f.write(tmp_str)
        f.write('\r\n')


def main():
    depth = 729
    start_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num='
    infoList = []
    box_list = []
    result = 0.0
    readBoxData(box_list)
    # print(box_list)
    # print(box_list[0][0], box_list[0][1], box_list[0][2])
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(i)
            html = getHTMLText(url)
            print(html)
            parsePage(infoList, html, box_list, result)
        except:
            continue
        print(i/depth)
        time.sleep(2)
    printGoodsList(infoList)
    print("End")
    print("prospective return: ", result)


main()