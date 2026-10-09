import pytest
from api.errror_api import simulate_timeout
from utils.requests_util import request_util
import requests


# 先登录 (这个接口需要token)
class TestTimeout:
    @pytest.mark.usefixtures("login_setup")
    def test_timeout(self):
        response = request_util.get("/api/error/timeout")
        """验证接口超时"""
        with pytest.raises(requests.exceptions.Timeout):
            simulate_timeout(delay=15)
