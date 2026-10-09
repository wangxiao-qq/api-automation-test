# utils/assert_util.py
# 工具层：封装通用的断言方法
# 让测试用例的断言部分更简洁

def assert_success(response):
    """
    通用断言：接口调用成功
    适用场景：正常业务场景
    验证：
        1. HTTP 状态码为 200
        2. 业务 code 为 0（代表业务成功）
    """
    resp_data = response.json()

    # 断言 HTTP 状态码
    assert response.status_code == 200, \
        f"HTTP 状态码异常，期望 200，实际 {response.status_code}"

    # 断言业务状态码
    assert resp_data["code"] == 0, \
        f"业务状态码异常，期望 0，实际 {resp_data['code']}，消息：{resp_data['message']}"


def assert_error(response, expect_code=400):
    """
    通用断言：接口返回业务错误
    适用场景：参数校验失败、业务逻辑错误
    验证：
        1. HTTP 状态码等于 expect_code（默认 400）
        2. 业务 code != 0
    """
    resp_data = response.json()

    assert response.status_code == expect_code, \
        f"HTTP 状态码异常，期望 {expect_code}，实际 {response.status_code}"

    # 业务 code 应该不等于 0（非成功状态）
    assert resp_data["code"] != 0, "期望业务失败，但 code 为 0"


def assert_status_code(response, expect_code):
    """
    断言 HTTP 状态码
    适用场景：需要验证特定状态码时
    """
    assert response.status_code == expect_code, \
        f"HTTP 状态码异常，期望 {expect_code}，实际 {response.status_code}"


def assert_field_equal(response, field_path, expect_value):
    """
    断言返回数据中某个字段的值等于期望值
    适用场景：验证某个具体字段的内容
    参数：
        response: 响应对象
        field_path: 字段路径，如 "data.title"
        expect_value: 期望值
    """
    resp_data = response.json()

    # 按点号分隔路径，逐层取值
    # 比如 field_path="data.title" → 先取 data，再取 title
    fields = field_path.split(".")
    value = resp_data
    for field in fields:
        value = value[field]

    assert value == expect_value, \
        f"字段 {field_path} 值异常，期望 {expect_value}，实际 {value}"