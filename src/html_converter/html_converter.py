"""
HTML to PDF 변환 핵심 로직 (비동기 버전)
"""
from pathlib import Path
from src.html_converter.browser_manager import BrowserManager
from src.utils.exceptions import ConversionError
from src.utils.file_manager import FileManager


class HTMLConverter:
    """HTML to PDF 변환기 클래스 (비동기)"""
    
    def __init__(self):
        pass
    
    async def convert_html_to_pdf(self, html_path: str) -> dict:
        """
        HTML 파일을 PDF로 변환 (비동기)
        
        Args:
            html_path: HTML 파일 경로
        
        Returns:
            변환 결과 정보
        """
        try:
            # 입력 파일 존재 여부 확인
            if not Path(html_path).exists():
                return {
                    "success": False,
                    "error": f"HTML 파일이 존재하지 않습니다: {html_path}",
                    "message": f"파일을 찾을 수 없습니다: {html_path}"
                }
            
            # HTML 파일 크기 확인
            html_size = Path(html_path).stat().st_size
            print(f"📊 HTML 파일 크기: {html_size} bytes")
            
            if html_size == 0:
                return {
                    "success": False,
                    "error": "HTML 파일이 비어있습니다",
                    "message": "HTML 파일이 비어있어 변환할 수 없습니다"
                }
            
            # 임시 디렉토리 사용 (권한 문제 해결)
            import tempfile
            temp_dir = tempfile.gettempdir()
            output_dir = Path(temp_dir) / "sec_filings" / "pdf"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"📁 출력 디렉토리: {output_dir}")
            
            # PDF 파일명 생성
            html_filename = Path(html_path).stem
            pdf_filename = f"{html_filename}.pdf"
            pdf_path = output_dir / pdf_filename
            
            print(f"📄 HTML 파일: {html_path}")
            print(f"📄 PDF 파일: {pdf_path}")
            
            print(f"🔄 HTML to PDF 변환 시작: {html_path}")
            
            # 비동기 브라우저 변환
            try:
                async with BrowserManager() as browser_manager:
                    page = await browser_manager.create_page()
                    await browser_manager.convert_html_to_pdf(str(html_path), str(pdf_path), page)
                    await page.close()
                
                # 변환된 PDF 파일 존재 여부 확인
                if not pdf_path.exists():
                    return {
                        "success": False,
                        "error": "PDF 파일이 생성되지 않았습니다",
                        "message": "PDF 변환은 완료되었지만 파일이 생성되지 않았습니다"
                    }
                
                print(f"✅ PDF 변환 완료: {pdf_path}")
                
                return {
                    "success": True,
                    "pdf_path": str(pdf_path),
                    "original_html": html_path
                }
                
            except Exception as browser_error:
                print(f"❌ 브라우저 변환 오류: {browser_error}")
                return {
                    "success": False,
                    "error": str(browser_error),
                    "message": f"브라우저 변환 실패: {browser_error}"
                }
            
        except Exception as e:
            print(f"❌ HTML to PDF 변환 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"변환 실패: {e}"
            }
