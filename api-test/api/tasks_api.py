# api/tasks_api.py
# 接口层：封装任务相关的接口
import requests

from utils.requests_util import request_util

def get_tasks(params=None):
    """
    获取任务列表
    params: 可选参数，如 {"status": "done", "page": 1}
    """
    response = request_util.get(url=f"/api/tasks", params=params)
    return response

def get_task_detail(task_id):
    """
    获取任务详情
    """
    response = request_util.get(url=f"/api/tasks/{task_id}")
    return response

def create_task(title, description="", status="todo", priority="medium"):
    """
    创建任务
    """
    data = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority
    }
    response = request_util.post(url=f"/api/tasks", json=data)
    return response

def update_task(task_id,  update_data=None):
    """
    更新任务
    """
    response = request_util.put(url=f"/api/tasks/{task_id}", json=update_data)
    return response

def delete_task(task_id):
    """
    删除任务
    """
    response = request_util.delete(url=f"/api/tasks/{task_id}")
    return response

def batch_delete_tasks(task_ids):
    """
      批量删除任务
      task_ids: 任务ID列表，如 [1, 2, 3]
      """
    response = request_util.post(url=f"/api/tasks/batch", json={"ids":task_ids})
    return response