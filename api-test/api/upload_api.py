# api/upload_api.py
# 接口层：封装文件上传接口
from utils.requests_util import request_util

def upload_file(file_path):
      """
      上传文件
      file_path: 本地文件路径
      """
      with open(file_path, "rb") as f:
          files = {"file": f}
          response = request_util.upload("/api/upload",files=files)
      return response
