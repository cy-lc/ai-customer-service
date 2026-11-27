import requests
import time
from lxml import html
import csv
import re
MOVIE_csv="share/movies.csv"

BASE_URL='https://movie.douban.com/top250'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0",
    "Cookie": """ll="118341"; bid=aUjjwXTYgpE; _pk_id.100001.4cf6=6a343866dd4eb912.1793458542.; _vwo_uuid_v2=D6344ADE71820C76583709EF79BC6E8D9|8b4ffbc7e17338aa360a996ffa56325a; _ga=GA1.1.1548654812.1793459732; _ga_Y4GN1R87RG=GS2.1.s1793465717$o2$g1$t1793467231$j38$l0$h0; __utmc=30149280; __utmz=223695111; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1793510958%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.1379341331.1793458542.1793469233.1793511016.4; __utmz=30149280.1793511016.4.3.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.980235730.1793458542.1793469233.1793511016.4; __utmb=223695111.0.10.1793511016; __utmc=223695111; __utmz=223695111.1793511016.4.3.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; dbcl2="297867292:WnmvAWGB/V0"; ck=0Jyx; frodotk_db="eb825ffbd7e7556cc2871ff387b60044"; __utmt=1; __utmv=30149280.29786; _utm_douban=1; loc-last-index-location-id="118341"; __utmb=30149280.15.10.1793511016; u=0, i"""
}
import re  # 如果你文件最上面没写这行，记得加上


# 处理上映时间的函数
def get_movies_data(movie_date):
    # 1. 如果没抓到数据，直接返回空字符串
    if not movie_date:
        return ''

    # 2. 强行转为字符串（防住 tuple 报错）
    date_str = str(movie_date)

    # 3. 用正则提取所有符合 YYYY-MM-DD 的日期
    matches = re.findall(r'(\d{4}-\d{2}-\d{2})', date_str)

    # 4. 如果匹配到了，返回第一个；如果没匹配到，返回空字符串
    return matches[0] if matches else ''


# 处理年份的函数
def get_movies_years(movie_years):
    # 1. 如果没抓到数据，直接返回空字符串
    if not movie_years:
        return ''

    # 2. 强行转为字符串
    year_str = str(movie_years)

    # 3. 用正则直接提取 4 位数字（不管是 (1994) 还是 1994年，都能提取出 1994）
    matches = re.findall(r'\d{4}', year_str)

    # 4. 返回提取到的第一个 4 位数字
    return matches[0] if matches else ''
def save_all_movies(all_movies):
    with open(MOVIE_csv,'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['电影名', '年份', '上映时间', '类型', '时长', '评分', '语言', '导演', '主演', '简介'])
        writer.writeheader()
        writer.writerows(all_movies)

def get_movies(url):
    #1.发送请求，获取电影详情
    movie_response=requests.get(url,headers=headers,timeout=30)
    time.sleep(1)
    movie_doc=html.fromstring(movie_response.text)
    movie_name=movie_doc.xpath("//*[@id='content']/h1/span[@property='v:itemreviewed']/text()")
    #电影年份
    movie_years=movie_doc.xpath("//*[@id='content']/h1/span[2]/text()")
    #电影上映时间
    movie_date=movie_doc.xpath("//*[@property='v:initialReleaseDate']/text()")
    #电影类型
    movie_types=movie_doc.xpath("//span[@property='v:genre']/text()")
    #电影时长
    movie_duration=movie_doc.xpath("//*[@property='v:runtime']/text()")
    #电影评分
    movie_score=movie_doc.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()")
    #电影语言
    # 1. 找到文字是“语言:”的 span 标签，然后提取它后面的第一段纯文本
    movie_language = movie_doc.xpath('//span[@class="pl" and text()="语言:"]/following-sibling::text()[1]')

    # 2. 清洗数据（因为提取出来的文本前面通常带有空格，比如 " 英语"）
    if movie_language:
        language_str = movie_language[0].strip()
        print("语言:", language_str)
    else:
        print("未找到语言")
    #电影导演
    movie_director=movie_doc.xpath("//*[@id='info']/span[1]/span[2]/a/text()")
    #电影主演
    movie_actors=movie_doc.xpath("//*[@rel='v:starring']/text()")
    #电影简介
    movie_introduction=movie_doc.xpath("//*[@property='v:summary']/text()")
    movie_info={
        "电影名":movie_name[0].strip() if movie_name else None,
        "年份":get_movies_years(movie_years),
        "上映时间":get_movies_data(movie_date),
        "类型":movie_types[0] if movie_types else None,
        "时长":movie_duration[0] if movie_duration else None,
        "评分":movie_score[0] if movie_score else None,
        "语言":movie_language[0] if movie_language else None,
        "导演":'/'.join(movie_director) if movie_director else None,
        "主演":'/'.join(movie_actors) if movie_actors else None,
        "简介":movie_introduction[0] .strip() if movie_introduction else None

    }
    print(movie_info)
    print("获取电影数据")
    return movie_info



all_movies=[]
print("开始爬取数据")
for page in range(0,250,25):
    print(f"正在爬取第{page/25+1}页数据")

    target_url=f"{BASE_URL}?start={page}"

    response=requests.get(target_url,headers=headers)
    document=html.fromstring(response.text)
    movie_url_list=document.xpath("//div[@class='hd']/a/@href")
    for url in movie_url_list:
         movie_info=get_movies(url)
         all_movies.append(movie_info)

save_all_movies(all_movies)
