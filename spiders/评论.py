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
    def get_ip(self):
        response = requests.get(self.ip_url, headers=self.headers)
        # print(ip)
        ip_data = response.json()
        print(ip_data)
        # 提取代理IP
        ip = ip_data['data'][0]['server']
        print(f"Using proxy: {ip}")
        self.ip_queue.put(ip)
    def js(self,params):
        params_str = urllib.parse.urlencode(params)
        ctx = execjs.compile(open('douyin.js').read())
        a_bogus = ctx.call('getSign', params_str)
        params['a_bogus'] = a_bogus
    def request_url(self,ID):
        global cursor,has_more
        while self.has_more==1:
            params = {
                'device_platform': 'webapp',
                'aid': '6383',
                'channel': 'channel_pc_web',
                'aweme_id': ID,
                'cursor': self.cursor,
                'count': '50',
                'item_type': '0',
                'insert_ids': '',
                'whale_cut_token': '',
                'cut_version': '1',
                'rcFT': '',
                'update_version_code': '170400',
                'pc_client_type': '1',
                'version_code': '170400',
                'version_name': '17.4.0',
                'cookie_enabled': 'true',
                'screen_width': '1707',
                'screen_height': '960',
                'browser_language': 'zh-CN',
                'browser_platform': 'Win32',
                'browser_name': 'Chrome',
                'browser_version': '127.0.0.0',
                'browser_online': 'true',
                'engine_name': 'Blink',
                'engine_version': '127.0.0.0',
                'os_name': 'Windows',
                'os_version': '10',
                'cpu_core_num': '16',
                'device_memory': '8',
                'platform': 'PC',
                'downlink': '1.55',
                'effective_type': '3g',
                'round_trip_time': '300',
                'webid': '7367376568496866879',
                'verifyFp': 'verify_lyvc82p9_zLVuRZRJ_TAKA_48JW_9BH0_8keV5LISyFVz',
                'fp': 'verify_lyvc82p9_zLVuRZRJ_TAKA_48JW_9BH0_8keV5LISyFVz',
                'msToken': 'wavKpg-5ZRYp8hxZIT3t9iL8qNyxtnTqS5BZuoDQ0gjnlRKoqeTgHa46Jf1dx8Cnc3GwgjNYP06SZ34JoiZzphcI-4eNM8BQJtLrn_qQZV4pJVkoTQ_S3gZYG6xyAuU=',
                # 'a_bogus': 'dy80MVL6diVihfSg5fALfY3q6l33YM140trEMD2f4V3NBy39HMTR9exuhMhvGtfjN4/kIeujy4hbTrOgrQ2G0Zwf9Skw/2A2mESkKl5Q5xSSs1XyeykgJUhimktRSeo2RkBlrOXQq7pHKR8D09oHmhK4bIOwu3GMlj==',
            }
            # print('剩余评论：',self.all_comments-params['cursor'])
            self.js(params)
            if self.ip_queue.empty():
                self.get_ip()
            ip=self.ip_queue.get()
            print(ip)
                # self.headers['user-Agent'] = UserAgent().random
            # print(self.headers['user-Agent'])
            proxies = {
                'http': 'http://' + ip,
                'https': 'http://' + ip
            }
            try:
                res=requests.get('https://www.baidu.com', proxies=proxies,verify=False,timeout=10)
                print(res)
                response = requests.get('https://www.douyin.com/aweme/v1/web/comment/list/', params=params,headers=self.headers, cookies=cookies,proxies=proxies,timeout=5)
                self.ip_queue.put(ip)
            except :
                try:
                    self.ip_queue.task_done()
                    response = requests.get('https://www.douyin.com/aweme/v1/web/comment/list/', params=params,
                                headers=self.headers, cookies=cookies,timeout=5)
                except Exception as e:
                    print(e)

            try:
                if response.status_code == 200:
                    # print(response.text)
                    response=response.json()
                    # print(response)
                    self.parse(response,params)
            except Exception as e:
                print(e)
                # print(e)
                print('》》》》》》》》》》》》》》》》》》')
                print('异常')
                sys.exit()
    def parse(self,response,params):
        global cursor,has_more
        # "total": 541, 总评论
        try:
            self.all_comments = response['total']
            # print(self.all_comments)
            # "cursor": 20, 现在的数目
            # "has_more": 1, 是否还有
            self.cursor = response['cursor']
            self.has_more = response['has_more']
            params['cursor'] = self.cursor
            # print('剩余评论：',self.all_comments-params['cursor'])
            # 评论内容
            comments = response['comments']

            for comment in comments:
                temp={}
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
                reply_all=comment['reply_comment_total']
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
                self.result.append(temp)
        except Exception as e:
            self.has_more = 0
            print(e)
            print('或许此视频五评论')
            print('??')
    def main(self):
        blog=input('请输入博主:')
        data=pd.read_csv(r'blog\{}.csv'.format(blog))
        # 假设你的脚本位于 'E:\桌面\计算机\爬虫\'
        # 那么相对路径就是 '抖音\blog'
        relative_path = 'comment\{}'.format(blog)
        # 获取当前工作目录
        current_dir = os.getcwd()
        # 构建完整的相对路径
        file_name = os.path.join(current_dir, relative_path)
        # 检查路径是否存在，如果不存在则创建
        if not os.path.exists(file_name):
            os.makedirs(file_name)
        logs='log'
        # 获取当前工作目录
        current_dir = os.getcwd()
        # 构建完整的相对路径
        file_e = os.path.join(current_dir, logs)
        if not os.path.exists(file_e):
            os.makedirs(file_e)
        try:
            data2=pd.read_csv(r'log\{}.csv'.format(blog))
        except:
            print("文件未找到，请检查路径是否正确。")
            data2 = pd.DataFrame(columns=['Awesome ID'])  # 创建一个空的DataFrame，包含'title'列
        IDs=data['Awesome ID'].to_list()
        names=data['Title'].to_list()

        for ID,name in zip(IDs,names):
            if ID not in data2['Awesome ID'].to_list():
                self.all_comments=0
                self.cursor = 0
                self.has_more = 1
                self.request_url(ID)
                df = pd.DataFrame(self.result)
                path=os.path.join(file_name,'{}.csv'.format(ID))
                df.to_csv(path,index=False)
                print('--------------------------------------')
                print(self.result)
                data_dict = {
                    '博主': blog,
                    'Awesome ID': ID,
                    '标题': name,
                }
                # 将字典转换为DataFrame
                path2 = os.path.join(file_e, '{}.csv'.format(blog))
                db = pd.DataFrame([data_dict])
                self.result=[]
                # db.to_csv(path2, index=False)
                with open(path2, 'a', encoding='utf-8') as f:
                    # 写入文件头，只在第一次写入时需要
                    if f.tell() == 0:  # 如果文件指针在文件开头，说明文件是空的
                        db.to_csv(f, index=False)  # 写入文件头
                    else:
                        db.to_csv(f, index=False, header=False)  # 追加数据，不写入文件头

                    # 打印消息，表明数据已成功存入
                    print(ID, '存入成功')
            else:
                print('数据重复')
if __name__ == '__main__':
    pin=Pin()
    # pin.get_ip()
    # page = ChromiumPage()
    do1 = ChromiumOptions().auto_port().set_paths(local_port=9121, user_data_path=r'D:\data4')
    # page = ChromiumPage(do1)
    page = ChromiumPage(do1)
    page.get('https://www.douyin.com/?recommend=1', retry=3, interval=2, timeout=5)
    cookies = page.cookies(as_dict=True)
    pin.main()