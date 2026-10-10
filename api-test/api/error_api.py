# api/error_api.py
# 接口层：封装异常场景接口，用于验证测试框架的异常处理能力

from utils.requests_util import request_util


def simulate_timeout(delay=15):
    """
    模拟接口超时
    delay: 服务端延迟响应秒数，需大于工具层 timeout 才会触发超时
    """
    response = request_util.post("/api/error/timeout", json={"delay": delay})
    return response


def simulate_server_error():
    """模拟服务端 500 错误"""
    response = request_util.get("/api/error/server-error")
    return response
