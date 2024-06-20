import os
import re
import sys
import time
import requests
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import pypandoc
import subprocess

# 为防止程序运行时，mac熄屏或者进入屏保，建议mac电脑取消下行代码注释；如果您的电脑并非mac，请使用其他避免休眠代码，无须取消下行代码注释。
# caffeinate_process = subprocess.Popen(['caffeinate', '-u'])

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
path2 = f'{path}/法规爬虫/{dic[type]}/{dic[type]}库'  # 法律库目录（绝对路径）。
path3 = f'{path}/法规爬虫/{dic[type]}/法规索引'  # 法规索引库目录（绝对路径）。
path4 = f'{path}/法规爬虫/{dic[type]}/中间文档'  # 中间文档目录（绝对路径）。

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

t = time.strftime('%Y-%m-%d')
with open(f'{path4}/{t}-下载索引.txt') as f0:
    ff = f0.read()
regex = re.compile(r"\d+：.+|"
                   r'链接.+')
law_list = regex.findall(ff)

browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
begin = os.listdir(path2)  # 实现断点续传功能
try:
    begin.remove('.DS_Store')
except:
    pass
reg = re.compile(r"\d+")
begin_list = [0]
for k in begin:
    num = reg.findall(k)
    begin_list.append(int(num[0]))
begin_num = max(begin_list)

if begin_num > 0:
    begin_test = input(
        f'检测到已下载文件，是否从该文件处继续下载？\n从最大编号处（{begin_num}）继续下载则输入y\n从自选编号处继续下载则输入编号（举例来说，如果要下载201,202...则输入200）\n从头开始下载则直接按回车。')
    if not begin_test:
        begin_num = 0
    elif begin_test == 'y':
        pass
    else:
        begin_num = int(begin_test)
print('如果长时间无输出，当前ip可能被限制，请更换IP或者稍等一段时间后再次尝试。')


def selenium_downloader(url):  # 下载提供了下载源的文件
    browser.get(url)
    time.sleep(1)
    browser.refresh()  # 可酌情删除提高下载速度
    time.sleep(1)  # 可酌情删除提高下载速度
    url_name = os.path.basename(url)
    chance = 4  # 可酌情减少循环次数提高下载速度
    while True:
        database = os.listdir(path2)
        for j in database:
            if url_name in j:
                if url_name[-1] == 'x':  # 绝大多数文件以docx格式存储
                    os.rename(f'{path2}/{j}', f'{path2}/{i + 1}.{title}.docx')
                elif url_name[-1] == 'c':  # 个别文件以doc格式存储
                    os.rename(f'{path2}/{j}', f'{path2}/{i + 1}.{title}.doc')
                elif url_name[-1] == 'C':  # 个别文件以DOC格式存储
                    os.rename(f'{path2}/{j}', f'{path2}/{i + 1}.{title}.DOC')
                print(f'{i + 1}.{title}  已下载！')
                break

        else:
            if chance >= 0:
                time.sleep(1)
                chance = chance - 1
                continue
            else:
                if url[-1] == 'x':  # 个别文件以doc格式存储
                    new_url = url[:-1]
                    selenium_downloader(new_url)
                    break
                elif url[-1] == 'c':  # 个别文件以DOC格式存储
                    new_url = url[:-3] + 'DOC'
                    selenium_downloader(new_url)
                    break
                else:
                    print(f'{i + 1}.{title}  下载失败')
                    print('当前ip可能被限制，请更换ip或者稍等一段时间后再次尝试。')
                    sys.exit()
        break


for i in range(begin_num, int(len(law_list) / 2)):  # begin_num实现断点续传功能
    try:
        title = re.sub(r'\d+：', '', law_list[2 * i])
        url = law_list[2 * i + 1][3:]
        if f'https://wb.flk.npc.gov.cn/{type}/texthtml' in url:  # 下载未提供下载源的文件
            r = requests.get(url)
            r.raise_for_status()
            if r.status_code == 200:
                with open(f"{path2}/{title}.html", "wb") as code:
                    code.write(r.content)
            output = pypandoc.convert_file(f"{path2}/{title}.html", 'docx', outputfile=f"{path2}/{i + 1}.{title}.docx")
            os.remove(f"{path2}/{title}.html")
            print(f'{i + 1}.{title}  已下载！')

        elif f'https://wb.flk.npc.gov.cn/{type}/WORD' in url:  # 下载提供了下载源的文件
            selenium_downloader(url)

    except selenium.common.exceptions.TimeoutException:
        print(f'{law_list[2 * i]}下载失败')
        print('当前ip可能被限制，请更换ip或者稍等一段时间后再次尝试。')
        sys.exit()
else:
    print(f'{dic[type]}库下载完毕')
# 以下为校验错误代码
print('校正错误中，请稍后……')
outcome = os.listdir(path2)
re = re.compile(r"^\d+\.")
for h in outcome:
    if h == '.DS_Store':
        pass
    elif re.match(h):
        pass
    else:
        print(f'发现错误  {h}')
        os.remove(path2 + '/' + h)
print('校正完毕，感谢使用')

# 为防止程序运行时，mac熄屏或者进入屏保，建议mac电脑取消下行代码注释；如果您的电脑并非mac，请使用其他避免休眠代码，无须取消下行代码注释。
# caffeinate_process.terminate()
