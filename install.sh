#!/bin/bash

# SEC Filing Processor MCP Server for Claude Desktop 설치 스크립트

echo "🚀 SEC Filing Processor MCP Server 설치를 시작합니다..."

# 현재 디렉토리 확인
if [ ! -f "main.py" ]; then
    echo "❌ main.py 파일을 찾을 수 없습니다. 올바른 디렉토리에서 실행해주세요."
    exit 1
fi

# uv 설치 확인
if ! command -v uv &> /dev/null; then
    echo "❌ uv가 설치되지 않았습니다."
    echo "📦 uv 설치 방법:"
    echo "   macOS: brew install uv"
    echo "   기타: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

echo "✅ uv 설치 확인됨: $(uv --version)"

# FastMCP CLI 설치 확인
if ! command -v fastmcp &> /dev/null; then
    echo "📦 FastMCP CLI 설치 중..."
    uv pip install fastmcp
fi

echo "✅ FastMCP CLI 설치 확인됨: $(fastmcp --version)"

# Claude Desktop에 MCP 서버 설치
echo "🔧 Claude Desktop에 MCP 서버 설치 중..."
fastmcp install claude-desktop main.py --with-requirements requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ MCP 서버 설치 완료!"
    echo ""
    echo "📋 다음 단계:"
    echo "1. Claude Desktop을 완전히 종료하세요"
    echo "2. Claude Desktop을 다시 실행하세요"
    echo "3. 입력창 하단에 🔨 아이콘이 나타나는지 확인하세요"
    echo ""
    echo "🎉 설치가 완료되었습니다!"
else
    echo "❌ MCP 서버 설치에 실패했습니다."
    echo "문제 해결 방법:"
    echo "1. uv가 올바르게 설치되었는지 확인"
    echo "2. requirements.txt 파일이 존재하는지 확인"
    echo "3. main.py 파일이 올바른 형식인지 확인"
    exit 1
fi 