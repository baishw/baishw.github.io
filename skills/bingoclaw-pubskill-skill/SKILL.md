---
name: bingoclaw-pubskill-skill
version: 1.2.0
description: "发布技能到 SkillHub 系统：提取目标技能信息，通过 API 注册到技能管理系统，上传技能包到 baishw.github.io，返回技能分享页 URL。Use when user wants to publish a skill to SkillHub platform, including skill information extraction, API registration, package upload, and sharing URL generation."
homepage: https://gitee.com/baishw/bingoclaw-skills
metadata:
  {
    "openclaw": {
      "emoji": "🚀",
      "os": ["darwin", "linux", "win32"],
      "requires": {
        "bins": ["python3"],
        "env": ["SKILLHUB_API_URL", "GITHUB_TOKEN"]
      },
      "primaryEnv": "SKILLHUB_API_URL",
      "skillKey": "bingoclaw-pubskill-skill",
      "install": [
        {
          "id": "pip-requests",
          "kind": "pip",
          "package": "requests",
          "label": "Install Requests"
        },
        {
          "id": "pip-pyyaml",
          "kind": "pip",
          "package": "pyyaml",
          "label": "Install PyYAML"
        }
      ]
    }
  }
---

# PubSkill - 技能发布工具

PubSkill 是一个用于将技能发布到 SkillHub 系统的技能，支持技能信息提取、API 注册、技能包上传和分享链接生成。

## 使用场景

✅ **USE when:**
- 用户需要将开发完成的技能发布到 SkillHub 平台
- 用户需要通过 API 注册技能信息到技能管理系统
- 用户需要将技能包上传到 baishw.github.io 网站
- 用户需要获取技能分享页 URL 进行分享

❌ **DON'T use when:**
- 用户只想查询已发布的技能（使用 search 或 index API）
- 用户需要修改已发布的技能信息（使用 update API）
- 用户需要删除技能（使用 delete API）

## 快速开始

```bash
# 发布技能（从 SKILL.md 文件）
pubskill publish --skill-file ./myskill/SKILL.md

# 发布技能（从目录自动提取）
pubskill publish --skill-dir ./myskill

# 指定技能类型发布
pubskill publish --skill-dir ./myskill --type function

# 发布后验证
pubskill verify --skill-name myskill
```

## 功能详解

### 1. 技能信息提取

PubSkill 会自动从技能文件中提取以下信息：

**从 SKILL.md 提取：**
- `name`: 技能名称（唯一标识）
- `description`: 技能描述（用于 AI 理解）
- `metadata`: 元数据信息

**从目录结构提取：**
- 脚本文件（`scripts/`）
- 配置文件（`config/`）
- 文档文件（`docs/`）
- 资源文件（`assets/`）

**示例：**
```bash
pubskill extract --skill-dir ./myskill
```

**输出示例：**
```json
{
  "name": "myskill",
  "description": "技能描述",
  "type": "function",
  "version": "1.0.0",
  "params": {...},
  "returns": {...}
}
```

### 2. 技能注册（API）

通过 SkillHub API 将技能信息注册到技能管理系统。

**API 端点：**
```
POST {SKILLHUB_API_URL}/api/skill/create
```

**请求参数：**
```bash
pubskill register \
  --name myskill \
  --username baishw \
  --type function \
  --version 1.0.0 \
  --description "技能描述" \
  --summary "简短摘要"
```

**API 响应：**
```json
{
  "code": 1,
  "msg": "Skill created successfully",
  "time": 1699999999,
  "data": {
    "id": 1,
    "name": "myskill",
    "username": "baishw",
    "type": "function",
    "version": "1.0.0",
    "status": "normal"
  }
}
```

### 3. 技能包上传

将技能包上传到 baishw.github.io 网站。

**上传方式：**
- Git Push（推荐）
- GitHub API
- 直接上传

**Git Push 方式：**
```bash
pubskill upload --skill-dir ./myskill --repo baishw.github.io
```

**GitHub API 方式：**
```bash
pubskill upload \
  --skill-dir ./myskill \
  --github-api \
  --token $GITHUB_TOKEN
```

**上传结构：**
```
baishw.github.io/
└── skills/
    └── myskill/
        ├── SKILL.md
        ├── scripts/
        ├── config/
        └── README.md
```

### 4. 分享链接生成

生成技能分享页 URL。

**分享页格式：**
```
https://baishw.github.io/skills/{skill-name}/
```

**示例：**
```bash
pubskill share --skill-name myskill
```

**输出：**
```
✅ 技能发布成功！

技能名称：myskill
技能 ID: 1
分享链接：https://baishw.github.io/skills/myskill/
API 详情：{SKILLHUB_API_URL}/api/skill/detail?id=1
```

## 完整发布流程

### 方式一：一键发布

```bash
pubskill publish-all --skill-dir ./myskill
```

**自动执行：**
1. ✅ 提取技能信息
2. ✅ 验证技能配置
3. ✅ 注册到 SkillHub API
4. ✅ 上传到 GitHub
5. ✅ 生成分享链接

### 方式二：分步发布

**步骤 1：提取信息**
```bash
pubskill extract --skill-dir ./myskill --output skill-info.json
```

**步骤 2：验证信息**
```bash
pubskill verify --skill-info skill-info.json
```

**步骤 3：注册 API**
```bash
pubskill register --skill-info skill-info.json
```

**步骤 4：上传技能包**
```bash
pubskill upload --skill-dir ./myskill
```

**步骤 5：获取分享链接**
```bash
pubskill share --skill-name myskill
```

## 配置选项

### 环境变量

| 变量名 | 说明 | 必填 |
|---|---|---|
| `SKILLHUB_API_URL` | SkillHub API 基础 URL | 是 |
| `GITHUB_TOKEN` | GitHub Personal Access Token | 是 |
| `GITHUB_REPO` | GitHub 仓库名（默认 baishw.github.io） | 否 |
| `GITHUB_OWNER` | GitHub 用户名（默认 baishw） | 否 |

### 配置文件

创建 `.pubskill.json` 配置文件：

```json
{
  "api_url": "https://api.skillhub.example.com",
  "github": {
    "owner": "baishw",
    "repo": "baishw.github.io",
    "branch": "main"
  },
  "skill_path": "skills",
  "auto_verify": true,
  "auto_backup": true
}
```

## 技能类型说明

| 类型 | 说明 | 使用场景 |
|---|---|---|
| `function` | 函数 - 本地函数调用 | 工具函数、数据处理 |
| `api` | API 接口 - 外部 API 调用 | 第三方服务集成 |
| `database` | 数据库 - 数据库操作 | 数据查询、存储 |
| `workflow` | 工作流 - 自动化工作流 | 多步骤任务自动化 |

## 错误处理

| 错误类型 | 错误码 | 处理方式 |
|---|---|---|
| 技能已存在 | 1001 | 提示用户使用 update API 更新 |
| 技能信息不完整 | 1002 | 列出缺失字段并要求补充 |
| API 认证失败 | 2001 | 提示检查 API URL 和认证信息 |
| GitHub 上传失败 | 3001 | 提示检查 Token 权限和网络 |
| 技能验证失败 | 4001 | 显示验证错误详情 |

## 验证规则

PubSkill 会对技能进行以下验证：

**必填字段检查：**
- ✅ `name`: 技能名称（唯一标识）
- ✅ `username`: 提供者用户名
- ✅ `type`: 工具类型

**格式验证：**
- ✅ 名称格式：只允许字母、数字、下划线
- ✅ 版本号格式：语义化版本（x.y.z）
- ✅ 类型值：function/api/database/workflow

**内容验证：**
- ✅ SKILL.md 文件存在
- ✅ 目录结构完整
- ✅ 无敏感信息泄露

## 安全注意

⚠️ **重要提示：**
- GitHub Token 需要妥善保管，建议存储在环境变量中
- 不要将 Token 提交到代码仓库
- 发布前检查技能文件是否包含敏感信息
- 建议先发布到测试环境验证

## 示例：发布一个天气查询技能

**1. 准备技能文件**
```bash
mkdir weather-skill
cd weather-skill
# 创建 SKILL.md、scripts/、config/ 等文件
```

**2. 发布技能**
```bash
pubskill publish-all --skill-dir ./weather-skill
```

**3. 验证发布结果**
```bash
pubskill verify --skill-name weather-skill
```

**4. 分享技能**
```
✅ 技能发布成功！

技能名称：weather-skill
技能 ID: 42
分享链接：https://baishw.github.io/skills/weather-skill/
API 详情：https://api.skillhub.example.com/api/skill/detail?id=42
```

## 相关文件

- `scripts/main.py` - 核心业务逻辑脚本
- `scripts/api_client.py` - SkillHub API 客户端
- `scripts/github_client.py` - GitHub 上传客户端
- `scripts/extractor.py` - 技能信息提取器
- `scripts/validator.py` - 技能验证器

## 相关 API

- `POST /api/skill/create` - 创建技能
- `POST /api/skill/update` - 更新技能
- `POST /api/skill/delete` - 删除技能
- `GET /api/skill/detail` - 获取技能详情
- `GET /api/skill/search` - 搜索技能

## 常见问题

**Q: 发布失败提示"技能已存在"怎么办？**
A: 使用 update API 更新技能信息，或更换技能名称重新发布。

**Q: GitHub 上传失败怎么办？**
A: 检查 GITHUB_TOKEN 是否有效，确认有仓库写入权限。

**Q: 如何修改已发布的技能？**
A: 修改技能文件后，使用 `pubskill update` 命令重新发布。

**Q: 如何删除已发布的技能？**
A: 使用 `pubskill delete --skill-name <name>` 命令删除。
