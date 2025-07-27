"""
PDF to Markdown 변환 핵심 로직
"""
from pathlib import Path
from typing import Dict, Any
from src.markdown_converter.docling_wrapper import DoclingWrapper
from src.utils.exceptions import ConversionError
from src.utils.file_manager import FileManager


class MarkdownConverter:
    """PDF to Markdown 변환 클래스"""
    
    def __init__(self):
        self.docling_wrapper = DoclingWrapper()
    
    def convert_pdf_to_markdown(self, pdf_path: str) -> Dict[str, Any]:
        """
        PDF 파일을 Markdown으로 변환
        
        Args:
            pdf_path: PDF 파일 경로
        
        Returns:
            변환 결과 정보
        """
        try:
            # 임시 디렉토리 사용 (권한 문제 해결)
            import tempfile
            temp_dir = tempfile.gettempdir()
            output_dir = Path(temp_dir) / "sec_filings" / "markdown"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Markdown 파일명 생성
            pdf_filename = Path(pdf_path).stem
            markdown_filename = f"{pdf_filename}.md"
            markdown_path = output_dir / markdown_filename
            
            print(f"🔄 PDF to Markdown 변환 시작: {pdf_path}")
            
            # Docling으로 변환
            markdown_text = self.docling_wrapper.convert_pdf_to_markdown(pdf_path)
            
            # 파일 저장
            FileManager.save_file(markdown_text, markdown_path)
            
            print(f"✅ Markdown 변환 완료: {markdown_path}")
            
            return {
                "success": True,
                "markdown_path": str(markdown_path),
                "original_pdf": pdf_path,
                "content_length": len(markdown_text)
            }
            
        except Exception as e:
            print(f"❌ PDF to Markdown 변환 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"변환 실패: {e}"
            }


def convert_pdf_to_markdown(
    pdf_path: str,
    output_dir: str = "data/markdown",
    overwrite: bool = True
) -> str:
    """
    단일 PDF 파일을 Markdown으로 변환 (기존 함수 호환성 유지)
    
    Args:
        pdf_path: PDF 파일 경로
        output_dir: 출력 디렉토리
        overwrite: 기존 파일 덮어쓰기 여부
    
    Returns:
        생성된 Markdown 파일 경로
    """
    converter = MarkdownConverter()
    result = converter.convert_pdf_to_markdown(pdf_path)
    
    if result["success"]:
        return result["markdown_path"]
    else:
        raise ConversionError(result["error"])
