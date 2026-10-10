# 接口自动化测试实战项目

从 0 到 1 学习接口自动化测试的完整项目，包含：被测系统（Node.js + Express 任务管理 API）+ 自动化测试框架（pytest + requests + 分层封装 + YAML 数据驱动 + Allure 报告）。

框架采用 **工具层 / 接口层 / 用例层** 三层分层设计：用例层只写业务断言，接口地址、鉴权头、超时等细节全部下沉到下层，新增用例不需要关心请求怎么发。

## 项目结构

```
api-auto-project/
├── api-server/                   # 被测系统（Node.js + Express）
│   ├── server.js                 # API 服务主程序（内存数据 + JWT 鉴权）
│   └── package.json              # 服务端依赖
├── api-test/                     # 接口自动化测试框架
│   ├── conftest.py               # pytest 全局 fixture（session 级登录）
│   ├── pytest.ini                # pytest 配置
│   ├── utils/                    # 工具层：与业务无关的能力封装
│   │   ├── requests_util.py      # requests 二次封装（统一 base_url / 超时 / 鉴权头）
│   │   ├── data_util.py          # YAML 测试数据读取
│   │   └── assert_util.py        # 断言工具
│   ├── api/                      # 接口层：按业务模块封装接口调用
│   │   ├── login_api.py          # 登录 / 注册
│   │   ├── tasks_api.py          # 任务增删改查 / 批量删除
│   │   ├── category_api.py       # 分类查询
│   │   ├── upload_api.py         # 文件上传
│   │   └── error_api.py          # 异常场景模拟（接口超时）
│   ├── data/
│   │   └── login_data.yaml       # 登录用例数据（YAML 数据驱动）
│   └── testcases/                # 用例层：只写断言，不写请求细节
│       ├── test_login.py         # 登录（参数化 4 条）
│       ├── test_tasks.py         # 任务管理（4 条）
│       ├── test_category.py      # 分类查询（1 条）
│       ├── test_upload.py        # 文件上传（1 条）
│       ├── test_exception.py     # 鉴权与参数校验异常（5 条）
│       ├── test_timeout.py       # 接口超时（1 条）
│       └── test_allure_demo.py   # Allure 报告演示（3 条）
├── requirements.txt
├── 项目解释文档.md                # 框架逐层讲解 + 基础 pytest 命令
└── api-auto-learning-guide.md    # 从 0 到 1 学习指南（每章配面试题）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动被测系统

```bash
cd api-server
npm install
node server.js
```

控制台输出 `任务管理API已启动: http://localhost:3000` 即为成功。

> 注意：服务端数据存放在内存中（预置 3 个用户、5 个任务、3 个分类），**重启进程后数据会重置**。上传的文件写入 `api-server/uploads/`。

### 3. 运行测试

```bash
cd api-test

# 运行全部用例
pytest

# 显示详细输出
pytest -v

# 运行单个模块
pytest testcases/test_login.py

# 只跑某个用例（参数化用例用测试 ID 筛选）
pytest testcases/test_login.py -k login_success
```

### 4. 生成 Allure 报告

```bash
# 安装 Python 插件
pip install allure-pytest

# 生成报告数据并打开（需要本机已安装 Allure 命令行工具）
pytest --alluredir=allure-results
allure serve allure-results
```

## 被测接口清单

服务端提供 14 个接口，统一响应格式：成功 `{code: 0, message, data}`，失败 `{code: 4xx/500, message}`。

| # | 方法 | 路径 | 作用 | 需 token |
|---|------|------|------|:---:|
| 1 | POST | `/api/login` | 登录，返回 token | - |
| 2 | GET | `/api/user/info` | 获取当前用户信息 | ✓ |
| 3 | POST | `/api/user/register` | 注册（用户名 3-20 位、密码 6-30 位、查重） | - |
| 4 | GET | `/api/tasks` | 任务列表，支持 status / priority / keyword / 分页 / 排序 | ✓ |
| 5 | GET | `/api/tasks/:id` | 任务详情 | ✓ |
| 6 | POST | `/api/tasks` | 创建任务（title 非空且 ≤ 50 字符） | ✓ |
| 7 | PUT | `/api/tasks/:id` | 更新任务 | ✓ |
| 8 | DELETE | `/api/tasks/:id` | 删除任务 | ✓ |
| 9 | POST | `/api/tasks/batch` | 批量删除 | ✓ |
| 10 | GET | `/api/categories` | 分类列表 | - |
| 11 | POST | `/api/categories` | 创建分类 | - |
| 12 | POST | `/api/upload` | 文件上传（multipart，字段名 `file`，限 5MB） | ✓ |
| 13 | POST | `/api/error/timeout` | 模拟超时 | ✓ |
| 14 | GET | `/api/error/server-error` | 模拟 500 错误 | - |

鉴权方式：JWT，token 有效期 2 小时，放在请求头 `Authorization: Bearer <token>`。

## 用例覆盖

总计 **19 条用例**（16 个测试函数，登录模块参数化展开 4 条）。

| 模块 | 正向 | 异常 | 边界 | 用例数 |
|------|:---:|:---:|:---:|:---:|
| 登录（test_login） | ✓ | ✓ | ✓ | 4 |
| 任务管理（test_tasks） | ✓ | ✓ | - | 4 |
| 分类查询（test_category） | ✓ | - | - | 1 |
| 文件上传（test_upload） | ✓ | - | - | 1 |
| 鉴权与参数异常（test_exception） | - | ✓ | ✓ | 5 |
| 接口超时（test_timeout） | - | ✓ | - | 1 |
| Allure 演示（test_allure_demo） | ✓ | ✓ | - | 3 |

覆盖的异常与边界场景：无 token / 伪造 token → 401、空 title → 400、title 超长（51 字符）→ 400、查询不存在的任务 → 404、接口延迟 → 连接超时。

## 覆盖的知识点

### requests 二次封装
- 统一 base_url、超时时间、默认请求头
- `set_token()` 一次设置，后续所有请求自动带上 `Authorization`
- 上传接口单独处理：复制请求头并移除 `Content-Type`，交给 requests 自动生成 multipart 边界

### 分层设计
- 工具层（`utils/`）与业务无关，可复用到其他项目
- 接口层（`api/`）按业务模块封装，一个函数对应一个接口
- 用例层（`testcases/`）只写数据和断言

### 数据驱动
- 测试数据放在 `data/login_data.yaml`，与代码分离
- `utils/data_util.py` 的 `read_yaml()` 读取 YAML
- `test_login.py` 用 `@pytest.mark.parametrize` 把数据铺开，一组数据一条用例

### pytest 进阶用法
- `conftest.py` 中 `scope="session"` 的 fixture `login_setup`：整个会话只登录一次，避免每条用例重复登录
- `@pytest.mark.usefixtures` 类级 / 方法级使用 fixture
- `pytest.raises` 断言异常类型
- `ids` 自定义参数化用例 ID，让报告可读

### Allure 报告
- `@allure.feature` / `@allure.story` / `@allure.title` 组织用例层级
- `with allure.step(...)` 让执行步骤可视化
- `allure.attach` 附加请求/响应数据，便于失败时定位

### 面试题索引

| 面试题 | 对应代码 |
|--------|----------|
| requests 二次封装怎么做 | `utils/requests_util.py` |
| 接口依赖（登录后的 token）怎么处理 | `api/login_api.py` 登录成功自动 `set_token`，`utils/requests_util.py` 统一带 token |
| 测试数据怎么管理 | `data/login_data.yaml` + `utils/data_util.py` |
| 参数化怎么用 | `testcases/test_login.py` |
| 框架分层怎么设计 | `utils/` → `api/` → `testcases/` 三层调用链 |
| 全局只登录一次怎么做 | `conftest.py` 的 session 级 fixture `login_setup` |
| 超时场景怎么测 | `testcases/test_timeout.py` + `api/error_api.py` |
| 文件上传怎么测 | `testcases/test_upload.py` + `utils/requests_util.py` 的 `upload()` |
| 断言怎么统一 | `utils/assert_util.py` |
| 测试报告怎么出 | `testcases/test_allure_demo.py` |

## 说明

本项目为个人学习实践项目，被测系统（`api-server/`）为配套编写的练习用服务，数据存于内存，仅供自动化测试练习使用。
