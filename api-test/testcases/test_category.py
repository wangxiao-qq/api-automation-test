# testcases/test_category.py
# 测试分类管理接口
from api.category_api import get_categories
from utils.assert_util import assert_success

class TestCategory:

    def test_get_categories(self):
        """获取所有分类"""
        response = get_categories()
        assert_success(response)
        resp_data = response.json()
        # 验证返回的分类列表不为空
        assert len(resp_data["data"]) > 0
        print(f"\n分类列表: {resp_data['data']}")