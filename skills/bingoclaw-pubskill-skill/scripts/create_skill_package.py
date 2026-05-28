#!/usr/bin/env python3
"""
创建 .skill 格式的 Zip 压缩包
"""

import zipfile
import os

def create_skill_package(source_dir, output_file):
    """创建 .skill 格式的 Zip 压缩包
    
    Args:
        source_dir: 源目录路径
        output_file: 输出文件路径（.skill 文件）
    """
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # 跳过隐藏目录和特定目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                # 跳过隐藏文件、压缩文件和 .skill 文件
                if file.startswith('.') or file.endswith('.pyc') or file.endswith('.tar.gz') or file.endswith('.skill'):
                    continue
                
                file_path = os.path.join(root, file)
                # 计算相对路径（相对于源目录）
                rel_path = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, rel_path)
                print(f'添加: {rel_path}')

if __name__ == '__main__':
    source_dir = 'dist/bingoclaw-pubskill-skill-1.2.0'
    output_file = 'dist/bingoclaw-pubskill-skill-1.2.0/skill-sharer.skill'
    
    create_skill_package(source_dir, output_file)
    print(f'\n✅ 技能包已创建: {output_file}')
    print(f'类型: Zip archive data')
