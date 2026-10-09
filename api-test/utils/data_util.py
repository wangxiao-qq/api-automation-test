# utils/data_util.py
# 工具层：读取测试数据文件

import yaml
import os


def read_yaml(file_name):
    """
    读取 YAML 文件
    file_name: 文件名（如 login_data.yaml）
    返回：Python 字典
    """
    # os.path.join 拼接文件路径
    # __file__ 表示当前文件所在目录
    # 拼起来就是 data/login_data.yaml
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        file_name
    )

    # 打开并读取 YAML 文件
    with open(file_path, encoding="utf-8") as f:
        # yaml.safe_load 把 YAML 内容转成 Python 字典
        data = yaml.safe_load(f)

    return data