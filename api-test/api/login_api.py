# api/login_api.py
# 接口层：封装登录相关的接口
# 测试用例层调用这里的函数，不需要知道接口地址和格式
from lxml.html.diff import token
from pygments.lexers import json5
import requests

from utils.requests_util import request_util


def login(username, password):
    """
      登录接口
      参数：
          username: 用户名
          password: 密码
      返回：
          response 对象（包含状态码、返回数据等）
      """

    # 准备请求数据
    data = {
        "username": username,
        "password": password
    }

    # 调用工具层发 POST 请求
    # 路径 /api/login 会拼上 base_url 变成 http://localhost:3000/api/login
    response = request_util.post("/api/login",json=data)
    # ★ 如果登录成功，自动把 token 设置到工具类中
    # 这样后面调其他接口时就不用手动传 token 了
    if response.status_code == 200 and response.json().get("code")==0:
        token = response.json()["data"]["token"]
        request_util.set_token(token)
        print(f"\n[login_api] 登录成功，token 已自动设置")
        return response


def register(username,password,nickname):
    """
    注册接口
    参数：
        username: 用户名
        password: 密码
        nickname: 昵称
    返回：
        response 对象（包含状态码、返回数据等）
    """
    # 准备请求数据
    data = {
        "username": username,
        "password": password,
        "nickname": nickname
    }

    # 调用工具层发 POST 请求
    # 路径 /api/register 会拼上 base_url 变成 http://localhost:3000/api/register
    response = request_util.post("/api/register", json=data)
    return response
