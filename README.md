# ClassGradeDashboard
从零构建的班级成绩分析看板系统，基于 Python Flask + Vue 3 + ECharts

## 功能特性

### 数据管理
- 支持手动录入学生成绩（学生姓名、科目、分数）
- 支持通过 Excel 文件批量导入成绩数据
- 提供示例 Excel 模板下载

### 统计分析
- 按科目统计：平均分、最高分、最低分、及格率、优秀率（≥90 分）
- 按学生统计：总分排名
- 成绩分布直方图（按分数段 0-59/60-69/70-79/80-89/90-100）

### 可视化看板
- 首页展示全班概览卡片（总人数、平均分、及格率、优秀率）
- 各科目成绩对比柱状图（圆角+渐变效果）
- 分数段分布饼图
- 学生成绩排名表格（支持按科目排序和搜索，排名前三特殊高亮）

## 技术栈

- 后端：Python + Flask
- 前端：Vue 3 + ECharts + Element Plus
- 容器化：Docker + Docker Compose

## 快速启动

### 使用 Docker Compose（推荐）

```bash
# 一键启动
docker compose up

# 访问地址
# 前端：http://localhost:8080
# 后端：http://localhost:5000
```

### 项目结构

```
ClassGradeDashboard/
├── backend/              # 后端 Flask 应用
│   ├── app.py           # 主应用文件
│   ├── requirements.txt # Python 依赖
│   └── Dockerfile       # 后端 Docker 镜像
├── frontend-user/       # 前端 Vue 3 应用
│   ├── src/
│   │   ├── components/  # Vue 组件
│   │   ├── App.vue      # 根组件
│   │   └── main.js      # 入口文件
│   ├── package.json     # Node 依赖
│   ├── vite.config.js   # Vite 配置
│   └── Dockerfile       # 前端 Docker 镜像
└── docker-compose.yml   # Docker Compose 配置
```

