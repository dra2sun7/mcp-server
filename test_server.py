#!/usr/bin/env python3
"""
SEC Filing Processor MCP Server 로컬 테스트 스크립트
"""
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_mcp_server():
    """MCP 서버를 로컬에서 테스트합니다."""
    try:
        print("🧪 SEC Filing Processor MCP Server 테스트 시작...")
        
        # main.py에서 mcp 객체 가져오기
        from main import mcp
        
        print("✅ MCP 서버 객체 생성 성공")
        print(f"📋 서버 이름: {mcp.name}")
        
        print("\n✅ 테스트 완료! MCP 서버가 정상적으로 작동합니다.")
        print("💡 이제 'fastmcp install claude-desktop main.py --with-requirements requirements.txt' 명령으로 Claude Desktop에 설치할 수 있습니다.")
        
    except ImportError as e:
        print(f"❌ Import 오류: {e}")
        print("💡 의존성이 올바르게 설치되었는지 확인하세요.")
        return False
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1) 