# -*- coding: utf-8 -*-
# @Time    : 2023/8/24 下午8:07
# @Author  : 顾安
# @File    : 1.腾讯招聘.py
# @Software: PyCharm

"""
https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1692878740516&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=python&pageIndex=2&pageSize=10&language=zh-cn&area=cn
    获取腾讯招聘中的岗位信息并存储到mysql中
"""

import pymysql
import requests


class TxWork:

    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='321542', db='mysql')
        self.cursor = self.db.cursor()

    def create_table(self):
        sql = """
                 CREATE TABLE spider_douyin (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- 自增主键
    cid VARCHAR(255) NOT NULL,           -- 评论 ID
    text TEXT NOT NULL,                   -- 评论内容
    aweme_id VARCHAR(255) NOT NULL,      -- 视频 ID
    create_time DATETIME NOT NULL,       -- 创建时间
    ip VARCHAR(45) NOT NULL,              -- IP 地址
    reply_all INT DEFAULT 0,             -- 回复总数
    nickname VARCHAR(255) NOT NULL,      
    awemeid VARCHAR(255) NOT NULL,-- 用户昵称
    signature TEXT                        -- 用户签名
);

               """
        try:
            self.cursor.execute(sql)
            print('数据表创建成功...')
        except Exception as e:
            print('数据表创建失败: ', e)

    def main(self):
        self.create_table()

        self.db.close()


if __name__ == '__main__':
    tx_work = TxWork()
    tx_work.main()

