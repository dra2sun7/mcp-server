"""
Playwright 브라우저 관리 클래스
"""
from playwright.sync_api import sync_playwright, Page
from pathlib import Path
from ..utils.exceptions import ConversionError


class BrowserManager:
    """Playwright 브라우저 관리 클래스"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        return self
    
    def __exit__(self):
        """컨텍스트 매니저 종료"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def create_page(self) -> Page:
        """새 페이지 생성"""
        if not self.browser:
            raise ConversionError("브라우저가 초기화되지 않았습니다.")
        return self.browser.new_page()
    
    def convert_html_to_pdf(self, html_path: str, pdf_path: str, page: Page) -> None:
        """HTML 파일을 PDF로 변환"""
        try:
            # HTML 파일 로드
            abs_html_path = Path(html_path).resolve()
            page.goto(f"file://{abs_html_path}")
            
            # PDF 생성
            page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True
            )
        except Exception as e:
            raise ConversionError(f"PDF 변환 실패: {e}") 