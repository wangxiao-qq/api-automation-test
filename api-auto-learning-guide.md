# 接口自动化框架从零搭建实战

**项目：任务管理系统 API**

> 本文档带你从零搭建一个完整的接口自动化测试框架，每步都有：
> - 📖 知识点讲解
> - 💻 动手练习（含代码和逐行解释）
> - 🎤 面试官会问的问题
>
> **版本说明（2026-10-18）**：本指南按"从零搭建"的教学顺序展开，标注 **【教学中间版】** 的代码是这一步的简化版、后面会被改造；标注 **【仓库最终版】** 的代码块已与仓库实际文件逐条核对。**一切以仓库代码为准**。
>
> 实测（先启动 `api-server`，在 `api-test/` 下运行 `python -m pytest -q`）：**19 passed in 10.33s**。

---

## 准备工作

### 安装清单

```
1. Python 3.8+          → 用于写自动化脚本
2. VSCode 或 PyCharm    → 写代码的工具
3. Postman              → 先手工调试接口，再转自动化
```

### 启动项目 API 服务器

```bash
cd C:\Users\xiaow\Desktop\软件测试项目\接口自动化\api-auto-project\api-server
npm start
```

服务器启动后，终端会显示：
```
任务管理API已启动: http://localhost:3000
预置账号: admin / admin123  或  tester / tester123
```

> **小知识**：`http://localhost:3000` 中的 `localhost` 代表本机，`3000` 是端口号。API 服务器的地址就是 `http://localhost:3000`，后面加上具体接口路径，比如登录接口就是 `http://localhost:3000/api/login`

> **端口可配置**：服务端读 `PORT` 环境变量，测试框架读 `API_BASE_URL`，JWT 密钥读 `JWT_SECRET`，默认值都是本地 3000 端口。两者要一起改：
>
> ```bash
> set PORT=3001
> set API_BASE_URL=http://localhost:3001
> ```
>
> `npm start` 等价于 `node server.js`（见 `api-server/package.json` 的 `scripts.start`）。

---

## 项目总览

我们先看看这个项目有哪些接口：

| 接口 | 方法 | 地址 | 是否需要登录 |
|------|------|------|:----------:|
| 用户登录 | POST | /api/login | ❌ |
| 用户注册 | POST | /api/user/register | ❌ |
| 获取用户信息 | GET | /api/user/info | ✅ |
| 获取任务列表 | GET | /api/tasks | ✅ |
| 获取任务详情 | GET | /api/tasks/:id | ✅ |
| 创建任务 | POST | /api/tasks | ✅ |
| 更新任务 | PUT | /api/tasks/:id | ✅ |
| 删除任务 | DELETE | /api/tasks/:id | ✅ |
| 批量删除 | POST | /api/tasks/batch | ✅ |
| 获取分类 | GET | /api/categories | ❌ |
| 创建分类 | POST | /api/categories | ❌ |
| 上传文件 | POST | /api/upload | ✅ |
| 模拟超时 | POST | /api/error/timeout | ✅ |
| 服务器错误 | GET | /api/error/server-error | ❌ |

---

## 学习路线（6天）

| 天数 | 内容 | 难度 |
|:---:|------|:---:|
| Day 1 | 环境搭建 + 发送第一个请求 | ⭐ |
| Day 2 | pytest 基础 + 测试用例结构 | ⭐⭐ |
| Day 3 | 接口关联 + token 处理 | ⭐⭐ |
| Day 4 | 数据驱动 + 分层封装 | ⭐⭐⭐ |
| Day 5 | 异常场景 + 断言封装 | ⭐⭐⭐ |
| Day 6 | 完整框架整合 + Allure 报告 | ⭐⭐⭐⭐ |

---

# Day 1：环境搭建 + 发送第一个请求

## 📖 知识点

### 什么是接口自动化？

说白了就是：**用代码代替 Postman，自动调用接口并检查返回结果对不对。**

比如在 Postman 里你手动做这些事：
1. 输入 URL 和参数
2. 点 Send
3. 看返回结果

自动化就是写一段代码，让代码替你做这 3 步，而且可以一次跑几百个接口。

### 需要用到的 Python 库

- **requests**：发送 HTTP 请求的库（发请求、收响应）
- **pytest**：运行测试用例的框架（组织用例、生成报告）
- **allure-pytest**：生成漂亮的测试报告（项目最终用的是 Allure，见 Day 6）

---

## 💻 动手：第一步——发送第一个请求

### 1. 创建项目目录结构

在 `C:\Users\xiaow\Desktop\软件测试项目\接口自动化\api-auto-project\` 下创建：

```
api-auto-project/
├── api-server/         # API 服务器（已建好）
└── api-test/           # 我们要写的自动化测试代码（新建）
    ├── testcases/       # 测试用例文件夹
    ├── conftest.py      # pytest 配置文件
    └── pytest.ini       # pytest 配置文件
```

先创建目录：

```bash
cd C:\Users\xiaow\Desktop\软件测试项目\接口自动化\api-auto-project
mkdir api-test
cd api-test
mkdir testcases
```

### 2. 安装 Python 依赖

在 `api-test` 目录下创建一个 `requirements.txt` 文件，内容如下：

项目根目录的 `requirements.txt`（仓库里已经建好，不需要在 `api-test/` 下另建）实际内容：

```
requests>=2.31.0
pytest>=8.0.0
PyYAML>=6.0
allure-pytest>=2.13.0
```

> 版本用 `>=` 而不是 `==`：练习项目不锁死小版本，避免换机器时因版本过旧装不上。生产项目通常锁 `==` 保证环境一致——两种策略都可以，面试时能说清取舍即可。

然后安装：

```bash
pip install -r requirements.txt
```

> **代码解释**：`requirements.txt` 是 Python 项目的"清单文件"，写明了项目依赖哪些第三方库。`pip install` 会读取这个文件并自动下载安装。`==2.31.0` 表示指定版本号，避免版本不一致导致问题。

### 3. 第一个脚本：发请求 + 打印结果

在 `api-test` 目录下创建一个文件 `first_request.py`：

```python
# first_request.py
# 第一个接口自动化脚本 —— 发送请求并查看结果

# 导入 requests 库，用来发送 HTTP 请求
import requests

# 定义接口地址
url = "http://localhost:3000/api/login"

# 定义请求参数（Python 字典格式）
# 字典就是 {"key": "value"} 这样一对一对的数据
payload = {
    "username": "admin",
    "password": "admin123"
}

# 发送 POST 请求
# requests.post() 就是发 POST 请求
# url= 指定地址，json= 指定请求体（自动转成 JSON 格式）
response = requests.post(url=url, json=payload)

# 打印响应内容
# response 是服务器返回的"响应对象"
# response.status_code 是 HTTP 状态码（200 表示成功）
# response.json() 是把返回的 JSON 字符串转成 Python 字典
print("状态码:", response.status_code)
print("返回数据:", response.json())
```

> **逐行解释**：
> - `import requests` → 引入 requests 库，有了它才能发 HTTP 请求
> - `url = "..."` → 定义变量 `url`，存接口地址
> - `payload = {...}` → 定义变量 `payload`（载荷），存要发给服务器的数据
> - `requests.post(url=url, json=payload)` → 用 POST 方法把数据发给服务器
> - `response.status_code` → 服务器返回的 HTTP 状态码，200=成功，404=找不到，500=服务器挂了
> - `response.json()` → 把服务器返回的 JSON 字符串解析成 Python 能操作的数据

运行这个脚本：

```bash
cd C:\Users\xiaow\Desktop\软件测试项目\接口自动化\api-auto-project\api-test
python first_request.py
```

**你看到的输出应该是：**

```
状态码: 200
返回数据: {'code': 0, 'message': '登录成功', 'data': {'token': 'xxx...', 'user': {...}}}
```

### 4. 第二个脚本：获取任务列表（GET 请求）

创建一个文件 `get_tasks.py`：

```python
# get_tasks.py
# 演示 GET 请求 + 带 token 的认证

import requests

# 🅰 第一步：先登录，拿到 token
# 因为获取任务列表需要登录后才能访问
login_url = "http://localhost:3000/api/login"
login_data = {
    "username": "admin",
    "password": "admin123"
}

# 发登录请求
login_resp = requests.post(url=login_url, json=login_data)

# 从登录返回的数据中，提取 token
# response.json() 返回的是字典
# 我们一层一层取数据：data → token
token = login_resp.json()["data"]["token"]
print("获取到 token:", token[:20] + "...")


# 🅱 第二步：用 token 获取任务列表
# 在 HTTP 请求的 headers（请求头）中带上 token
# 服务器通过 Authorization 字段来验证身份
tasks_url = "http://localhost:3000/api/tasks"

# 构建请求头
# headers 是一个字典，用来放"元数据"
# Bearer 是固定的前缀，后面跟 token
headers = {
    "Authorization": "Bearer " + token
}

# 发送 GET 请求
# params 用来传 URL 中的查询参数，比如 ?status=done&page=1
# 这里我们传了分页参数 page=1，每页 pageSize=3 条
params = {
    "page": 1,
    "pageSize": 3
}

tasks_resp = requests.get(url=tasks_url, headers=headers, params=params)

print("状态码:", tasks_resp.status_code)
print("返回数据:", tasks_resp.json())
```

> **逐行解释**：
> - `login_resp.json()["data"]["token"]` → 从登录返回中一层层提取 token。返回数据格式是 `{code:0, data:{token:"...", user:{...}}}`，所以要先取 `data`，再从 `data` 里取 `token`
> - `headers = {"Authorization": "Bearer " + token}` → 构建认证头。`Bearer` 是一种认证方式，意思是"持有者令牌"，后面跟具体的 token 字符串
> - `requests.get(url=..., headers=..., params=...)` → GET 请求比 POST 多了个 `params`，用来放 URL 问号后面的参数（如 `?page=1&pageSize=3`）

---

## 🎤 面试题

**Q1：GET 和 POST 有什么区别？**

> 回答要点：GET 用来获取数据，参数写在 URL 里（如 `?page=1`）；POST 用来提交数据，参数写在请求体里。GET 是幂等的（多次请求结果一样），POST 不是。GET 有长度限制，POST 没有。

**Q2：HTTP 状态码 200、201、400、401、404、500 分别表示什么？**

> - 200：请求成功
> - 201：创建成功（通常 POST 请求返回）
> - 400：请求参数有误（服务器不知道你要什么）
> - 401：未认证/认证失败（你没登录或 token 过期）
> - 404：资源不存在（接口地址写错了）
> - 500：服务器内部错误（服务器崩溃了）

**Q3：token 是什么？为什么要用 token？**

> 回答要点：token 是服务器发给客户端的"身份令牌"，客户端每次请求都带上它证明身份。相比用户名密码每次都要传，token 更安全，而且可以设置过期时间，过期后客户端需要重新登录获取新 token。

---

# Day 2：pytest 基础 + 测试用例结构

## 📖 知识点

### 什么是 pytest？

pytest 是 Python 最流行的测试框架，用来：
1. **组织测试用例**：自动找到以 `test_` 开头的函数或文件
2. **断言判断**：用 `assert` 关键字判断结果对不对
3. **生成报告**：输出谁通过了、谁失败了

### pytest 的规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 文件名 | 必须以 `test_` 开头或 `_test` 结尾 | `test_login.py` |
| 函数名 | 必须以 `test_` 开头 | `def test_login_success():` |
| 类名 | 必须以 `Test` 开头 | `class TestLogin:` |
| 断言 | 用 `assert` 加判断条件 | `assert code == 0` |

---

## 💻 动手：第一个 pytest 测试用例

### 1. 创建测试文件

在 `api-test/testcases/` 下创建 `test_login.py`（**【教学中间版】**，Day 4 会改造成 YAML 数据驱动）：

```python
# testcases/test_login.py
# 测试登录接口 —— 第一个 pytest 测试用例

import requests

# 定义一个测试函数
# 函数名必须以 test_ 开头，pytest 会自动找到它
def test_login_success():
    """测试登录成功"""
    
    # 1. 准备测试数据
    url = "http://localhost:3000/api/login"
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    
    # 2. 发送请求
    response = requests.post(url=url, json=payload)
    
    # 3. 获取返回数据
    resp_data = response.json()
    
    # 4. 断言 —— 判断结果对不对
    # assert 是 Python 关键字，后面跟 True 或 False
    # 如果 assert 后面的结果是 False，测试失败
    assert response.status_code == 200  # 状态码应该是200
    assert resp_data["code"] == 0       # 业务code应该是0（0代表成功）
    assert resp_data["message"] == "登录成功"  # 消息应该是"登录成功"
    assert "token" in resp_data["data"] # 返回数据中应该包含 token


def test_login_wrong_password():
    """测试密码错误"""
    
    url = "http://localhost:3000/api/login"
    payload = {
        "username": "admin",
        "password": "wrong_password"  # 故意输错密码
    }
    
    response = requests.post(url=url, json=payload)
    resp_data = response.json()
    
    # 密码错误时，code 应该是 400（业务错误码）
    assert response.status_code == 400
    assert resp_data["code"] == 400
    assert resp_data["message"] == "用户名或密码错误"


def test_login_no_username():
    """测试用户名为空"""
    
    url = "http://localhost:3000/api/login"
    # 只传密码，不传用户名
    payload = {
        "password": "admin123"
    }
    
    response = requests.post(url=url, json=payload)
    resp_data = response.json()
    
    assert response.status_code == 400
    assert resp_data["message"] == "用户名不能为空"
```

> **代码解释——assert 断言**：
> - `assert` 后面跟一个判断条件，条件为真就通过，为假就报错
> - `assert 1 == 1` → 通过 ✅
> - `assert 1 == 2` → 失败 ❌（会报 `AssertionError`）
> - 测试中，我们用 assert 来验证"服务器返回的结果是否符合预期"

### 2. 运行测试

打开终端，在 `api-test` 目录下运行：

```bash
cd C:\Users\xiaow\Desktop\软件测试项目\接口自动化\api-auto-project\api-test
python -m pytest testcases/test_login.py -v
```

> **命令解释**：
> - `python -m pytest` → 用 Python 运行 pytest
> - `testcases/test_login.py` → 指定要运行哪个测试文件
> - `-v` → verbose 模式，会显示更详细的输出信息

**期望输出：**

```
============================= test session starts =============================
collected 3 items

testcases/test_login.py::test_login_success PASSED                      [ 33%]
testcases/test_login.py::test_login_wrong_password PASSED               [ 66%]
testcases/test_login.py::test_login_no_username PASSED                  [100%]

============================== 3 passed in 0.12s ==============================
```

如果某一个失败了，它会显示具体的失败信息和行号，方便你定位问题。

### 3. 生成 HTML 测试报告

```bash
python -m pytest testcases/test_login.py -v --html=report.html
```

> `--html=report.html` 需要先装 `pytest-html`，它**不在项目 `requirements.txt` 里**（想试这条命令就 `pip install pytest-html`）。项目最终用的是 Allure 报告，见 Day 6。

---

## 🎤 面试题

**Q4：你用 pytest 做接口自动化，怎么组织测试用例的？**

> 回答思路：按接口模块分文件，一个文件测试一个接口的多种场景。比如 `test_login.py` 里放登录相关的用例（成功、密码错误、账号不存在、参数为空等），`test_tasks.py` 里放任务相关的用例。

**Q5：pytest 中的 assert 和 unittest 中的 assertEqual 有什么区别？**

> 回答要点：pytest 的 assert 是 Python 内置关键字，更简洁；unittest 的 `assertEqual(a, b)` 需要从父类继承方法。pytest 的 assert 失败时会有更详细的上下文信息，比如实际值和期望值对比。

**Q6：如何只运行部分测试用例？**

> - 按文件名运行：`pytest test_login.py`
> - 按关键字运行：`pytest -k "login"`
> - 按标记运行：`pytest -m smoke`（需要先给用例加 `@pytest.mark.smoke` 装饰器）

---

# Day 3：接口关联 + token 处理

## 📖 知识点

### 什么是接口关联？

接口关联就是：**A 接口的返回值，作为 B 接口的入参**。

最常见的例子就是 token：
1. 登录接口返回 token
2. 后面的所有接口都需要这个 token

### 为什么需要统一处理 token？

如果每个测试函数都先调登录再取 token，代码会非常重复。我们需要一个**通用的机制**：
- 每个用例运行前，自动登录并获取 token
- token 自动加到每个请求的 header 里

pytest 的 **fixture** 可以解决这个问题。

### 什么是 fixture？

fixture 是 pytest 的"预处理机制"，可以理解为：
- **在每个测试用例执行之前**，先执行一段代码
- 把这段代码的结果**自动传给测试用例**用

> 可以把它想象成一个"自动准备工具"——你要用什么东西，fixture 提前帮你准备好，你直接用就行。

常见的 fixture 用途：
- 准备测试数据
- 登录获取 token
- 连接数据库
- 清理测试环境

---

## 💻 动手：用 fixture 统一管理 token

### 1. 创建 conftest.py（【教学中间版】）

> 这一步先手写 `get_token` fixture，把"登录一次、全程复用"的思路跑通；Day 4 引入分层封装后，它会改成调用 `api/login_api.py` 的 `login_setup`，那才是仓库最终版。

在 `api-test` 目录下创建 `conftest.py`：

```python
# conftest.py
# pytest 的配置文件
# 这个文件里的 fixture 可以被所有测试文件共享使用
# 不需要 import，pytest 会自动找到它

import pytest
import requests


# @pytest.fixture 是一个"装饰器"，告诉 pytest 下面的函数是一个 fixture
@pytest.fixture()
def get_token():
    """
    登录并获取 token
    这个 fixture 会在需要它的测试用例执行前自动运行
    yield 后面的值会传给测试用例使用
    """
    # ★ 第一步：发送登录请求
    url = "http://localhost:3000/api/login"
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(url=url, json=payload)
    
    # 从返回数据中提取 token
    token = response.json()["data"]["token"]
    
    print("\n[conftest] 获取到 token，准备给测试用例使用")
    
    # ★ 第二步：通过 yield 把 token 传给测试用例
    # yield 就像 return，但更强大
    # yield 之前的代码在测试前执行
    # yield 把值传给测试用例
    # yield 之后的代码在测试后执行（用于清理）
    yield token
    
    print("\n[conftest] 测试用例执行完毕，清理工作")
```

> **逐行解释**：
> - `@pytest.fixture()` → 固定写法，把下面的函数声明为 fixture
> - `def get_token():` → fixture 的名称，测试用例通过这个名称来引用它
> - `yield token` → 把 token 返回给测试用例使用。`yield` 和 `return` 的区别是：`yield` 之后还可以继续执行清理代码
> - 测试用例引用 fixture 时，只需要在参数中写上 fixture 的名字就行

### 2. 使用 fixture 的测试用例（【教学中间版】）

在 `testcases/` 下创建 `test_tasks_with_fixture.py`（**【教学中间版】**，仅用于演示 fixture，最终仓库里没有这个文件；它的职责后来由 `api/` 层 + `login_setup` 承担）：

```python
# testcases/test_tasks_with_fixture.py
# 演示如何使用 fixture 获取 token

import requests


def test_get_tasks(get_token):
    """
    获取任务列表
    参数中的 get_token 就是从 conftest.py 中拿到的 fixture
    """
    # ★ fixture 返回的 token 可以直接用
    token = get_token
    
    # 构建请求头，带上 token
    headers = {
        "Authorization": "Bearer " + token
    }
    
    # 发送请求获取任务列表
    url = "http://localhost:3000/api/tasks"
    response = requests.get(url=url, headers=headers)
    resp_data = response.json()
    
    # 断言
    assert response.status_code == 200
    assert resp_data["code"] == 0
    assert "list" in resp_data["data"]
    assert "total" in resp_data["data"]
    print(f"获取到 {resp_data['data']['total']} 个任务")


def test_create_task(get_token):
    """
    创建新任务
    同样使用了 get_token fixture
    """
    token = get_token
    
    headers = {
        "Authorization": "Bearer " + token
    }
    
    url = "http://localhost:3000/api/tasks"
    payload = {
        "title": "测试自动化创建的任务",
        "description": "这是通过自动化脚本创建的",
        "priority": "high",
        "status": "todo"
    }
    
    response = requests.post(url=url, json=payload, headers=headers)
    resp_data = response.json()
    
    assert response.status_code == 200
    assert resp_data["code"] == 0
    assert resp_data["data"]["title"] == "测试自动化创建的任务"
    
    print(f"创建任务成功，任务ID: {resp_data['data']['id']}")
```

运行测试：

```bash
cd C:\Users\xiaow\Desktop\软件测试项目\接口自动化\api-auto-project\api-test
python -m pytest testcases/test_tasks_with_fixture.py -v -s
```

> `-s` 参数让 print 的内容显示出来（默认 pytest 会隐藏 print 输出）

### 3. 认识 scope（fixture 的作用范围）

fixture 有个重要的参数叫 `scope`，控制 fixture 的执行次数：

```python
@pytest.fixture(scope="function")  # 默认，每个测试函数都执行一次
@pytest.fixture(scope="class")     # 每个测试类执行一次
@pytest.fixture(scope="module")    # 每个文件执行一次（一个 .py 文件就是一个 module）
@pytest.fixture(scope="session")   # 整个测试过程只执行一次
```

Token 获取适合用 `scope="session"`，因为 token 在 2 小时内有效，不需要每次都登录：

```python
# conftest.py
import pytest
import requests


# scope="session" 表示整个测试过程中，get_token 只执行一次
# 这样就不用每个用例都去登录一次了
@pytest.fixture(scope="session")
def get_token():
    """登录获取 token，整个测试只登录一次"""
    url = "http://localhost:3000/api/login"
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(url=url, json=payload)
    token = response.json()["data"]["token"]
    print("\n[conftest] 登录一次，获取 token")
    yield token
    print("\n[conftest] 所有测试结束")
```

> **scope 选择建议**：
> - 获取 token → 用 `session`（一次登录，全程使用）
> - 准备测试数据 → 用 `function`（每个用例需要独立数据）
> - 打开/关闭数据库连接 → 用 `session` 或 `module`

---

## 🎤 面试题

**Q7：说说你对 pytest fixture 的理解，它和 setup/teardown 有什么区别？**

> 回答要点：fixture 更灵活。fixture 可以：
> 1. **返回值**给测试用例用（setup 不能直接传递数据）
> 2. **控制作用范围**（scope 参数）
> 3. **自动清理**（yield 后面的代码做 teardown）
> 4. **依赖其他 fixture**（一个 fixture 可以引用另一个）

**Q8：接口关联你们是怎么做的？举个例子。**

> 回答要点：最常见的接口关联就是 token 传递。用 pytest 的 fixture 在 conftest.py 中统一处理，所有测试用例共享。其他场景比如"创建任务后拿到任务ID，再用它去查任务详情"，可以用变量保存，或者在 fixture 中封装好。

**Q9：token 过期了怎么办？**

> 回答思路：可以在 fixture 里加过期检测。如果请求返回 401（未授权），说明 token 过期了，这个时候自动重新登录获取新 token，然后重试失败的那个请求。这叫**token 自动刷新机制**。

---

# Day 4：数据驱动 + 分层封装

## 📖 知识点

### 什么是数据驱动？

**把测试数据和测试代码分开**。简单说就是：

- 代码里只写"怎么做"（发送请求、断言）
- 数据写在单独的文件里（用什么数据来测）

好处：
- 加一条用例只需要加数据，不需要改代码
- 数据可以用 Excel、YAML、JSON 等文件管理
- 非技术人员也能维护测试数据

### 什么是分层封装？

接口自动化的代码不要全写在一个文件里，要分三层：

```
┌─────────────────────────────────┐
│  第1层：用例层（tests/）          │  ← 只写"测什么"和"断言什么"
│  只调用封装的接口，写测试数据      │
├─────────────────────────────────┤
│  第2层：接口层（api/）             │  ← 只写"怎么调接口"
│  封装每个接口的 URL、参数、header   │
├─────────────────────────────────┤
│  第3层：工具层（utils/）           │  ← 写"通用工具"
│  读取文件、发送请求、处理 token     │
└─────────────────────────────────┘
```

**分层的好处**：如果接口 URL 变了，只需要改 api 层的一个地方；如果添加新用例，只需要在 tests 层加数据。

---

## 💻 动手：实现分层封装

### 创建项目结构

在 `api-test` 目录下创建以下文件和文件夹：

```
api-test/
├── testcases/         # 用例层
│   ├── test_login.py
│   └── test_tasks.py
├── api/               # 接口层（新建）
│   ├── __init__.py
│   ├── login_api.py
│   └── tasks_api.py
├── data/              # 测试数据（新建）
│   └── login_data.yaml
├── utils/             # 工具层（新建）
│   ├── __init__.py
│   └── requests_util.py
├── conftest.py
└── pytest.ini
```

> 注意：`__init__.py` 是空文件，告诉 Python 这个文件夹是一个"包"，可以被 import。

### 第一步：工具层——封装请求工具

**【仓库最终版】** `utils/requests_util.py`：

```python
# utils/requests_util.py
# 工具层：封装通用的请求方法
# 所有测试用例都通过这个工具发请求
# 统一处理：URL 拼接、超时、鉴权头、异常等

import os

import requests

# 被测服务地址：优先读环境变量 API_BASE_URL，默认本地 3000 端口
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")


class RequestsUtil:
    """
    请求工具类
    封装了 GET、POST、PUT、DELETE 等方法
    统一添加 base_url 和超时时间
    """

    def __init__(self, base_url=BASE_URL, timeout=10):
        self.base_url = base_url              # 被测服务地址
        self.headers = {
            "Content-Type": "application/json"
        }
        self.timeout = timeout                # 超过这个时间抛超时异常

    def set_token(self, token):
        """设置认证 token，之后所有请求自动带上 Authorization"""
        self.headers["Authorization"] = "Bearer " + token

    def get(self, url, params=None):
        return requests.get(
            url=self.base_url + url,
            headers=self.headers,
            params=params,
            timeout=self.timeout
        )

    def post(self, url, json=None):
        return requests.post(
            url=self.base_url + url,
            headers=self.headers,
            json=json,
            timeout=self.timeout
        )

    def put(self, url, json=None):
        return requests.put(
            url=self.base_url + url,
            headers=self.headers,
            json=json,
            timeout=self.timeout
        )

    def delete(self, url):
        return requests.delete(
            url=self.base_url + url,
            headers=self.headers,
            timeout=self.timeout
        )

    def upload(self, url, files=None, data=None):
        """文件上传：复制请求头并去掉 Content-Type

        不能带 application/json，否则 requests 不会自动生成
        multipart/form-data 的边界（boundary），服务端解析不了文件
        """
        upload_headers = self.headers.copy()
        upload_headers.pop("Content-Type", None)

        return requests.post(
            url=self.base_url + url,
            headers=upload_headers,
            files=files,
            data=data,
            timeout=self.timeout
        )


# 全局请求工具实例：其他地方 import 这个实例就能用
request_util = RequestsUtil()
```

> **逐行解释**：
> - `BASE_URL = os.getenv("API_BASE_URL", ...)` → 配置与代码分离：换环境只改环境变量，不改代码
> - `def __init__(self, base_url=BASE_URL, timeout=10):` → 默认值来自环境变量；测试里也可以 `RequestsUtil(base_url=...)` 临时指定（`test_exception.py` 就靠这个创建"不带 token"的独立实例）
> - `self.headers` → 对象的请求头，`set_token` 往这个字典里添加 `Authorization`
> - 每个方法统一 `url=self.base_url + url` + `timeout=self.timeout`，用例层永远不关心地址和超时
> - `upload()` → 单独处理文件上传：去掉 `Content-Type`，让 requests 自己生成 multipart 边界
> - `request_util = RequestsUtil()` → 全局实例，`api/` 层直接 import 使用

> 【教学中间版 → 最终版】的变化：`base_url` 从硬编码改为环境变量；参数名 `path`/`json_data` 改为 `url`/`json`（与 requests 保持一致）；新增 `upload()`；`__init__` 支持自定义 `base_url` 和 `timeout`。

### 第二步：接口层——封装每个接口

```python
# api/login_api.py
# 接口层：封装登录相关的接口
# 测试用例层调用这里的函数，不需要知道接口地址和格式

from utils.requests_util import request_util


def login(username, password):
    """
    登录接口
    参数：
        username: 用户名
        password: 密码
    返回：
        response 对象（包含状态码、返回数据等）
    """
    # 准备请求数据
    data = {
        "username": username,
        "password": password
    }
    
    # 调用工具层发 POST 请求
    # 路径 /api/login 会拼上 base_url 变成 http://localhost:3000/api/login
    response = request_util.post("/api/login", json=data)
    
    # ★ 如果登录成功，自动把 token 设置到工具类中
    # 这样后面调其他接口时就不用手动传 token 了
    if response.status_code == 200 and response.json().get("code") == 0:
        token = response.json()["data"]["token"]
        request_util.set_token(token)
        print("\n[login_api] 登录成功，token 已自动设置")
    
    return response


def register(username, password, nickname):
    """注册接口"""
    data = {
        "username": username,
        "password": password,
        "nickname": nickname
    }
    response = request_util.post("/api/user/register", json=data)
    return response
```

```python
# api/tasks_api.py
# 接口层：封装任务相关的接口

from utils.requests_util import request_util

def get_tasks(params=None):
    """获取任务列表
    params: 可选参数，如 {"status": "done", "page": 1}
    """
    response = request_util.get(url=f"/api/tasks", params=params)
    return response

def get_task_detail(task_id):
    """获取任务详情"""
    response = request_util.get(url=f"/api/tasks/{task_id}")
    return response

def create_task(title, description="", status="todo", priority="medium"):
    """创建任务"""
    data = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority
    }
    response = request_util.post(url=f"/api/tasks", json=data)
    return response

def update_task(task_id, update_data=None):
    """更新任务"""
    response = request_util.put(url=f"/api/tasks/{task_id}", json=update_data)
    return response

def delete_task(task_id):
    """删除任务"""
    response = request_util.delete(url=f"/api/tasks/{task_id}")
    return response

def batch_delete_tasks(task_ids):
    """批量删除任务
    task_ids: 任务ID列表，如 [1, 2, 3]
    """
    response = request_util.post(url=f"/api/tasks/batch", json={"ids": task_ids})
    return response
```

### 第三步：改造 conftest.py（使用封装后的工具）【仓库最终版】

```python
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
```

> `login()` 成功时会自动 `request_util.set_token(token)`，所以这个 session 级 fixture **不返回 token**，后续用例共用同一个全局实例，请求会自动带鉴权头。

### 第四步：改造测试用例层（简洁多了！）

**【仓库最终版】** `testcases/test_tasks.py`：

```python
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
        response = get_tasks()

        # 一行断言代替 3 行
        assert_success(response)

        # 验证返回数据的结构
        resp_data = response.json()
        assert isinstance(resp_data["data"]["list"], list), "list 应该是一个列表"
        assert isinstance(resp_data["data"]["total"], int), "total 应该是一个整数"

    def test_create_task_with_assert(self):
        """创建任务并使用字段断言"""
        response = create_task(title="测试断言封装", priority="high")

        assert_success(response)

        assert_field_equal(response, "data.title", "测试断言封装")
        assert_field_equal(response, "data.priority", "high")
        assert_field_equal(response, "data.status", "todo")

    def test_task_not_found(self):
        """测试查询不存在的任务"""
        response = get_task_detail(99999)
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

        # 3. 批量删除这两个任务
        resp_delete = batch_delete_tasks([task_id_a, task_id_b])
        assert_success(resp_delete)
        assert "成功删除 2 个任务" in resp_delete.json()["message"]

        # 4. 验证：再去查这两个任务，应该返回 404
        assert_status_code(get_task_detail(task_id_a), 404)
        assert_status_code(get_task_detail(task_id_b), 404)
```

> **代码解释——类的使用**：
> - `class TestTasksAdvanced:` → 把多个相关的测试函数组织在一起（类名必须 `Test` 开头）
> - `@pytest.mark.usefixtures("login_setup")` → 类级别的 fixture 声明，类里所有测试都共享这次登录
> - `self` → 类中方法的第一个参数，代表类的实例
> - **接口关联**：`test_batch_delete_tasks` 里先创建任务拿到 ID，再用 ID 去批量删除、查询详情——这就是"A 接口返回值作为 B 接口入参"的完整例子

### 第五步：数据驱动——用 YAML 文件管理测试数据

创建 `data/login_data.yaml`：

```yaml
# data/login_data.yaml
# 测试数据文件
# YAML 格式类似 Python 字典，用缩进表示层级

# 登录成功用例
login_success:
  username: "admin"
  password: "admin123"
  expect_code: 0
  expect_message: "登录成功"

# 密码错误
login_wrong_password:
  username: "admin"
  password: "wrong"
  expect_code: 400
  expect_message: "用户名或密码错误"

# 用户名为空
login_no_username:
  username: ""
  password: "admin123"
  expect_code: 400
  expect_message: "用户名不能为空"

# 密码为空
login_no_password:
  username: "admin"
  password: ""
  expect_code: 400
  expect_message: "密码不能为空"
```

> 仓库里的 `data/login_data.yaml` 就是这 **4 条**：登录成功、密码错误、用户名为空、密码为空。

创建读取 YAML 的工具：

```python
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
```

**【仓库最终版】** 使用数据驱动的登录测试 `testcases/test_login.py`：

```python
# testcases/test_login.py
# 登录接口测试：YAML 数据驱动 + pytest 参数化

import pytest

from api.login_api import login
from utils.data_util import read_yaml

# 从 YAML 读取测试数据
# 每个 key 是一组用例，字段：username / password / expect_code / expect_message
login_data = read_yaml("login_data.yaml")

# 把 YAML 字典转成参数化需要的列表：
# [ (用例名, 用户名, 密码, 期望状态码, 期望消息), ... ]
parametrize_data = [
    (
        case_name,
        case["username"],
        case["password"],
        case["expect_code"],
        case["expect_message"],
    )
    for case_name, case in login_data.items()
]


# 有多少组数据，这个用例就跑多少遍
@pytest.mark.parametrize(
    "case_name, username, password, expect_code, expect_message",
    parametrize_data,
    ids=[case[0] for case in parametrize_data],   # 用 YAML 里的用例名作为测试 ID
)
def test_login(case_name, username, password, expect_code, expect_message):
    """登录接口参数化测试：一组数据对应一条用例"""
    response = login(username, password)
    resp_data = response.json()

    assert resp_data["code"] == expect_code
    assert resp_data["message"] == expect_message
```

> **代码解释——参数化**：
> - `read_yaml()` 返回字典：`{"login_success": {...}, "login_wrong_password": {...}, ...}`
> - 列表推导式把字典转成"一行数据一个元组"，同时保留 `case_name` 作为用例 ID
> - `ids=[...]` 让报告显示 `test_login[login_wrong_password]`，而不是 `test_login[case1]`
> - 解析后共 **4 条**用例：`login_success` / `login_wrong_password` / `login_no_username` / `login_no_password`
> - 和【教学中间版】的硬编码列表相比：加用例只改 YAML，不动代码——这才是"数据驱动"的实际收益

---

## 🎤 面试题

**Q10：你们接口自动化框架是怎么分层的？每层负责什么？**

> 回答思路：三层架构——工具层（RequestsUtil，统一处理请求发送）、接口层（每个接口一个函数，封装URL和参数）、用例层（写测试数据和断言）。这样接口地址变了只改接口层，加新用例只改用例层。

**Q11：数据驱动的好处是什么？你们用什么存数据？**

> 回答要点：代码和数据分离，加用例不加代码；可以用 YAML/JSON/Excel 管理数据；非技术人员也能维护。面试中说出"我把几百条用例数据放在 YAML 里，用 pytest 的 parametrize 驱动执行"就很好了。

**Q12：你封装的请求工具类里，统一处理了哪些东西？**

> - base_url 统一拼接
> - headers 统一管理（token 自动设置）
> - 超时时间统一设置
> - 可以统一加日志、异常处理

---

# Day 5：异常场景 + 断言封装

## 📖 知识点

### 为什么要测异常场景？

接口测试不只是测"正常能不能通"，更要测**"异常情况下系统表现是否合理"**：

| 异常类型 | 测试点 | 预期 |
|---------|--------|------|
| 参数异常 | 少传参数、传 null、传超长字符串 | 返回 400 + 明确的提示信息 |
| 认证异常 | 不传 token、传假 token、token 过期 | 返回 401 |
| 超时异常 | 接口响应超过预期时间 | 不能一直卡死 |
| 服务器异常 | 服务器返回 500 | 不能暴露敏感信息 |

### 什么是断言封装？

断言封装就是：**把常用的断言逻辑写成函数，不用每次重复写3行代码**。

比如每次都要写：
```python
assert response.status_code == 200
assert resp_data["code"] == 0
assert resp_data["message"] == "成功"
```

可以封装成：
```python
assert_success(response)  # 一行搞定
```

---

## 💻 动手：异常测试 + 断言封装

### 1. 封装通用断言

创建 `utils/assert_util.py`：

```python
# utils/assert_util.py
# 工具层：封装通用的断言方法
# 让测试用例的断言部分更简洁

def assert_success(response):
    """
    通用断言：接口调用成功
    适用场景：正常业务场景
    验证：
        1. HTTP 状态码为 200
        2. 业务 code 为 0（代表业务成功）
    """
    resp_data = response.json()
    
    # 断言 HTTP 状态码
    assert response.status_code == 200, \
        f"HTTP 状态码异常，期望 200，实际 {response.status_code}"
    
    # 断言业务状态码
    assert resp_data["code"] == 0, \
        f"业务状态码异常，期望 0，实际 {resp_data['code']}，消息：{resp_data['message']}"


def assert_error(response, expect_code=400):
    """
    通用断言：接口返回业务错误
    适用场景：参数校验失败、业务逻辑错误
    验证：
        1. HTTP 状态码等于 expect_code（默认 400）
        2. 业务 code != 0
    """
    resp_data = response.json()
    
    assert response.status_code == expect_code, \
        f"HTTP 状态码异常，期望 {expect_code}，实际 {response.status_code}"
    
    # 业务 code 应该不等于 0（非成功状态）
    assert resp_data["code"] != 0, "期望业务失败，但 code 为 0"


def assert_status_code(response, expect_code):
    """
    断言 HTTP 状态码
    适用场景：需要验证特定状态码时
    """
    assert response.status_code == expect_code, \
        f"HTTP 状态码异常，期望 {expect_code}，实际 {response.status_code}"


def assert_field_equal(response, field_path, expect_value):
    """
    断言返回数据中某个字段的值等于期望值
    适用场景：验证某个具体字段的内容
    参数：
        response: 响应对象
        field_path: 字段路径，如 "data.title"
        expect_value: 期望值
    """
    resp_data = response.json()
    
    # 按点号分隔路径，逐层取值
    # 比如 field_path="data.title" → 先取 data，再取 title
    fields = field_path.split(".")
    value = resp_data
    for field in fields:
        value = value[field]
    
    assert value == expect_value, \
        f"字段 {field_path} 值异常，期望 {expect_value}，实际 {value}"
```

> **逐行解释**：
> - `\` → Python 中的行连接符，一行太长时换行用
> - `f"xxx {variable}"` → f-string，在字符串中嵌入变量的值
> - `field_path.split(".")` → 把 `"data.title"` 拆成 `["data", "title"]` 列表
> - `for field in fields: value = value[field]` → 循环取值：先取 `data`，再从 `data` 里取 `title`

### 2. 用封装后的断言改写测试用例

```python
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
        response = get_tasks()
        assert_success(response)

        resp_data = response.json()
        assert isinstance(resp_data["data"]["list"], list), "list 应该是一个列表"
        assert isinstance(resp_data["data"]["total"], int), "total 应该是一个整数"

    def test_create_task_with_assert(self):
        """创建任务并使用字段断言"""
        response = create_task(title="测试断言封装", priority="high")
        assert_success(response)

        assert_field_equal(response, "data.title", "测试断言封装")
        assert_field_equal(response, "data.priority", "high")
        assert_field_equal(response, "data.status", "todo")

    def test_task_not_found(self):
        """测试查询不存在的任务"""
        response = get_task_detail(99999)
        assert_status_code(response, 404)

    def test_batch_delete_tasks(self):
        """先创建两个任务，再批量删除它们"""
        resp_a = create_task(title="待批量删除-A")
        assert_success(resp_a)
        task_id_a = resp_a.json()["data"]["id"]

        resp_b = create_task(title="待批量删除-B")
        assert_success(resp_b)
        task_id_b = resp_b.json()["data"]["id"]

        resp_delete = batch_delete_tasks([task_id_a, task_id_b])
        assert_success(resp_delete)
        assert "成功删除 2 个任务" in resp_delete.json()["message"]

        assert_status_code(get_task_detail(task_id_a), 404)
        assert_status_code(get_task_detail(task_id_b), 404)
```

### 3. 异常场景测试

**【仓库最终版】** `testcases/test_exception.py`——用例里**不出现接口地址**，全部走工具层/接口层：

```python
# testcases/test_exception.py
# 异常场景测试：鉴权失败、参数校验失败、服务端错误

import pytest

from api.error_api import simulate_server_error
from api.tasks_api import create_task
from utils.assert_util import assert_error, assert_status_code
from utils.requests_util import RequestsUtil


class TestAuthException:
    """鉴权类异常：使用独立的请求实例，不带 token / 带伪造 token

    注意：全局 request_util 在会话登录后会自动带上真实 token，
    所以这里单独 new 一个实例，避免用例之间互相影响
    """

    def test_no_token(self):
        """不传 token 访问需要鉴权的接口，应返回 401"""
        client = RequestsUtil()
        response = client.get("/api/tasks")
        assert_status_code(response, 401)

    def test_fake_token(self):
        """使用伪造的 token，应返回 401"""
        client = RequestsUtil()
        client.set_token("fake_token_123")
        response = client.get("/api/tasks")
        assert_status_code(response, 401)


@pytest.mark.usefixtures("login_setup")
class TestParamException:
    """参数校验类异常：登录态由 session 级 fixture 提供"""

    def test_empty_title_create_task(self):
        """创建任务时标题为空，应返回 400"""
        response = create_task(title="")
        assert_error(response, 400)
        assert response.json()["message"] == "任务标题不能为空"

    def test_long_title(self):
        """标题超过 50 字符限制，应返回 400"""
        response = create_task(title="a" * 51)
        assert_error(response, 400)
        assert "50个字符" in response.json()["message"]

    def test_server_error(self):
        """模拟服务端 500 错误"""
        response = simulate_server_error()
        assert_status_code(response, 500)
```

> **比【教学中间版】改进的地方**：
> 1. 不再手写 `requests.post(..., headers=...)`，鉴权头由 `RequestsUtil` 统一管理
> 2. 鉴权异常和参数异常分成两个类：前者不能用全局 token，后者需要登录态，需求相反，混在一起必然互相影响
> 3. `simulate_server_error()` 收进 `api/error_api.py`，用例层不拼 URL

---

## 🎤 面试题

**Q13：接口自动化测试中，你通常会覆盖哪些异常场景？**

> 回答要点：1) 参数类异常（空值、超长、类型错误） 2) 认证类异常（无 token、假 token、过期 token） 3) 业务异常（数据不存在、重复提交） 4) 环境异常（超时、500 错误）

**Q14：断言封装你是怎么做的？**

> 回答思路：把常用的断言写成函数，比如 `assert_success(response)` 同时验证状态码 200 和业务 code 为 0，`assert_field_equal(response, "data.name", "期望值")` 验证某个字段。定义接口返回数据的结构（比如必须包含 code、message、data 三个字段）。

---

# Day 6：完整框架整合 + Allure 报告

## 📖 知识点

### 完整框架的结构

**【仓库最终版】** 完整结构：

```
api-auto-project/
├── api-server/                   # 被测系统（Node.js + Express）
│   ├── server.js                 # API 服务主程序（内存数据 + JWT 鉴权）
│   └── package.json              # 服务端依赖与 npm start
├── api-test/                     # 接口自动化测试框架
│   ├── conftest.py               # pytest 全局 fixture（session 级登录）
│   ├── pytest.ini                # pytest 配置
│   ├── utils/                    # 工具层
│   │   ├── __init__.py
│   │   ├── requests_util.py      # requests 二次封装（base_url / 超时 / token / 上传）
│   │   ├── data_util.py          # YAML 测试数据读取
│   │   └── assert_util.py        # 断言工具
│   ├── api/                      # 接口层
│   │   ├── __init__.py
│   │   ├── login_api.py          # 登录 / 注册
│   │   ├── tasks_api.py          # 任务增删改查 / 批量删除
│   │   ├── category_api.py       # 分类查询
│   │   ├── upload_api.py         # 文件上传
│   │   └── error_api.py          # 异常场景模拟（超时 / 500）
│   ├── data/
│   │   └── login_data.yaml       # 登录用例数据（4 条）
│   └── testcases/                # 用例层
│       ├── test_login.py         # 登录（参数化 4 条）
│       ├── test_tasks.py         # 任务管理（4 条）
│       ├── test_category.py      # 分类查询（1 条）
│       ├── test_upload.py        # 文件上传（1 条）
│       ├── test_exception.py     # 鉴权与参数校验异常（5 条）
│       ├── test_timeout.py       # 接口超时（1 条）
│       └── test_allure_demo.py   # Allure 报告演示（3 条）
├── requirements.txt              # 依赖清单（在项目根目录）
├── README.md
├── 项目解释文档.md
└── api-auto-learning-guide.md    # 本文档
```

**用例总数：19 条** = 16 个测试函数 + 登录模块参数化展开 4 条（其余 15 个函数各 1 条）。实测 `19 passed in 10.33s`。

> 注意 `test_timeout.py` 的用时：它故意让服务端延迟 15 秒（工具层 timeout=10 秒），所以跑全量时这 1 条就要占约 10 秒，属于预期行为。

### Allure 报告

Allure 是一个漂亮的测试报告工具，比 pytest-html 好看得多：

```
pytest-html 报告：表格形式，显示通过/失败/数量
Allure 报告：统计图 + 分类 + 步骤详情 + 失败截图
```

---

## 💻 动手：安装 Allure + 生成报告

### 1. 安装 Allure

**Windows 安装：**

推荐用 `scoop` 安装（如果没 scoop，也可以手动下载）：
```bash
scoop install allure
```

或者手动安装：
1. 去 https://github.com/allure-framework/allure2/releases 下载最新版
2. 解压到 `C:\allure`
3. 把 `C:\allure\bin` 加到系统环境变量 Path 中

**验证安装：**
```bash
allure --version
```

### 2. 安装 Python Allure 依赖

```bash
pip install allure-pytest
```

### 3. 给测试用例加 Allure 注解

```python
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
                name="响应数据",   # 显示的标题
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
```

### 4. 运行并生成 Allure 报告

```bash
cd C:\Users\xiaow\Desktop\软件测试项目\接口自动化\api-auto-project\api-test

# 第一步：运行测试，生成 Allure 数据（存到 allure-results 文件夹）
python -m pytest testcases/test_allure_demo.py --alluredir=allure-results

# 第二步：用 Allure 数据生成 HTML 报告并自动打开
allure serve allure-results
```

`allure serve` 命令会自动启动一个 Web 服务器，在浏览器中打开漂亮的报告页面。

### 5. 把常用命令做成脚本（可选练习，仓库里没有这个文件）

创建 `run.bat`（Windows 批处理文件）：

```bat
@echo off
:: run.bat
:: 自动化测试一键运行脚本

echo ====================================
echo  任务管理系统 - 接口自动化测试
echo ====================================

echo.
echo Step 1: 运行所有测试用例...
call python -m pytest testcases/ --alluredir=allure-results -v

echo.
echo Step 2: 生成 Allure 报告...
call allure serve allure-results

pause
```

双击 `run.bat` 就能一键运行全部测试并查看报告。

### 6. 仓库里的另外三个模块（上传 / 分类 / 超时）

除了上面按天讲解的主线，最终仓库还补齐了三类"框架能力"用例，代码都很短，建议对照看一遍：

```python
# api/upload_api.py —— 文件上传
from utils.requests_util import request_util

def upload_file(file_path):
    """file_path: 本地文件路径"""
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = request_util.upload("/api/upload", files=files)
    return response
```

```python
# testcases/test_upload.py —— 用 tmp_path 造临时文件，跑完自动清理
import pytest
from api.upload_api import upload_file
from utils.assert_util import assert_success


class TestUpload:

    @pytest.mark.usefixtures("login_setup")
    def test_upload_file(self, tmp_path):
        """上传一个文本文件"""
        file_path = tmp_path / "test_upload.txt"
        file_path.write_text("这是测试上传的文件内容", encoding="utf-8")

        response = upload_file(str(file_path))
        assert_success(response)

        resp_data = response.json()["data"]
        assert resp_data["originalname"] == "test_upload.txt"
        assert resp_data["size"] > 0
        assert "/uploads/" in resp_data["url"]
```

```python
# api/category_api.py —— 分类查询（不需要登录）
from utils.requests_util import request_util

def get_categories():
    response = request_util.get("/api/categories")
    return response


# testcases/test_category.py
from utils.assert_util import assert_success

class TestCategory:

    def test_get_categories(self):
        response = get_categories()
        assert_success(response)
        assert len(response.json()["data"]) > 0
```

```python
# api/error_api.py —— 超时 / 500 两个异常接口
from utils.requests_util import request_util

def simulate_timeout(delay=15):
    """delay 需大于工具层 timeout=10，才会触发超时"""
    return request_util.post("/api/error/timeout", json={"delay": delay})

def simulate_server_error():
    return request_util.get("/api/error/server-error")


# testcases/test_timeout.py —— 断言"抛出 Timeout 异常"而不是断言返回值
import pytest
import requests

from api.error_api import simulate_timeout

class TestTimeout:
    @pytest.mark.usefixtures("login_setup")
    def test_timeout(self):
        with pytest.raises(requests.exceptions.Timeout):
            simulate_timeout(delay=15)
```

> 这三个模块对应面试里的三类问题：**文件上传**（multipart 边界、`tmp_path` 数据隔离）、**公开接口 vs 鉴权接口**、**超时异常**（`pytest.raises` 断言异常，而不是断言状态码）。

---

## 🎤 面试题

**Q15：描述一下你搭建的接口自动化框架的整体架构。**

> 回答思路（可以照着这个说）：
> "我用的是 pytest + requests + allure 搭建的接口自动化框架，采用三层架构：
> 1. **工具层**：封装了 RequestsUtil 统一处理 base_url 拼接、header 管理、超时设置
> 2. **接口层**：每个接口封装成一个函数，对外暴露业务方法名（如 `login()`、`create_task()`）
> 3. **用例层**：用 pytest 组织测试用例，数据驱动用 parametrize + YAML 文件
> 4. **报告层**：用 Allure 生成测试报告，有步骤详情和统计数据

**Q16：为什么选择 pytest 而不是 unittest？**

> 回答要点：pytest 更简洁（assert 原生关键字）、fixture 机制灵活、参数化方便、插件生态好（allure、html 报告）、支持 conftest.py 共享配置。

**Q17：接口自动化的 ROI（投入产出比）你怎么看？哪些接口值得自动化？**

> 回答思路：核心业务接口、频繁回归的接口、需要跨版本稳定的接口值得自动化。经常变动的接口、一次性使用的接口不值得。做之前先分析"这个接口我一个月要回归几次"。

---

# 面试高频题汇总

## 基础理论题

| 题目 | 核心考点 |
|------|---------|
| HTTP 中 GET 和 POST 的区别 | 幂等性、参数位置、安全性、长度限制 |
| 常见的 HTTP 状态码及含义 | 200/201/301/400/401/403/404/500/502/503 |
| RESTful 接口规范是什么 | URL 是资源、用 HTTP 方法表示动作、无状态 |
| Cookie、Session、Token 的区别 | 存的位置、安全性、跨域支持 |

## 框架设计题

| 题目 | 核心考点 |
|------|---------|
| 你的接口自动化框架怎么分层 | 工具层/接口层/用例层 |
| 怎么处理接口依赖（接口关联） | fixture 实现 token 共享 |
| 怎么实现数据驱动 | YAML + parametrize |
| token 过期怎么处理 | 自动刷新 + 重试机制 |
| 接口异常场景怎么处理 | 超时设置、状态码验证、异常断言 |

## 场景题

| 题目 | 考查方向 |
|------|---------|
| 如何测试一个登录接口 | 用例设计思维 |
| 如何测试一个支付接口 | 数据一致性、幂等性 |
| 如何测试一个文件上传接口 | 文件类型/大小/并发/限速 |
| 如何保证接口自动化稳定性 | 数据隔离、环境治理、重试机制 |

---

> **面试小技巧**：面试官问"接口自动化"时，他们真正想听的是：
> 1. 你**真的动手做过**，不只是看过文档
> 2. 你**知道为什么**要这么做，不只是知道怎么做
> 3. 你**踩过坑并有解决方案**，不只是照着教程敲了一遍
>
> 回答时多用自己的项目经历说话，比如"我在做这个项目时遇到过 xxx 问题，后来通过 xxx 解决了"，比背概念更有说服力。

---

## 下一步建议

学完这 6 天的内容后，你可以：

1. **扩展项目**：给这个 API 服务器加新接口，然后写对应的自动化用例
2. **加 CI/CD**：用 GitHub Actions 或 Jenkins 自动跑测试
3. **加性能测试**：用 JMeter 或 Locust 对同样的接口做压测
4. **加日志收集**：把失败信息记录到日志文件，方便排查

---

需要我帮你做什么？比如：
- 带你走某一天的动手练习？
- 模拟面试考你接口自动化的题？
- 讲解某个你没看懂的部分？
