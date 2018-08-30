# coding:utf-8
import urllib2
import re
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 1. 获取主页面内容, 也可以用于获取详情页
def OpenPage(url):
    '''
    根据 url 构造 HTTP 请求发送给服务器.
    获取到 HTTP 服务器的响应
    '''
    # 为了构造请求对象, 所构造的 header 对象
    # headers = {}
    # 构造请求对象
    req = urllib2.Request(url)
    # 发送 http 请求, 获取到了一个文件对象
    f = urllib2.urlopen(req)
    # 从文件中读取返回结果
    data = f.read()
    # decode 操作是把 GBK 编码格式 转成 unicode 的编码格式
    # encode 操作是把 unicode 转成 utf-8 格式
    data = data.decode('GBK', errors='ignore').encode('UTF-8')
    return data


def Test1():
    url = 'http://www.shengxu6.com/book/2967.html'
    print OpenPage(url)


def ParseMainPage(page):
    soup = BeautifulSoup(page, 'html.parser')
    # 筛选出所有符合条件的 a 标签. 筛选规则:
    # 查找所有带有 href 属性的标签, 并且 href 中包含的 url 中
    # 又包含 "read" 关键字
    chapter_list = soup.find_all(href=re.compile('read'))
    # 获取出 a 标签中的 url
    url_list = ['http://www.shengxu6.com' + item['href']
                for item in chapter_list]
    return url_list


def Test2():
    url = 'http://www.shengxu6.com/book/2967.html'
    html = OpenPage(url)
    ParseMainPage(html)


def Test3():
    url = 'http://www.shengxu6.com/read/2967_2008684.html'
    html = OpenPage(url)
    print html


def ParseDetailPage(page):
    soup = BeautifulSoup(page, 'html.parser')
    result = soup.find_all(class_='content-body')[0].get_text()
    return result[:-len('_drgd200();') - 1]


def Test4():
    url = 'http://www.shengxu6.com/read/2967_2008684.html'
    html = OpenPage(url)
    result = ParseDetailPage(html)
    print result


def Write(file_path, data):
    with open(file_path, 'a+') as f:
        f.write(data)


def Run():
    '''
    整个项目的入口函数
    '''
    # 1. 获取到小说网站的主页面
    main_url = 'http://www.shengxu6.com/book/2967.html'
    page = OpenPage(main_url)
    # 2. 根据主页面解析出所有详细页的 url
    url_list = ParseMainPage(page)
    for url in url_list:
        # 3. 遍历详细页, 获取到每个详细页的小说内容
        detail_page = OpenPage(url)
        result = ParseDetailPage(detail_page)
        # 4. 把详细页的内容写到文件中
        Write('./result.txt', result)


if __name__ == '__main__':
    # Test1()
    # Test2()
    # Test3()
    # Test4()
    Run()
