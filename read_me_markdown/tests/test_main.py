import os
import pytest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# main.py의 함수를 import
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import convert_all_pdfs_to_markdown

# 테스트 환경 설정
os.environ['TESTING'] = 'true'

class TestPDFToMarkdown:
    
    def test_pdf_directory_exists(self):
        """pdf 폴더가 존재하는지 테스트"""
        assert os.path.exists("pdf"), "pdf 폴더가 존재하지 않습니다"
    
    def test_pdf_files_in_directory(self):
        """pdf 폴더에 PDF 파일이 있는지 테스트"""
        has_pdf = any(f.lower().endswith('.pdf') for f in os.listdir("pdf"))
        assert has_pdf, "pdf 폴더에 PDF 파일이 없습니다"
    
    def test_convert_single_pdf(self):
        """단일 PDF 파일 변환 테스트"""
        pdf_files = [f for f in os.listdir("pdf") if f.lower().endswith('.pdf')]
        if pdf_files:
            # 첫 번째 PDF 파일로 테스트
            test_pdf = pdf_files[0]
            pdf_path = os.path.join("pdf", test_pdf)
            
            # Docling DocumentConverter 모킹
            with patch('main.DocumentConverter') as mock_converter:
                # Mock 설정
                mock_doc = MagicMock()
                mock_doc.export_to_markdown.return_value = "# Test Markdown\n\nThis is a test."
                mock_converter_instance = MagicMock()
                mock_converter_instance.convert.return_value.document = mock_doc
                mock_converter.return_value = mock_converter_instance
                
                # 함수 실행
                convert_all_pdfs_to_markdown()
                
                # Mock이 호출되었는지 확인
                mock_converter_instance.convert.assert_called()
                mock_doc.export_to_markdown.assert_called()
    
    def test_convert_with_empty_directory(self):
        """빈 폴더에서의 동작 테스트"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 임시 빈 폴더로 테스트
            convert_all_pdfs_to_markdown(temp_dir)
            # 에러 없이 실행되어야 함
    
    def test_convert_with_invalid_pdf(self):
        """잘못된 PDF 파일 처리 테스트"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 잘못된 PDF 파일 생성
            invalid_pdf_path = os.path.join(temp_dir, "invalid.pdf")
            with open(invalid_pdf_path, 'w') as f:
                f.write("This is not a PDF file")
            
            # 에러가 발생하지 않고 계속 실행되어야 함
            convert_all_pdfs_to_markdown(temp_dir)
    
    def test_markdown_output_format(self):
        """Markdown 출력 형식 테스트"""
        pdf_files = [f for f in os.listdir("pdf") if f.lower().endswith('.pdf')]
        if pdf_files:
            test_pdf = pdf_files[0]
            pdf_path = os.path.join("pdf", test_pdf)
            
            with patch('main.DocumentConverter') as mock_converter:
                mock_doc = MagicMock()
                mock_doc.export_to_markdown.return_value = "# Test Title\n\nTest content"
                mock_converter_instance = MagicMock()
                mock_converter_instance.convert.return_value.document = mock_doc
                mock_converter.return_value = mock_converter_instance
                
                # 출력 캡처
                with patch('builtins.print') as mock_print:
                    convert_all_pdfs_to_markdown()
                    
                    # print가 호출되었는지 확인
                    assert mock_print.called, "출력이 생성되지 않았습니다"
    
    def test_no_file_creation_in_testing(self):
        """테스트 환경에서 파일이 생성되지 않는지 확인"""
        pdf_files = [f for f in os.listdir("pdf") if f.lower().endswith('.pdf')]
        if pdf_files:
            test_pdf = pdf_files[0]
            pdf_path = os.path.join("pdf", test_pdf)
            expected_md_path = os.path.splitext(pdf_path)[0] + ".md"
            
            # 기존 .md 파일이 있다면 백업
            original_md_exists = os.path.exists(expected_md_path)
            if original_md_exists:
                backup_path = expected_md_path + ".backup"
                shutil.move(expected_md_path, backup_path)
            
            try:
                with patch('main.DocumentConverter') as mock_converter:
                    mock_doc = MagicMock()
                    mock_doc.export_to_markdown.return_value = "# Test Markdown"
                    mock_converter_instance = MagicMock()
                    mock_converter_instance.convert.return_value.document = mock_doc
                    mock_converter.return_value = mock_converter_instance
                    
                    # 함수 실행
                    convert_all_pdfs_to_markdown()
                    
                    # .md 파일이 생성되지 않았는지 확인
                    assert not os.path.exists(expected_md_path), "테스트 환경에서 .md 파일이 생성되었습니다"
                    
            finally:
                # 백업 파일 복원
                if original_md_exists:
                    shutil.move(backup_path, expected_md_path)

if __name__ == "__main__":
    pytest.main([__file__]) 