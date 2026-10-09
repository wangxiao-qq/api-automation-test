# api/category_api.py
  # 接口层：封装分类相关的接口


from utils.requests_util import request_util


def get_categories():
    """
          获取分类列表
          不需要登录，可以直接调用
          """
    response = request_util.get("/api/categories")
    return response