# 1. FastMCP 라이브러리 import
from fastmcp import FastMCP

# 2. FastMCP 인스턴스 생성
mcp = FastMCP(name="SEC Filing Tools")

# 3. 첫 번째 Tool 등록 - SEC Filing 다운로드
@mcp.tool
def download_sec_filing(cik: str, year: str, filing_type: str) -> dict:
    """SEC EDGAR에서 특정 회사의 Filing을 다운로드합니다."""
    return {"message": f"다운로드 완료: {cik}, {year}, {filing_type}"}

# 4. 두 번째 Tool 등록 - HTML to PDF 변환
@mcp.tool
def html_to_pdf(input_path: str) -> dict:
    """HTML 파일을 PDF로 변환합니다."""
    return {"message": f"PDF 변환 완료: {input_path}"}

# 5. 세 번째 Tool 등록 - PDF to Markdown 변환
@mcp.tool
def read_me_markdown(pdf_path: str) -> dict:
    """PDF 파일을 마크다운으로 변환합니다."""
    return {"message": f"마크다운 변환 완료: {pdf_path}"}

# 6. 메인 실행 부분
if __name__ == "__main__":
    print("🚀 MCP Server 시작...")
    mcp.run()
