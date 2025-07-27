"""
SEC Filing Processor MCP Server for Claude Desktop
"""
import sys
import os
import asyncio
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# src 디렉토리를 Python 경로에 추가
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from fastmcp import FastMCP
from src.sec_downloader.downloader import SECDownloader
from src.html_converter.html_converter import HTMLConverter
from src.markdown_converter.markdown_converter import MarkdownConverter
from src.utils.file_manager import FileManager


# FastMCP 서버 생성
mcp = FastMCP(
    name="SEC Filing Processor",
    dependencies=["docling", "playwright", "requests"]
)


@mcp.tool
async def process_sec_filing_pipeline(cik: str, year: str, filing_type: str) -> dict:
    """SEC Filing을 다운로드하고 Markdown으로 변환하는 전체 파이프라인을 실행합니다.
    
    Args:
        cik: 회사 CIK 번호
        year: 다운로드할 년도
        filing_type: Filing 타입 (8-K, 10-Q, 10-K, DEF 14A)
    
    Returns:
        dict: 파이프라인 실행 결과
    """
    try:
        print(f"🚀 파이프라인 시작: CIK={cik}, Year={year}, Type={filing_type}")
        
        # 1단계: SEC Filing 다운로드
        print("📥 1단계: SEC Filing 다운로드 시작...")
        downloader = SECDownloader()
        download_result = downloader.download_filing(cik, year, filing_type)
        
        if not download_result.get("success", False):
            return {
                "success": False,
                "message": "다운로드 단계에서 실패",
                "error": download_result.get("error", "Unknown error")
            }
        
        html_path = download_result.get("file_path")
        print(f"✅ 다운로드 완료: {html_path}")
        
        # 2단계: HTML to PDF 변환 (비동기)
        print("🔄 2단계: HTML to PDF 변환 시작...")
        html_converter = HTMLConverter()
        convert_result = await html_converter.convert_html_to_pdf(html_path)
        
        if not convert_result.get("success", False):
            return {
                "success": False,
                "message": "PDF 변환 단계에서 실패",
                "error": convert_result.get("error", "Unknown error")
            }
        
        pdf_path = convert_result.get("pdf_path")
        print(f"✅ PDF 변환 완료: {pdf_path}")
        
        # 3단계: PDF to Markdown 변환
        print("📝 3단계: PDF to Markdown 변환 시작...")
        markdown_converter = MarkdownConverter()
        markdown_result = markdown_converter.convert_pdf_to_markdown(pdf_path)
        
        if not markdown_result.get("success", False):
            return {
                "success": False,
                "message": "Markdown 변환 단계에서 실패",
                "error": markdown_result.get("error", "Unknown error")
            }
        
        markdown_path = markdown_result.get("markdown_path")
        print(f"✅ Markdown 변환 완료: {markdown_path}")
        
        print("🎉 전체 파이프라인 완료!")
        
        return {
            "success": True,
            "message": "전체 파이프라인 실행 완료",
            "html_file": html_path,
            "pdf_file": pdf_path,
            "markdown_file": markdown_path,
            "cik": cik,
            "year": year,
            "filing_type": filing_type
        }
        
    except Exception as e:
        print(f"❌ 파이프라인 오류: {e}")
        return {
            "success": False,
            "message": f"파이프라인 실행 실패: {str(e)}",
            "error": str(e)
        }


if __name__ == "__main__":
    # STDIO 모드로 실행 (Claude Desktop용)
    mcp.run() 