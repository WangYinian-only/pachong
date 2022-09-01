# -*- coding:utf-8 -*-

import requests
import json
import time
import random
import xlwt

# 创建excell保存数据
file = xlwt.Workbook(encoding='utf-8')
sheet = file.add_sheet('data', cell_overwrite_ok=True)

agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

for i in range(105):  # for循环遍历，批量爬取评论信息
    try:
        # 构造url，通过在网页不断点击下一页发现，url中只有page后数字随页数变化，批量遍历就是根据这个
        # url去掉了callback部分，因为这部分内没有有用数据，并且不去掉后面转换为json格式会有问题
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100014352539&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        # 构造headers
        cookie = 'shshshfpa=cb5bb473-788d-5394-cdfb-04c95be61593-1607327879; shshshfpb=rKP7lqv2XQL/DCe8WrYkgBg==; __jdu=1623557258595384509951; __jdc=122270672; areaId=5; shshshfp=81859f009e71bb66ce297270743ffd99; ip_cityCode=142; ipLoc-djd=5-142-42547-54561; unpl=JF8EAK5nNSttD0pXAh0DGxNAHwlSW1wITUcEazcMUgkNTAFXGQBIGkB7XlVdXhRKFR9vZRRVW1NPUw4ZCisSEXteVV1YCE0TAGlnNWRtW0tkBCsCHBEST1lSXVkBTx8HbW4AUFxQQ1AFKzIbGhR7XVVfXAhOFQdsYwdcbWhOVAQaBR4UFEtaZF9tCXtBbW9mBFVcWUpUBh1PGxUTSVlQWF4MQhMLa2UMUVlZQ1wBGzIaIhM; CCC_SE=ADC_7n94M6UHc+BcNPNCLwh5GfRhsHny0Ahpe8vRJKeCcTB4zq/Dd9TSaihboPli+UEwrCM4WuAIMH16maUBRuSgcK948Z+JJ8IQ2bQKq2iPnU49gP8WmeXwTgCdzGpCqewmvHGpnsi643sL4O6yluUQbD/dhc2yPKsG+cfFH2KixmBhI8xfX8beBW2D6A1NilzFoVQk0lrzGtPU0v9JRbDEWtbHvN0Wt6dUvQK2UuY9N5eUEi06z/iwHh3SjA6l+GO0RGGWVkXB1Fs1LcC6/W7abjMDxcMo8ghqdjOKrWIZP61wP9um6gwMyyC+R0de2aJ6/k1H/oYBoi0AmQO/5DN3DqZ0ruouUJyrz4f5e2wp1ogyZLEFc+fiU5I2pWfQiqPkubDuVb0uJw1J/1KI0qRaMj1SVGjc9XVWegaa5nR9DsTwCAiqPzDQxAZLXlajMuM5ZnoI9/Jv3KVStIZPFc0kVTicpa+NFxctp11efX0PH+9mjcqIyKHQ5VthggvAiHLgclOKXpeK2KcrFgC4lsWyCg==; __jda=122270672.1623557258595384509951.1623557258.1647129370.1647129402.5; jwotest_product=99; token=5793dd058944f98d5daa52efb7d36450,2,915072; __tk=e811b9a54df23c59030b56a7cf038d5c,2,915072; JSESSIONID=B699D0F2B3E9847E445601962AB99746.s1; 3AB9D23F7A4B3C9B=QR4LGBGBB4EUIIW3NXB3GBTWVIYXMYSJESVV2OPAEWNVXKSBTQWKCBJJOPLQEPJKJMO4H6SB62D73VBIZVETJQUHWM; shshshsID=2788170c937ccdeb4c8f2290f89686b1_11_1647130043025; __jdb=122270672.9.1623557258595384509951|5.1647129402; __jdv=122270672|jd.idey.cn|t_2024175271_|tuiguang|f0267010aee74017a65a87ed6dc33b9a|1647130043346'
        headers = {
            'User-Agent': ''.join(random.sample(agents, 1)),
            'Referer': 'https://item.jd.com/1981570.html',
            'Cookie': cookie
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)  # 字符串转换为json数据
        page = i * 10  # 这里是存储在excell中用到的，因为每爬取一个url会有10条评论，占excell 10列
        if (data['comments']):
            for temp in data['comments']:
                sheet.write(page, 0, page)  # 序号
                sheet.write(page, 1, temp['content'])  # 评论
                sheet.write(page, 2, temp['score'])  # 用户打的星级
                page = page + 1
            print('第%s页爬取成功' % i)
        else:
            print('.............第%s页爬取失败' % i)
            file.save('F:\\t\\t.xlsx')  # 保存到本地

    except Exception as e:
        print('爬取失败，url：%s' % url)
        print('page是%s' % i)
        continue
    time.sleep(random.random() * 5)  # 每循环一次，随机时间暂停再爬
file.save('F:\\t\\t.xlsx')
