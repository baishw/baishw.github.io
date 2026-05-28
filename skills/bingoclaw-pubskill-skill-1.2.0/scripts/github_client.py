#!/usr/bin/env python3
"""
GitHub 客户端

用于将技能包上传到 GitHub 仓库（baishw.github.io）
"""

import base64
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import requests


class GitHubClient:
    """GitHub API 客户端"""
    
    def __init__(self, token: str, owner: str = 'baishw', 
                 repo: str = 'baishw.github.io', branch: str = 'main'):
        """初始化 GitHub 客户端
        
        Args:
            token: GitHub Personal Access Token
            owner: 仓库所有者
            repo: 仓库名称
            branch: 分支名称
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        })
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """发送 HTTP 请求
        
        Args:
            method: HTTP 方法
            endpoint: API 端点
            data: 请求数据
            
        Returns:
            dict: API 响应
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, timeout=30)
            else:
                raise ValueError(f"不支持的 HTTP 方法：{method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        
        except requests.exceptions.Timeout:
            raise Exception("GitHub API 请求超时")
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get('message', str(e)) if e.response.content else str(e)
            raise Exception(f"GitHub API 错误：{error_msg}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"GitHub 请求失败：{str(e)}")
    
    def get_file(self, path: str) -> Optional[Dict]:
        """获取文件信息
        
        Args:
            path: 文件路径
            
        Returns:
            dict: 文件信息，不存在则返回 None
        """
        try:
            response = self._request('GET', f'/contents/{path}')
            return response
        except Exception:
            return None
    
    def create_file(self, path: str, content: str, message: str) -> Dict:
        """创建文件
        
        Args:
            path: 文件路径
            content: 文件内容
            message: 提交信息
            
        Returns:
            dict: API 响应
        """
        data = {
            'message': message,
            'content': base64.b64encode(content.encode('utf-8')).decode('utf-8'),
            'branch': self.branch
        }
        
        return self._request('PUT', f'/contents/{path}', data=data)
    
    def update_file(self, path: str, content: str, sha: str, message: str) -> Dict:
        """更新文件
        
        Args:
            path: 文件路径
            content: 文件内容
            sha: 文件 SHA
            message: 提交信息
            
        Returns:
            dict: API 响应
        """
        data = {
            'message': message,
            'content': base64.b64encode(content.encode('utf-8')).decode('utf-8'),
            'sha': sha,
            'branch': self.branch
        }
        
        return self._request('PUT', f'/contents/{path}', data=data)
    
    def delete_file(self, path: str, sha: str, message: str) -> Dict:
        """删除文件
        
        Args:
            path: 文件路径
            sha: 文件 SHA
            message: 提交信息
            
        Returns:
            dict: API 响应
        """
        data = {
            'message': message,
            'sha': sha,
            'branch': self.branch
        }
        
        return self._request('DELETE', f'/contents/{path}', data=data)
    
    def upload_file(self, source_path: Path, target_path: str, 
                   message: Optional[str] = None) -> Dict:
        """上传单个文件
        
        Args:
            source_path: 源文件路径
            target_path: 目标路径（GitHub 仓库中的路径）
            message: 提交信息
            
        Returns:
            dict: API 响应
        """
        if not source_path.exists():
            raise ValueError(f"文件不存在：{source_path}")
        
        # 读取文件内容
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文件是否已存在
        existing = self.get_file(target_path)
        
        if message is None:
            message = f"Upload {target_path}"
        
        if existing:
            # 更新文件
            return self.update_file(target_path, content, existing['sha'], message)
        else:
            # 创建文件
            return self.create_file(target_path, content, message)
    
    def upload_directory(self, source_dir: Path, target_path: str,
                        message: Optional[str] = None) -> str:
        """上传整个目录
        
        Args:
            source_dir: 源目录路径
            target_path: 目标路径（GitHub 仓库中的路径）
            message: 提交信息
            
        Returns:
            str: 上传后的 URL
        """
        if not source_dir.exists():
            raise ValueError(f"目录不存在：{source_dir}")
        if not source_dir.is_dir():
            raise ValueError(f"不是目录：{source_dir}")
        
        # 收集所有文件
        files_to_upload = []
        for root, dirs, files in os.walk(source_dir):
            # 跳过隐藏目录和特定目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                # 跳过隐藏文件和特定文件
                if file.startswith('.') or file.endswith('.pyc'):
                    continue
                
                source_path = Path(root) / file
                relative_path = source_path.relative_to(source_dir)
                target_file_path = f"{target_path}/{relative_path}"
                
                files_to_upload.append((source_path, target_file_path))
        
        if not files_to_upload:
            raise ValueError(f"目录为空：{source_dir}")
        
        # 上传文件
        upload_count = 0
        for source_path, target_path in files_to_upload:
            try:
                file_message = f"Upload {target_path}" if message is None else f"{message}: {target_path}"
                self.upload_file(source_path, target_path, file_message)
                upload_count += 1
                print(f"   ✓ 上传：{target_path}")
            except Exception as e:
                print(f"   ✗ 上传失败 {target_path}: {e}")
        
        print(f"\n   共上传 {upload_count}/{len(files_to_upload)} 个文件")
        
        # 返回 GitHub Pages URL
        return f"https://{self.owner}.github.io/{self.repo}/{target_path}/"
    
    def create_tree(self, files: List[Dict], base_tree: Optional[str] = None) -> Dict:
        """创建 Git 树
        
        Args:
            files: 文件列表，每个元素包含 path, content, mode
            base_tree: 基础树 SHA
            
        Returns:
            dict: 创建的树信息
        """
        tree_data = []
        for file in files:
            # 创建 blob
            blob_data = {
                'content': file['content']
            }
            blob_response = self._request('POST', '/git/blobs', data=blob_data)
            
            tree_data.append({
                'path': file['path'],
                'mode': file.get('mode', '100644'),
                'type': 'blob',
                'sha': blob_response['sha']
            })
        
        data = {
            'tree': tree_data
        }
        
        if base_tree:
            data['base_tree'] = base_tree
        
        return self._request('POST', '/git/trees', data=data)
    
    def create_commit(self, tree_sha: str, message: str, 
                     parents: List[str]) -> Dict:
        """创建提交
        
        Args:
            tree_sha: 树 SHA
            message: 提交信息
            parents: 父提交 SHA 列表
            
        Returns:
            dict: 提交信息
        """
        data = {
            'message': message,
            'tree': tree_sha,
            'parents': parents
        }
        
        return self._request('POST', '/git/commits', data=data)
    
    def update_ref(self, ref: str, sha: str, force: bool = False) -> Dict:
        """更新引用
        
        Args:
            ref: 引用名称（如 heads/main）
            sha: 新的 SHA
            force: 是否强制更新
            
        Returns:
            dict: 更新后的引用信息
        """
        data = {
            'sha': sha,
            'force': force
        }
        
        return self._request('PATCH', f'/git/refs/{ref}', data=data)
