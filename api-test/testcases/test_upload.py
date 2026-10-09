# testcases/test_upload.py
# 测试文件上传接口
import pytest
from api.upload_api import upload_file
from utils.assert_util import assert_success


class TestUpload:

    @pytest.mark.usefixtures("login_setup")
    def test_upload_file(self):
        """上传一个文本文件"""
        # 先创建一个临时文件用来上传
        with open("test_upload.txt", "w", encoding="utf-8") as f:
            f.write("这是测试上传的文件内容")

        response = upload_file("test_upload.txt")
        assert_success(response)

        resp_data = response.json()["data"]
        assert resp_data["originalname"] == "test_upload.txt"
        assert resp_data["size"] > 0
        assert "http://localhost:3000/uploads/" in resp_data["url"]
        print(f"\n上传成功: {resp_data}")