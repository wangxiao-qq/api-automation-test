# testcases/test_tasks.py
# 任务管理接口测试：使用封装的断言，验证正向流程与异常分支

import pytest

from api.tasks_api import (
    batch_delete_tasks,
    create_task,
    get_task_detail,
    get_tasks,
)
from utils.assert_util import assert_field_equal, assert_status_code, assert_success


@pytest.mark.usefixtures("login_setup")
class TestTasksAdvanced:

    def test_get_tasks(self):
        """用封装的断言来写"""
        # 获取任务列表
        response = get_tasks()

        # 一行断言代替3行
        assert_success(response)

        # 验证返回数据的结构
        resp_data = response.json()
        assert isinstance(resp_data["data"]["list"], list), "list 应该是一个列表"
        assert isinstance(resp_data["data"]["total"], int), "total 应该是一个整数"

    def test_create_task_with_assert(self):
        """创建任务并使用字段断言"""
        response = create_task(title="测试断言封装", priority="high")

        assert_success(response)

        # 用封装的字段断言，一行验证一个字段
        assert_field_equal(response, "data.title", "测试断言封装")
        assert_field_equal(response, "data.priority", "high")
        assert_field_equal(response, "data.status", "todo")

    def test_task_not_found(self):
        """测试查询不存在的任务"""
        response = get_task_detail(99999)

        # 期望返回 404
        assert_status_code(response, 404)

    def test_batch_delete_tasks(self):
        """先创建两个任务，再批量删除它们"""
        # 1. 创建任务 A
        resp_a = create_task(title="待批量删除-A")
        assert_success(resp_a)
        task_id_a = resp_a.json()["data"]["id"]

        # 2. 创建任务 B
        resp_b = create_task(title="待批量删除-B")
        assert_success(resp_b)
        task_id_b = resp_b.json()["data"]["id"]

        print(f"\n已创建两个任务: {task_id_a}, {task_id_b}")

        # 3. 批量删除这两个任务
        resp_delete = batch_delete_tasks([task_id_a, task_id_b])
        assert_success(resp_delete)
        assert "成功删除 2 个任务" in resp_delete.json()["message"]

        # 4. 验证：再去查这两个任务，应该返回 404
        assert_status_code(get_task_detail(task_id_a), 404)
        assert_status_code(get_task_detail(task_id_b), 404)
