#!/usr/bin/env python3
"""
SkillHub API 测试脚本

参考 tests/test_skill_create.php 和 docs/cxus_API.md 完善技能创建调用
API域名: https://skill.cxus.cn
测试账号: skillpuber / 123456
"""

import sys
import json
import os
import time
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from api_client import SkillHubAPIClient


class APITester:
    """API 测试类"""
    
    def __init__(self, api_url):
        """初始化测试器"""
        self.client = SkillHubAPIClient(api_url)
        self.token = None
        self.created_skill_id = None
        self.test_skill_name = f"test_py_skill_{int(time.time())}"
    
    def login(self, account, password):
        """用户登录获取 Token"""
        print("\n" + "=" * 60)
        print("测试用户登录接口 (POST /api/user/login)")
        print("=" * 60)
        
        data = {
            'account': account,
            'password': password
        }
        
        print(f"\n请求数据: {json.dumps(data, ensure_ascii=False)}")
        
        try:
            # 使用 form-urlencoded 格式登录
            response = self.client._request('POST', '/api/user/login', data=data)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                self.token = response['data']['userinfo']['token']
                print(f"\n✅ 登录成功！")
                print(f"   Token: {self.token[:20]}...")
                print(f"   用户名: {response['data']['userinfo'].get('username', '未知')}")
                
                # 更新客户端的 Token
                self.client.session.headers.update({'Token': self.token})
                return True
            else:
                print(f"\n❌ 登录失败: {response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def test_create_skill(self):
        """测试创建技能接口"""
        if not self.token:
            print("\n⚠️ 跳过创建技能测试：未登录")
            return None
        
        print("\n" + "=" * 60)
        print("测试创建技能接口 (POST /api/skill/create)")
        print("=" * 60)
        
        # 测试数据（参考 PHP 测试案例）
        skill_info = {
            'name': self.test_skill_name,
            'username': 'skillpuber',
            'type': 'function',
            'version': '1.0.0',
            'description': 'Python测试技能描述 - 用于单元测试',
            'summary': 'Python测试技能摘要',
            'params': '{"type":"object","properties":{"input":{"type":"string"}}}',
            'returns': '{"type":"object","properties":{"result":{"type":"string"}}}',
            'dependencies': '[]',
            'risk_level': 'low',
            'rate_limit': 100,
            'timeout': 30,
            'method': 'POST',
            'auth_type': 'none',
            'icon': ''
        }
        
        print(f"\n请求数据:")
        print(json.dumps(skill_info, indent=2, ensure_ascii=False))
        
        try:
            response = self.client.create_skill(skill_info)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                self.created_skill_id = response['data'].get('id')
                print(f"\n✅ 创建技能成功！")
                print(f"   技能 ID: {self.created_skill_id}")
                print(f"   技能名称: {response['data']['name']}")
                return True
            else:
                print(f"\n❌ 创建技能失败: {response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def test_create_api_skill(self):
        """测试创建API类型技能"""
        if not self.token:
            print("\n⚠️ 跳过创建API技能测试：未登录")
            return None
        
        print("\n" + "=" * 60)
        print("测试创建API类型技能 (POST /api/skill/create)")
        print("=" * 60)
        
        api_skill_name = f"test_api_skill_{int(time.time())}"
        
        skill_info = {
            'name': api_skill_name,
            'username': 'skillpuber',
            'type': 'api',
            'version': '1.0.0',
            'description': 'API类型技能测试',
            'endpoint': 'https://api.example.com/test',
            'method': 'GET',
            'risk_level': 'medium',
            'auth_type': 'none'
        }
        
        print(f"\n请求数据:")
        print(json.dumps(skill_info, indent=2, ensure_ascii=False))
        
        try:
            response = self.client.create_skill(skill_info)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                print(f"\n✅ 创建API技能成功！")
                print(f"   技能 ID: {response['data']['id']}")
                return True
            else:
                print(f"\n❌ 创建API技能失败: {response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def test_get_skill_detail(self):
        """测试获取技能详情接口"""
        if not self.created_skill_id:
            print("\n⚠️ 跳过详情测试：没有已创建的技能")
            return None
        
        print("\n" + "=" * 60)
        print("测试获取技能详情接口 (GET /api/skill/detail)")
        print("=" * 60)
        
        try:
            response = self.client.get_skill_detail(self.created_skill_id)
            print(f"\n请求参数: id={self.created_skill_id}")
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response and 'id' in response:
                print(f"\n✅ 获取技能详情成功！")
                print(f"   技能名称: {response.get('name')}")
                print(f"   版本: {response.get('version')}")
                return True
            else:
                print(f"\n❌ 获取技能详情失败: {response.get('msg', '未知错误') if response else '无响应'}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def test_update_skill(self):
        """测试更新技能接口"""
        if not self.created_skill_id:
            print("\n⚠️ 跳过更新测试：没有已创建的技能")
            return None
        
        print("\n" + "=" * 60)
        print("测试更新技能接口 (POST /api/skill/update)")
        print("=" * 60)
        
        # 更新数据
        updates = {
            'id': self.created_skill_id,
            'version': '1.1.0',
            'description': '更新后的技能描述',
            'summary': '更新后的技能摘要',
            'risk_level': 'medium'
        }
        
        print(f"\n请求数据:")
        print(json.dumps(updates, indent=2, ensure_ascii=False))
        
        try:
            response = self.client.update_skill(updates)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                print(f"\n✅ 更新技能成功！")
                print(f"   技能 ID: {self.created_skill_id}")
                return True
            else:
                print(f"\n❌ 更新技能失败: {response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def test_search_skills(self):
        """测试搜索技能接口"""
        print("\n" + "=" * 60)
        print("测试搜索技能接口 (GET /api/skill/search)")
        print("=" * 60)
        
        try:
            response = self.client.search_skills(query='test')
            print(f"\n搜索关键词: test")
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                skill_list = response.get('data', {}).get('list', [])
                print(f"\n✅ 搜索成功！")
                print(f"   找到 {len(skill_list)} 个技能")
                return True
            else:
                print(f"\n❌ 搜索失败: {response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def test_delete_skill(self):
        """测试删除技能接口"""
        if not self.created_skill_id:
            print("\n⚠️ 跳过删除测试：没有已创建的技能")
            return None
        
        print("\n" + "=" * 60)
        print("测试删除技能接口 (POST /api/skill/delete)")
        print("=" * 60)
        
        try:
            response = self.client.delete_skill(self.created_skill_id)
            print(f"\n请求参数: id={self.created_skill_id}")
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                print(f"\n✅ 删除技能成功！")
                self.created_skill_id = None
                return True
            else:
                print(f"\n❌ 删除技能失败: {response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def test_token_check(self):
        """测试 Token 检查接口"""
        if not self.token:
            print("\n⚠️ 跳过Token检查测试：未登录")
            return None
        
        print("\n" + "=" * 60)
        print("测试 Token 检查接口 (GET /api/token/check)")
        print("=" * 60)
        
        try:
            response = self.client._request('GET', '/api/token/check')
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                print(f"\n✅ Token检查成功！")
                print(f"   Token: {response['data']['token'][:20]}...")
                print(f"   有效期: {response['data']['expires_in']} 秒")
                return True
            else:
                print(f"\n❌ Token检查失败: {response.get('msg', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False


def main():
    """运行所有测试"""
    API_URL = "https://skill.cxus.cn"
    
    # 测试账号（参考 PHP 测试案例）
    TEST_ACCOUNT = "skillpuber"
    TEST_PASSWORD = "123456"
    
    print(f"\n🧪 SkillHub API 测试套件")
    print(f"📡 API 地址: {API_URL}")
    print(f"� 测试账号: {TEST_ACCOUNT}")
    print()
    
    tester = APITester(API_URL)
    results = []
    
    # 运行测试
    results.append(("用户登录", tester.login(TEST_ACCOUNT, TEST_PASSWORD)))
    results.append(("Token检查", tester.test_token_check()))
    results.append(("搜索技能", tester.test_search_skills()))
    results.append(("创建function技能", tester.test_create_skill()))
    results.append(("创建api技能", tester.test_create_api_skill()))
    results.append(("获取技能详情", tester.test_get_skill_detail()))
    results.append(("更新技能", tester.test_update_skill()))
    # 取消注释以测试删除功能
    # results.append(("删除技能", tester.test_delete_skill()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result is True)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    for name, result in results:
        if result is True:
            status = "✅ 通过"
        elif result is False:
            status = "❌ 失败"
        else:
            status = "⚠️ 跳过"
        print(f"{status} - {name}")
    
    print(f"\n总计：{passed}/{total} 测试通过 ({skipped} 跳过)")
    
    if tester.created_skill_id:
        print(f"\n📝 已创建的测试技能 ID: {tester.created_skill_id}")
    
    return passed == (total - skipped)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
