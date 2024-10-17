import os
import time
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Actions
from queue import Queue
import redis
import threading
import pickle
import pprint
import requests
import sys
from urllib.parse import unquote
import re
import time
import json
import requests
import pandas as pd

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    'referer': 'https://www.douyin.com',
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}
class Install():
    def __init__(self):
        self.url_queue = Queue()
        self.cook = Queue()
        self.par = Queue()
        self.awe=Queue()
        self.ip_url = 'https://share.proxy.qg.net/get?key=ESDKF0H8&pwd=BC20D73ADC0A'
        self.ip_queue = Queue()
    def get_ip(self):
        response = requests.get(self.ip_url)
        # print(ip)
        ip_data = response.json()
        print(ip_data)
        # 提取代理IP
        ip = ip_data['data'][0]['server']
        print(f"Using proxy: {ip}")
        self.ip_queue.put(ip)
    def login(self,data,file_name,data2):
        page = ChromiumPage()
        page.get('https://www.douyin.com/?recommend=1', retry=3, interval=2, timeout=5)
        # page.clear_cache()
        print('请于30秒内扫码登录')
        time.sleep(30)
        self.start(data,file_name,page,data2)
    def start(self,data,file_name,page,data2):
        print(55555555555555555555555555555)
        sec = data['sec_user_id'].to_list()[1]
        Awesome_ID = data['Awesome ID'].to_list()
        blog = data['博主'].to_list()[1]
        # time.sleep(2)
        cookies = page.cookies(as_dict=True)
        url = "https://www.douyin.com/user/{}".format(sec)
        for i in Awesome_ID:
            if i in data2['Awesome ID'].to_list():
                print('{}此视频已经下载'.format(i))
                continue

            self.cook.put(cookies)
            # self.par.put(params)
            self.url_queue.put(url)
            self.awe.put(i)
            # self.par(response,blog,i,file_name)
            # print(response.text)
            # print(response)
    def pars(self,blog,file_name):
        while True:
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
            cookies=self.cook.get()
            # params=self.par.get()
            url=self.url_queue.get()
            i=self.awe.get()
            try:

                params = {
                    'modal_id': i,
                    # 'vid':i
                }
                try:
                    response = requests.get(url, headers=headers, cookies=cookies, params=params,proxies=proxies)
                    print(ip)
                except:
                    response = requests.get(url, headers=headers, cookies=cookies, params=params)
                info = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', response.text)[0]
                # print(response.text)
                json_str = unquote(info)
                json_data = json.loads(json_str)
                hrefs = json_data['app']['videoDetail']['download']['urlList']
                href = ''
                for mmm in hrefs:
                    if 'http://v3-web.douyinvod.com' in mmm:
                        href = mmm
                print(href)
                title = json_data['app']['videoDetail']['desc']
                if len(title) <= 2:
                    title = str(i)
                print(title)
                new_title = re.sub(r'[\\/:*?"<>|\n\r]', '', title)
                size = 0

                print('准备下载', title)

                start = time.time()  # 开始时间
                res = requests.get(href, headers=headers, stream=True)
                flie = os.path.join(file_name, str(i))
                # print(res.content)
                with open(flie, 'wb') as f:
                    f.write(res.content)


                data_dict = {
                    '博主': blog,
                    'Awesome ID': i
                }
                # 将字典转换为DataFrame
                df = pd.DataFrame([data_dict])
                # 打开文件，追加数据，并写入CSV格式
                relative_path = 'record'
                # 获取当前工作目录
                current_dir = os.getcwd()
                # 构建完整的相对路径
                record_file = os.path.join(current_dir, relative_path)
                # record_file = r'E:\桌面\计算机\爬虫\抖音\record'
                if not os.path.exists(record_file):
                    os.makedirs(record_file)
                file = os.path.join(record_file, blog + '.csv')
                with open(file, 'a', encoding='utf-8') as f:
                    # 写入文件头，只在第一次写入时需要
                    if f.tell() == 0:  # 如果文件指针在文件开头，说明文件是空的
                        df.to_csv(f, index=False)  # 写入文件头
                    else:
                        df.to_csv(f, index=False, header=False)  # 追加数据，不写入文件头

                    # 打印消息，表明数据已成功存入
                    print(i, '存入成功')
            except Exception as e:
                print(url)
                print(e)
                sys.exit()
            finally:
                self.cook.task_done()
                # self.par.task_done()
                self.awe.task_done()
                self.url_queue.task_done()

    def main(self):
            #传入查询列表
            name=input('请输入你要下载的博主视频：')
            data = pd.read_csv('blog/{}.csv'.format(name), encoding='utf-8')
            if os.path.exists(r'record\{}.csv'.format(name)):
                data2=pd.read_csv(r'record\{}.csv'.format(name), encoding='utf-8')
            else:
                print("文件未找到，请检查路径是否正确。")
                data2 = pd.DataFrame(columns=['Awesome ID'])  # 创建一个空的DataFrame，包含'title'列
            blog=data['博主'].to_list()[1]
            # 保存路径
            file_name=r'video\{}'.format(blog)
            if not os.path.exists(file_name):
                os.makedirs(file_name)
            m=input("是否登录，0or1\n")
            if m=='0':
                self.login(data,file_name,data2)
            else:
                do1 = ChromiumOptions().set_paths(local_port=9121, user_data_path=r'D:\data5')
                page = ChromiumPage(do1)
                # page = ChromiumPage()
                page.get('https://www.douyin.com/?recommend=1', retry=3, interval=2, timeout=5)
                self.start(data,file_name,page,data2)
                time.sleep(2)
                thread_list = list()
                for _ in range(3):
                    t_get_info = threading.Thread(target=self.pars,args=(blog,file_name))
                    thread_list.append(t_get_info)
                for t_obj in thread_list:
                    t_obj.daemon = True
                    # t_obj.daemon = True
                    t_obj.start()
                time.sleep(2000)
                for queue in [self.url_queue,self.cook,self.par,self.awe]:
                    queue.join()
if __name__ == '__main__':
    install = Install()
    install.main()