# utils/requests_util.py
# 工具层：封装通用的请求方法
# 所有测试用例都通过这个工具发请求
# 统一处理：URL 拼接、超时、鉴权头、异常等

import os

import requests

# 被测服务地址：优先读环境变量 API_BASE_URL，默认本地 3000 端口
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")


class RequestsUtil:
    """
    请求工具类
    封装了 GET、POST、PUT、DELETE 等方法
    统一添加 base_url 和超时时间
    """

    def __init__(self, base_url=BASE_URL, timeout=10):
        # 被测服务地址
        self.base_url = base_url

        # 默认请求头
        self.headers = {
            "Content-Type": "application/json"
        }

        # 默认超时时间（秒）
        # 如果接口响应超过这个时间，会抛超时异常
        self.timeout = timeout

    def set_token(self, token):
        """
        设置认证 token
        调用这个方法后，后续所有请求都会自动带上 token
        """
        self.headers["Authorization"] = "Bearer " + token

    def get(self, url, params=None):
        """
        GET 请求
        url: 接口路径，如 /api/tasks
        params: URL 查询参数，如 {"page": 1}
        """
        return requests.get(
            url=self.base_url + url,
            headers=self.headers,
            params=params,
            timeout=self.timeout
        )

    def post(self, url, json=None):
        """
        POST 请求
        url: 接口路径
        json: 请求体数据，如 {"title": "Task 1"}
        """
        return requests.post(
            url=self.base_url + url,
            headers=self.headers,
            json=json,
            timeout=self.timeout
        )

    def put(self, url, json=None):
        """
        PUT 请求
        url: 接口路径
        json: 请求体数据
        """
        return requests.put(
            url=self.base_url + url,
            headers=self.headers,
            json=json,
            timeout=self.timeout
        )

    def delete(self, url):
        """
        DELETE 请求
        url: 接口路径
        """
        return requests.delete(
            url=self.base_url + url,
            headers=self.headers,
            timeout=self.timeout
        )

    def upload(self, url, files=None, data=None):
        """
        文件上传请求
        上传时不能带 Content-Type: application/json
        requests 会自动设置 multipart/form-data 的 Content-Type 与边界
        """
        upload_headers = self.headers.copy()
        upload_headers.pop("Content-Type", None)

        return requests.post(
            url=self.base_url + url,
            headers=upload_headers,
            files=files,
            data=data,
            timeout=self.timeout
        )


# 创建一个全局的请求工具实例
# 这样其他地方只需要 import 这个实例就能用
request_util = RequestsUtil()
