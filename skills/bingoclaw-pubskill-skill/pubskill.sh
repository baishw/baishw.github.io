#!/bin/bash
# PubSkill 快捷启动脚本
# 使用方法: ./pubskill.sh <command> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 scripts/main.py "$@"
