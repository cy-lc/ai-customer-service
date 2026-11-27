import requests
from lxml import html

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}

def louceng(l):
    for i in l:
        clean_louceng = i.replace("\n", "").replace(" ", "").strip()
    return clean_louceng
url = "https://gy.ke.com/ershoufang/"
url2 = "https://gy.ke.com/ershoufang/pg2/"
loucengs=[]
for i in range(1,11):
    re_url = requests.get(url,headers=headers,timeout=10)
    re_url = html.fromstring(re_url.text)
    jiage=re_url.xpath('//*[@class="totalPrice totalPrice2"]/span/text()')
    didian=re_url.xpath('//*[@class="positionInfo"]/a[1]/text()')
    lou=re_url.xpath('//div[@class="houseIcon"]/span/text()')
    clean_louceng=louceng(lou)
    loucengs.append(clean_louceng)
print(jiage)
print(didian)
print(loucengs)








