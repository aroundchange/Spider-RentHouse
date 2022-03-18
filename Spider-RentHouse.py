# -*- coding = utf8 -*-
# @Time: 2022/3/7 21:26
# @Author: Nico
# File: Spider-RentHouse.py
# @Software: PyCharm

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request  # 指定URL，获取网页数据
import urllib.error
import xlwt  # 进行Excel操作
import time


def main():
    baseurl = "https://sh.lianjia.com/zufang/jingan/pg"
    datalist = getData(baseurl)
    savepath = "静安区租房信息.xls"
    saveData(datalist, savepath)


findLink = re.compile(r'<a class="twoline" href="(.*?)" target="_blank">', re.S)  # 创建正则表达式对象，表示规则（字符串的模式）
findStreet = re.compile(r'</a>-<a href=".*target="_blank">(.*?)</a>-', re.S)
findArea = re.compile(r' title="(.*?)">', re.S)
findSize = re.compile(r'<i>/</i>(.*?)<i>/</i>', re.S)
findPrice = re.compile(r'<em>(.*?)</em>', re.S)
findOrientation = re.compile(r'        <i>/</i>(.*?)        <i>/</i>', re.S)
findLayout = re.compile(r'        <i>/</i>.*        <i>/</i>(.*?)        <span', re.S)


# 爬取网页
def getData(baseurl):
    print("爬取中...")
    datalist = []
    for i in range(1, 35):
        # time.sleep(3)
        url = baseurl + str(i)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="content__list--item--main"):  # 查找符合要求的字符串，形成列表
            # print(item)       # 测试：查看item全部信息
            data = []
            item = str(item)
            # print(item)       # 打印一个item，方便查找匹配规则
            # break     # 查找到第一个item后退出循环
            link = 'https://sh.lianjia.com' + re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)
            street = re.findall(findStreet, item)[0]
            data.append(street)
            area = re.findall(findArea, item)[0]
            data.append(area)
            size = re.findall(findSize, item)[0]
            data.append(size.strip())
            price = re.findall(findPrice, item)[0]
            data.append(price)
            orientation = re.findall(findOrientation, item)[0]
            data.append(orientation)
            layout = re.findall(findLayout, item)[0]
            data.append(layout.strip())
            datalist.append(data)
            # print('https://sh.lianjia.com'+link)
        print(datalist)
    return datalist


# 得到指定的一个URL的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 99.0.4844.51Safari / 537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据
def saveData(datalist, savepath):
    print("Save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('静安区租房信息', cell_overwrite_ok=True)  # 创建工作表
    col = ("链接", "街道", "小区", "面积", "价格", "朝向", "户型")
    for i in range(0, 7):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 1020):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 7):
            sheet.write(i + 1, j, data[j])  # 数据
    book.save(savepath)  # 保存


if __name__ == "__main__":
    main()
    print("爬取完毕！")
