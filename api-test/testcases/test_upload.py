# testcases/test_upload.py
# 文件上传接口测试

import pytest

from api.upload_api import upload_file
from utils.assert_util import assert_success


class TestUpload:

    @pytest.mark.usefixtures("login_setup")
    def test_upload_file(self, tmp_path):
        """上传一个文本文件"""
        # 在 pytest 提供的临时目录里造文件，跑完自动清理，不污染项目目录
        file_path = tmp_path / "test_upload.txt"
        file_path.write_text("这是测试上传的文件内容", encoding="utf-8")

        response = upload_file(str(file_path))
        assert_success(response)

        resp_data = response.json()["data"]
        assert resp_data["originalname"] == "test_upload.txt"
        assert resp_data["size"] > 0
        assert "/uploads/" in resp_data["url"]
        print(f"\n上传成功: {resp_data}")
