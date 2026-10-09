# utils/requests_util.py
# 工具层：封装通用的请求方法
# 所有测试用例都通过这个工具发请求
# 统一处理：URL拼接、超时、异常等

import requests


class RequestsUtil:
    """
        请求工具类
        封装了 GET、POST、PUT、DELETE 等方法
        统一添加 base_url 和超时时间
    """

    def __init__(self):
        # base_url
        self.base_url = "http://localhost:3000"

        # 默认请求头
        self.headers = {
            "Content-Type": "application/json"
        }

        # 默认超时时间（秒）
        # 如果接口响应超过这个时间，会报超时异常
        self.timeout = 10

    def set_token(self,token):
        """
               设置认证 token
               调用这个方法后，后续所有请求都会自动带上 token
               """
        self.headers["Authorization"] = "Bearer " + token

    def get(self,url,params=None):
        """
        GET 请求
        path: 接口路径，如 /api/tasks
        params: URL 查询参数，如 {"page": 1}
        """
        url = self.base_url + url
        response = requests.get(
            url=url,
            headers=self.headers,
            params=params,
            timeout=self.timeout
        )
        return response

    def post(self,url,json=None):
        """
        POST 请求
        path: 接口路径
        data: 请求体数据，如 {"title": "Task 1"}
        """
        url = self.base_url + url
        response = requests.post(
            url=url,
            headers=self.headers,
            json=json,
            timeout=self.timeout
        )
        return response

    def put(self,url,json=None):
        """
        PUT 请求
        path: 接口路径
        data: 请求体数据，如 {"title": "Task 1"}
        """
        url = self.base_url + url
        response = requests.put(
            url=url,
            headers=self.headers,
            json=json,
            timeout=self.timeout
        )
        return response
    def delete(self,url):
        """
        DELETE 请求
        path: 接口路径
        """
        url = self.base_url + url
        response = requests.delete(
            url=url,
            headers=self.headers,
            timeout=self.timeout
        )
        return response

    def upload(self, url, files=None, data=None):
        url = self.base_url + url
        # 上传文件时不能带 Content-Type: application/json
        # requests 会自动设置 multipart/form-data 的Content - Type
        upload_headers = self.headers.copy()
        upload_headers.pop("Content-Type", None)

        response = requests.post(
            url=url,
            headers=upload_headers,
            files=files,
            data=data,
            timeout=self.timeout
        )
        return response


# 创建一个全局的请求工具实例
# 这样其他地方只需要 import 这个实例就能用
request_util = RequestsUtil()