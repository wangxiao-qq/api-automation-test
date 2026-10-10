# testcases/test_timeout.py
# 超时场景：模拟接口延迟，验证 requests 会抛出 Timeout 异常

import pytest
import requests

from api.error_api import simulate_timeout


class TestTimeout:
    @pytest.mark.usefixtures("login_setup")
    def test_timeout(self):
        """接口响应时间超过 timeout 时，应抛出 requests.exceptions.Timeout"""
        with pytest.raises(requests.exceptions.Timeout):
            simulate_timeout(delay=15)
