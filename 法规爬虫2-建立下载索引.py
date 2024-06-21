import os
import sys
import time
import re
import selenium
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import subprocess

# 为防止程序运行时，mac熄屏或者进入屏保，建议mac电脑取消下行代码的注释；如果您的电脑并非mac，请使用其他避免休眠代码，无须取消下行代码注释。
# caffeinate_process = subprocess.Popen(['caffeinate', '-u'])

# 规范类型与此前建立法规索引、浏览索引的法规一致。

type = str(input('''爬取规范类型：
1.flfg（法律法规）；
2.xzfg（行政法规）；
3.sfjs（司法解释）；
4.dfxfg（地方性法规）；
输入拼音：（如flfg）'''))

dic = {'flfg': '法律法规', 'xzfg': '行政法规', 'sfjs': '司法解释', 'dfxfg': '地方性法规'}

path = input('输入数据库所在目录（绝对路径）：')
path2 = f'{path}/法规爬虫/{dic[type]}/{dic[type]}库'  # 法律库目录（绝对路径）。
path4 = f'{path}/法规爬虫/{dic[type]}/中间文档'  # 中间文档目录（绝对路径）。

t = time.strftime('%Y-%m-%d')

try:
    with open(f'{path4}/{t}-浏览索引.txt') as f0:
        ff = f0.read()
    regex = re.compile(r"名称.+|"
                       r'链接.+')
    law_list = regex.findall(ff)
except FileNotFoundError:
    print('未找到当日浏览索引；请确保目录输入正确，且当日已运行法规爬虫1、建立浏览索引；如果您想使用已有的浏览索引，请将其命名为当日日期。')
    caffeinate_process.terminate()
    sys.exit()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory': path2,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
}
chrome_options.add_experimental_option('prefs', prefs)
no = 0

browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                           chrome_options=chrome_options)  # 请确保您的chromedriver内核与chrome浏览器兼容；请确保此处executable_path为您的chromedriver路径
print('首次运行程序可能会有一段启动时间。')
print("程序运行过程中会出现一段时间内无输出现象，此为程序写入过程，无须特别关注。")
print('但如果程序长时间无输出，或者报错TimeoutException，当前ip可能被限制，请更换ip或者稍等一段时间后再次尝试。')
print('下载索引建立完毕后，程序将自动校验已建立的下载索引中的错误；如果您已建立了部分下载索引，可手动运行法规爬虫2-校验其错误。')


def download_index(no):
    for i in range(no, int(len(law_list) / 2)):
        title = law_list[2 * i][3:]
        url = law_list[2 * i + 1][3:]
        browser.get(url)
        codeMa = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'codeMa')))
        png = codeMa.get_attribute('src')
        png = re.sub(r'PNG', 'WORD', png)
        if f'//{type}' in png:  # 有的文件，国家法律法规数据库提供的链接有错误
            png = re.sub(rf'//{type}', f'/{type}', png)
        doc = re.sub(r'\.png', '.docx', png)
        if 'images/qr' in doc:  # 有的文件未提供下载源
            file = browser.find_element_by_id("viewDoc")
            doc = file.get_attribute("src")
        print(f'{i + 1}：{title}', file=f)
        print(f'链接：{doc}\n', file=f)
        print(f'{i + 1}：《{title}》已建立下载索引！')


try:
    with open(f'{path4}/{t}-下载索引.txt', 'r') as f:
        fff = f.read()
        regex = re.compile(r"\d+：")
        last = regex.findall(fff)[-1]
        no = int(last[:-1])
        regex = re.compile(r"\d+：|"
                           r'链接.+')
        l_list = regex.findall(fff)
        if not re.match(r'链接.+', l_list[-1]):  # 有时由于网络波动或者不当关闭程序，下载断点处没有获取到下载链接
            title = l_list[-1][:-1] + '.' + law_list[no*2][3:]
            print(f'{title}未建立下载链接，正在校正……')
            u = law_list[no*2+1][3:]
            browser.get(u)
            codeMa = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'codeMa')))
            png = codeMa.get_attribute('src')
            png = re.sub(r'PNG', 'WORD', png)
            if f'//{type}' in png:  # 有的文件，国家法律法规数据库提供的链接有错误
                png = re.sub(rf'//{type}', f'/{type}', png)
            doc = re.sub(r'\.png', '.docx', png)
            if 'images/qr' in doc:  # 有的文件未提供下载源
                file = browser.find_element_by_id("viewDoc")
                doc = file.get_attribute("src")
    with open(f'{path4}/{t}-下载索引.txt', 'a+', encoding='utf-8') as f:
        if not re.match(r'链接.+', l_list[-1]):
            print(f'链接：{doc}\n', file=f)
            print(f'{title}已建立下载链接！')
        download_index(no)
    print(f'{dic[type]}已建立下载索引！')
except FileNotFoundError:
    with open(f'{path4}/{t}-下载索引.txt', 'a+', encoding='utf-8') as f:
        download_index(no)
    print(f'{dic[type]}已建立下载索引！')

except IndexError:
    with open(f'{path4}/{t}-下载索引.txt', 'a+', encoding='utf-8') as f:
        download_index(no)
    print(f'{dic[type]}已建立下载索引！')

except selenium.common.exceptions.TimeoutException:
    print('链接超时，当前ip可能被限制，请更换ip或者稍等一段时间后再次尝试。')

# 以下为检验错误代码
print('正在校验错误，请稍后……')
f3 = ''
with open(f'{path4}/{t}-下载索引.txt', 'r') as f1:
    f2 = f1.read()
    regex = re.compile(r"\d+：|"
                       r'链接.+')
    l_list = regex.findall(f2)

if not re.match(r'链接.+', l_list[-1]):  # 有时由于网络波动或者不当关闭程序，下载断点处没有获取到下载链接
    no = int(l_list[-1][:-1]) - 1
    title = l_list[-1][:-1] + '.' + law_list[no*2][3:]
    print(f'{title}未建立下载链接，正在校正……')
    u = law_list[no*2+1][3:]
    try:
        browser.get(u)
        codeMa = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'codeMa')))
        png = codeMa.get_attribute('src')
        png = re.sub(r'PNG', 'WORD', png)
        if f'//{type}' in png:  # 有的文件，国家法律法规数据库提供的链接有错误
            png = re.sub(rf'//{type}', f'/{type}', png)
        doc = re.sub(r'\.png', '.docx', png)
        if 'images/qr' in doc:  # 有的文件未提供下载源
            file = browser.find_element_by_id("viewDoc")
            doc = file.get_attribute("src")
        with open(f'{path4}/{t}-下载索引.txt', 'a+', encoding='utf-8') as f1:
            print(f'链接：{doc}\n', file=f1)
        print(f'{title}已建立下载链接！')
    except selenium.common.exceptions.TimeoutException:
        print('链接超时，当前ip可能被限制，请更换ip或者稍等一段时间后再次尝试。')
        sys.exit()

for i in range(len(l_list)):
    if i + 1 < len(l_list):  # 在没有获取下载链接的下载断点处继续下载，将导致后续链接全部出错，须自下载断点处重新运行脚本。
        if re.match(r'\d+：', l_list[i]) and (not re.match(r'链接.+', l_list[i + 1])):
            title = l_list[i][:-1] + '.' + law_list[i][3:]
            u = law_list[2 * i + 1][3:]
            print(f'{title}未建立下载链接，正在校正……')
            no = int(l_list[i][:-1])
            try:
                browser.get(u)
                codeMa = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'codeMa')))
                png = codeMa.get_attribute('src')
                png = re.sub(r'PNG', 'WORD', png)
                if f'//{type}' in png:  # 有的文件，国家法律法规数据库提供的链接有错误
                    png = re.sub(rf'//{type}', f'/{type}', png)
                doc = re.sub(r'\.png', '.docx', png)
                if 'images/qr' in doc:  # 有的文件未提供下载源
                    file = browser.find_element_by_id("viewDoc")
                    doc = file.get_attribute("src")
                f3 = f3 + l_list[i] + law_list[i][3:] + '\n'
                f3 = f3 + '链接：' + doc + '\n' + '\n'
                with open(f'{path4}/{t}-下载索引.txt', 'w') as f4:
                    f4.write(f3)
                print(f'{no + 1}：《{title}》已校正！')
                print(f'请重新运行法规爬虫2-建立下载索引.py，将从出错处重新建立下载索引。')
                sys.exit()
            except selenium.common.exceptions.TimeoutException:
                print('链接超时，当前ip可能被限制，请更换ip或者稍等一段时间后再次尝试。')
                sys.exit()

    if f'{type}/html' in l_list[i] or 'detail2.html?' in l_list[i]:  # 有的文件提供了下载源，单纯获取下载链接出错
        title = l_list[i - 1][:-1] + '.' + law_list[i - 1][3:]
        print(f'发现错误：{title}')
        u = law_list[i][3:]
        try:
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
        except selenium.common.exceptions.TimeoutException:
            print('链接超时，当前ip可能被限制，请更换ip或者稍等一段时间后再次尝试。')
            sys.exit()

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

    elif '链接：' in l_list[i]:  # 正确的链接
        f3 = f3 + l_list[i] + '\n' + '\n'
    else:  # 序号及名称
        f3 = f3 + l_list[i] + law_list[i][3:] + '\n'
print('正在纠正错误中，请稍后……')
with open(f'{path4}/{t}-下载索引.txt', 'w') as f4:
    f4.write(f3)
print(f'本次下载索引建立完毕，感谢使用；如果未建立全部下载索引，可再次运行本程序；如果尚有错误未校正，建议您先运行法规爬虫2-校验错误，校正错误后，再重新运行本脚本。')

# 为防止程序运行时，mac熄屏或者进入屏保，建议mac电脑取消下行代码的注释；如果您的电脑并非mac，请使用其他避免休眠代码，无须取消下行代码注释。
# caffeinate_process.terminate()
