# SkillHub API 文档

## 基础信息

**基础地址**: `https://skill.cxus.cn`

**数据格式**: JSON

**字符编码**: UTF-8

## 认证机制

### Token 认证

所有需要登录的接口都需要在请求中携带 Token，支持以下三种方式：

#### 方式 1: HTTP 请求头（推荐）
```http
Token: 550e8400-e29b-41d4-a716-446655440000
```

#### 方式 2: URL 参数
```
https://skill.cxus.cn/api/user/index?token=550e8400-e29b-41d4-a716-446655440000
```

#### 方式 3: Cookie
```
Cookie: token=550e8400-e29b-41d4-a716-446655440000
```

### Token 有效期

Token 默认有效期为 30 天（2592000 秒）。

---

## 统一响应格式

### 成功响应
```json
{
    "code": 1,
    "msg": "操作成功",
    "time": 1779893012,
    "data": {
        "key": "value"
    }
}
```

### 失败响应
```json
{
    "code": 0,
    "msg": "错误信息",
    "time": 1779893012,
    "data": null
}
```

### 响应字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 响应状态码，1 表示成功，0 表示失败 |
| msg | string | 响应消息 |
| time | int | 服务器时间戳 |
| data | any | 响应数据，可为 null |

---

## 用户接口

### 1. 用户登录

**接口**: `POST /api/user/login`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| account | string | 是 | 账号（用户名/邮箱/手机号） |
| password | string | 是 | 密码 |

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/user/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "account=skillpuber&password=123456"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Logged in successful",
    "data": {
        "userinfo": {
            "id": 2,
            "username": "skillpuber",
            "nickname": "",
            "mobile": "",
            "avatar": "",
            "score": 0,
            "token": "68129bce-5b1b-4dbe-8aef-e9fb32ea9a86",
            "expires_in": 2592000
        }
    }
}
```

---

### 2. 手机验证码登录

**接口**: `POST /api/user/mobilelogin`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mobile | string | 是 | 手机号 |
| captcha | string | 是 | 验证码 |

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/user/mobilelogin \
  -d "mobile=13800138000&captcha=123456"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Logged in successful",
    "data": {
        "userinfo": {
            "id": 1,
            "username": "13800138000",
            "token": "550e8400-e29b-41d4-a716-446655440000",
            "expires_in": 2592000
        }
    }
}
```

---

### 3. 用户注册

**接口**: `POST /api/user/register`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |
| email | string | 否 | 邮箱 |
| mobile | string | 否 | 手机号 |
| code | string | 是 | 手机验证码 |

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/user/register \
  -d "username=newuser&password=123456&mobile=13900139000&code=123456"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Sign up successful",
    "data": {
        "userinfo": {
            "id": 3,
            "username": "newuser",
            "token": "550e8400-e29b-41d4-a716-446655440001",
            "expires_in": 2592000
        }
    }
}
```

---

### 4. 退出登录

**接口**: `POST /api/user/logout`

**无需登录**: 否

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/user/logout \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Logout successful",
    "data": null
}
```

---

### 5. 会员中心

**接口**: `GET /api/user/index`

**无需登录**: 否

**请求示例**:
```bash
curl https://skill.cxus.cn/api/user/index \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "welcome": "技能发布者"
    }
}
```

---

### 6. 修改个人信息

**接口**: `POST /api/user/profile`

**无需登录**: 否

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| avatar | string | 否 | 头像地址 |
| username | string | 否 | 用户名 |
| nickname | string | 否 | 昵称 |
| bio | string | 否 | 个人简介 |

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/user/profile \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86" \
  -d "nickname=新昵称"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": null
}
```

---

### 7. 重置密码

**接口**: `POST /api/user/resetpwd`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 验证类型 (mobile/email)，默认 mobile |
| mobile | string | 否 | 手机号 |
| email | string | 否 | 邮箱 |
| newpassword | string | 是 | 新密码（6-30 位） |
| captcha | string | 是 | 验证码 |

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/user/resetpwd \
  -d "type=mobile&mobile=13800138000&newpassword=654321&captcha=123456"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Reset password successful",
    "data": null
}
```

---

## Token 接口

### 1. 检测 Token

**接口**: `GET /api/token/check`

**无需登录**: 否

**请求示例**:
```bash
curl https://skill.cxus.cn/api/token/check \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "token": "68129bce-5b1b-4dbe-8aef-e9fb32ea9a86",
        "expires_in": 2591900
    }
}
```

---

### 2. 刷新 Token

**接口**: `GET /api/token/refresh`

**无需登录**: 否

**说明**: 刷新 Token 会删除旧 Token，生成新 Token。

**请求示例**:
```bash
curl https://skill.cxus.cn/api/token/refresh \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "token": "880e8400-e29b-41d4-a716-446655440000",
        "expires_in": 2592000
    }
}
```

---

## 技能接口

### 1. 技能列表

**接口**: `GET /api/skill/index`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 技能类型 (function/api/database/workflow) |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**请求示例**:
```bash
curl "https://skill.cxus.cn/api/skill/index?type=function&page=1&limit=10"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "list": [
            {
                "id": 7,
                "name": "test_skill_1779893011",
                "username": "skillpuber",
                "type": "function",
                "version": "1.0.0",
                "description": "Test skill",
                "summary": "Test summary",
                "params": "{}",
                "returns": "{}",
                "dependencies": "[]",
                "risk_level": "low",
                "rate_limit": 100,
                "timeout": 30,
                "endpoint": null,
                "method": "POST",
                "auth_type": "none",
                "icon": "",
                "status": "normal",
                "installcount": 0,
                "createtime": 1779893012
            }
        ],
        "total": 1,
        "page": 1,
        "limit": 10
    }
}
```

---

### 2. 搜索技能

**接口**: `GET /api/skill/search`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 否 | 搜索关键词（搜索名称、描述、摘要） |
| type | string | 否 | 技能类型筛选 |
| risk_level | string | 否 | 风险等级筛选 |
| auth_type | string | 否 | 认证方式筛选 |
| method | string | 否 | 请求方法筛选 |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**请求示例**:
```bash
curl "https://skill.cxus.cn/api/skill/search?q=test&type=function&page=1&limit=10"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "list": [
            {
                "id": 7,
                "name": "test_skill_1779893011",
                "type": "function",
                "description": "Test skill",
                "summary": "Test summary"
            }
        ],
        "total": 1,
        "page": 1,
        "limit": 10
    }
}
```

---

### 3. 最新技能

**接口**: `GET /api/skill/latest`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 技能类型筛选 |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**请求示例**:
```bash
curl "https://skill.cxus.cn/api/skill/latest?page=1&limit=5"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "list": [],
        "total": 0,
        "page": 1,
        "limit": 5
    }
}
```

---

### 4. 热门技能

**接口**: `GET /api/skill/hot`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 技能类型筛选 |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**请求示例**:
```bash
curl "https://skill.cxus.cn/api/skill/hot?limit=10"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "list": [],
        "total": 0,
        "page": 1,
        "limit": 10
    }
}
```

---

### 5. 技能详情

**接口**: `GET /api/skill/detail`

**无需登录**: 是

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 技能 ID |

**请求示例**:
```bash
curl "https://skill.cxus.cn/api/skill/detail?id=7"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "data": {
        "id": 7,
        "name": "test_skill_1779893011",
        "username": "skillpuber",
        "type": "function",
        "version": "1.0.0",
        "description": "Test skill",
        "summary": "Test summary",
        "params": "{}",
        "returns": "{}",
        "dependencies": "[]",
        "risk_level": "low",
        "rate_limit": 100,
        "timeout": 30,
        "method": "POST",
        "auth_type": "none",
        "status": "normal",
        "installcount": 0,
        "createtime": 1779893012
    }
}
```

---

### 6. 创建技能

**接口**: `POST /api/skill/create`

**无需登录**: 否

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 技能名称 |
| username | string | 是 | 提供者用户名 |
| type | string | 是 | 技能类型 (function/api/database/workflow) |
| version | string | 否 | 版本号，默认 0.0.0 |
| description | string | 否 | 技能描述 |
| summary | string | 否 | 简短摘要 |
| params | string | 否 | 参数定义 (JSON Schema)，默认 {} |
| returns | string | 否 | 返回值定义 (JSON Schema)，默认 {} |
| dependencies | string | 否 | 依赖工具列表 (JSON)，默认 [] |
| risk_level | string | 否 | 风险等级 (low/medium/high/critical)，默认 low |
| rate_limit | int | 否 | 调用频率限制(次/分钟)，默认 0 |
| timeout | int | 否 | 超时时间(秒)，默认 30 |
| endpoint | string | 否 | API 端点 URL |
| method | string | 否 | 请求方法 (GET/POST/PUT/DELETE)，默认 POST |
| auth_type | string | 否 | 认证方式 (none/api_key/oauth2/token)，默认 none |
| icon | string | 否 | 图标 URL |

**请求示例（表单格式）**:
```bash
curl -X POST https://skill.cxus.cn/api/skill/create \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86" \
  -d "name=my_new_skill&username=skillpuber&type=function&version=1.0.0&description=我的新技能&summary=技能摘要&risk_level=low&params={}&returns={}&dependencies=[]"
```

**请求示例（JSON 格式）**:
```bash
curl -X POST https://skill.cxus.cn/api/skill/create \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_new_skill",
    "username": "skillpuber",
    "type": "function",
    "version": "1.0.0",
    "description": "我的新技能",
    "summary": "技能摘要",
    "risk_level": "low",
    "params": "{}",
    "returns": "{}",
    "dependencies": "[]"
  }'
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Skill created successfully",
    "data": {
        "id": 8,
        "name": "my_new_skill",
        "username": "skillpuber",
        "type": "function",
        "version": "1.0.0",
        "description": "我的新技能",
        "summary": "技能摘要",
        "risk_level": "low",
        "status": "normal",
        "installcount": 0,
        "createtime": 1779893020
    }
}
```

---

### 7. 更新技能

**接口**: `POST /api/skill/update`

**无需登录**: 否

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 技能 ID |
| name | string | 否 | 技能名称 |
| username | string | 否 | 提供者用户名 |
| type | string | 否 | 技能类型 |
| version | string | 否 | 版本号 |
| description | string | 否 | 技能描述 |
| summary | string | 否 | 简短摘要 |
| params | string | 否 | 参数定义 |
| returns | string | 否 | 返回值定义 |
| dependencies | string | 否 | 依赖工具列表 |
| risk_level | string | 否 | 风险等级 |
| rate_limit | int | 否 | 调用频率限制 |
| timeout | int | 否 | 超时时间 |
| endpoint | string | 否 | API 端点 URL |
| method | string | 否 | 请求方法 |
| auth_type | string | 否 | 认证方式 |
| icon | string | 否 | 图标 URL |
| status | string | 否 | 状态 |
| installcount | int | 否 | 安装次数 |

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/skill/update \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86" \
  -d "id=7&version=1.0.1&description=更新后的技能描述"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Skill updated successfully",
    "data": {
        "id": 7,
        "version": "1.0.1",
        "description": "更新后的技能描述"
    }
}
```

---

### 8. 删除技能

**接口**: `POST /api/skill/delete`

**无需登录**: 否

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 技能 ID |

**请求示例**:
```bash
curl -X POST https://skill.cxus.cn/api/skill/delete \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86" \
  -d "id=7"
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Skill deleted successfully",
    "data": null
}
```

---

## 枚举值说明

### 技能类型
| 值 | 说明 |
|------|------|
| function | 函数类型 |
| api | API 类型 |
| database | 数据库类型 |
| workflow | 工作流类型 |

### 风险等级
| 值 | 说明 |
|------|------|
| low | 低风险 |
| medium | 中风险 |
| high | 高风险 |
| critical | 极高风险 |

### 请求方法
| 值 | 说明 |
|------|------|
| GET | GET 请求 |
| POST | POST 请求 |
| PUT | PUT 请求 |
| DELETE | DELETE 请求 |

### 认证方式
| 值 | 说明 |
|------|------|
| none | 无认证 |
| api_key | API Key 认证 |
| oauth2 | OAuth 2.0 认证 |
| token | Token 认证 |

### 技能状态
| 值 | 说明 |
|------|------|
| normal | 正常 |
| disabled | 禁用 |
| pending | 待审核 |

---

## 完整示例流程

### 1. 用户登录获取 Token
```bash
curl -X POST https://skill.cxus.cn/api/user/login \
  -d "account=skillpuber&password=123456"
```

### 2. 携带 Token 创建技能
```bash
curl -X POST https://skill.cxus.cn/api/skill/create \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "weather_skill",
    "username": "skillpuber",
    "type": "api",
    "version": "1.0.0",
    "description": "天气查询技能",
    "summary": "查询指定城市的天气信息",
    "risk_level": "low",
    "endpoint": "https://api.example.com/weather",
    "method": "GET",
    "auth_type": "none"
  }'
```

### 3. 查询技能列表
```bash
curl "https://skill.cxus.cn/api/skill/index?type=api"
```

### 4. 获取技能详情
```bash
curl "https://skill.cxus.cn/api/skill/detail?id=9"
```

### 5. 退出登录
```bash
curl -X POST https://skill.cxus.cn/api/user/logout \
  -H "Token: 68129bce-5b1b-4dbe-8aef-e9fb32ea9a86"
```

---

## 错误码说明

| HTTP 状态码 | code | 说明 |
|------|------|------|
| 200 | 1 | 操作成功 |
| 200 | 0 | 操作失败 |
| 401 | 0 | 未登录或 Token 失效 |
| 403 | 0 | 无权限访问 |
| 404 | 0 | 资源不存在 |

---

## 更新日志

### v1.0.0 (2026-05-27)
- 初始版本发布
- 支持用户注册、登录、Token 管理
- 支持技能的 CRUD 操作
- 支持技能搜索、筛选、排序
