# PubSkill 使用示例

## 示例 1：发布一个简单的天气查询技能

### 1. 准备技能目录结构

```bash
mkdir weather-skill
cd weather-skill

# 创建目录结构
mkdir -p scripts config docs assets
```

### 2. 创建 SKILL.md 文件

```markdown
---
name: weather
description: "获取指定城市的天气信息"
metadata:
  {
    "openclaw": {
      "emoji": "🌤️",
      "os": ["darwin", "linux", "win32"],
      "requires": {
        "bins": ["python3"],
        "env": ["WEATHER_API_KEY"]
      },
      "primaryEnv": "WEATHER_API_KEY",
      "skillKey": "weather",
      "install": [
        {
          "id": "pip-requests",
          "kind": "pip",
          "package": "requests",
          "label": "Install Requests"
        }
      ]
    }
  }
---

# Weather - 天气查询技能

查询指定城市的天气信息。

## 使用场景

✅ **USE when:**
- 用户需要查询某个城市的当前天气
- 用户需要了解温度、湿度等气象数据

❌ **DON'T use when:**
- 用户需要历史天气数据（需要使用其他 API）
- 用户需要长期天气预报（超过 7 天）
```

### 3. 创建主脚本

创建 `scripts/main.py`：

```python
#!/usr/bin/env python3
"""
Weather - 天气查询技能

获取指定城市的天气信息
"""

import requests
import os


def get_weather(city: str) -> dict:
    """获取城市天气
    
    Args:
        city: 城市名称
        
    Returns:
        dict: 天气信息
    """
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return {'error': 'WEATHER_API_KEY 环境变量未设置'}
    
    url = f"https://api.weather.com/v1/current?key={api_key}&city={city}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            'city': city,
            'temperature': data.get('temp'),
            'humidity': data.get('humidity'),
            'condition': data.get('condition'),
            'wind_speed': data.get('wind_speed')
        }
    except requests.exceptions.Timeout:
        return {'error': '请求超时'}
    except requests.exceptions.RequestException as e:
        return {'error': f'请求失败：{str(e)}'}


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        city = sys.argv[1]
        result = get_weather(city)
        print(result)
    else:
        print("用法：python main.py <城市名称>")
```

### 4. 创建配置文件

创建 `config/bingoclaw.json`：

```json
{
  "name": "weather",
  "type": "function",
  "version": "1.0.0",
  "description": "获取指定城市的天气信息",
  "params": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名称"
      }
    },
    "required": ["city"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      },
      "temperature": {
        "type": "number"
      },
      "humidity": {
        "type": "number"
      },
      "condition": {
        "type": "string"
      }
    }
  },
  "risk_level": "low",
  "timeout": 30
}
```

### 5. 发布技能

```bash
# 设置环境变量
export SKILLHUB_API_URL="https://api.skillhub.example.com"
export GITHUB_TOKEN="your_github_token"

# 发布技能
python ../pubskill/scripts/main.py publish --skill-dir ./weather-skill
```

### 6. 验证发布结果

```bash
# 验证技能
python ../pubskill/scripts/main.py verify --skill-name weather

# 获取技能详情
curl "https://api.skillhub.example.com/api/skill/detail?id=1"
```

### 7. 分享技能

发布成功后会输出：

```
✅ 技能发布成功！

技能名称：weather
技能 ID: 1
分享链接：https://baishw.github.io/skills/weather/
API 详情：https://api.skillhub.example.com/api/skill/detail?id=1
```

---

## 示例 2：批量发布多个技能

```bash
#!/bin/bash

# 批量发布脚本

SKILLS_DIR="./skills"
PUBSKILL_SCRIPT="../pubskill/scripts/main.py"

for skill_dir in "$SKILLS_DIR"/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        echo "🚀 发布技能：$skill_name"
        
        python "$PUBSKILL_SCRIPT" publish --skill-dir "$skill_dir"
        
        if [ $? -eq 0 ]; then
            echo "✅ $skill_name 发布成功"
        else
            echo "❌ $skill_name 发布失败"
        fi
        
        echo ""
    fi
done
```

---

## 示例 3：更新已发布的技能

```bash
# 修改技能文件后...

# 方式 1：使用 update 命令
python pubskill/scripts/main.py update --skill-name weather --skill-dir ./weather-skill

# 方式 2：重新发布（会自动更新）
python pubskill/scripts/main.py publish --skill-dir ./weather-skill --skip-verify
```

---

## 示例 4：分步发布流程

```bash
# 步骤 1：提取技能信息
python pubskill/scripts/main.py extract \
    --skill-dir ./weather-skill \
    --output skill-info.json

# 查看提取的信息
cat skill-info.json

# 步骤 2：验证技能
python pubskill/scripts/main.py verify --skill-info skill-info.json

# 步骤 3：注册到 API
python pubskill/scripts/main.py register --skill-info skill-info.json

# 步骤 4：上传技能包
python pubskill/scripts/main.py upload --skill-dir ./weather-skill

# 步骤 5：生成分享链接
python pubskill/scripts/main.py share --skill-name weather --skill-id 1
```

---

## 示例 5：使用配置文件

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

然后直接发布：

```bash
python pubskill/scripts/main.py publish --skill-dir ./weather-skill
```

---

## 示例 6：搜索和验证技能

```bash
# 搜索技能
python pubskill/scripts/main.py search --query weather

# 查看技能列表
python pubskill/scripts/main.py list --type function

# 查看热门技能
python pubskill/scripts/main.py hot --limit 10

# 查看最新技能
python pubskill/scripts/main.py latest --limit 10
```

---

## 示例 7：删除技能

```bash
# 删除技能
python pubskill/scripts/main.py delete --skill-name weather

# 确认删除（需要二次确认）
# 是否确认删除技能 'weather'？[y/N]: y

# ✅ 技能 'weather' 已删除
```

---

## 常见问题

### Q1: 发布失败提示"技能已存在"

**解决方案：**
```bash
# 使用 update 命令更新
python pubskill/scripts/main.py update --skill-name myskill --skill-dir ./myskill

# 或者删除后重新发布
python pubskill/scripts/main.py delete --skill-name myskill
python pubskill/scripts/main.py publish --skill-dir ./myskill
```

### Q2: GitHub 上传失败

**检查项：**
1. GITHUB_TOKEN 是否有效
2. Token 是否有仓库写入权限
3. 网络连接是否正常

```bash
# 测试 Token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# 检查仓库权限
curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/repos/baishw/baishw.github.io
```

### Q3: 技能验证失败

**常见错误：**
- 缺少必填字段（name, username, type）
- 名称格式错误
- 版本号格式错误
- 包含敏感信息

**解决方案：**
```bash
# 查看详细错误
python pubskill/scripts/main.py verify --skill-dir ./myskill

# 根据错误提示修复 SKILL.md 和配置文件
```

---

## 最佳实践

1. **版本管理**：使用语义化版本号（如 1.0.0, 1.1.0, 2.0.0）
2. **描述清晰**：提供详细的技能描述和使用场景
3. **测试充分**：发布前在本地充分测试
4. **文档完整**：包含 README.md 和使用示例
5. **安全第一**：不要在代码中硬编码敏感信息
6. **依赖最小化**：只安装必需的依赖包
