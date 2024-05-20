import json
import os
import requests
import re
import time


def send_msg(page, type):
    try:
        url = f'https://flk.npc.gov.cn/api/?page={page}&type={type}&searchType=title%3Bvague&sortTr=f_bbrq_s%3Bdesc&gbrqStart=&gbrqEnd=&sxrqStart=&sxrqEnd=&sort=true&size=10&_={time.time()}'
        headers = {
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive"
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        data = r.text
        law = json.loads(data)
        return law
    except json.decoder.JSONDecodeError:
        print(f'第{page}页(第{page * 10 - 9}-{page * 10}条)请求错误，请程序终止后再次尝试。')
        # send_msg(page,i)


def law_index(law, t, p, path3, path4):
    # law = send_msg(page,0)
    law_list = law['result']['data']
    # 把旧数据导入进来，形成列表，新数据与旧数据比对，名称相同、日期不同/无名称-下载新法
    filenames = os.listdir(f'{path3}')
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')
    if f'{t}-最新规范.txt' in filenames:
        filenames.remove(f'{t}-最新规范.txt')
    if filenames:
        filename = max(filenames)
        with open(f'{path3}/{filename}') as f0:
            ff = f0.read()
        regex = re.compile(r"名称.+|"
                           r'公布日期.+')
        old_law_list = regex.findall(ff)
    # 新数据-生成最新法律索引
    with open(f'{path3}/{t}-最新规范.txt', 'a+', encoding='utf-8') as f1:
        for i in range(len(law_list)):
            title = law_list[i]['title']
            office = law_list[i]['office']
            publish = law_list[i]['publish']
            expiry = law_list[i]['expiry']
            type_ = law_list[i]['type']
            status = law_list[i].get('status')
            if status == '1':
                status = '有效（规范）'
            elif status == '3':
                status = '尚未生效'
            elif status == '5':
                status = '已修改'
            elif status == '7':
                status = '有效（决定）'
            elif status == '9':
                status = '已废止'
            url_ = 'https://flk.npc.gov.cn' + law_list[i]['url'][1:]
            print(f'''No.{p}-{i + 1}
名称：{title}
制定机关：{office}
公布日期：{publish}
生效日期：{expiry}
法律性质：{type_}
时效性：{status}
网址：{url_}
''', file=f1)
            # 更新旧数据-法律库
            # 有旧法规索引，旧法修改
            if filenames and f'名称：{title}' in old_law_list:
                n = old_law_list.index(f'名称：{title}')
                old_publish = old_law_list[n + 1][5:]
                if publish > old_publish:
                    # download_file(url_, f'{path1}', f'{path2}', title)
                    print(f'《{title}》已被{office}修改，新规范公布日期为{publish}。')
                    with open(f'{path4}/{t}-下载索引.txt', 'a+', encoding='utf-8') as f2:
                        print(f'名称：{title}\n链接：{url_}\n', file=f2)
                # else: 仅显示更新规范？
                # print(f'{office}制定的《{title}》已为最新，公布日期为{publish}。')
            # 有旧法规索引，新制定法
            elif filenames and f'名称：{title}' not in old_law_list:
                # download_file(url_, f'{path1}', f'{path2}', title)
                print(f'{office}新制定了《{title}》，新规范公布日期为{publish}。')
                with open(f'{path4}/{t}-下载索引.txt', 'a+', encoding='utf-8') as f2:
                    print(f'名称：{title}\n链接：{url_}\n', file=f2)
            # 无旧法规索引，建立法规索引库、法律库
            elif not filenames:
                # download_file(url_, f'{path1}', f'{path2}', title)
                print(f'{office}制定的《{title}》已入库，该规范公布日期为{publish}。')
                with open(f'{path4}/{t}-下载索引.txt', 'a+', encoding='utf-8') as f2:
                    print(f'名称：{title}\n链接：{url_}\n', file=f2)


type = str(input('''爬取规范类型：
1.flfg（法律法规）；
2.xzfg（行政法规）；
3.sfjs（司法解释）；
4.dfxfg（地方性法规）
输入拼音：（如flfg）'''))


dic = {'flfg': '法律法规', 'xzfg': '行政法规', 'sfjs': '司法解释', 'dfxfg': '地方性法规'}

path = input('输入数据库所在目录（绝对路径）：')
os.makedirs(f'{path}/法规爬虫/{dic[type]}/{dic[type]}库', exist_ok=True)
os.makedirs(f'{path}/法规爬虫/{dic[type]}/法规索引', exist_ok=True)
os.makedirs(f'{path}/法规爬虫/{dic[type]}/中间文档', exist_ok=True)

path3 = f'{path}/法规爬虫/{dic[type]}/法规索引'  # 法规索引库目录（绝对路径）。
path4 = f'{path}/法规爬虫/{dic[type]}/中间文档'  # 中间文档目录（绝对路径）。

t = time.strftime('%Y-%m-%d')
l = []

e1 = int(input('输入起始页：（爬取全库则输入0；爬取全库可能受反爬虫机制限制而出错，出错时请从出错页数起手动爬取，出错页数为法规索引中末尾规范编号+1）'))
e2 = int(input('输入末页：（爬取全库则输入0；不建议超过100页，如超过100页请分多次爬取）'))
print('如果第1条就出错，说明当前ip被限制了，须等待一段时间再爬取数据；或者更换ip爬取数据。')
if e1 + e2 == 0:
    error = 0
else:
    error = range(e1 - 1, e2)
l0 = send_msg(1, type)
total_num = int(l0['result']['totalSizes']) if not error else (e2 - e1) * 10 + 10
print(f"截至{t}，共检索到{dic[type]}{total_num}条。")
if not error:
    with open(f'{path3}/{t}-最新规范.txt', 'a+', encoding='utf-8') as fa:
        print(f'截至{t}，{dic[type]}共{total_num}条，共{total_num // 10 if total_num % 10 == 0 else total_num // 10 + 1}页。',
              file=fa)
n = total_num // 1000 + 1
for i in range(n):
    n1 = (i + 1) * 1000 if (i + 1) * 1000 < total_num else total_num
    if not error:
        p = 1 + i * 100
        for j in range(i * 100, n1 // 10 if n1 % 10 == 0 else n1 // 10 + 1):
            l.append(send_msg(j + 1, type))
        for law in l:
            law_index(law, t, p, path3, path4)
            print(f'已检索{p * 10 if p * 10 < total_num else total_num}条。')
            p += 1
    else:
        p = e1
        for k in error:
            l.append(send_msg(k + 1, type))
        for law in l:
            law_index(law, t, p, path3, path4)
            print(f'已检索{p * 10 if p < e2 else e2 * 10}条。')
            p += 1
    l.clear()
