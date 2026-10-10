# testcases/test_login.py
# 登录接口测试：YAML 数据驱动 + pytest 参数化

import pytest

from api.login_api import login
from utils.data_util import read_yaml

# 从 YAML 读取测试数据
# 每个 key 是一组用例，字段：username / password / expect_code / expect_message
login_data = read_yaml("login_data.yaml")

# 把 YAML 字典转成参数化需要的列表：
# [ (用例名, 用户名, 密码, 期望状态码, 期望消息), ... ]
parametrize_data = [
    (
        case_name,
        case["username"],
        case["password"],
        case["expect_code"],
        case["expect_message"],
    )
    for case_name, case in login_data.items()
]


# 有多少组数据，这个用例就跑多少遍
@pytest.mark.parametrize(
    "case_name, username, password, expect_code, expect_message",
    parametrize_data,
    ids=[case[0] for case in parametrize_data],  # 用 YAML 里的用例名作为测试 ID
)
def test_login(case_name, username, password, expect_code, expect_message):
    """登录接口参数化测试：一组数据对应一条用例"""
    response = login(username, password)
    resp_data = response.json()

    assert resp_data["code"] == expect_code
    assert resp_data["message"] == expect_message
