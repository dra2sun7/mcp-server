"""
Playwright 브라우저 관리 클래스 (비동기 버전)
"""
import asyncio
from playwright.async_api import async_playwright, Page
from pathlib import Path
from src.utils.exceptions import ConversionError


class BrowserManager:
    """Playwright 브라우저 관리 클래스 (비동기)"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.playwright = await async_playwright().start()
        
        # 브라우저 시작 최적화
        self.browser = await self.playwright.chromium.launch(
            headless=True,  # 헤드리스 모드로 빠른 실행
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def create_page(self) -> Page:
        """새 페이지 생성"""
        if not self.browser:
            raise ConversionError("브라우저가 초기화되지 않았습니다.")
        
        # 페이지 생성 최적화
        page = await self.browser.new_page()
        
        # 페이지 로딩 최적화
        await page.set_viewport_size({"width": 1200, "height": 800})
        
        return page
    
    async def convert_html_to_pdf(self, html_path: str, pdf_path: str, page: Page) -> None:
        """HTML 파일을 PDF로 변환"""
        try:
            # HTML 파일 로드 (타임아웃 설정)
            abs_html_path = Path(html_path).resolve()
            await page.goto(f"file://{abs_html_path}", timeout=30000)  # 30초 타임아웃
            
            # 페이지 로딩 대기
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            # PDF 생성 (최적화된 설정)
            await page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True,
                margin={
                    'top': '0.5in',
                    'right': '0.5in',
                    'bottom': '0.5in',
                    'left': '0.5in'
                }
            )
        except Exception as e:
            raise ConversionError(f"PDF 변환 실패: {e}") 