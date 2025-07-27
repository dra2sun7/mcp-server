"""
HTML to PDF 변환 핵심 로직
"""
from pathlib import Path
from .browser_manager import BrowserManager
from ..utils.exceptions import ConversionError
from ..utils.file_manager import FileManager


def convert_html_to_pdf(
    html_path: str,
    output_dir: str = "data/pdf",
    overwrite: bool = True
) -> str:
    """
    단일 HTML 파일을 PDF로 변환
    
    Args:
        html_path: HTML 파일 경로
        output_dir: 출력 디렉토리
        overwrite: 기존 파일 덮어쓰기 여부
    
    Returns:
        생성된 PDF 파일 경로
    """
    try:
        # 입력 파일 검증
        if not FileManager.file_exists(html_path):
            raise ConversionError(f"HTML 파일이 존재하지 않습니다: {html_path}")
        
        # 출력 디렉토리 생성
        output_path = FileManager.ensure_directory(output_dir)
        
        # PDF 파일명 생성
        html_filename = Path(html_path).stem
        pdf_filename = f"{html_filename}.pdf"
        pdf_path = output_path / pdf_filename
        
        # 기존 파일 체크
        if pdf_path.exists() and not overwrite:
            print(f"⚠️  이미 존재하는 파일: {pdf_path}")
            return str(pdf_path)
        
        print(f"🔄 HTML to PDF 변환 시작: {html_path}")
        
        # 브라우저로 변환
        with BrowserManager() as browser_manager:
            page = browser_manager.create_page()
            browser_manager.convert_html_to_pdf(str(html_path), str(pdf_path), page)
            page.close()
        
        print(f"✅ PDF 변환 완료: {pdf_path}")
        return str(pdf_path)
        
    except ConversionError:
        raise
    except Exception as e:
        raise ConversionError(f"변환 중 예상치 못한 오류: {e}")
