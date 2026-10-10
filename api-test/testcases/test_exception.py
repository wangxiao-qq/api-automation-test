# testcases/test_exception.py
# 异常场景测试：鉴权失败、参数校验失败、服务端错误
# 全部通过工具层 / 接口层发请求，用例里不出现接口地址

import pytest

from api.error_api import simulate_server_error
from api.tasks_api import create_task
from utils.assert_util import assert_error, assert_status_code
from utils.requests_util import RequestsUtil


class TestAuthException:
    """
    鉴权类异常：使用独立的请求实例，不带 token / 带伪造 token

    注意：全局 request_util 在会话登录后会自动带上真实 token，
    所以这里单独 new 一个实例，避免用例之间互相影响
    """

    def test_no_token(self):
        """不传 token 访问需要鉴权的接口，应返回 401"""
        client = RequestsUtil()
        response = client.get("/api/tasks")
        assert_status_code(response, 401)

    def test_fake_token(self):
        """使用伪造的 token，应返回 401"""
        client = RequestsUtil()
        client.set_token("fake_token_123")
        response = client.get("/api/tasks")
        assert_status_code(response, 401)


@pytest.mark.usefixtures("login_setup")
class TestParamException:
    """参数校验类异常：登录态由 session 级 fixture 提供"""

    def test_empty_title_create_task(self):
        """创建任务时标题为空，应返回 400"""
        response = create_task(title="")
        assert_error(response, 400)
        assert response.json()["message"] == "任务标题不能为空"

    def test_long_title(self):
        """标题超过 50 字符限制，应返回 400"""
        response = create_task(title="a" * 51)
        assert_error(response, 400)
        assert "50个字符" in response.json()["message"]

    def test_server_error(self):
        """模拟服务端 500 错误"""
        response = simulate_server_error()
        assert_status_code(response, 500)
