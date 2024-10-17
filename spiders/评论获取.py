import sys
from datetime import datetime
from queue import Queue
import pandas as pd
import requests
import execjs
import urllib.parse
import os
from DrissionPage import ChromiumPage,ChromiumOptions
from fake_useragent import UserAgent
import pymysql
class Pin:
    def __init__(self):
        self.result=[]
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.douyin.com/?recommend=1',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
        self.cursor=0
        self.has_more=1
        self.ip_url='https://share.proxy.qg.net/get?key=ESDKF0H8&pwd=BC20D73ADC0A'
        self.ip_queue=Queue()
        self.open=True
        self.all_comments=0
        self.pi=Queue()
        self.shuju=Queue()
        # 创建 UserAgent 对象
        self.ua = UserAgent()
        self.db = pymysql.connect(host='localhost', user='root', password='321542', db='mysql')
        self.cursor = self.db.cursor()
    def js(self, params):
        params_str = urllib.parse.urlencode(params)
        print(params_str)
        ctx = execjs.compile(open('douyin.js').read())
        print(ctx)
        a_bogus = ctx.call('getSign', params_str)
        # paramsss=ctx.call('get', params_str)
        # print(paramsss)
        print(a_bogus)
        params['a_bogus'] = a_bogus
        # 获取一个随机的用户代理
        user_agent = self.ua.random
        params['user_agent'] = user_agent

    def get_ip(self):
        response = requests.get(self.ip_url, headers=self.headers)
        # print(ip)
        ip_data = response.json()
        print(ip_data)
        # 提取代理IP
        ip = ip_data['data'][0]['server']
        print(f"Using proxy: {ip}")
        self.ip_queue.put(ip)
    def request_url(self,cursor):
        # for i in range(0,100,50):
        cursor=int(cursor)
        open=True
        while open:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "aweme_id": "7417438026374188329",
                "cursor": cursor,
                "count": 50,
                "item_type": "0",
                "insert_ids": "",
                "whale_cut_token": "",
                "cut_version": "1",
                "rcFT": "",
                "update_version_code": "170400",
                "pc_client_type": "1",
                "pc_libra_divert": "Windows",
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "screen_width": "1707",
                "screen_height": "960",
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "129.0.0.0",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "129.0.0.0",
                "os_name": "Windows",
                "os_version": "10",
                "cpu_core_num": "16",
                "device_memory": "8",
                "platform": "PC",
                "downlink": "10",
                "effective_type": "4g",
                "round_trip_time": "150",
                "webid": "7426640757047477771",
                "msToken": "yA6NFxH1UH6T3Ls1ShTSUuZZemlaBeuzIZiOkXE8RLWHG2mbgIgMKvJEvXoW1bdnPtRYhq1SxSlLBhGdlHnnf0MIqFNZFvr_D4TUE0AMR2A7GKAg5nR8A84c8v6tutOYDV6HrdOpCTx4c1lQJhiDQolZ2oUXTlh2IK9R3NGN5-FuqKt11k2jMA==",
                # "a_bogus": "xX0fDzSEDqWjKdMbYKGLyfZUMF9ANBSyLei/bOOPexY4bZlasRNd2ObanxuOdqFLRuBwkK37JD0lYxVcMTUhZ9rpqmpkuYsjCT/AnU8LZqqvYtTmDqSPCwUFuw0uURwia5nRiIR56s0JId95IqAmApVGS5zLQQL2WrMVpMTyjDCW3sLTnxdve5GAowE=",
                "verifyFp": "verify_m2cz0jiq_aHiTir6m_u5Yy_4y0W_9VQM_QuUYgW7Q0JJX",
                "fp": "verify_m2cz0jiq_aHiTir6m_u5Yy_4y0W_9VQM_QuUYgW7Q0JJX"
                }
            # print('剩余评论：',self.all_comments-params['cursor'])
            self.js(params)
            self.aweme_id=params['aweme_id']
            response = requests.get('https://www.douyin.com/aweme/v1/web/comment/list/', params=params,headers=self.headers, cookies=self.cookies,timeout=5)

            try:
                if response.status_code == 200:
                    # print(response.text)
                    response=response.json()
                    cursor += 50
                    if cursor == 500 or cursor == 1000 or cursor == 1500 or cursor == 2000 or cursor == 2500 or cursor == 3000:
                        open=False
                        break
                    # print(response)
                    self.parse(response,params)
            except Exception as e:
                    print(e)
                    # print(e)
                    print('》》》》》》》》》》》》》》》》》》')
                    print('异常')
                    open=False
                    break


    def parse(self, response, params):
        # global cursor, has_more
        # "total": 541, 总评论
        try:
            self.all_comments = response['total']
            print(self.all_comments)
            # print(self.all_comments)
            # "cursor": 20, 现在的数目
            # "has_more": 1, 是否还有
            # self.cursor = response['cursor']
            # self.has_more = response['has_more']
            # params['cursor'] = self.cursor
            # # print('剩余评论：',self.all_comments-params['cursor'])
            # # 评论内容
            comments = response['comments']

            for comment in comments:
                temp = {}
                # "cid": "7397074750557963058", 二级评论的参数
                # "text": "这个是哪一集叫什么名？哪一季", 一级评论
                # "aweme_id": "7384836050629299466", 作品id
                # "create_time": 1722265677, 创建时间
                # "digg_count": 0, 点赞量
                cid = comment['cid']
                text = comment['text']
                aweme_id = comment['aweme_id']
                create_time = comment['create_time']
                # 使用fromtimestamp方法将时间戳转换为datetime对象
                current_time = datetime.fromtimestamp(create_time)
                # "ip_label": "山东", ip属地
                # "reply_comment_total": 0,    回复量
                ip = comment['ip_label']
                reply_all = comment['reply_comment_total']
                # user
                # "nickname": "盛夏的猎户座", 用户名称
                # "signature": "人间非净土，各有各的苦。同是红尘悲伤客，末笑谁是可怜人。\n好好生活吧", 用户签名
                nickname = comment['user']['nickname']
                signature = comment['user']['signature']
                temp['cid'] = cid
                temp['text'] = text
                temp['aweme_id'] = aweme_id
                temp['create_time'] = current_time
                temp['ip'] = ip
                temp['reply_all'] = reply_all
                temp['nickname'] = nickname
                temp['signature'] = signature
                print(temp)
                self.shuju.put(temp)
                # self.result.append(temp)
        except Exception as e:
            self.has_more = 0
            print(e)
            print('或许此视频五评论')
            print('??')
    # def save(self):
    def save(self):
        while True:
            comment = self.shuju.get()
            sql = """INSERT INTO spider_douyin (cid, text, aweme_id, create_time, ip, reply_all, nickname,awemeid, signature)
                      VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)
                   """
            values = (comment['cid'], comment['text'], comment['aweme_id'], comment['create_time'],
                      comment['ip'], comment['reply_all'], comment['nickname'],self.aweme_id, comment['signature'])
            try:
                self.cursor.execute(sql, values)
                self.db.commit()
                self.shuju.task_done()
                print('数据插入成功...')
            except Exception as e:
                print('数据插入失败: ', e)
                self.db.rollback()

    def main(self):
        import json
        import time
        from DrissionPage import ChromiumPage, ChromiumOptions
        n=input('输入登录账号：')
        with open('cookies{}.json'.format(n), 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        # page = ChromiumPage(local_port=9122, user_data_path=r'D:\data6')
        do1 = ChromiumOptions().auto_port().set_paths(local_port=9122, user_data_path=r'D:\data6')
        # page = ChromiumPage(do1)
        page = ChromiumPage(do1)
        # 清除浏览器cookie
        page.set.cookies.clear()
        for cookie in cookies:
            # 构造cookie的格式
            cookie_dict = {
                "domain": "www.douyin.com",
                "name": cookie.get("name"),
                "value": cookie.get("value"),
            }
            # 断言一下
            if 'sameSite' in cookie_dict:
                assert cookie_dict["sameSite"] in ["Strict", "Lax", "None"]
            # 一条条添加进浏览器
            page.set.cookies(cookie_dict)
        page.get('https://www.douyin.com')
        self.cookies = page.cookies().as_dict()
        thread_list = list()
        for cursor in range(0, 3000, 500):
            import threading
            t_get_info = threading.Thread(target=self.request_url, args=(str(cursor),))  # 修正这里
            thread_list.append(t_get_info)
        save_th = threading.Thread(target=self.save)  # 修正这里
        thread_list.append(save_th)

        for t_obj in thread_list:
            t_obj.daemon = True
            # t_obj.daemon = True
            t_obj.start()
        time.sleep(10)
        for queue in [self.pi,self.shuju]:
            queue.join()
        # self.request_url()
if __name__ == '__main__':
    pin = Pin()
    pin.main()
