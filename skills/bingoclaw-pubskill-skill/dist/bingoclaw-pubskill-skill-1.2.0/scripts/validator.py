#!/usr/bin/env python3
"""
技能验证器

验证技能信息是否符合 SkillHub 标准
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Tuple


class SkillValidator:
    """技能验证器"""
    
    def __init__(self):
        """初始化验证器"""
        # 有效的技能类型
        self.valid_types = ['function', 'api', 'database', 'workflow']
        
        # 有效的风险等级
        self.valid_risk_levels = ['low', 'medium', 'high', 'critical']
        
        # 有效的请求方法
        self.valid_methods = ['GET', 'POST', 'PUT', 'DELETE']
        
        # 有效的认证方式
        self.valid_auth_types = ['none', 'api_key', 'oauth2', 'token']
        
        # 有效的状态
        self.valid_status = ['normal', 'hidden', 'disabled']
        
        # 名称验证正则
        self.name_pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]*$')
        
        # 版本号验证正则（语义化版本）
        self.version_pattern = re.compile(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.\d+)?)?$')
    
    def validate(self, skill_info: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证技能信息
        
        Args:
            skill_info: 技能信息字典
            
        Returns:
            tuple: (是否通过验证，错误列表)
        """
        errors = []
        
        # 验证必填字段
        self._validate_required_fields(skill_info, errors)
        
        # 验证字段格式
        self._validate_field_formats(skill_info, errors)
        
        # 验证字段值
        self._validate_field_values(skill_info, errors)
        
        # 验证内容完整性
        self._validate_content(skill_info, errors)
        
        return len(errors) == 0, errors
    
    def _validate_required_fields(self, skill_info: Dict[str, Any], 
                                  errors: List[str]) -> None:
        """验证必填字段
        
        Args:
            skill_info: 技能信息字典
            errors: 错误列表
        """
        # name: 技能名称
        if 'name' not in skill_info:
            errors.append("缺少必填字段：name（技能名称）")
        elif not skill_info['name']:
            errors.append("技能名称不能为空")
        
        # username: 提供者用户名
        if 'username' not in skill_info:
            errors.append("缺少必填字段：username（提供者用户名）")
        elif not skill_info['username']:
            errors.append("提供者用户名不能为空")
        
        # type: 技能类型
        if 'type' not in skill_info:
            errors.append("缺少必填字段：type（技能类型）")
        elif not skill_info['type']:
            errors.append("技能类型不能为空")
    
    def _validate_field_formats(self, skill_info: Dict[str, Any], 
                                errors: List[str]) -> None:
        """验证字段格式
        
        Args:
            skill_info: 技能信息字典
            errors: 错误列表
        """
        # 验证名称格式
        if 'name' in skill_info and skill_info['name']:
            name = skill_info['name']
            if not self.name_pattern.match(name):
                errors.append(
                    f"技能名称格式错误：'{name}'，只能包含字母、数字、下划线和连字符，"
                    "且必须以字母开头"
                )
            
            # 检查长度
            if len(name) > 50:
                errors.append(f"技能名称过长：'{name}'，最多 50 个字符")
            
            # 检查是否为保留名称
            reserved_names = ['all', 'list', 'create', 'update', 'delete', 'skill']
            if name.lower() in reserved_names:
                errors.append(f"技能名称 '{name}' 是保留名称，不能使用")
        
        # 验证版本号格式
        if 'version' in skill_info and skill_info['version']:
            version = skill_info['version']
            if not self.version_pattern.match(version):
                errors.append(
                    f"版本号格式错误：'{version}'，应为语义化版本格式（如 1.0.0）"
                )
        
        # 验证描述长度
        if 'description' in skill_info and skill_info['description']:
            description = skill_info['description']
            if len(description) > 2000:
                errors.append(f"描述过长，最多 2000 个字符，当前 {len(description)} 个")
        
        # 验证摘要长度
        if 'summary' in skill_info and skill_info['summary']:
            summary = skill_info['summary']
            if len(summary) > 200:
                errors.append(f"摘要过长，最多 200 个字符，当前 {len(summary)} 个")
    
    def _validate_field_values(self, skill_info: Dict[str, Any], 
                               errors: List[str]) -> None:
        """验证字段值
        
        Args:
            skill_info: 技能信息字典
            errors: 错误列表
        """
        # 验证技能类型
        if 'type' in skill_info and skill_info['type']:
            skill_type = skill_info['type']
            if skill_type not in self.valid_types:
                errors.append(
                    f"无效的技能类型：'{skill_type}'，有效值为：{', '.join(self.valid_types)}"
                )
        
        # 验证风险等级
        if 'risk_level' in skill_info and skill_info['risk_level']:
            risk_level = skill_info['risk_level']
            if risk_level not in self.valid_risk_levels:
                errors.append(
                    f"无效的风险等级：'{risk_level}'，有效值为：{', '.join(self.valid_risk_levels)}"
                )
        
        # 验证请求方法
        if 'method' in skill_info and skill_info['method']:
            method = skill_info['method']
            if method.upper() not in self.valid_methods:
                errors.append(
                    f"无效的请求方法：'{method}'，有效值为：{', '.join(self.valid_methods)}"
                )
        
        # 验证认证方式
        if 'auth_type' in skill_info and skill_info['auth_type']:
            auth_type = skill_info['auth_type']
            if auth_type not in self.valid_auth_types:
                errors.append(
                    f"无效的认证方式：'{auth_type}'，有效值为：{', '.join(self.valid_auth_types)}"
                )
        
        # 验证状态
        if 'status' in skill_info and skill_info['status']:
            status = skill_info['status']
            if status not in self.valid_status:
                errors.append(
                    f"无效的状态：'{status}'，有效值为：{', '.join(self.valid_status)}"
                )
        
        # 验证 rate_limit
        if 'rate_limit' in skill_info and skill_info['rate_limit'] is not None:
            rate_limit = skill_info['rate_limit']
            if not isinstance(rate_limit, int) or rate_limit < 0:
                errors.append(f"调用频率限制必须是非负整数：{rate_limit}")
        
        # 验证 timeout
        if 'timeout' in skill_info and skill_info['timeout'] is not None:
            timeout = skill_info['timeout']
            if not isinstance(timeout, int) or timeout <= 0:
                errors.append(f"超时时间必须是正整数：{timeout}")
        
        # 验证 endpoint（API 类型必填）
        if skill_info.get('type') == 'api':
            if 'endpoint' not in skill_info or not skill_info.get('endpoint'):
                errors.append("API 类型技能必须提供 endpoint（API 端点 URL）")
            elif not skill_info['endpoint'].startswith(('http://', 'https://')):
                errors.append("API 端点必须是完整的 URL（以 http:// 或 https:// 开头）")
    
    def _validate_content(self, skill_info: Dict[str, Any], 
                         errors: List[str]) -> None:
        """验证内容完整性
        
        Args:
            skill_info: 技能信息字典
            errors: 错误列表
        """
        # 检查是否包含敏感信息
        if 'description' in skill_info:
            description = skill_info['description']
            sensitive_patterns = [
                r'password\s*[=:]\s*\S+',
                r'secret\s*[=:]\s*\S+',
                r'token\s*[=:]\s*\S+',
                r'api[_-]?key\s*[=:]\s*\S+',
            ]
            
            for pattern in sensitive_patterns:
                if re.search(pattern, description, re.IGNORECASE):
                    errors.append("描述中包含敏感信息（密码、密钥、Token 等），请移除")
                    break
        
        # 检查 params 和 returns 是否为有效的 JSON Schema
        if 'params' in skill_info:
            params = skill_info['params']
            if isinstance(params, str):
                try:
                    import json
                    params = json.loads(params)
                except json.JSONDecodeError:
                    errors.append("params 不是有效的 JSON 格式")
        
        if 'returns' in skill_info:
            returns = skill_info['returns']
            if isinstance(returns, str):
                try:
                    import json
                    returns = json.loads(returns)
                except json.JSONDecodeError:
                    errors.append("returns 不是有效的 JSON 格式")
        
        # 检查 dependencies 是否为列表
        if 'dependencies' in skill_info:
            dependencies = skill_info['dependencies']
            if isinstance(dependencies, str):
                try:
                    import json
                    dependencies = json.loads(dependencies)
                except json.JSONDecodeError:
                    errors.append("dependencies 不是有效的 JSON 格式")
            
            if not isinstance(dependencies, list):
                errors.append("dependencies 必须是数组格式")
    
    def validate_skill_directory(self, skill_dir: Path) -> Tuple[bool, List[str]]:
        """验证技能目录
        
        Args:
            skill_dir: 技能目录路径
            
        Returns:
            tuple: (是否通过验证，错误列表)
        """
        errors = []
        
        # 检查目录是否存在
        if not skill_dir.exists():
            errors.append(f"技能目录不存在：{skill_dir}")
            return False, errors
        
        if not skill_dir.is_dir():
            errors.append(f"不是目录：{skill_dir}")
            return False, errors
        
        # 检查 SKILL.md 文件
        skill_md = skill_dir / 'SKILL.md'
        if not skill_md.exists():
            errors.append("缺少 SKILL.md 文件")
        
        # 检查 scripts 目录
        scripts_dir = skill_dir / 'scripts'
        if not scripts_dir.exists():
            errors.append("缺少 scripts 目录")
        elif not scripts_dir.is_dir():
            errors.append("scripts 必须是目录")
        else:
            # 检查是否有 Python 脚本
            py_files = list(scripts_dir.glob('*.py'))
            if not py_files:
                errors.append("scripts 目录中没有 Python 脚本文件")
        
        # 检查是否有配置文件
        config_dir = skill_dir / 'config'
        if not config_dir.exists():
            errors.append("缺少 config 目录")
        
        # 检查是否有文档
        docs_dir = skill_dir / 'docs'
        if not docs_dir.exists():
            # 警告级别，不添加错误
            pass
        
        # 检查隐藏文件
        hidden_files = [f for f in skill_dir.iterdir() if f.name.startswith('.')]
        if hidden_files:
            # 警告级别
            pass
        
        return len(errors) == 0, errors
