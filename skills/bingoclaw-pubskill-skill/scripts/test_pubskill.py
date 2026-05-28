#!/usr/bin/env python3
"""
PubSkill 测试脚本

测试各个模块的基本功能
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from extractor import SkillExtractor
from validator import SkillValidator


def test_extractor():
    """测试提取器"""
    print("=" * 60)
    print("测试技能提取器")
    print("=" * 60)
    
    # 测试提取当前技能
    current_dir = Path(__file__).parent.parent
    extractor = SkillExtractor()
    
    try:
        skill_info = extractor.extract(current_dir)
        print(f"\n✅ 提取成功")
        print(f"   技能名称：{skill_info.get('name')}")
        print(f"   技能类型：{skill_info.get('type', 'function')}")
        print(f"   描述：{skill_info.get('description', '')[:100]}...")
        return True
    except Exception as e:
        print(f"\n❌ 提取失败：{e}")
        return False


def test_validator():
    """测试验证器"""
    print("\n" + "=" * 60)
    print("测试技能验证器")
    print("=" * 60)
    
    # 测试技能信息
    skill_info = {
        'name': 'test-skill',
        'username': 'admin',
        'type': 'function',
        'version': '1.0.0',
        'description': '测试技能',
        'risk_level': 'low',
        'timeout': 30
    }
    
    validator = SkillValidator()
    is_valid, errors = validator.validate(skill_info)
    
    if is_valid:
        print(f"\n✅ 验证通过")
        return True
    else:
        print(f"\n❌ 验证失败:")
        for error in errors:
            print(f"   - {error}")
        return False


def test_validator_with_invalid_data():
    """测试验证器（无效数据）"""
    print("\n" + "=" * 60)
    print("测试技能验证器（无效数据）")
    print("=" * 60)
    
    # 测试无效技能信息
    skill_info = {
        'name': '123-invalid',  # 无效：以数字开头
        'type': 'invalid-type',  # 无效：不支持的类型
        'risk_level': 'invalid',  # 无效：不支持的风险等级
    }
    
    validator = SkillValidator()
    is_valid, errors = validator.validate(skill_info)
    
    if not is_valid:
        print(f"\n✅ 正确识别出错误:")
        for error in errors:
            print(f"   - {error}")
        return True
    else:
        print(f"\n❌ 应该验证失败但通过了")
        return False


def test_api_client_structure():
    """测试 API 客户端结构"""
    print("\n" + "=" * 60)
    print("测试 API 客户端结构")
    print("=" * 60)
    
    from api_client import SkillHubAPIClient
    
    try:
        client = SkillHubAPIClient('https://api.example.com')
        print(f"\n✅ API 客户端创建成功")
        print(f"   基础 URL: {client.base_url}")
        print(f"   超时时间：{client.timeout}秒")
        
        # 检查方法是否存在
        methods = ['create_skill', 'update_skill', 'delete_skill', 
                  'get_skill_detail', 'search_skills']
        for method in methods:
            if hasattr(client, method):
                print(f"   ✓ 方法存在：{method}")
            else:
                print(f"   ✗ 方法缺失：{method}")
        
        return True
    except Exception as e:
        print(f"\n❌ 创建失败：{e}")
        return False


def test_github_client_structure():
    """测试 GitHub 客户端结构"""
    print("\n" + "=" * 60)
    print("测试 GitHub 客户端结构")
    print("=" * 60)
    
    from github_client import GitHubClient
    
    try:
        client = GitHubClient(
            token='fake_token',
            owner='baishw',
            repo='baishw.github.io'
        )
        print(f"\n✅ GitHub 客户端创建成功")
        print(f"   仓库：{client.owner}/{client.repo}")
        print(f"   分支：{client.branch}")
        
        # 检查方法是否存在
        methods = ['upload_file', 'upload_directory', 'create_file', 
                  'update_file', 'delete_file']
        for method in methods:
            if hasattr(client, method):
                print(f"   ✓ 方法存在：{method}")
            else:
                print(f"   ✗ 方法缺失：{method}")
        
        return True
    except Exception as e:
        print(f"\n❌ 创建失败：{e}")
        return False


def main():
    """运行所有测试"""
    print("\n🧪 PubSkill 测试套件\n")
    
    results = []
    
    # 运行测试
    results.append(("技能提取器", test_extractor()))
    results.append(("技能验证器（有效数据）", test_validator()))
    results.append(("技能验证器（无效数据）", test_validator_with_invalid_data()))
    results.append(("API 客户端结构", test_api_client_structure()))
    results.append(("GitHub 客户端结构", test_github_client_structure()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计：{passed}/{total} 测试通过")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
