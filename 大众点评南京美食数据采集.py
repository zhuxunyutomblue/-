import requests
from bs4 import BeautifulSoup
import csv
import os


# 链接url
def gethtml(num):
    try:
        number = num + 1
        print('{:<2d}{:<}{:<}'.format(number,'页',':'))#打印正在爬取的页数
        url = 'https://www.dianping.com/search/category/5/10/p' + str(num)
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'#转码
        return r.text
    except Exception as e:
        print(e)
        return ''


# 爬取资源
def findhtml(text, ul):
    soup = BeautifulSoup(text, 'lxml')
    links = soup.find_all('li', class_='')
    for link in links:
        ui = []
        if link.h4 != None:#爬取店铺名
            ui.append(link.h4.string)
            print('{:^50s}'.format(link.h4.string))#打印店铺名
            a1 = link.find('a', class_='review-num')#爬取点评数
            if a1:
                ui.append(a1.b.string)
            else:
                ui.append(' ')
            a2 = link.find('a', class_='mean-price')#爬取花费
            try:
                if a2:
                    ui.append(a2.b.string)
                else:
                    ui.append(' ')
            except:
                ui.append('')
            a3 = link.find('a', {'data-midas-extends': 'module=5_ad_kwcat'})#爬取菜系
            if a3:
                ui.append(a3.string)
            else:
                ui.append(' ')
            a4 = link.find('a', {'data-midas-extends': 'module=5_ad_kwregion'})
            span1 = link.find('span', {'class': 'addr'})
            if a4 and span1:
                ui.append(a4.string + ' ' + span1.string)
            elif a4 == None and span1 != None:
                ui.append(span1.string)
            elif a4 != None and span1 == None:
                ui.append(a4.string)
            else:
                ui.append(' ')
            try:
                spans = link.find('span', class_='comment-list')#爬取地点
                spanss = spans.contents
                ui.append(spanss[1].b.string)
                ui.append(spanss[3].b.string)
                ui.append(spanss[5].b.string)
            except:
                ui.append('')
                ui.append('')
                ui.append('')
        ul.append(ui)


# 保存资源
def savehtml(uls):
    path = 'D:/数据/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, '大众点评南京美食.csv'),'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['店名', '点评数', '花费', '菜系', '地点', '口味', '环境', '服务'])
        for i in range(len(uls)):
            try:
                if uls[i]:
                    writer.writerow(
                        [uls[i][0], uls[i][1], uls[i][2], uls[i][3], uls[i][4], uls[i][5], uls[i][6], uls[i][7]])#写入csv文件
            except:
                continue
                    


# main()
def main(i):
    ulist = []
    it = int(i)
    for number in range(it):
        html = gethtml(number)
        findhtml(html, ulist)

    savehtml(ulist)

yeshu = input('输入要查询的总页数（1~50）:')
main(yeshu)
