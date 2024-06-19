import os
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

type = str(input('''爬取规范类型：
1.flfg（法律法规）；
2.xzfg（行政法规）；
3.sfjs（司法解释）；
4.dfxfg（地方性法规）；
5.shuangbian（双边条约）；
6.duobian（多边条约）
输入拼音：（如flfg）'''))

dic = {'flfg': '法律法规', 'xzfg': '行政法规', 'sfjs': '司法解释', 'dfxfg': '地方性法规'}
path = input('输入数据库所在目录（绝对路径）：')
path2 = f'{path}/法规爬虫/{dic[type]}/{dic[type]}库'   # 法律库目录（绝对路径）。
path4 = f'{path}/法规爬虫/{dic[type]}/中间文档'  # 中间文档目录（绝对路径）。

t = time.strftime('%Y-%m-%d')

with open(f'{path4}/{t}-浏览索引.txt') as f0:
    ff = f0.read()
regex = re.compile(r"名称.+|"
                   r'链接.+')
law_list = regex.findall(ff)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
print('正在校验错误，请稍后……')
f3 = ''
with open(f'{path4}/{t}-下载索引.txt', 'r') as f1:
    f2 = f1.read()
    regex = re.compile(r"\d+：|"
                       r'链接.+')
    l_list = regex.findall(f2)

for i in range(len(l_list)):
    if f'{type}/html' in l_list[i] or 'detail2.html?' in l_list[i]:  # 有的文件提供了下载源，单纯获取下载链接出错
        title = l_list[i - 1][:-1] + '.' + law_list[i - 1][3:]
        print(f'发现错误：{title}')
        u = law_list[i][3:]
        browser.get(u)
        codeMa = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'codeMa')))
        png = codeMa.get_attribute('src')
        png = re.sub(r'PNG', 'WORD', png)
        doc = re.sub(r'\.png', '.docx', png)
        if 'images/qr' in doc:  # 有的文件仅有pdf，或者其他错误，直接下载文件
            WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'downLoadFile')))
            d = WebDriverWait(browser, 20, 0.5).until(EC.element_to_be_clickable((By.ID, 'downLoadFile')))
            d.click()
            # time.sleep(2)
            while True:
                database = os.listdir(path2)
                for j in database:
                    regex = re.compile(r"[0-9a-zA-Z]+\.[a-zA-Z]+")
                    k = re.match(regex, j)
                    if ('download' not in j) and (j != '.DS_Store') and k:
                        reg = re.compile(r"\..+")
                        k = k.group()
                        end = re.findall(reg, k)
                        os.rename(f'{path2}/{j}', f'{path2}/{title}{end[0]}')
                        f3 = f3 + '链接：已下载' + '\n' + '\n'
                        break
                else:
                    time.sleep(1)
                    continue
                break
        else:
            f3 = f3 + '链接：' + doc + '\n' + '\n'

    elif type == 'flfg' and (
            '/sfjs/' in l_list[i] or '/xzfg/' in l_list[i] or '/dfxfg/' in l_list[i]):  # 有的文件，国家法律法规数据库提供的链接有错误
        title = l_list[i - 1] + law_list[i - 1][3:]
        print(f'发现错误：{title}')
        doc = re.sub(r"/sfjs/|/xzfg/|/dfxfg/", '/flfg/', l_list[i][3:])
        f3 = f3 + '链接：' + doc + '\n' + '\n'
    elif type == 'sfjs' and (
            '/flfg/' in l_list[i] or '/xzfg/' in l_list[i] or '/dfxfg/' in l_list[i]):  # 有的文件，国家法律法规数据库提供的链接有错误
        title = l_list[i - 1] + law_list[i - 1][3:]
        print(f'发现错误：{title}')
        doc = re.sub(r"/flfg/|/xzfg/|/dfxfg/", '/sfjs/', l_list[i][3:])
        f3 = f3 + '链接：' + doc + '\n' + '\n'
    elif type == 'xzfg' and (
            '/sfjs/' in l_list[i] or '/flfg/' in l_list[i] or '/dfxfg/' in l_list[i]):  # 有的文件，国家法律法规数据库提供的链接有错误
        title = l_list[i - 1] + law_list[i - 1][3:]
        print(f'发现错误：{title}')
        doc = re.sub(r"/sfjs/|/flfg/|/dfxfg/", '/xzfg/', l_list[i][3:])
        f3 = f3 + '链接：' + doc + '\n' + '\n'
    elif type == 'dfxfg' and (
            '/sfjs/' in l_list[i] or '/xzfg/' in l_list[i] or '/flfg/' in l_list[i]):  # 有的文件，国家法律法规数据库提供的链接有错误
        title = l_list[i - 1] + law_list[i - 1][3:]
        print(f'发现错误：{title}')
        doc = re.sub(r"/sfjs/|/xzfg/|/flfg/", '/dfxfg/', l_list[i][3:])
        f3 = f3 + '链接：' + doc + '\n' + '\n'

    elif '链接：' in l_list[i]:
        f3 = f3 + l_list[i] + '\n' + '\n'
    else:
        f3 = f3 + l_list[i] + law_list[i][3:] + '\n'
print('正在纠正错误中，请稍后……')
with open(f'{path4}/{t}-下载索引.txt', 'w') as f4:
    f4.write(f3)
print(f'校验完毕，感谢使用；如果您担心仍有错误，可再次运行本程序校验错误。')
