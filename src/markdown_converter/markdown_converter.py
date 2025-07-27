"""
PDF to Markdown 변환 핵심 로직
"""
from pathlib import Path
from .docling_wrapper import DoclingWrapper
from ..utils.exceptions import ConversionError
from ..utils.file_manager import FileManager


def convert_pdf_to_markdown(
    pdf_path: str,
    output_dir: str = "data/markdown",
    overwrite: bool = True
) -> str:
    """
    단일 PDF 파일을 Markdown으로 변환
    
    Args:
        pdf_path: PDF 파일 경로
        output_dir: 출력 디렉토리
        overwrite: 기존 파일 덮어쓰기 여부
    
    Returns:
        생성된 Markdown 파일 경로
    """
    try:
        # 입력 파일 검증
        if not FileManager.file_exists(pdf_path):
            raise ConversionError(f"PDF 파일이 존재하지 않습니다: {pdf_path}")
        
        # 출력 디렉토리 생성
        output_path = FileManager.ensure_directory(output_dir)
        
        # Markdown 파일명 생성
        pdf_filename = Path(pdf_path).stem
        markdown_filename = f"{pdf_filename}.md"
        markdown_path = output_path / markdown_filename
        
        # 기존 파일 체크
        if markdown_path.exists() and not overwrite:
            print(f"⚠️  이미 존재하는 파일: {markdown_path}")
            return str(markdown_path)
        
        print(f"🔄 PDF to Markdown 변환 시작: {pdf_path}")
        
        # Docling으로 변환
        docling_wrapper = DoclingWrapper()
        markdown_text = docling_wrapper.convert_pdf_to_markdown(pdf_path)
        
        # 파일 저장
        FileManager.save_file(markdown_text, markdown_path)
        
        print(f"✅ Markdown 변환 완료: {markdown_path}")
        return str(markdown_path)
        
    except ConversionError:
        raise
    except Exception as e:
        raise ConversionError(f"변환 중 예상치 못한 오류: {e}")
