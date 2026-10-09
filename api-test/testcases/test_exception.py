# testcases/test_exception_scenarios.py
# 测试异常场景

import pytest
import requests
from utils.assert_util import assert_status_code


class TestExceptionScenarios:

    def test_no_token(self):
        """测试不传 token 访问需要登录的接口"""
        response = requests.get("http://localhost:3000/api/tasks")
        assert_status_code(response, 401)

    def test_fake_token(self):
        """测试传假的 token"""
        headers = {"Authorization": "Bearer fake_token_123"}
        response = requests.get(
            "http://localhost:3000/api/tasks",
            headers=headers
        )
        assert_status_code(response, 401)

    def test_empty_title_create_task(self):
        """测试创建任务时标题为空"""
        # 先登录获取 token
        login_resp = requests.post(
            "http://localhost:3000/api/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_resp.json()["data"]["token"]

        headers = {"Authorization": "Bearer " + token}

        # 传空的 title
        response = requests.post(
            "http://localhost:3000/api/tasks",
            headers=headers,
            json={"title": ""}
        )

        # 期望返回 400
        assert_status_code(response, 400)
        assert response.json()["message"] == "任务标题不能为空"

    def test_server_error(self):
        """测试服务器500错误"""
        response = requests.get("http://localhost:3000/api/error/server-error")
        assert_status_code(response, 500)

    def test_long_title(self):
        """测试标题超过长度限制"""
        login_resp = requests.post(
            "http://localhost:3000/api/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_resp.json()["data"]["token"]

        headers = {"Authorization": "Bearer " + token}

        # 创建51个字符的标题（限制是50）
        long_title = "a" * 51
        response = requests.post(
            "http://localhost:3000/api/tasks",
            headers=headers,
            json={"title": long_title}
        )

        assert_status_code(response, 400)
        assert "50个字符" in response.json()["message"]