# SkillHub OpenClaw 技能管理 API 文档

## 概述

SkillHub API 提供用于管理 OpenClaw 工具技能的接口，支持技能的创建、查询、更新和删除操作。

**基础 URL**: `/api/skill`

**认证**: 大部分接口无需登录即可访问（查看 `noNeedLogin` 说明）

---

## 通用响应格式

### 成功响应
```json
{
    "code": 1,
    "msg": "操作成功",
    "time": 1699999999,
    "data": {}
}
```

### 错误响应
```json
{
    "code": 0,
    "msg": "错误信息",
    "time": 1699999999,
    "data": null
}
```

---

## 接口列表

### 1. 获取技能列表

**URL**: `GET /api/skill/index`

**无需登录**: 是

**功能**: 获取技能列表（按ID倒序）

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 否 | 技能类型筛选，可选值：`function`, `api`, `database`, `workflow` |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**示例请求**:
```
GET /api/skill/index?type=function&page=1&limit=10
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "time": 1699999999,
    "data": {
        "list": [
            {
                "id": 1,
                "name": "getWeather",
                "username": "admin",
                "type": "function",
                "version": "1.0.0",
                "description": "获取指定城市的天气信息",
                "summary": "天气查询工具",
                "params": "{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\",\"description\":\"城市名称\"}}}",
                "returns": "{\"type\":\"object\",\"properties\":{\"temp\":{\"type\":\"number\"}}}",
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
                "createtime": 1699999999,
                "updatetime": 1699999999,
                "deletetime": null
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

**URL**: `GET /api/skill/search`

**无需登录**: 是

**功能**: 支持关键词搜索和多条件筛选，可搜索技能名称、描述和摘要

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| q | string | 否 | 搜索关键词（匹配名称、描述、摘要） |
| type | string | 否 | 技能类型筛选，可选值：`function`, `api`, `database`, `workflow` |
| risk_level | string | 否 | 风险等级筛选，可选值：`low`, `medium`, `high`, `critical` |
| auth_type | string | 否 | 认证方式筛选，可选值：`none`, `api_key`, `oauth2`, `token` |
| method | string | 否 | 请求方法筛选，可选值：`GET`, `POST`, `PUT`, `DELETE` |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**示例请求**:
```
GET /api/skill/search?q=天气&type=function&risk_level=low
GET /api/skill/search?q=API&method=GET&page=1&limit=20
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "time": 1699999999,
    "data": {
        "list": [
            {
                "id": 1,
                "name": "getWeather",
                "username": "admin",
                "type": "function",
                "version": "1.0.0",
                "description": "获取指定城市的天气信息",
                "summary": "天气查询工具",
                "risk_level": "low",
                "method": "POST",
                "auth_type": "none",
                "status": "normal",
                "installcount": 10,
                "createtime": 1699999999,
                "updatetime": 1699999999
            }
        ],
        "total": 1,
        "page": 1,
        "limit": 10
    }
}
```

**筛选条件说明**:

- `q`: 关键词搜索，同时匹配 name、description、summary 字段
- `type`: 精确匹配技能类型
- `risk_level`: 精确匹配风险等级
- `auth_type`: 精确匹配认证方式
- `method`: 精确匹配请求方法
- 所有筛选条件可自由组合，空值参数会被忽略

---

### 3. 最新技能列表（按创建时间排序）

**URL**: `GET /api/skill/latest`

**无需登录**: 是

**功能**: 获取最新发布的技能列表，按创建时间倒序排列

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 否 | 技能类型筛选，可选值：`function`, `api`, `database`, `workflow` |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**示例请求**:
```
GET /api/skill/latest
GET /api/skill/latest?type=function&page=1&limit=10
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "time": 1699999999,
    "data": {
        "list": [
            {
                "id": 5,
                "name": "newTool",
                "username": "admin",
                "type": "function",
                "version": "1.0.0",
                "description": "最新工具",
                "createtime": 1699999999,
                "installcount": 5
            }
        ],
        "total": 5,
        "page": 1,
        "limit": 10
    }
}
```

---

### 4. 热门技能列表（按安装次数排序）

**URL**: `GET /api/skill/hot`

**无需登录**: 是

**功能**: 获取最受欢迎的技能列表，按安装次数倒序排列

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 否 | 技能类型筛选，可选值：`function`, `api`, `database`, `workflow` |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 10 |

**示例请求**:
```
GET /api/skill/hot
GET /api/skill/hot?type=api&page=1&limit=20
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "time": 1699999999,
    "data": {
        "list": [
            {
                "id": 3,
                "name": "popularTool",
                "username": "admin",
                "type": "function",
                "version": "2.0.0",
                "description": "热门工具",
                "installcount": 1000
            }
        ],
        "total": 10,
        "page": 1,
        "limit": 10
    }
}
```

---

### 5. 获取技能详情

**URL**: `GET /api/skill/detail`

**无需登录**: 是

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 技能ID |

**示例请求**:
```
GET /api/skill/detail?id=1
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "",
    "time": 1699999999,
    "data": {
        "id": 1,
        "name": "getWeather",
        "username": "admin",
        "type": "function",
        "version": "1.0.0",
        "description": "获取指定城市的天气信息",
        "summary": "天气查询工具",
        "params": {"type":"object","properties":{"city":{"type":"string","description":"城市名称"}}},
        "returns": {"type":"object","properties":{"temp":{"type":"number"}}},
        "dependencies": [],
        "risk_level": "low",
        "rate_limit": 100,
        "timeout": 30,
        "endpoint": null,
        "method": "POST",
        "auth_type": "none",
        "icon": "",
        "status": "normal",
        "installcount": 0,
        "createtime": 1699999999,
        "updatetime": 1699999999
    }
}
```

**错误响应** (技能不存在):
```json
{
    "code": 0,
    "msg": "Skill not found",
    "time": 1699999999,
    "data": null
}
```

---

### 6. 创建技能

**URL**: `POST /api/skill/create`

**无需登录**: 是

**Content-Type**: `application/x-www-form-urlencoded` 或 `application/json`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 工具名称，唯一标识 |
| username | string | 是 | 提供者用户名 |
| type | string | 是 | 工具类型：`function`, `api`, `database`, `workflow` |
| version | string | 否 | 版本号，默认 `0.0.0` |
| description | string | 否 | 工具描述（用于AI理解） |
| summary | string | 否 | 简短摘要 |
| params | string | 否 | 参数定义（JSON Schema） |
| returns | string | 否 | 返回值定义（JSON Schema） |
| dependencies | string | 否 | 依赖工具列表（JSON数组） |
| risk_level | string | 否 | 风险等级：`low`, `medium`, `high`, `critical`，默认 `low` |
| rate_limit | int | 否 | 调用频率限制(次/分钟)，默认 0 |
| timeout | int | 否 | 超时时间(秒)，默认 30 |
| endpoint | string | 否 | API端点URL |
| method | string | 否 | 请求方法：`GET`, `POST`, `PUT`, `DELETE`，默认 `POST` |
| auth_type | string | 否 | 认证方式：`none`, `api_key`, `oauth2`, `token`，默认 `none` |
| icon | string | 否 | 图标URL |

**示例请求**:
```bash
POST /api/skill/create
Content-Type: application/x-www-form-urlencoded

name=getWeather&username=admin&type=function&version=1.0.0&description=获取指定城市的天气信息&summary=天气查询工具&params={"type":"object","properties":{"city":{"type":"string"}}}&risk_level=low&timeout=30
```

**JSON格式示例**:
```json
POST /api/skill/create
Content-Type: application/json

{
    "name": "getWeather",
    "username": "admin",
    "type": "function",
    "version": "1.0.0",
    "description": "获取指定城市的天气信息",
    "summary": "天气查询工具",
    "params": {"type":"object","properties":{"city":{"type":"string","description":"城市名称"}}},
    "returns": {"type":"object","properties":{"temp":{"type":"number","description":"温度"}}},
    "dependencies": [],
    "risk_level": "low",
    "rate_limit": 100,
    "timeout": 30,
    "auth_type": "none"
}
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Skill created successfully",
    "time": 1699999999,
    "data": {
        "id": 1,
        "name": "getWeather",
        "username": "admin",
        "type": "function",
        "version": "1.0.0",
        "description": "获取指定城市的天气信息",
        "summary": "天气查询工具",
        "params": "{}",
        "returns": "{}",
        "dependencies": "[]",
        "risk_level": "low",
        "rate_limit": 0,
        "timeout": 30,
        "endpoint": null,
        "method": "POST",
        "auth_type": "none",
        "icon": "",
        "status": "normal",
        "installcount": 0,
        "createtime": 1699999999,
        "updatetime": 1699999999
    }
}
```

---

### 7. 更新技能

**URL**: `POST /api/skill/update`

**无需登录**: 是

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 技能ID |
| name | string | 否 | 工具名称 |
| username | string | 否 | 提供者用户名 |
| type | string | 否 | 工具类型 |
| version | string | 否 | 版本号 |
| description | string | 否 | 工具描述 |
| summary | string | 否 | 简短摘要 |
| params | string | 否 | 参数定义 |
| returns | string | 否 | 返回值定义 |
| dependencies | string | 否 | 依赖工具列表 |
| risk_level | string | 否 | 风险等级 |
| rate_limit | int | 否 | 调用频率限制 |
| timeout | int | 否 | 超时时间 |
| endpoint | string | 否 | API端点URL |
| method | string | 否 | 请求方法 |
| auth_type | string | 否 | 认证方式 |
| icon | string | 否 | 图标URL |
| status | string | 否 | 状态：`normal`, `hidden`, `disabled` |
| installcount | int | 否 | 安装次数 |

**示例请求**:
```bash
POST /api/skill/update
Content-Type: application/x-www-form-urlencoded

id=1&version=1.1.0&description=更新后的描述
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Skill updated successfully",
    "time": 1699999999,
    "data": {
        "id": 1,
        "name": "getWeather",
        "version": "1.1.0",
        "description": "更新后的描述",
        ...
    }
}
```

---

### 8. 删除技能

**URL**: `POST /api/skill/delete`

**无需登录**: 是

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 技能ID |

**示例请求**:
```bash
POST /api/skill/delete
Content-Type: application/x-www-form-urlencoded

id=1
```

**响应示例**:
```json
{
    "code": 1,
    "msg": "Skill deleted successfully",
    "time": 1699999999,
    "data": null
}
```

---

## 字段说明

### 工具类型 (type)

| 值 | 说明 |
|----|------|
| function | 函数 - 本地函数调用 |
| api | API接口 - 外部API调用 |
| database | 数据库 - 数据库操作 |
| workflow | 工作流 - 自动化工作流 |

### 风险等级 (risk_level)

| 值 | 说明 |
|----|------|
| low | 低风险 - 仅读操作，无副作用 |
| medium | 中风险 - 有轻微副作用或资源消耗 |
| high | 高风险 - 有显著副作用或资源消耗 |
| critical | 严重风险 - 可能造成数据丢失或系统损坏 |

### 请求方法 (method)

| 值 | 说明 |
|----|------|
| GET | GET 请求 - 获取资源 |
| POST | POST 请求 - 创建资源 |
| PUT | PUT 请求 - 更新资源 |
| DELETE | DELETE 请求 - 删除资源 |

### 认证方式 (auth_type)

| 值 | 说明 |
|----|------|
| none | 无需认证 |
| api_key | API Key 认证 |
| oauth2 | OAuth2.0 认证 |
| token | Token 认证 |

### 状态 (status)

| 值 | 说明 |
|----|------|
| normal | 正常 - 可正常使用 |
| hidden | 隐藏 - 不在列表中显示 |
| disabled | 禁用 - 暂时不可用 |

---

## OpenClaw 技能定义规范

技能定义需符合 OpenClaw 工具技能标准，包含以下核心字段：

### 必填字段
- `name`: 工具名称（唯一标识）
- `username`: 提供者用户名
- `type`: 工具类型

### 推荐字段
- `description`: 工具描述，用于 AI 理解工具用途
- `params`: 参数定义（JSON Schema 格式）
- `returns`: 返回值定义（JSON Schema 格式）
- `risk_level`: 风险等级

### 可选字段
- `version`: 版本号
- `summary`: 简短摘要
- `dependencies`: 依赖工具列表
- `rate_limit`: 调用频率限制
- `timeout`: 超时时间
- `endpoint`: API 端点（API类型必填）
- `method`: 请求方法
- `auth_type`: 认证方式
- `icon`: 图标

---

## 错误码

| code | 说明 |
|------|------|
| 1 | 成功 |
| 0 | 失败 |

---

## 使用示例

### cURL 示例

```bash
# 获取技能列表
curl -X GET "http://localhost/api/skill/index?type=function&page=1&limit=10"

# 搜索技能（关键词）
curl -X GET "http://localhost/api/skill/search?q=天气"

# 搜索技能（多条件组合）
curl -X GET "http://localhost/api/skill/search?q=API&type=api&risk_level=low&method=GET"

# 获取最新技能列表
curl -X GET "http://localhost/api/skill/latest"

# 获取热门技能列表
curl -X GET "http://localhost/api/skill/hot"

# 获取技能详情
curl -X GET "http://localhost/api/skill/detail?id=1"

# 创建技能
curl -X POST "http://localhost/api/skill/create" \
  -d "name=getWeather" \
  -d "username=admin" \
  -d "type=function" \
  -d "version=1.0.0" \
  -d "description=获取天气信息" \
  -d "risk_level=low"

# 更新技能
curl -X POST "http://localhost/api/skill/update" \
  -d "id=1" \
  -d "version=1.1.0"

# 删除技能
curl -X POST "http://localhost/api/skill/delete" \
  -d "id=1"
```

### JavaScript (fetch) 示例

```javascript
// 获取技能列表
const listResponse = await fetch('/api/skill/index?type=function');
const listData = await listResponse.json();
console.log(listData.data.list);

// 搜索技能
const searchResponse = await fetch('/api/skill/search?q=天气&type=function');
const searchData = await searchResponse.json();
console.log(searchData.data.list);

// 多条件搜索
const multiSearchResponse = await fetch('/api/skill/search?q=API&risk_level=low&method=GET');
const multiSearchData = await multiSearchResponse.json();
console.log(multiSearchData.data.list);

// 获取最新技能
const latestResponse = await fetch('/api/skill/latest');
const latestData = await latestResponse.json();
console.log(latestData.data.list);

// 获取热门技能
const hotResponse = await fetch('/api/skill/hot');
const hotData = await hotResponse.json();
console.log(hotData.data.list);

// 获取技能详情
const detailResponse = await fetch('/api/skill/detail?id=1');
const detailData = await detailResponse.json();
console.log(detailData.data);

// 创建技能
const createResponse = await fetch('/api/skill/create', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        name: 'getWeather',
        username: 'admin',
        type: 'function',
        version: '1.0.0',
        description: '获取天气信息',
        risk_level: 'low'
    })
});
const createData = await createResponse.json();
console.log(createData);

// 更新技能
await fetch('/api/skill/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'id=1&version=1.1.0'
});

// 删除技能
await fetch('/api/skill/delete', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'id=1'
});
```

### Python (requests) 示例

```python
import requests

BASE_URL = "http://localhost"

# 获取技能列表
def get_skill_list(type=None, page=1, limit=10):
    params = {'page': page, 'limit': limit}
    if type:
        params['type'] = type
    response = requests.get(f"{BASE_URL}/api/skill/index", params=params)
    return response.json()

# 搜索技能
def search_skill(q=None, type=None, risk_level=None, auth_type=None, method=None, page=1, limit=10):
    params = {'page': page, 'limit': limit}
    if q:
        params['q'] = q
    if type:
        params['type'] = type
    if risk_level:
        params['risk_level'] = risk_level
    if auth_type:
        params['auth_type'] = auth_type
    if method:
        params['method'] = method
    response = requests.get(f"{BASE_URL}/api/skill/search", params=params)
    return response.json()

# 获取最新技能列表
def get_latest_skill(type=None, page=1, limit=10):
    params = {'page': page, 'limit': limit}
    if type:
        params['type'] = type
    response = requests.get(f"{BASE_URL}/api/skill/latest", params=params)
    return response.json()

# 获取热门技能列表
def get_hot_skill(type=None, page=1, limit=10):
    params = {'page': page, 'limit': limit}
    if type:
        params['type'] = type
    response = requests.get(f"{BASE_URL}/api/skill/hot", params=params)
    return response.json()

# 获取技能详情
def get_skill_detail(id):
    response = requests.get(f"{BASE_URL}/api/skill/detail", params={'id': id})
    return response.json()

# 创建技能
def create_skill(data):
    response = requests.post(f"{BASE_URL}/api/skill/create", data=data)
    return response.json()

# 更新技能
def update_skill(data):
    response = requests.post(f"{BASE_URL}/api/skill/update", data=data)
    return response.json()

# 删除技能
def delete_skill(id):
    response = requests.post(f"{BASE_URL}/api/skill/delete", data={'id': id})
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 创建技能
    new_skill = create_skill({
        'name': 'getWeather',
        'username': 'admin',
        'type': 'function',
        'version': '1.0.0',
        'description': '获取天气信息',
        'risk_level': 'low'
    })
    print(f"创建技能: {new_skill}")

    # 获取技能列表
    skills = get_skill_list(type='function')
    print(f"技能列表: {skills}")

    # 搜索技能（关键词）
    results = search_skill(q='天气')
    print(f"搜索结果: {results}")

    # 多条件搜索
    results = search_skill(q='API', type='api', risk_level='low', method='GET')
    print(f"多条件搜索: {results}")

    # 获取最新技能
    latest = get_latest_skill()
    print(f"最新技能: {latest}")

    # 获取热门技能
    hot = get_hot_skill()
    print(f"热门技能: {hot}")

    # 获取技能详情
    skill = get_skill_detail(id=1)
    print(f"技能详情: {skill}")

    # 更新技能
    updated = update_skill({'id': 1, 'version': '1.1.0'})
    print(f"更新技能: {updated}")

    # 删除技能
    result = delete_skill(id=1)
    print(f"删除技能: {result}")
```
