#!/usr/bin/env python3
"""
技能信息提取器

从技能目录和 SKILL.md 文件中提取技能信息
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, List


class SkillExtractor:
    """技能信息提取器"""
    
    def __init__(self):
        """初始化提取器"""
        pass
    
    def extract(self, skill_dir: Path) -> Dict[str, Any]:
        """从技能目录提取信息
        
        Args:
            skill_dir: 技能目录路径
            
        Returns:
            dict: 技能信息字典
        """
        skill_info = {
            'name': skill_dir.name,
            'type': 'function',  # 默认类型
            'version': '1.0.0',
        }
        
        # 提取 SKILL.md 中的信息
        skill_md_path = skill_dir / 'SKILL.md'
        if skill_md_path.exists():
            md_info = self._extract_from_markdown(skill_md_path)
            skill_info.update(md_info)
        
        # 提取其他配置文件
        config_path = skill_dir / 'config' / 'bingoclaw.json'
        if config_path.exists():
            config_info = self._extract_from_config(config_path)
            skill_info.update(config_info)
        
        # 提取脚本信息
        scripts_dir = skill_dir / 'scripts'
        if scripts_dir.exists():
            script_info = self._extract_from_scripts(scripts_dir)
            skill_info.update(script_info)
        
        return skill_info
    
    def _extract_from_markdown(self, skill_md_path: Path) -> Dict[str, Any]:
        """从 SKILL.md 文件提取信息
        
        Args:
            skill_md_path: SKILL.md 文件路径
            
        Returns:
            dict: 提取的信息
        """
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = {}
        
        # 解析 YAML front matter
        front_matter = self._parse_front_matter(content)
        if front_matter:
            # 基本信息
            if 'name' in front_matter:
                info['name'] = front_matter['name']
            if 'description' in front_matter:
                info['description'] = front_matter['description']
            
            # 元数据
            metadata = front_matter.get('metadata', {})
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except json.JSONDecodeError:
                    metadata = {}
            
            openclaw_meta = metadata.get('openclaw', {})
            
            # 从 metadata 提取
            if 'skillKey' in openclaw_meta:
                info['name'] = openclaw_meta['skillKey']
            
            # 安装依赖
            install_list = openclaw_meta.get('install', [])
            dependencies = []
            for install in install_list:
                if install.get('kind') == 'pip' and 'package' in install:
                    dependencies.append(install['package'])
            
            if dependencies:
                info['dependencies'] = dependencies
        
        # 提取描述
        if 'description' not in info:
            description = self._extract_description(content)
            if description:
                info['description'] = description
        
        # 提取摘要
        summary = self._extract_summary(content)
        if summary:
            info['summary'] = summary
        
        # 提取使用场景（作为 params 和 returns 的参考）
        usage_scenarios = self._extract_usage_scenarios(content)
        if usage_scenarios:
            info['usage_scenarios'] = usage_scenarios
        
        return info
    
    def _parse_front_matter(self, content: str) -> Optional[Dict]:
        """解析 YAML front matter
        
        Args:
            content: 文件内容
            
        Returns:
            dict: 解析后的数据
        """
        # 匹配 front matter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        yaml_content = match.group(1)
        
        # 简单的 YAML 解析（处理常见格式）
        result = {}
        current_key = None
        current_indent = 0
        
        for line in yaml_content.split('\n'):
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # 计算缩进
            indent = len(line) - len(line.lstrip())
            line_content = line.strip()
            
            # 键值对
            if ':' in line_content:
                key, _, value = line_content.partition(':')
                key = key.strip()
                value = value.strip()
                
                if indent == 0:
                    current_key = key
                    if value:
                        # 简单值
                        if value.startswith('{') or value.startswith('['):
                            # JSON 格式
                            try:
                                result[key] = json.loads(value)
                            except json.JSONDecodeError:
                                result[key] = value
                        elif value.startswith('"') and value.endswith('"'):
                            result[key] = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            result[key] = value[1:-1]
                        elif value.lower() in ('true', 'false'):
                            result[key] = value.lower() == 'true'
                        elif value.isdigit():
                            result[key] = int(value)
                        else:
                            result[key] = value
                    else:
                        # 嵌套结构
                        result[key] = {}
                else:
                    # 嵌套键值对
                    if current_key and isinstance(result.get(current_key), dict):
                        if value:
                            if value.startswith('{') or value.startswith('['):
                                try:
                                    result[current_key][key] = json.loads(value)
                                except json.JSONDecodeError:
                                    result[current_key][key] = value
                            else:
                                result[current_key][key] = value
        
        return result
    
    def _extract_description(self, content: str) -> Optional[str]:
        """提取描述信息
        
        Args:
            content: 文件内容
            
        Returns:
            str: 描述文本
        """
        # 尝试从第一个段落提取
        lines = content.split('\n')
        in_section = False
        description_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # 跳过 front matter
            if stripped.startswith('---'):
                in_section = not in_section
                continue
            
            if in_section:
                continue
            
            # 找到第一个标题后的内容
            if stripped.startswith('# '):
                continue
            
            # 收集段落
            if stripped and not stripped.startswith('#'):
                description_lines.append(stripped)
            elif description_lines and not stripped:
                # 空行结束
                break
        
        if description_lines:
            return ' '.join(description_lines[:3])  # 最多 3 行
        
        return None
    
    def _extract_summary(self, content: str) -> Optional[str]:
        """提取摘要信息
        
        Args:
            content: 文件内容
            
        Returns:
            str: 摘要文本
        """
        # 尝试从描述中提取第一句
        description = self._extract_description(content)
        if description:
            # 取第一句作为摘要
            sentences = description.replace('。', '.').split('.')
            if sentences:
                return sentences[0].strip() + '.'
        
        return None
    
    def _extract_usage_scenarios(self, content: str) -> Dict[str, List[str]]:
        """提取使用场景
        
        Args:
            content: 文件内容
            
        Returns:
            dict: 使用场景列表
        """
        scenarios = {
            'use': [],
            'dont_use': []
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            stripped = line.strip()
            
            if '✅ **USE when:**' in stripped:
                current_section = 'use'
            elif "❌ **DON'T use when:**" in stripped:
                current_section = 'dont_use'
            elif stripped.startswith('- ') and current_section:
                # 提取列表项
                item = stripped[2:].strip()
                scenarios[current_section].append(item)
        
        return scenarios
    
    def _extract_from_config(self, config_path: Path) -> Dict[str, Any]:
        """从配置文件提取信息
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            dict: 提取的信息
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            info = {}
            
            # 提取技能类型
            if 'type' in config:
                info['type'] = config['type']
            
            # 提取版本
            if 'version' in config:
                info['version'] = config['version']
            
            # 提取参数定义
            if 'params' in config:
                info['params'] = config['params']
            
            # 提取返回值定义
            if 'returns' in config:
                info['returns'] = config['returns']
            
            return info
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _extract_from_scripts(self, scripts_dir: Path) -> Dict[str, Any]:
        """从脚本目录提取信息
        
        Args:
            scripts_dir: 脚本目录路径
            
        Returns:
            dict: 提取的信息
        """
        info = {}
        
        # 统计脚本文件
        script_files = list(scripts_dir.glob('*.py'))
        if script_files:
            info['script_count'] = len(script_files)
            
            # 尝试从 main.py 提取
            main_py = scripts_dir / 'main.py'
            if main_py.exists():
                with open(main_py, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取 docstring
                docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
                if docstring_match:
                    info['script_description'] = docstring_match.group(1).strip()[:200]
        
        return info
