import json
import time
from DrissionPage import ChromiumPage,ChromiumOptions
with open('cookies.json','r',encoding='utf-8') as f:
    cookies = json.load(f)
page = ChromiumPage()
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