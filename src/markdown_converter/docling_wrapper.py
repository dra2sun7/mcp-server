"""
Docling 라이브러리 래퍼 클래스
"""
import warnings
from docling.document_converter import DocumentConverter
from ..utils.exceptions import ConversionError


class DoclingWrapper:
    """Docling 라이브러리 래퍼 클래스"""
    
    def __init__(self):
        # MPS 관련 경고 필터링
        warnings.filterwarnings("ignore", message=".*pin_memory.*MPS.*")
        self.converter = DocumentConverter()
    
    def convert_pdf_to_markdown(self, pdf_path: str) -> str:
        """
        PDF 파일을 Markdown으로 변환
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            변환된 Markdown 텍스트
        """
        try:
            # PDF를 Docling Document로 변환
            doc = self.converter.convert(pdf_path).document
            
            # Markdown으로 내보내기
            markdown_text = doc.export_to_markdown()
            
            return markdown_text
            
        except Exception as e:
            raise ConversionError(f"PDF to Markdown 변환 실패: {e}") 