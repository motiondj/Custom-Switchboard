#!/usr/bin/env python3
"""
Config 파일 진단 스크립트
"""

import json
import os
import sys
from pathlib import Path

def check_config_file(file_path):
    """개별 config 파일을 검사합니다."""
    print(f"\n=== {file_path.name} 검사 ===")
    
    # 파일 존재 확인
    if not os.path.exists(file_path):
        print(f"❌ 파일이 존재하지 않습니다: {file_path}")
        return False
    
    # 파일 읽기 권한 확인
    if not os.access(file_path, os.R_OK):
        print(f"❌ 파일 읽기 권한이 없습니다: {file_path}")
        return False
    
    # JSON 형식 검사
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON 형식이 유효합니다")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 형식 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        return False
    
    # user_settings.json은 다른 검사 규칙 적용
    if file_path.name == 'user_settings.json':
        if 'config' in data:
            print(f"✅ config 필드가 있습니다: {data.get('config', 'None')}")
        else:
            print(f"⚠️  config 필드가 없습니다")
        return True
    
    # 프로젝트 config 파일용 필수 필드 확인
    required_fields = ['project_name', 'engine_dir']
    for field in required_fields:
        if field not in data:
            print(f"❌ 필수 필드 누락: {field}")
            return False
        elif not data[field]:
            print(f"⚠️  필드가 비어있음: {field}")
    
    # engine_dir 경로 확인
    if 'engine_dir' in data and data['engine_dir']:
        engine_path = Path(data['engine_dir'])
        if not engine_path.exists():
            print(f"❌ Engine 경로가 존재하지 않습니다: {data['engine_dir']}")
        else:
            print(f"✅ Engine 경로가 유효합니다: {data['engine_dir']}")
    
    # devices 섹션 확인
    if 'devices' not in data:
        print(f"⚠️  devices 섹션이 없습니다")
    else:
        device_count = len(data['devices'])
        print(f"✅ {device_count}개의 device가 설정되어 있습니다")
    
    return True

def main():
    print("=== Switchboard Config 파일 진단 ===")
    
    configs_dir = Path("configs")
    if not configs_dir.exists():
        print(f"❌ configs 디렉토리가 존재하지 않습니다")
        return
    
    # 모든 JSON 파일 검사
    json_files = list(configs_dir.glob("*.json"))
    if not json_files:
        print("❌ configs 디렉토리에 JSON 파일이 없습니다")
        return
    
    print(f"📁 {len(json_files)}개의 JSON 파일을 발견했습니다")
    
    valid_files = 0
    for json_file in json_files:
        if check_config_file(json_file):
            valid_files += 1
    
    print(f"\n=== 진단 결과 ===")
    print(f"✅ 유효한 파일: {valid_files}/{len(json_files)}")
    
    # user_settings.json 특별 검사
    user_settings = configs_dir / "user_settings.json"
    if user_settings.exists():
        print(f"\n=== user_settings.json 상세 검사 ===")
        try:
            with open(user_settings, 'r') as f:
                user_data = json.load(f)
            
            if 'config' in user_data and user_data['config']:
                current_config = configs_dir / user_data['config']
                if current_config.exists():
                    print(f"✅ 현재 선택된 config: {user_data['config']}")
                else:
                    print(f"❌ 선택된 config 파일이 존재하지 않습니다: {user_data['config']}")
            else:
                print(f"⚠️  config 필드가 비어있습니다")
                
        except Exception as e:
            print(f"❌ user_settings.json 읽기 오류: {e}")
    
    # 권한 확인
    print(f"\n=== 권한 확인 ===")
    print(f"configs 디렉토리 쓰기 권한: {'✅' if os.access(configs_dir, os.W_OK) else '❌'}")
    
    for json_file in json_files:
        readable = os.access(json_file, os.R_OK)
        writable = os.access(json_file, os.W_OK)
        print(f"{json_file.name}: 읽기{'✅' if readable else '❌'} 쓰기{'✅' if writable else '❌'}")

if __name__ == "__main__":
    main() 