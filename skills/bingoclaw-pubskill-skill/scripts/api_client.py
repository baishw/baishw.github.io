#!/usr/bin/env python3
"""
SkillHub API 客户端

提供与 SkillHub 技能管理 API 的交互功能
"""

import json
import requests
from typing import Optional, Dict, Any


class SkillHubAPIClient:
    """SkillHub API 客户端"""
    
    def __init__(self, base_url: str, timeout: int = 30, token: str = None):
        """初始化 API 客户端
        
        Args:
            base_url: API 基础 URL
            timeout: 请求超时时间（秒）
            token: 认证令牌
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # 添加认证头 (SkillHub 使用 Token 头)
        if token:
            self.session.headers.update({
                'Token': token
            })
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                 params: Optional[Dict] = None) -> Dict[str, Any]:
        """发送 HTTP 请求
        
        Args:
            method: HTTP 方法
            endpoint: API 端点
            data: 请求数据
            params: 查询参数
            
        Returns:
            dict: API 响应数据
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                # 支持两种格式：JSON 和 form-urlencoded
                if isinstance(data, dict):
                    # 尝试 JSON 格式
                    response = self.session.post(
                        url, 
                        json=data, 
                        params=params,
                        timeout=self.timeout
                    )
                else:
                    response = self.session.post(
                        url,
                        data=data,
                        params=params,
                        timeout=self.timeout
                    )
            else:
                raise ValueError(f"不支持的 HTTP 方法：{method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            return {
                'code': 0,
                'msg': f'请求超时（{self.timeout}秒）',
                'data': None
            }
        except requests.exceptions.RequestException as e:
            return {
                'code': 0,
                'msg': f'请求失败：{str(e)}',
                'data': None
            }
        except json.JSONDecodeError:
            return {
                'code': 0,
                'msg': 'API 响应格式错误',
                'data': None
            }
    
    def create_skill(self, skill_info: Dict) -> Dict[str, Any]:
        """创建技能
        
        Args:
            skill_info: 技能信息字典，包含：
                - name: 技能名称（必填）
                - username: 提供者用户名（必填）
                - type: 技能类型（必填）
                - version: 版本号（可选）
                - description: 描述（可选）
                - summary: 摘要（可选）
                - params: 参数定义（可选）
                - returns: 返回值定义（可选）
                - dependencies: 依赖列表（可选）
                - risk_level: 风险等级（可选）
                - rate_limit: 调用频率限制（可选）
                - timeout: 超时时间（可选）
                - endpoint: API 端点（可选）
                - method: 请求方法（可选）
                - auth_type: 认证方式（可选）
                - icon: 图标 URL（可选）
        
        Returns:
            dict: API 响应
        """
        # 准备请求数据
        data = {
            'name': skill_info.get('name'),
            'username': skill_info.get('username', 'admin'),
            'type': skill_info.get('type', 'function'),
            'version': skill_info.get('version', '1.0.0'),
            'description': skill_info.get('description', ''),
            'summary': skill_info.get('summary', ''),
            'params': json.dumps(skill_info.get('params', {})),
            'returns': json.dumps(skill_info.get('returns', {})),
            'dependencies': json.dumps(skill_info.get('dependencies', [])),
            'risk_level': skill_info.get('risk_level', 'low'),
            'rate_limit': skill_info.get('rate_limit', 0),
            'timeout': skill_info.get('timeout', 30),
            'endpoint': skill_info.get('endpoint'),
            'method': skill_info.get('method', 'POST'),
            'auth_type': skill_info.get('auth_type', 'none'),
            'icon': skill_info.get('icon', '')
        }
        
        # 移除空值
        data = {k: v for k, v in data.items() if v is not None}
        
        return self._request('POST', '/api/skill/create', data=data)
    
    def update_skill(self, updates: Dict) -> Dict[str, Any]:
        """更新技能
        
        Args:
            updates: 更新字段字典，必须包含 id
        
        Returns:
            dict: API 响应
        """
        if 'id' not in updates:
            return {
                'code': 0,
                'msg': '更新技能必须提供 id',
                'data': None
            }
        
        # 准备请求数据
        data = updates.copy()
        
        # JSON 字段序列化
        json_fields = ['params', 'returns', 'dependencies']
        for field in json_fields:
            if field in data and isinstance(data[field], (dict, list)):
                data[field] = json.dumps(data[field])
        
        return self._request('POST', '/api/skill/update', data=data)
    
    def delete_skill(self, skill_id: int) -> Dict[str, Any]:
        """删除技能
        
        Args:
            skill_id: 技能 ID
        
        Returns:
            dict: API 响应
        """
        return self._request('POST', '/api/skill/delete', data={'id': skill_id})
    
    def get_skill_detail(self, skill_id: int) -> Optional[Dict]:
        """获取技能详情
        
        Args:
            skill_id: 技能 ID
        
        Returns:
            dict: 技能详情，不存在则返回 None
        """
        response = self._request('GET', '/api/skill/detail', params={'id': skill_id})
        # 处理两种响应格式：标准格式和直接数据格式
        if response.get('code') == 1:
            return response['data']
        elif 'id' in response:
            # 直接返回数据格式
            return response
        return None
    
    def get_skill_by_name(self, skill_name: str) -> Optional[Dict]:
        """通过名称获取技能
        
        Args:
            skill_name: 技能名称
        
        Returns:
            dict: 技能详情，不存在则返回 None
        """
        # 使用搜索接口
        response = self._request('GET', '/api/skill/search', params={'q': skill_name})
        if response.get('code') == 1:
            list_data = response.get('data', {}).get('list', [])
            for skill in list_data:
                if skill.get('name') == skill_name:
                    # 获取完整详情
                    return self.get_skill_detail(skill['id'])
        return None
    
    def search_skills(self, query: str = '', skill_type: str = None, 
                     page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """搜索技能
        
        Args:
            query: 搜索关键词
            skill_type: 技能类型筛选
            page: 页码
            limit: 每页数量
        
        Returns:
            dict: API 响应
        """
        params = {
            'q': query,
            'type': skill_type,
            'page': page,
            'limit': limit
        }
        
        # 移除空值
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('GET', '/api/skill/search', params=params)
    
    def get_skill_list(self, skill_type: str = None, page: int = 1, 
                      limit: int = 10) -> Dict[str, Any]:
        """获取技能列表
        
        Args:
            skill_type: 技能类型筛选
            page: 页码
            limit: 每页数量
        
        Returns:
            dict: API 响应
        """
        params = {
            'type': skill_type,
            'page': page,
            'limit': limit
        }
        
        # 移除空值
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('GET', '/api/skill/index', params=params)
    
    def get_latest_skills(self, skill_type: str = None, page: int = 1,
                         limit: int = 10) -> Dict[str, Any]:
        """获取最新技能列表
        
        Args:
            skill_type: 技能类型筛选
            page: 页码
            limit: 每页数量
        
        Returns:
            dict: API 响应
        """
        params = {
            'type': skill_type,
            'page': page,
            'limit': limit
        }
        
        # 移除空值
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('GET', '/api/skill/latest', params=params)
    
    def get_hot_skills(self, skill_type: str = None, page: int = 1,
                      limit: int = 10) -> Dict[str, Any]:
        """获取热门技能列表
        
        Args:
            skill_type: 技能类型筛选
            page: 页码
            limit: 每页数量
        
        Returns:
            dict: API 响应
        """
        params = {
            'type': skill_type,
            'page': page,
            'limit': limit
        }
        
        # 移除空值
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('GET', '/api/skill/hot', params=params)
