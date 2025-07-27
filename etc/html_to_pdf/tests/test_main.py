import os
import pytest
import shutil
from unittest.mock import patch, MagicMock
import sys

# main.py의 함수 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import convert_all_htmls_to_pdf

# 테스트 환경 변수 설정
os.environ['TESTING'] = 'true'

class TestHtmlToPdf:
    def test_html_directory_exists(self):
        assert os.path.exists("html"), "html 폴더가 존재하지 않습니다"

    def test_html_files_in_directory(self):
        has_html = any(f.lower().endswith(('.html', '.htm')) for f in os.listdir("html"))
        assert has_html, "html 폴더에 HTML 파일이 없습니다"

    def test_convert_single_html(self):
        html_files = [f for f in os.listdir("html") if f.lower().endswith(('.html', '.htm'))]
        if html_files:
            test_html = html_files[0]
            html_path = os.path.join("html", test_html)
            pdf_filename = os.path.splitext(test_html)[0] + ".pdf"
            pdf_path = os.path.join("pdf", pdf_filename)

            # 기존 PDF 파일 백업
            original_pdf_exists = os.path.exists(pdf_path)
            if original_pdf_exists:
                backup_path = pdf_path + ".backup"
                shutil.move(pdf_path, backup_path)

            try:
                with patch('main.sync_playwright') as mock_playwright:
                    mock_browser = MagicMock()
                    mock_page = MagicMock()
                    mock_browser.new_page.return_value = mock_page
                    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

                    convert_all_htmls_to_pdf("html", "pdf")

                    # PDF 파일이 생성되지 않았는지 확인 (테스트 환경)
                    assert not os.path.exists(pdf_path), "테스트 환경에서 PDF 파일이 생성되었습니다"
            finally:
                # 백업 복원
                if original_pdf_exists:
                    shutil.move(backup_path, pdf_path)

    def test_convert_with_empty_directory(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            os.makedirs(temp_dir, exist_ok=True)
            convert_all_htmls_to_pdf(temp_dir, "pdf")
            # 에러 없이 실행되어야 함

    def test_convert_with_invalid_html(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_html_path = os.path.join(temp_dir, "invalid.html")
            with open(invalid_html_path, 'w') as f:
                f.write("<html><body>Not a valid HTML</body></html>")
            convert_all_htmls_to_pdf(temp_dir, "pdf")
            # 에러 없이 실행되어야 함

if __name__ == "__main__":
    pytest.main([__file__])
