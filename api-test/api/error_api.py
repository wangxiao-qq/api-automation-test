from utils.requests_util import request_util

def  simulate_timeout(delay=15):
    """模拟接口超时，delay 指定超时秒数"""
    response = request_util.post("/api/error/timeout",
                                 json={"delay": delay})
    return response