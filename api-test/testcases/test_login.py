# testcases/test_login_data_driven.py
# 演示数据驱动

import pytest
import requests
from utils.data_util import read_yaml

# 读取测试数据
# read_yaml() 返回一个字典，其中包含所有测试数据
# login_data = read_yaml("login_data.yaml")
#
#
# def test_login_success():
#     """测试登录成功——直接读取 YAML 中的数据"""
#
#     # 从读到的数据中取出"登录成功"这组数据
#     case = login_data["login_success"]
#
#     response = requests.post(
#         "http://localhost:3000/api/login",
#         json={
#             "username": case["username"],
#             "password": case["password"]
#         }
#     )
#     resp_data = response.json()
#
#     # 期望值也写在 YAML 里了
#     assert resp_data["code"] == case["expect_code"]
#     assert resp_data["message"] == case["expect_message"]


# ★ 更高级的用法：用 @pytest.mark.parametrize 实现参数化
# 一组数据跑一次用例，而不是每个场景写一个函数

# 先准备好参数化数据
# 列表里的每个元组，都是一组测试数据
parametrize_data = [
    # (用户名,    密码,        期望状态码, 期望消息)
    ("admin", "admin123", 0, "登录成功"),
    ("admin", "wrong", 400, "用户名或密码错误"),
    ("", "admin123", 400, "用户名不能为空"),
    ("admin", "", 400, "密码不能为空"),
]


# @pytest.mark.parametrize 是 pytest 的参数化装饰器
# 格式：(参数名1, 参数名2, ...), [ (值1, 值2), (值1, 值2), ... ]
# 有多少组数据，这个用例就跑多少遍
@pytest.mark.parametrize(
    "username, password, expect_code, expect_message",
    parametrize_data
)
def test_login_parametrize(username, password, expect_code, expect_message):
    """
    参数化测试登录接口
    一组数据跑一遍这个函数，总共跑4遍
    """
    response = requests.post(
        "http://localhost:3000/api/login",
        json={
            "username": username,
            "password": password
        }
    )
    resp_data = response.json()

    assert resp_data["code"] == expect_code
    assert resp_data["message"] == expect_message