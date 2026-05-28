#!/usr/bin/env python3
"""
SkillHub API 完整流程测试脚本

模拟从登录到创建、更新、删除技能的全流程
API域名: https://skill.cxus.cn
测试账号: skillpuber / 123456
"""

import sys
import json
import time
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from api_client import SkillHubAPIClient


class SkillFlowTester:
    """技能全流程测试类"""
    
    def __init__(self, api_url):
        """初始化测试器"""
        self.client = SkillHubAPIClient(api_url)
        self.token = None
        self.created_skill_ids = []
        self.test_skill_prefix = f"test_flow_{int(time.time())}"
    
    def step_login(self, account, password):
        """步骤1: 用户登录"""
        print("\n" + "=" * 70)
        print("【步骤 1/8】用户登录 (POST /api/user/login)")
        print("=" * 70)
        
        data = {'account': account, 'password': password}
        print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
        
        try:
            response = self.client._request('POST', '/api/user/login', data=data)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                self.token = response['data']['userinfo']['token']
                self.client.session.headers.update({'Token': self.token})
                print(f"\n✅ 登录成功")
                print(f"   用户名: {response['data']['userinfo'].get('username')}")
                print(f"   Token: {self.token[:20]}...")
                print(f"   有效期: {response['data']['userinfo'].get('expires_in')} 秒")
                return True
            else:
                print(f"\n❌ 登录失败: {response.get('msg', '未知错误')}")
                return False
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def step_create_function_skill(self):
        """步骤2: 创建function类型技能"""
        print("\n" + "=" * 70)
        print("【步骤 2/8】创建Function类型技能 (POST /api/skill/create)")
        print("=" * 70)
        
        skill_name = f"{self.test_skill_prefix}_function"
        
        skill_data = {
            'name': skill_name,
            'username': 'skillpuber',
            'type': 'function',
            'version': '1.0.0',
            'description': '全流程测试 - Function类型技能',
            'summary': 'Function技能摘要',
            'params': '{"type":"object","properties":{"input":{"type":"string"}}}',
            'returns': '{"type":"object","properties":{"result":{"type":"string"}}}',
            'dependencies': '[]',
            'risk_level': 'low',
            'rate_limit': 100,
            'timeout': 30,
            'method': 'POST',
            'auth_type': 'none'
        }
        
        print(f"请求数据:")
        print(json.dumps(skill_data, indent=2, ensure_ascii=False))
        
        try:
            response = self.client.create_skill(skill_data)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                skill_id = response['data']['id']
                self.created_skill_ids.append(skill_id)
                print(f"\n✅ 创建Function技能成功")
                print(f"   技能ID: {skill_id}")
                print(f"   技能名称: {skill_name}")
                return True
            else:
                print(f"\n❌ 创建失败: {response.get('msg', '未知错误')}")
                return False
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def step_create_api_skill(self):
        """步骤3: 创建API类型技能"""
        print("\n" + "=" * 70)
        print("【步骤 3/8】创建API类型技能 (POST /api/skill/create)")
        print("=" * 70)
        
        skill_name = f"{self.test_skill_prefix}_api"
        
        skill_data = {
            'name': skill_name,
            'username': 'skillpuber',
            'type': 'api',
            'version': '1.0.0',
            'description': '全流程测试 - API类型技能',
            'summary': 'API技能摘要',
            'endpoint': 'https://api.example.com/weather',
            'method': 'GET',
            'risk_level': 'medium',
            'auth_type': 'none'
        }
        
        print(f"请求数据:")
        print(json.dumps(skill_data, indent=2, ensure_ascii=False))
        
        try:
            response = self.client.create_skill(skill_data)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                skill_id = response['data']['id']
                self.created_skill_ids.append(skill_id)
                print(f"\n✅ 创建API技能成功")
                print(f"   技能ID: {skill_id}")
                print(f"   技能名称: {skill_name}")
                return True
            else:
                print(f"\n❌ 创建失败: {response.get('msg', '未知错误')}")
                return False
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def step_get_skill_detail(self):
        """步骤4: 获取技能详情"""
        print("\n" + "=" * 70)
        print("【步骤 4/8】获取技能详情 (GET /api/skill/detail)")
        print("=" * 70)
        
        if not self.created_skill_ids:
            print("⚠️ 没有已创建的技能，跳过此步骤")
            return None
        
        skill_id = self.created_skill_ids[0]
        
        print(f"请求参数: id={skill_id}")
        
        try:
            response = self.client.get_skill_detail(skill_id)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response and 'id' in response:
                print(f"\n✅ 获取技能详情成功")
                print(f"   技能ID: {response['id']}")
                print(f"   技能名称: {response.get('name')}")
                print(f"   版本: {response.get('version')}")
                print(f"   类型: {response.get('type_text', response.get('type'))}")
                return True
            else:
                print(f"\n❌ 获取失败")
                return False
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def step_update_skill(self):
        """步骤5: 更新技能"""
        print("\n" + "=" * 70)
        print("【步骤 5/8】更新技能 (POST /api/skill/update)")
        print("=" * 70)
        
        if not self.created_skill_ids:
            print("⚠️ 没有已创建的技能，跳过此步骤")
            return None
        
        skill_id = self.created_skill_ids[0]
        
        update_data = {
            'id': skill_id,
            'version': '2.0.0',
            'description': '全流程测试 - 更新后的描述',
            'summary': '更新后的摘要',
            'risk_level': 'medium',
            'rate_limit': 200
        }
        
        print(f"请求数据:")
        print(json.dumps(update_data, indent=2, ensure_ascii=False))
        
        try:
            response = self.client.update_skill(update_data)
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                print(f"\n✅ 更新技能成功")
                print(f"   技能ID: {skill_id}")
                print(f"   更新版本: {response['data']['version']}")
                print(f"   更新风险等级: {response['data']['risk_level']}")
                return True
            else:
                print(f"\n❌ 更新失败: {response.get('msg', '未知错误')}")
                return False
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def step_search_skills(self):
        """步骤6: 搜索技能"""
        print("\n" + "=" * 70)
        print("【步骤 6/8】搜索技能 (GET /api/skill/search)")
        print("=" * 70)
        
        try:
            response = self.client.search_skills(query=self.test_skill_prefix)
            print(f"搜索关键词: {self.test_skill_prefix}")
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                skill_list = response.get('data', {}).get('list', [])
                print(f"\n✅ 搜索成功")
                print(f"   找到 {len(skill_list)} 个匹配技能")
                for skill in skill_list:
                    print(f"   - {skill.get('name')} (ID: {skill.get('id')})")
                return True
            else:
                print(f"\n❌ 搜索失败: {response.get('msg', '未知错误')}")
                return False
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False
    
    def step_delete_skills(self):
        """步骤7: 删除技能"""
        print("\n" + "=" * 70)
        print("【步骤 7/8】删除技能 (POST /api/skill/delete)")
        print("=" * 70)
        
        if not self.created_skill_ids:
            print("⚠️ 没有已创建的技能，跳过此步骤")
            return None
        
        all_success = True
        
        for skill_id in self.created_skill_ids:
            print(f"\n删除技能 ID: {skill_id}")
            
            try:
                response = self.client.delete_skill(skill_id)
                print(f"响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
                
                if response.get('code') == 1:
                    print(f"✅ 删除成功")
                else:
                    print(f"❌ 删除失败: {response.get('msg')}")
                    all_success = False
            except Exception as e:
                print(f"❌ 请求异常: {e}")
                all_success = False
        
        if all_success:
            self.created_skill_ids = []
        
        return all_success
    
    def step_logout(self):
        """步骤8: 退出登录"""
        print("\n" + "=" * 70)
        print("【步骤 8/8】退出登录 (POST /api/user/logout)")
        print("=" * 70)
        
        try:
            response = self.client._request('POST', '/api/user/logout')
            print(f"响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('code') == 1:
                print(f"\n✅ 退出登录成功")
                self.token = None
                return True
            else:
                print(f"\n❌ 退出失败: {response.get('msg', '未知错误')}")
                return False
        except Exception as e:
            print(f"\n❌ 请求异常: {e}")
            return False


def main():
    """运行完整流程测试"""
    API_URL = "https://skill.cxus.cn"
    TEST_ACCOUNT = "skillpuber"
    TEST_PASSWORD = "123456"
    
    print("\n" + "*" * 70)
    print("* SkillHub API 完整流程测试")
    print(f"* API地址: {API_URL}")
    print(f"* 测试账号: {TEST_ACCOUNT}")
    print(f"* 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("*" * 70)
    
    tester = SkillFlowTester(API_URL)
    results = []
    
    # 执行完整流程
    results.append(("用户登录", tester.step_login(TEST_ACCOUNT, TEST_PASSWORD)))
    results.append(("创建Function技能", tester.step_create_function_skill()))
    results.append(("创建API技能", tester.step_create_api_skill()))
    results.append(("获取技能详情", tester.step_get_skill_detail()))
    results.append(("更新技能", tester.step_update_skill()))
    results.append(("搜索技能", tester.step_search_skills()))
    results.append(("删除技能", tester.step_delete_skills()))
    results.append(("退出登录", tester.step_logout()))
    
    # 输出测试总结
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result is True)
    skipped = sum(1 for _, result in results if result is None)
    failed = sum(1 for _, result in results if result is False)
    total = len(results)
    
    print(f"\n测试步骤: {total} | 通过: {passed} | 失败: {failed} | 跳过: {skipped}")
    print("\n详细结果:")
    
    for name, result in results:
        if result is True:
            status = "✅ 通过"
        elif result is False:
            status = "❌ 失败"
        else:
            status = "⚠️ 跳过"
        print(f"{status} - {name}")
    
    # 清理检查
    if tester.created_skill_ids:
        print(f"\n⚠️ 警告: 有 {len(tester.created_skill_ids)} 个测试技能未删除:")
        for skill_id in tester.created_skill_ids:
            print(f"   - 技能ID: {skill_id}")
    
    print("\n" + "=" * 70)
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查错误信息")
        return 1


if __name__ == '__main__':
    sys.exit(main())
