/**
 * 任务管理系统 API 服务器
 * 接口自动化学习练手项目
 *
 * 功能：用户管理、任务 CRUD、分类管理、文件上传
 * 端口：3000
 */

const express = require('express');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const multer = require('multer');
const path = require('path');

const app = express();
const PORT = 3000;
const SECRET_KEY = 'api-auto-study-2024';

// ===================== 中间件 =====================
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// ===================== 模拟数据库（存在内存中） =====================
let users = [
  { id: 1, username: 'admin', password: 'admin123', role: 'admin', nickname: '管理员' },
  { id: 2, username: 'tester', password: 'tester123', role: 'tester', nickname: '测试员' },
  { id: 3, username: 'zhangsan', password: '123456', role: 'tester', nickname: '张三' }
];

let tasks = [
  { id: 1, title: '完成登录模块测试', description: '包括功能测试和接口测试', status: 'done', priority: 'high', categoryId: 1, createTime: '2024-01-10 10:00:00', userId: 2 },
  { id: 2, title: '编写自动化测试用例', description: '使用 pytest 框架', status: 'doing', priority: 'high', categoryId: 2, createTime: '2024-01-11 14:30:00', userId: 1 },
  { id: 3, title: '性能测试摸底', description: '对核心接口做压力测试', status: 'todo', priority: 'medium', categoryId: 3, createTime: '2024-01-12 09:00:00', userId: 2 },
  { id: 4, title: '提交缺陷报告', description: '汇总本周发现的bug', status: 'todo', priority: 'low', categoryId: 1, createTime: '2024-01-13 16:00:00', userId: 1 },
  { id: 5, title: '部署测试环境', description: '更新测试服务器代码', status: 'done', priority: 'medium', categoryId: 2, createTime: '2024-01-14 11:00:00', userId: 1 }
];

let categories = [
  { id: 1, name: '功能测试', description: '功能相关的任务' },
  { id: 2, name: '自动化', description: '自动化相关的任务' },
  { id: 3, name: '性能测试', description: '性能相关的任务' }
];

let nextUserId = 4;
let nextTaskId = 6;
let nextCategoryId = 4;

// ===================== 文件上传配置 =====================
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, 'uploads'));
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});
// 限制文件大小 5MB
const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }
});

// 确保 uploads 目录存在
const fs = require('fs');
if (!fs.existsSync(path.join(__dirname, 'uploads'))) {
  fs.mkdirSync(path.join(__dirname, 'uploads'));
}

// ===================== 认证中间件 =====================
function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ code: 401, message: '未提供认证信息' });
  }

  // 支持 Bearer token 格式
  const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : authHeader;

  try {
    const decoded = jwt.verify(token, SECRET_KEY);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ code: 401, message: 'token 无效或已过期' });
  }
}

// ===================== 用户接口 =====================

/**
 * POST /api/login
 * 用户登录
 * 参数: { username, password }
 * 返回: { code, message, token, user }
 */
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  // 参数校验
  if (!username) {
    return res.status(400).json({ code: 400, message: '用户名不能为空' });
  }
  if (!password) {
    return res.status(400).json({ code: 400, message: '密码不能为空' });
  }

  // 查找用户
  const user = users.find(u => u.username === username);
  if (!user) {
    return res.status(400).json({ code: 400, message: '用户名或密码错误' });
  }

  if (user.password !== password) {
    return res.status(400).json({ code: 400, message: '用户名或密码错误' });
  }

  // 生成 token，有效期 2 小时
  const token = jwt.sign(
    { userId: user.id, username: user.username, role: user.role },
    SECRET_KEY,
    { expiresIn: '2h' }
  );

  res.json({
    code: 0,
    message: '登录成功',
    data: {
      token: token,
      user: {
        id: user.id,
        username: user.username,
        nickname: user.nickname,
        role: user.role
      }
    }
  });
});

/**
 * GET /api/user/info
 * 获取当前用户信息（需要登录）
 */
app.get('/api/user/info', authMiddleware, (req, res) => {
  const user = users.find(u => u.id === req.user.userId);
  if (!user) {
    return res.status(404).json({ code: 404, message: '用户不存在' });
  }

  res.json({
    code: 0,
    message: 'ok',
    data: {
      id: user.id,
      username: user.username,
      nickname: user.nickname,
      role: user.role
    }
  });
});

/**
 * POST /api/user/register
 * 用户注册
 * 参数: { username, password, nickname }
 */
app.post('/api/user/register', (req, res) => {
  const { username, password, nickname } = req.body;

  // 校验必填字段
  if (!username || !password || !nickname) {
    return res.status(400).json({ code: 400, message: '用户名、密码、昵称不能为空' });
  }

  // 检查用户名长度（3-20位）
  if (username.length < 3 || username.length > 20) {
    return res.status(400).json({ code: 400, message: '用户名长度应在3-20位之间' });
  }

  // 检查密码长度（6-30位）
  if (password.length < 6 || password.length > 30) {
    return res.status(400).json({ code: 400, message: '密码长度应在6-30位之间' });
  }

  // 检查用户名是否已存在
  if (users.find(u => u.username === username)) {
    return res.status(400).json({ code: 400, message: '用户名已存在' });
  }

  const newUser = {
    id: nextUserId++,
    username,
    password,
    nickname,
    role: 'tester'
  };
  users.push(newUser);

  res.json({
    code: 0,
    message: '注册成功',
    data: { id: newUser.id, username: newUser.username, nickname: newUser.nickname }
  });
});

// ===================== 任务接口 =====================

/**
 * GET /api/tasks
 * 获取任务列表（需要登录）
 * 查询参数: status, priority, keyword（搜索标题）, page, pageSize, sortBy, sortOrder
 */
app.get('/api/tasks', authMiddleware, (req, res) => {
  const { status, priority, keyword, page = 1, pageSize = 10, sortBy = 'createTime', sortOrder = 'desc' } = req.query;

  let result = [...tasks];

  // 按状态筛选
  if (status) {
    result = result.filter(t => t.status === status);
  }

  // 按优先级筛选
  if (priority) {
    result = result.filter(t => t.priority === priority);
  }

  // 按标题关键词搜索
  if (keyword) {
    result = result.filter(t => t.title.includes(keyword));
  }

  // 排序
  result.sort((a, b) => {
    if (sortOrder === 'asc') {
      return a[sortBy] > b[sortBy] ? 1 : -1;
    } else {
      return a[sortBy] < b[sortBy] ? 1 : -1;
    }
  });

  // 分页
  const total = result.length;
  const start = (Number(page) - 1) * Number(pageSize);
  const end = start + Number(pageSize);
  const pageData = result.slice(start, end);

  res.json({
    code: 0,
    message: 'ok',
    data: {
      list: pageData,
      total: total,
      page: Number(page),
      pageSize: Number(pageSize)
    }
  });
});

/**
 * GET /api/tasks/:id
 * 获取任务详情（需要登录）
 */
app.get('/api/tasks/:id', authMiddleware, (req, res) => {
  const task = tasks.find(t => t.id === Number(req.params.id));
  if (!task) {
    return res.status(404).json({ code: 404, message: '任务不存在' });
  }
  res.json({ code: 0, message: 'ok', data: task });
});

/**
 * POST /api/tasks
 * 创建任务（需要登录）
 * 参数: { title, description, status, priority, categoryId }
 */
app.post('/api/tasks', authMiddleware, (req, res) => {
  const { title, description, status, priority, categoryId } = req.body;

  if (!title) {
    return res.status(400).json({ code: 400, message: '任务标题不能为空' });
  }
  if (title.length > 50) {
    return res.status(400).json({ code: 400, message: '任务标题不能超过50个字符' });
  }

  const newTask = {
    id: nextTaskId++,
    title,
    description: description || '',
    status: status || 'todo',
    priority: priority || 'medium',
    categoryId: categoryId || 1,
    createTime: new Date().toISOString().replace('T', ' ').slice(0, 19),
    userId: req.user.userId
  };
  tasks.push(newTask);

  res.json({ code: 0, message: '创建成功', data: newTask });
});

/**
 * PUT /api/tasks/:id
 * 更新任务（需要登录）
 */
app.put('/api/tasks/:id', authMiddleware, (req, res) => {
  const task = tasks.find(t => t.id === Number(req.params.id));
  if (!task) {
    return res.status(404).json({ code: 404, message: '任务不存在' });
  }

  const { title, description, status, priority, categoryId } = req.body;
  if (title !== undefined) task.title = title;
  if (description !== undefined) task.description = description;
  if (status !== undefined) task.status = status;
  if (priority !== undefined) task.priority = priority;
  if (categoryId !== undefined) task.categoryId = categoryId;

  res.json({ code: 0, message: '更新成功', data: task });
});

/**
 * DELETE /api/tasks/:id
 * 删除任务（需要登录）
 */
app.delete('/api/tasks/:id', authMiddleware, (req, res) => {
  const index = tasks.findIndex(t => t.id === Number(req.params.id));
  if (index === -1) {
    return res.status(404).json({ code: 404, message: '任务不存在' });
  }
  tasks.splice(index, 1);
  res.json({ code: 0, message: '删除成功' });
});

/**
 * POST /api/tasks/batch
 * 批量删除任务（需要登录）
 * 参数: { ids: [1, 2, 3] }
 */
app.post('/api/tasks/batch', authMiddleware, (req, res) => {
  const { ids } = req.body;
  if (!ids || !Array.isArray(ids) || ids.length === 0) {
    return res.status(400).json({ code: 400, message: '请提供要删除的任务ID列表' });
  }
  tasks = tasks.filter(t => !ids.includes(t.id));
  res.json({ code: 0, message: `成功删除 ${ids.length} 个任务` });
});

// ===================== 分类接口 =====================

/**
 * GET /api/categories
 * 获取分类列表
 */
app.get('/api/categories', (req, res) => {
  res.json({ code: 0, message: 'ok', data: categories });
});

/**
 * POST /api/categories
 * 创建分类
 * 参数: { name, description }
 */
app.post('/api/categories', (req, res) => {
  const { name, description } = req.body;
  if (!name) {
    return res.status(400).json({ code: 400, message: '分类名称不能为空' });
  }
  const newCategory = {
    id: nextCategoryId++,
    name,
    description: description || ''
  };
  categories.push(newCategory);
  res.json({ code: 0, message: '创建成功', data: newCategory });
});

// ===================== 文件上传接口 =====================

/**
 * POST /api/upload
 * 上传文件（需要登录）
 * 参数: file（multipart/form-data）
 */
app.post('/api/upload', authMiddleware, upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ code: 400, message: '请选择要上传的文件' });
  }
  res.json({
    code: 0,
    message: '上传成功',
    data: {
      filename: req.file.filename,
      originalname: req.file.originalname,
      size: req.file.size,
      url: `http://localhost:${PORT}/uploads/${req.file.filename}`
    }
  });
});

// ===================== 模拟错误接口（用于测试异常场景） =====================

/**
 * POST /api/error/timeout
 * 模拟超时（delay 参数指定秒数，默认5秒）
 */
app.post('/api/error/timeout', authMiddleware, (req, res) => {
  const delay = (req.body.delay || 5) * 1000;
  setTimeout(() => {
    res.json({ code: 0, message: '超时模拟结束', data: { waited: delay / 1000 + '秒' } });
  }, delay);
});

/**
 * GET /api/error/server-error
 * 模拟服务器500错误
 */
app.get('/api/error/server-error', (req, res) => {
  res.status(500).json({ code: 500, message: '服务器内部错误' });
});

// ===================== 启动服务器 =====================
app.listen(PORT, () => {
  console.log(`任务管理API已启动: http://localhost:${PORT}`);
  console.log('预置账号: admin / admin123  或  tester / tester123');
  console.log('按 Ctrl+C 停止服务器');
});
