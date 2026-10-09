# testcases/test_allure_demo.py
# 演示 Allure 报告的使用

import allure
import pytest
from api.tasks_api import get_tasks, create_task, get_task_detail, delete_task


# @allure.feature() 用于标记功能模块
# 在 Allure 报告中会按 feature 分组显示
@allure.feature("任务管理")
class TestTasksAllure:

    # @allure.story() 用于标记子功能
    @allure.story("查询任务")
    # @allure.title() 自定义用例标题（默认是函数名）
    @allure.title("获取任务列表")
    @pytest.mark.usefixtures("login_setup")
    def test_get_tasks(self):
        """获取任务列表"""

        # @allure.step() 标记操作步骤
        # 报告中会清楚显示每一步的执行情况
        with allure.step("发送请求获取任务列表"):
            response = get_tasks()

        with allure.step("验证返回数据"):
            assert response.status_code == 200
            assert response.json()["code"] == 0
            assert len(response.json()["data"]["list"]) > 0

    @allure.story("创建任务")
    @allure.title("创建新任务-正向场景")
    @pytest.mark.usefixtures("login_setup")
    def test_create_task(self):
        """创建任务"""

        with allure.step("准备创建任务的参数"):
            task_data = {
                "title": "Allure 报告测试任务",
                "description": "用于演示 Allure 功能",
                "priority": "high"
            }

        with allure.step("发送创建任务请求"):
            response = create_task(**task_data)

        with allure.step("验证任务创建成功"):
            assert response.status_code == 200
            resp_data = response.json()
            assert resp_data["code"] == 0
            assert resp_data["data"]["title"] == "Allure 报告测试任务"

            # allure.attach() 可以附加信息到报告
            allure.attach(
                str(resp_data),  # 要附加的内容
                name="响应数据",  # 显示的标题
                attachment_type=allure.attachment_type.JSON  # 格式
            )

    @allure.story("删除任务")
    @allure.title("创建-删除-验证任务")
    @pytest.mark.usefixtures("login_setup")
    def test_create_and_delete(self):
        """创建->删除->验证任务已删除"""

        with allure.step("第一步：创建任务"):
            create_resp = create_task(title="待删除的任务")
            assert create_resp.status_code == 200
            task_id = create_resp.json()["data"]["id"]
            allure.attach(f"创建的任务ID: {task_id}", name="创建结果")

        with allure.step("第二步：删除任务"):
            delete_resp = delete_task(task_id)
            assert delete_resp.status_code == 200

        with allure.step("第三步：验证任务已删除"):
            detail_resp = get_task_detail(task_id)
            assert detail_resp.status_code == 404