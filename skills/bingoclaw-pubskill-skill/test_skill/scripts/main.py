#!/usr/bin/env python3
"""
测试技能主程序
"""

import json
import sys

def main():
    try:
        # 读取输入
        input_data = json.loads(sys.stdin.read())
        
        # 处理请求
        name = input_data.get('name', '朋友')
        result = {
            'message': f'你好，{name}！'
        }
        
        # 输出结果
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({'error': str(e)}))

if __name__ == '__main__':
    main()
