# bingoclaw-pubskill-skill - 技能发布工具

bingoclaw-pubskill-skill 是一个用于将技能发布到 SkillHub 系统的工具。

## 功能

1. **技能信息提取** - 从技能目录和 SKILL.md 文件中自动提取技能信息
2. **技能注册** - 通过 SkillHub API 将技能注册到技能管理系统
3. **技能包上传** - 将技能包上传到 baishw.github.io 网站
4. **分享链接生成** - 为发布的技能生成分享页 URL

---

## 快速开始

### 1. 首次配置

首次使用时，只需配置你的 SkillHub 登录凭据：

```bash
# 复制配置示例
cp .pubskill.example.json .pubskill.json

# 编辑配置文件，填入你的用户名和密码
# github_token 等配置已预置，无需修改
```

### 2. 发布技能

```bash
# 发布技能（完整流程）
python scripts/main.py publish --skill-dir ./test_skill
```

---

## 配置说明

### 默认配置（已预置）

所有用户共享以下默认配置，无需修改：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `api_url` | `https://skill.cxus.cn` | SkillHub API 地址 |
| `github_token` | 已预置共享 Token | GitHub Personal Access Token |
| `github_owner` | `baishw` | GitHub 仓库所有者 |
| `github_repo` | `baishw.github.io` | GitHub 仓库名称 |
| `github_branch` | `main` | GitHub 分支 |
| `skill_path` | `skills` | 技能在仓库中的存储路径 |

### 必需配置（用户填写）

| 配置项 | 说明 | 环境变量 |
|--------|------|----------|
| `username` | 你的 SkillHub 用户名 | `SKILLHUB_USERNAME` |
| `password` | 你的 SkillHub 密码 | `SKILLHUB_PASSWORD` |

### 配置方式

**方式一：使用配置文件（推荐）**

```json
{
  "username": "your_skillhub_username",
  "password": "your_skillhub_password"
}
```

**方式二：使用环境变量**

```bash
export SKILLHUB_USERNAME="your_username"
export SKILLHUB_PASSWORD="your_password"
```

### 配置文件优先级

1. 环境变量（优先级最高）
2. `.pubskill.json` 配置文件
3. 默认值（优先级最低）

---

## 命令说明

### `extract` - 提取技能信息

```bash
python scripts/main.py extract --skill-dir <技能目录> [--output 输出文件]
```

**示例：**
```bash
python scripts/main.py extract --skill-dir ./test_skill --output skill-info.json
```

### `verify` - 验证技能信息

```bash
python scripts/main.py verify --skill-dir <技能目录>
# 或
python scripts/main.py verify --skill-info skill-info.json
```

### `register` - 注册技能到 API

```bash
python scripts/main.py register --skill-info skill-info.json
```

### `upload` - 上传技能包

```bash
python scripts/main.py upload --skill-dir <技能目录>
```

### `share` - 生成分享链接

```bash
python scripts/main.py share --skill-name <技能名称> [--skill-id 技能 ID]
```

### `publish` - 发布技能（完整流程）

```bash
python scripts/main.py publish --skill-dir <技能目录> [--skip-verify]
```

**完整流程：**
1. 提取技能信息
2. 验证技能配置
3. 注册到 SkillHub API
4. 上传到 GitHub
5. 生成分享链接

### `update` - 更新技能

```bash
python scripts/main.py update --skill-name <技能名称> [--skill-dir 技能目录]
```

### `delete` - 删除技能

```bash
python scripts/main.py delete --skill-name <技能名称>
```

---

## 技能目录结构

```
my-skill/
├── SKILL.md              # 技能定义文件（必需）
├── scripts/              # 脚本目录（必需）
│   ├── main.py          # 主脚本
│   └── ...
├── config/              # 配置目录（必需）
│   └── bingoclaw.json   # 技能配置文件
├── docs/                # 文档目录（可选）
│   └── README.md
└── assets/              # 资源目录（可选）
    └── ...
```

### SKILL.md 格式

```yaml
---
name: my-skill
type: function
version: 1.0.0
risk_level: low
description: 技能描述
---

技能详细文档...
```

### bingoclaw.json 格式

```json
{
  "type": "function",
  "version": "1.0.0",
  "name": "my-skill",
  "description": "技能描述",
  "risk_level": "low",
  "timeout": 30,
  "params": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "参数说明"
      }
    },
    "required": ["param1"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "result": {
        "type": "string",
        "description": "返回值说明"
      }
    }
  }
}
```

---

## 技能类型

| 类型 | 说明 |
|------|------|
| `function` | 函数：本地函数调用 |
| `api` | API 接口：外部 API 调用 |
| `database` | 数据库：数据库操作 |
| `workflow` | 工作流：自动化工作流 |

### 风险等级

| 等级 | 说明 |
|------|------|
| `low` | 低风险：无敏感操作 |
| `medium` | 中等风险：部分敏感操作 |
| `high` | 高风险：系统级操作 |

---

## 完整使用示例

### 示例 1：发布测试技能

```bash
# 1. 查看测试技能
ls -la test_skill/

# 2. 确保配置文件正确
cat .pubskill.json

# 3. 发布技能
python scripts/main.py publish --skill-dir ./test_skill
```

### 示例 2：分步发布

```bash
# 1. 提取技能信息
python scripts/main.py extract --skill-dir ./test_skill --output skill-info.json

# 2. 验证技能
python scripts/main.py verify --skill-info skill-info.json

# 3. 注册到 API
python scripts/main.py register --skill-info skill-info.json

# 4. 上传技能包
python scripts/main.py upload --skill-dir ./test_skill

# 5. 生成分享链接
python scripts/main.py share --skill-name test_skill --skill-id 16
```

### 示例 3：更新已发布的技能

```bash
# 修改技能文件...

# 更新技能
python scripts/main.py update --skill-name test_skill --skill-dir ./test_skill
```

---

## 相关 API

| 接口 | 方法 | 说明 | 认证 |
|------|------|------|------|
| `/api/user/login` | POST | 用户登录 | 无 |
| `/api/user/logout` | POST | 用户登出 | Token |
| `/api/skill/create` | POST | 创建技能 | Token |
| `/api/skill/update` | POST | 更新技能 | Token |
| `/api/skill/delete` | POST | 删除技能 | Token |
| `/api/skill/detail` | GET | 获取技能详情 | 无 |
| `/api/skill/search` | GET | 搜索技能 | 无 |

详细 API 文档请参考 [`docs/skill_api.md`](./docs/skill_api.md)

---

## 安全注意事项

- **`.pubskill.json` 已在 `.gitignore` 中**：不会提交到代码仓库
- **GitHub Token 已预置共享**：所有用户使用同一个，无需单独配置
- **敏感信息保护**：只要求用户配置 SkillHub 账号，其他配置已安全预置
- **发布前检查**：确保技能文件不包含敏感信息

---

## 错误处理

程序会输出详细的错误信息帮助排查问题：

| 错误类型 | 说明 |
|----------|------|
| 技能信息不完整 | 列出缺失字段 |
| 格式错误 | 说明正确的格式要求 |
| API 错误 | 显示 API 返回的错误信息 |
| GitHub 上传错误 | 提示检查 Token 权限和网络 |

---

## 项目结构

```
bingoclaw-pubskill-skill/
├── .pubskill.json          # 用户配置文件（不提交）
├── .pubskill.example.json   # 配置示例文件（可提交）
├── .gitignore              # Git 忽略配置
├── README.md               # 本文件
├── SKILL.md               # 技能定义
├── scripts/               # 脚本目录
│   ├── main.py           # 主程序入口
│   ├── api_client.py     # SkillHub API 客户端
│   ├── extractor.py      # 技能信息提取器
│   ├── validator.py      # 技能验证器
│   ├── github_client.py  # GitHub 上传客户端
│   └── test_api.py       # API 测试脚本
├── docs/                 # 文档目录
│   ├── skill_api.md     # API 文档
│   └── PUBLISH_REPORT.md # 发布记录
└── test_skill/           # 测试技能示例
    ├── SKILL.md
    ├── config/bingoclaw.json
    └── scripts/main.py
```

---

## 许可证

MIT License

---

## 更新日志

### v1.0.0 (2026-05-28)

- ✅ 简化配置流程，预置共享 Token
- ✅ 优化用户首次使用体验
- ✅ 完整的技能发布流程
- ✅ 支持技能创建、更新、删除
