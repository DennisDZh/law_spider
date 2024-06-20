一、功能：

爬取国家法律法规数据库、国际条约库，建立法律、行政法规、司法解释、地方性法规、双边条约、多边条约的法规索引、浏览索引、下载索引，并下载全库法规。


二、使用方式：

1.运行“法规爬虫1-建立法规索引、浏览索引.py”，建立法律/行政法规/司法解释/地方性法规/条约之法规索引、浏览索引。

由于国家法律法规数据库反爬虫机制限制，建立法律/行政法规/司法解释/地方性法规索引时，可能需要手动重复运行本步骤。

反爬虫机制针对ip地址进行限制，可等待一段时间再运行本步骤，或者更换ip地址（比如分别用wifi与流量，或者挂梯子）。

目前法律、行政法规、司法解释均不超过1000条，一般运行一次即可建立索引；地方性法规为2万余条，需要运行多次，每次建议爬取不超过1000条。

国际条约库没有反爬虫机制，建立索引、下载法规较为便捷，无须运行多次，且建立索引与下载均可在本步骤完成，无须进行后续2、3步。

如欲下载法律/行政法规/司法解释/地方性法规，则须进行后续2、3步。


2.运行“法规爬虫2-建立下载索引.py”，建立法律/行政法规/司法解释/地方性法规之下载索引。

由于国家法律法规数据库反爬虫机制限制，可能需要手动重复运行本步骤。

反爬虫机制针对ip地址进行限制，可等待一段时间再运行本步骤，或者更换ip地址（比如分别用wifi与流量，或者挂梯子）。

目前法律、行政法规、司法解释均不超过1000条，一般运行2-4次即可建立索引；地方性法规为2万余条，需要运行多次。

建立的下载索引很可能有错误，脚本“法规爬虫2-建立下载索引.py”在全部规范爬取完毕后将自动校正错误；如果您想在爬取部分规范时（比如因反爬虫机制程序终止），校正已建立的部分下载索引，可手动运行脚本“法规爬虫2-校验错误”。


3.运行“法规爬虫3-库下载.py”，下载已建立下载索引的法规库。

由于国家法律法规数据库反爬虫机制限制，可能需要手动重复运行本步骤。

反爬虫机制针对ip地址进行限制，可等待一段时间再运行本步骤，或者更换ip地址（比如分别用wifi与流量，或者挂梯子）。

目前法律、行政法规、司法解释均不超过1000条，一般运行2-4次即可建立索引；地方性法规为2万余条，需要运行多次。

下载的法规小概率有错误，脚本“法规爬虫3-库下载.py”在全部规范爬取完毕后将自动校正错误。


三、注意事项：

请自行安装脚本依赖库：requests，BeautifulSoup，selenium，pypandoc，subprocess。

    “法规爬虫1-建立法规索引、浏览索引.py”除基本的os，re，json，time外，需要requests，BeautifulSoup，subprocess；

    “法规爬虫2-建立下载索引.py”除基本的os，re，sys，time外，需要selenium，subprocess；

    “法规爬虫3-库下载.py”除基本的os，re，sys，time外，需要requests，selenium，pypandoc，subprocess。

本脚本selenium使用chrome浏览器，请自行下载与您的chrome浏览器兼容的chromedriver，并确保其路径配置正确。即确保“法规爬虫2-建立下载索引.py”第58行、“法规爬虫2-校验错误.py”第36行、“法规爬虫3-库下载.py”第51行处的“executable_path”正确指向您的chromedriver。


四、示例：

法规索引的基本格式为：

    【法律法规、行政法规、司法解释、地方性法规】
    
    截至2024-06-19，法律法规共663条，共67页。
    
    No.1-1
    
    名称：中华人民共和国学位法
    
    制定机关：全国人民代表大会常务委员会
    
    公布日期：2024-04-26 00:00:00
    
    生效日期：2025-01-01 00:00:00
    
    法律性质：法律
    
    时效性：尚未生效
    
    网址：https://flk.npc.gov.cn/detail2.html?ZmY4MDgxODE4ZDZhNDI0YjAxOGYxYTYzYjQ5YTc5NmE%3D

    【双边条约、多边条约】

    1-4.《中华人民共和国政府和捷克斯洛伐克共和国政府保健合作协定》
    
    类别：双边
    
    文本：中文本预览

    条约通过时间：1957.03.27
    
    条约生效时间：1957.08.09
    
    保存机关：
    
    领域：卫生
    
    我国签署时间：1957.03.27
    
    签署地点：北京
    
    我国批准/核准/接受/加入时间：1957.05.06
    
    条约适用于港澳情况：
    
    对我国生效时间：1957.08.09
    
    我国声明保留情况：
    
    其他：


浏览索引的基本格式为：

    【法律法规、行政法规、司法解释、地方性法规】
    
    名称：中华人民共和国学位法
    
    链接：https://flk.npc.gov.cn/detail2.html?ZmY4MDgxODE4ZDZhNDI0YjAxOGYxYTYzYjQ5YTc5NmE%3D


下载索引的基本格式为：

    【法律法规、行政法规、司法解释、地方性法规】

    1：中华人民共和国学位法
    
    链接：https://wb.flk.npc.gov.cn/flfg/WORD/a41c27c366f7428f9256dbbebf06a431.docx


五、后续计划：

计划推出gui，并加入检索、下载单条法规等功能。
