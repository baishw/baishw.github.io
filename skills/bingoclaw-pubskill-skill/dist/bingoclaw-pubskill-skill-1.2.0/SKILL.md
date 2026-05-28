---
name: bingoclaw-pubskill-skill
version: 1.2.0
description: "发布技能到 SkillHub 系统：提取目标技能信息，通过 API 注册到技能管理系统，上传技能包到 baishw.github.io，返回技能分享页 URL。Use when user wants to publish a skill to SkillHub platform, including skill information extraction, API registration, package upload, and sharing URL generation."
homepage: https://gitee.com/baishw/bingoclaw-skills
metadata:
  {
    "keywords": ["skill", "publish", "SkillHub", "API"],
    "author": "baishw",
    "license": "MIT",
    "category": "tool"
  }
---

# bingoclaw-pubskill-skill

技能发布工具，用于将技能发布到 SkillHub 系统。

## 功能特性

- 技能信息提取：从技能目录自动提取技能信息
- 技能验证：验证技能配置完整性
- API注册：将技能注册到 SkillHub 系统
- 技能包上传：上传技能包到 GitHub Pages
- 分享链接生成：生成技能分享页面 URL

## 快速开始

```bash
# 发布技能
python scripts/main.py publish --skill-dir ./my-skill
```

## 命令说明

| 命令 | 说明 |
|------|------|
| `extract` | 提取技能信息 |
| `verify` | 验证技能配置 |
| `register` | 注册技能到 API |
| `upload` | 上传技能包 |
| `share` | 生成分享链接 |
| `publish` | 发布技能（完整流程） |
| `update` | 更新技能 |
| `delete` | 删除技能 |

## 版本历史

- v1.2.0: 新增技能展示页面，支持动态技能信息展示
- v1.1.0: 简化配置流程，预置共享 Token
- v1.0.0: 初始版本
