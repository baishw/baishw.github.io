#!/usr/bin/env python3
"""
PubSkill - 技能发布工具主程序

功能：
1. 提取目标技能的信息
2. 通过技能管理后台的 API 将技能添加到技能管理系统
3. 技能包上传到 baishw.github.io 网站
4. 为用户返回一个技能分享页 URL
"""

import argparse
import json
import os
import sys
from pathlib import Path

from api_client import SkillHubAPIClient
from extractor import SkillExtractor
from github_client import GitHubClient
from validator import SkillValidator


class PubSkill:
    """技能发布主类"""
    
    def __init__(self, config=None, auto_login=True):
        """初始化 PubSkill
        
        Args:
            config: 配置字典，可从配置文件或环境变量加载
            auto_login: 是否自动登录
        """
        self.config = config or self._load_config()
        self.api_client = SkillHubAPIClient(self.config['api_url'])
        self.github_client = GitHubClient(
            token=self.config.get('github_token'),
            owner=self.config.get('github_owner', 'baishw'),
            repo=self.config.get('github_repo', 'baishw.github.io'),
            branch=self.config.get('github_branch', 'main')
        )
        self.extractor = SkillExtractor()
        self.validator = SkillValidator()
        self.token = None
        
        # 自动登录
        if auto_login:
            self.login()
    
    def _load_config(self):
        """加载配置
        
        优先级：
        1. 配置文件 (.pubskill.json)
        2. 环境变量
        3. 默认值
        
        首次安装时会检查必要的登录凭据配置。
        """
        config = {}
        missing_configs = []
        
        # 尝试加载配置文件
        config_file = Path('.pubskill.json')
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
        
        # 环境变量覆盖
        if os.getenv('SKILLHUB_API_URL'):
            config['api_url'] = os.getenv('SKILLHUB_API_URL')
        if os.getenv('SKILLHUB_USERNAME'):
            config['username'] = os.getenv('SKILLHUB_USERNAME')
        if os.getenv('SKILLHUB_PASSWORD'):
            config['password'] = os.getenv('SKILLHUB_PASSWORD')
        if os.getenv('GITHUB_TOKEN'):
            config['github_token'] = os.getenv('GITHUB_TOKEN')
        if os.getenv('GITHUB_OWNER'):
            config['github_owner'] = os.getenv('GITHUB_OWNER')
        if os.getenv('GITHUB_REPO'):
            config['github_repo'] = os.getenv('GITHUB_REPO')
        if os.getenv('GITHUB_BRANCH'):
            config['github_branch'] = os.getenv('GITHUB_BRANCH')
        
        # 默认值
        if 'api_url' not in config:
            config['api_url'] = 'https://skill.cxus.cn'
        if 'github_token' not in config or not config['github_token']:
            # 从环境变量获取 GitHub Token
            env_token = os.getenv('SKILLHUB_GITHUB_TOKEN')
            if env_token:
                config['github_token'] = env_token
            else:
                raise ValueError("GitHub Token 未配置，请设置 SKILLHUB_GITHUB_TOKEN 环境变量或在配置文件中设置 github_token")
        if 'github_owner' not in config:
            config['github_owner'] = 'baishw'
        if 'github_repo' not in config:
            config['github_repo'] = 'baishw.github.io'
        if 'github_branch' not in config:
            config['github_branch'] = 'main'
        if 'skill_path' not in config:
            config['skill_path'] = 'skills'
        
        # 检查必要配置
        if 'username' not in config or not config['username']:
            missing_configs.append('SKILLHUB_USERNAME')
        if 'password' not in config or not config['password']:
            missing_configs.append('SKILLHUB_PASSWORD')
        
        # 如果缺少配置，输出提示信息
        if missing_configs:
            self._print_config_reminder(missing_configs)
        
        return config
    
    def _print_config_reminder(self, missing_configs):
        """打印配置提醒信息"""
        print("════════════════════════════════════════════════════════════════════════")
        print("⚠️  首次使用 PubSkill 技能，请完成以下配置")
        print("════════════════════════════════════════════════════════════════════════")
        print("")
        print("1️⃣  复制配置示例文件：")
        print("    cp .pubskill.example.json .pubskill.json")
        print("")
        print("2️⃣  编辑 .pubskill.json，填入你的凭据：")
        print("    必需填写：")
        if 'SKILLHUB_USERNAME' in missing_configs:
            print("      - username: 你的 SkillHub 用户名")
        if 'SKILLHUB_PASSWORD' in missing_configs:
            print("      - password: 你的 SkillHub 密码")
        print("")
        print("    可选配置：")
        print("      - github_token: GitHub Personal Access Token（需设置）")
        print("      - github_owner: GitHub 仓库所有者（默认 baishw）")
        print("      - github_repo: GitHub 仓库名称（默认 baishw.github.io）")
        print("      - github_branch: GitHub 分支（默认 main）")
        print("      - skill_path: 技能存储路径（默认 skills）")
        print("")
        print("3️⃣  或者使用环境变量：")
        if 'SKILLHUB_USERNAME' in missing_configs:
            print("    export SKILLHUB_USERNAME='your_username'")
        if 'SKILLHUB_PASSWORD' in missing_configs:
            print("    export SKILLHUB_PASSWORD='your_password'")
        print("")
        print("════════════════════════════════════════════════════════════════════════")
        print("💡 提示：.pubskill.json 已在 .gitignore 中，不会提交到仓库")
        print("════════════════════════════════════════════════════════════════════════")
        print("")
    
    def login(self):
        """登录 SkillHub
        
        使用配置中的用户名和密码进行登录，获取 Token。
        如果缺少凭据，会输出提醒信息。
        """
        username = self.config.get('username')
        password = self.config.get('password')
        
        if not username or not password:
            print("⚠️ 未配置登录凭据，部分功能可能受限")
            print("   请设置 SKILLHUB_USERNAME 和 SKILLHUB_PASSWORD 环境变量")
            return False
        
        try:
            response = self.api_client._request(
                'POST', '/api/user/login',
                data={'account': username, 'password': password}
            )
            
            if response.get('code') == 1:
                self.token = response['data']['userinfo']['token']
                self.api_client.session.headers.update({'Token': self.token})
                print(f"✅ 登录成功")
                print(f"   用户：{response['data']['userinfo'].get('username')}")
                print(f"   Token：{self.token[:20]}...")
                return True
            else:
                print(f"❌ 登录失败：{response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"❌ 登录异常：{e}")
            return False
    
    def extract(self, skill_dir, output=None):
        """提取技能信息
        
        Args:
            skill_dir: 技能目录路径
            output: 输出文件路径（可选）
            
        Returns:
            dict: 技能信息字典
        """
        # 验证技能目录名称（技能名称）
        skill_dir = Path(skill_dir)
        if not skill_dir.exists():
            raise ValueError(f"技能目录不存在：{skill_dir}")
        
        skill_name = skill_dir.name
        if not skill_name or skill_name.startswith('.'):
            raise ValueError(f"无效的技能名称：{skill_name}")
        
        skill_info = self.extractor.extract(skill_dir)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(skill_info, f, indent=2, ensure_ascii=False)
            print(f"✅ 技能信息已保存到：{output}")
        
        return skill_info
    
    def verify(self, skill_info=None, skill_dir=None):
        """验证技能信息
        
        Args:
            skill_info: 技能信息字典（可选）
            skill_dir: 技能目录路径（可选）
            
        Returns:
            bool: 验证是否通过
        """
        if skill_info is None and skill_dir is not None:
            skill_info = self.extractor.extract(Path(skill_dir))
        
        if skill_info is None:
            raise ValueError("未提供技能信息或技能目录")
        
        is_valid, errors = self.validator.validate(skill_info)
        
        if is_valid:
            print("✅ 技能验证通过")
            return True
        else:
            print("❌ 技能验证失败:")
            for error in errors:
                print(f"  - {error}")
            return False
    
    def register(self, skill_info):
        """注册技能到 SkillHub
        
        Args:
            skill_info: 技能信息字典
            
        Returns:
            dict: API 响应数据
        """
        response = self.api_client.create_skill(skill_info)
        
        if response.get('code') == 1:
            print(f"✅ 技能注册成功")
            print(f"   技能 ID: {response['data']['id']}")
            print(f"   技能名称：{response['data']['name']}")
        else:
            print(f"❌ 技能注册失败：{response.get('msg', '未知错误')}")
        
        return response
    
    def upload(self, skill_dir):
        """上传技能包到 GitHub
        
        Args:
            skill_dir: 技能目录路径
            
        Returns:
            str: 上传后的 URL
        """
        skill_dir = Path(skill_dir)
        skill_name = skill_dir.name
        
        # 构建目标路径
        target_path = f"{self.config['skill_path']}/{skill_name}"
        
        # 上传文件
        upload_url = self.github_client.upload_directory(
            source_dir=skill_dir,
            target_path=target_path
        )
        
        print(f"✅ 技能包上传成功")
        print(f"   目标路径：{target_path}")
        
        return upload_url
    
    def share(self, skill_name, skill_id=None):
        """生成技能分享链接
        
        Args:
            skill_name: 技能名称
            skill_id: 技能 ID（可选）
            
        Returns:
            dict: 分享链接信息
        """
        share_url = f"https://baishw.github.io/skills/{skill_name}/"
        api_url = f"{self.config['api_url']}/api/skill/detail?id={skill_id}" if skill_id else None
        
        print("\n✅ 技能发布成功！")
        print(f"\n技能名称：{skill_name}")
        if skill_id:
            print(f"技能 ID: {skill_id}")
        print(f"分享链接：{share_url}")
        if api_url:
            print(f"API 详情：{api_url}")
        
        return {
            'skill_name': skill_name,
            'skill_id': skill_id,
            'share_url': share_url,
            'api_url': api_url
        }
    
    def publish(self, skill_dir, skip_verify=False):
        """发布技能（完整流程）
        
        Args:
            skill_dir: 技能目录路径
            skip_verify: 是否跳过验证
            
        Returns:
            dict: 发布结果
        """
        print(f"🚀 开始发布技能：{skill_dir}")
        print("=" * 60)
        
        # 步骤 1: 提取技能信息
        print("\n📋 步骤 1/5: 提取技能信息")
        try:
            skill_info = self.extractor.extract(Path(skill_dir))
            
            # 如果技能信息中没有 username，使用配置中的用户名
            if 'username' not in skill_info or not skill_info['username']:
                skill_info['username'] = self.config.get('username')
            
            print(f"   技能名称：{skill_info['name']}")
            print(f"   技能类型：{skill_info.get('type', 'function')}")
            print(f"   提供者：{skill_info.get('username')}")
        except Exception as e:
            print(f"❌ 提取技能信息失败：{e}")
            import traceback
            traceback.print_exc()
            raise
        
        # 步骤 2: 验证技能
        if not skip_verify:
            print("\n✓ 步骤 2/5: 验证技能配置")
            if not self.verify(skill_info=skill_info):
                raise ValueError("技能验证失败，无法继续发布")
        else:
            print("\n⊘ 步骤 2/5: 跳过验证")
        
        # 步骤 3: 注册或更新技能到 API
        print("\n📝 步骤 3/5: 注册/更新到 SkillHub API")
        
        # 检查技能是否已存在
        existing_skill = self.api_client.get_skill_by_name(skill_info['name'])
        
        if existing_skill:
            # 技能已存在，更新技能信息（包括版本号）
            print(f"   技能已存在，更新技能信息...")
            updates = {
                'id': existing_skill['id'],
                'name': skill_info.get('name'),
                'type': skill_info.get('type', 'function'),
                'version': skill_info.get('version', '1.0.0'),
                'description': skill_info.get('description', ''),
                'summary': skill_info.get('summary', ''),
                'params': skill_info.get('params', {}),
                'returns': skill_info.get('returns', {}),
                'dependencies': skill_info.get('dependencies', []),
                'risk_level': skill_info.get('risk_level', 'low'),
                'rate_limit': skill_info.get('rate_limit', 0),
                'timeout': skill_info.get('timeout', 30),
                'endpoint': skill_info.get('endpoint'),
                'method': skill_info.get('method', 'POST'),
                'auth_type': skill_info.get('auth_type', 'none'),
                'icon': skill_info.get('icon', '')
            }
            update_result = self.api_client.update_skill(updates)
            if update_result.get('code') != 1:
                raise ValueError(f"技能更新失败：{update_result.get('msg', '未知错误')}")
            skill_id = existing_skill['id']
            print(f"   ✅ 技能更新成功")
            print(f"   技能 ID: {skill_id}")
            print(f"   版本号: {skill_info.get('version', '1.0.0')}")
        else:
            # 技能不存在，创建新技能
            register_result = self.register(skill_info)
            if register_result.get('code') != 1:
                raise ValueError(f"技能注册失败：{register_result.get('msg', '未知错误')}")
            skill_id = register_result['data']['id']
            print(f"   ✅ 技能注册成功")
            print(f"   技能 ID: {skill_id}")
            print(f"   版本号: {skill_info.get('version', '1.0.0')}")
        
        # 步骤 4: 上传技能包
        print("\n📤 步骤 4/5: 上传技能包到 GitHub")
        self.upload(skill_dir)
        
        # 步骤 5: 生成分享链接
        print("\n🔗 步骤 5/5: 生成分享链接")
        share_info = self.share(skill_info['name'], skill_id)
        
        print("\n" + "=" * 60)
        print("🎉 发布完成！")
        
        return {
            'success': True,
            'skill_info': skill_info,
            'skill_id': skill_id,
            'share_info': share_info
        }
    
    def update(self, skill_name, skill_dir=None, updates=None):
        """更新技能
        
        Args:
            skill_name: 技能名称
            skill_dir: 技能目录路径（可选）
            updates: 更新字段字典（可选）
        """
        # 获取技能详情
        detail = self.api_client.get_skill_by_name(skill_name)
        if not detail:
            raise ValueError(f"技能不存在：{skill_name}")
        
        skill_id = detail['id']
        
        # 更新技能信息
        if updates:
            updates['id'] = skill_id
            result = self.api_client.update_skill(updates)
            if result.get('code') == 1:
                print(f"✅ 技能信息更新成功")
            else:
                print(f"❌ 技能信息更新失败：{result.get('msg', '未知错误')}")
        
        # 重新上传技能包
        if skill_dir:
            self.upload(skill_dir)
        
        print(f"✅ 技能 '{skill_name}' 更新完成")
    
    def delete(self, skill_name):
        """删除技能
        
        Args:
            skill_name: 技能名称
        """
        # 获取技能详情
        detail = self.api_client.get_skill_by_name(skill_name)
        if not detail:
            raise ValueError(f"技能不存在：{skill_name}")
        
        skill_id = detail['id']
        
        # 删除技能
        result = self.api_client.delete_skill(skill_id)
        if result.get('code') == 1:
            print(f"✅ 技能 '{skill_name}' 已删除")
        else:
            print(f"❌ 技能删除失败：{result.get('msg', '未知错误')}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='PubSkill - 技能发布工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # extract 命令
    extract_parser = subparsers.add_parser('extract', help='提取技能信息')
    extract_parser.add_argument('--skill-dir', required=True, help='技能目录路径')
    extract_parser.add_argument('--output', help='输出文件路径')
    
    # verify 命令
    verify_parser = subparsers.add_parser('verify', help='验证技能信息')
    verify_parser.add_argument('--skill-dir', help='技能目录路径')
    verify_parser.add_argument('--skill-info', help='技能信息 JSON 文件')
    
    # register 命令
    register_parser = subparsers.add_parser('register', help='注册技能到 API')
    register_parser.add_argument('--skill-info', required=True, help='技能信息 JSON 文件')
    
    # upload 命令
    upload_parser = subparsers.add_parser('upload', help='上传技能包')
    upload_parser.add_argument('--skill-dir', required=True, help='技能目录路径')
    
    # share 命令
    share_parser = subparsers.add_parser('share', help='生成分享链接')
    share_parser.add_argument('--skill-name', required=True, help='技能名称')
    share_parser.add_argument('--skill-id', type=int, help='技能 ID')
    
    # publish 命令
    publish_parser = subparsers.add_parser('publish', help='发布技能（完整流程）')
    publish_parser.add_argument('--skill-dir', required=True, help='技能目录路径')
    publish_parser.add_argument('--skip-verify', action='store_true', help='跳过验证')
    
    # update 命令
    update_parser = subparsers.add_parser('update', help='更新技能')
    update_parser.add_argument('--skill-name', required=True, help='技能名称')
    update_parser.add_argument('--skill-dir', help='技能目录路径')
    
    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除技能')
    delete_parser.add_argument('--skill-name', required=True, help='技能名称')
    
    args = parser.parse_args()
    
    try:
        pubskill = PubSkill()
        
        if args.command == 'extract':
            skill_info = pubskill.extract(args.skill_dir, args.output)
            print(json.dumps(skill_info, indent=2, ensure_ascii=False))
        
        elif args.command == 'verify':
            if args.skill_info:
                with open(args.skill_info, 'r', encoding='utf-8') as f:
                    skill_info = json.load(f)
                pubskill.verify(skill_info=skill_info)
            elif args.skill_dir:
                pubskill.verify(skill_dir=args.skill_dir)
            else:
                print("❌ 请提供 --skill-info 或 --skill-dir")
        
        elif args.command == 'register':
            with open(args.skill_info, 'r', encoding='utf-8') as f:
                skill_info = json.load(f)
            pubskill.register(skill_info)
        
        elif args.command == 'upload':
            pubskill.upload(args.skill_dir)
        
        elif args.command == 'share':
            pubskill.share(args.skill_name, args.skill_id)
        
        elif args.command == 'publish':
            result = pubskill.publish(args.skill_dir, args.skip_verify)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'update':
            pubskill.update(args.skill_name, args.skill_dir)
        
        elif args.command == 'delete':
            pubskill.delete(args.skill_name)
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
