# conftest.py
# pytest 配置文件

import pytest
from api.login_api import login

@pytest.fixture(scope="session")
def login_setup():
    """
    登录 fixture
    使用封装好的 login 函数，代码更简洁
    登录 fixture，所有测试用例共享一次登录
     """
    # 调用 api 层的登录接口
    response = login("admin", "admin123")

    # 断言登录成功
    assert response.status_code == 200
    assert response.json()["code"] == 0

    print("\n[conftest] 登录设置完成")
    yield
    print("\n[conftest] 测试全部结束")




