# -*- codeing = utf-8 -*-
# @Time : 2022/3/13 8:08
# @Author : 王伊念
# File : pachong.py
# @Software : PyCharm

import urllib.request
import json
import random
import time as time0
import re, os
import pandas as pd

# 设置代理
agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def product_reviews(product_id=None, p=0, maxPage=99):
    root_dir = '京东手机评论_详细字典'
    # 判断之前是否爬取过这个型号手机的评论(一种型号的手机，颜色和内存不同，但评论共享)
    os.makedirs(root_dir, exist_ok=True)
    phone_list = os.listdir(root_dir)
    phone_txt = str(product_id) + '.txt'
    if phone_txt in phone_list:
        print(product_id)
        return []

    k_head = 0
    while p < maxPage:
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100014352539&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        url = url.format(product_id, p, maxPage)
        # 仿造请求头，骗过浏览器
        cookie = 'shshshfpa=cb5bb473-788d-5394-cdfb-04c95be61593-1607327879; shshshfpb=rKP7lqv2XQL/DCe8WrYkgBg==; __jdu=1623557258595384509951; __jdc=122270672; areaId=5; shshshfp=81859f009e71bb66ce297270743ffd99; ip_cityCode=142; ipLoc-djd=5-142-42547-54561; unpl=JF8EAK5nNSttD0pXAh0DGxNAHwlSW1wITUcEazcMUgkNTAFXGQBIGkB7XlVdXhRKFR9vZRRVW1NPUw4ZCisSEXteVV1YCE0TAGlnNWRtW0tkBCsCHBEST1lSXVkBTx8HbW4AUFxQQ1AFKzIbGhR7XVVfXAhOFQdsYwdcbWhOVAQaBR4UFEtaZF9tCXtBbW9mBFVcWUpUBh1PGxUTSVlQWF4MQhMLa2UMUVlZQ1wBGzIaIhM; CCC_SE=ADC_7n94M6UHc+BcNPNCLwh5GfRhsHny0Ahpe8vRJKeCcTB4zq/Dd9TSaihboPli+UEwrCM4WuAIMH16maUBRuSgcK948Z+JJ8IQ2bQKq2iPnU49gP8WmeXwTgCdzGpCqewmvHGpnsi643sL4O6yluUQbD/dhc2yPKsG+cfFH2KixmBhI8xfX8beBW2D6A1NilzFoVQk0lrzGtPU0v9JRbDEWtbHvN0Wt6dUvQK2UuY9N5eUEi06z/iwHh3SjA6l+GO0RGGWVkXB1Fs1LcC6/W7abjMDxcMo8ghqdjOKrWIZP61wP9um6gwMyyC+R0de2aJ6/k1H/oYBoi0AmQO/5DN3DqZ0ruouUJyrz4f5e2wp1ogyZLEFc+fiU5I2pWfQiqPkubDuVb0uJw1J/1KI0qRaMj1SVGjc9XVWegaa5nR9DsTwCAiqPzDQxAZLXlajMuM5ZnoI9/Jv3KVStIZPFc0kVTicpa+NFxctp11efX0PH+9mjcqIyKHQ5VthggvAiHLgclOKXpeK2KcrFgC4lsWyCg==; __jda=122270672.1623557258595384509951.1623557258.1647129370.1647129402.5; jwotest_product=99; token=5793dd058944f98d5daa52efb7d36450,2,915072; __tk=e811b9a54df23c59030b56a7cf038d5c,2,915072; JSESSIONID=B699D0F2B3E9847E445601962AB99746.s1; 3AB9D23F7A4B3C9B=QR4LGBGBB4EUIIW3NXB3GBTWVIYXMYSJESVV2OPAEWNVXKSBTQWKCBJJOPLQEPJKJMO4H6SB62D73VBIZVETJQUHWM; shshshsID=2788170c937ccdeb4c8f2290f89686b1_11_1647130043025; __jdb=122270672.9.1623557258595384509951|5.1647129402; __jdv=122270672|jd.idey.cn|t_2024175271_|tuiguang|f0267010aee74017a65a87ed6dc33b9a|1647130043346'
        headers = {
            'User-Agent': ''.join(random.sample(agents, 1)),
            'Referer': 'https://item.jd.com/1981570.html',
            'Cookie': cookie
        }
        # 发起请求
        request = urllib.request.Request(url=url, headers=headers)
        time0.sleep(2.5)
        try:
            content = urllib.request.urlopen(request).read().decode('utf-8')
        except:
            print('第%d页评论代码出错' % p)
            p = p + 1
            continue
        # 去掉多余得到json格式
        content = content.strip('fetchJSON_comment98vv995();')

        # 评论的最大页数
        try:
            maxPage = int(re.findall('"maxPage":(.*?),"', content, re.S)[100])
        except:
            pass

        try:
            obj = json.loads(content)
        except:
            print('信号不好，再次尝试！')
            print([content])
            print(url)
            continue

        comments = obj['comments']
        # 产品评论总结
        productCommentSummary = obj['productCommentSummary']
        dict_pars_info = {}
        # 平均分
        dict_pars_info['平均分'] = str(productCommentSummary['averageScore'])
        # 好评率
        dict_pars_info['好评率'] = str(productCommentSummary['goodRate'])
        # 当前总评论数
        dict_pars_info['当前评论数'] = str(productCommentSummary['commentCount'])
        # 默认评论数
        dict_pars_info['默认评论数'] = str(productCommentSummary['defaultGoodCount'])
        # 追评、好评、中评、差评
        dict_pars_info['追评数'] = str(productCommentSummary['afterCount'])
        dict_pars_info['好评数'] = str(productCommentSummary['goodCount'])
        dict_pars_info['中评数'] = str(productCommentSummary['generalCount'])
        dict_pars_info['差评数'] = str(productCommentSummary['poorCount'])

        if len(comments) > 0:
            # print(comments)
            for comment in comments:
                # print(comment)
                name = comment['referenceName']

                id = comment['id']

                con = comment['content']

                time = comment['creationTime']

                img_url = comment['userImageUrl']

                score = comment['score']

                likes = comment['usefulVoteCount']

                replyCount = comment['replyCount']

                try:
                    productColor = comment['productColor']
                except:
                    productColor = ''

                try:
                    productSize = comment['productSize']
                except:
                    productSize = ''

                item = {
                    'name': name,
                    'id': id,
                    'score': score,
                    'con': con,
                    'time': time,
                    'productColor': productColor,
                    'productSize': productSize,
                    'likes': likes,
                    'replyCount': replyCount,
                    'img_url': img_url,
                }
                item.update(dict_pars_info)
                string = str(item)

                # 1.保存为csv格式
                item_dataframe = pd.DataFrame([item])
                # print(item_dataframe)
                if k_head == 0:
                    item_dataframe.to_csv(root_dir + '/%d.csv' % product_id, mode='w', header=True, index=False,
                                          encoding='utf-8')
                    k_head += 1
                else:
                    item_dataframe.to_csv(root_dir + '/%d.csv' % product_id, mode='a', header=False, index=False,
                                          encoding='utf-8')

                # 2.保存成txt
                fp = open(root_dir + '/%d.txt' % product_id, 'a', encoding='utf-8')
                fp.write(string + '\n')
                fp.close()
            print('%s-page---finish(%s/%s)' % (p, p, maxPage))
        else:
            return []
        p = p + 1


if __name__ == '__main__':
    phone_id = 100014352539
    product_reviews(product_id=phone_id)

