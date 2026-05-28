# PubSkill 快速启动指南

## 1 分钟快速开始

### 1. 安装依赖

```bash
cd pubskill
pip install requests pyyaml
```

### 2. 配置环境变量

```bash
export SKILLHUB_API_URL="https://api.skillhub.example.com"
export GITHUB_TOKEN="your_github_personal_access_token"
```

### 3. 发布技能

```bash
# 方式一：一键发布（推荐）
python scripts/main.py publish --skill-dir ./your-skill

# 方式二：分步发布
python scripts/main.py extract --skill-dir ./your-skill --output skill-info.json
python scripts/main.py verify --skill-info skill-info.json
python scripts/main.py register --skill-info skill-info.json
python scripts/main.py upload --skill-dir ./your-skill
python scripts/main.py share --skill-name your-skill --skill-id 1
```

## 可用命令

```bash
# 查看所有命令
python scripts/main.py --help

# 查看具体命令帮助
python scripts/main.py publish --help
```

### 命令列表

| 命令 | 说明 |
|------|------|
| `extract` | 提取技能信息 |
| `verify` | 验证技能配置 |
| `register` | 注册到 API |
| `upload` | 上传技能包 |
| `share` | 生成分享链接 |
| `publish` | 一键发布（完整流程） |
| `update` | 更新技能 |
| `delete` | 删除技能 |

## 技能目录结构要求

```
your-skill/
├── SKILL.md              # 必需：技能定义文件
├── scripts/              # 必需：脚本目录
│   └── main.py          # 必需：主脚本
├── config/              # 必需：配置目录
│   └── bingoclaw.json   # 必需：配置文件
├── docs/                # 可选：文档目录
└── assets/              # 可选：资源目录
```

## 示例：发布天气查询技能

```bash
# 1. 准备技能目录
mkdir weather-skill
cd weather-skill
mkdir -p scripts config

# 2. 创建 SKILL.md（参考 pubskill/SKILL.md）
# 3. 创建 scripts/main.py
# 4. 创建 config/bingoclaw.json

# 5. 发布
python ../pubskill/scripts/main.py publish --skill-dir ./weather-skill
```

## 常见问题

### Q: GitHub Token 在哪里获取？

A: 在 GitHub Settings -> Developer settings -> Personal access tokens 中生成

### Q: 发布失败怎么办？

A: 使用 `--skip-verify` 跳过验证，或查看详细错误信息：
```bash
python scripts/main.py publish --skill-dir ./your-skill -v
```

### Q: 如何更新已发布的技能？

A: 使用 update 命令：
```bash
python scripts/main.py update --skill-name your-skill --skill-dir ./your-skill
```

## 下一步

- 查看 [README.md](README.md) 了解详细说明
- 查看 [docs/EXAMPLES.md](docs/EXAMPLES.md) 了解使用示例
- 查看 [docs/IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md) 了解实现细节
