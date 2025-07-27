"""
파일 관리 유틸리티
"""
from pathlib import Path
from .exceptions import FileManagerError


class FileManager:
    """파일 및 디렉토리 관리 클래스"""
    
    @staticmethod
    def create_output_directories() -> None:
        """필요한 출력 디렉토리들을 생성합니다."""
        directories = [
            "data/html",
            "data/pdf", 
            "data/markdown"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def ensure_directory(path: str) -> Path:
        """디렉토리가 존재하는지 확인하고, 없으면 생성합니다."""
        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    
    @staticmethod
    def create_filename(company_name: str, year: str, filing_type: str) -> str:
        """파일명을 생성합니다."""
        # 회사명 정리 (공백을 언더스코어로, 점 제거)
        clean_company_name = company_name.replace(' ', '_').replace('.', '')
        # Filing 타입 정리 (공백을 언더스코어로)
        clean_filing_type = filing_type.replace(' ', '_')
        
        return f"{clean_company_name}_{year}_{clean_filing_type}.html"
    
    @staticmethod
    def save_file(content: str, file_path: Path, encoding: str = 'utf-8') -> None:
        """파일을 저장합니다."""
        try:
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
        except Exception as e:
            raise FileManagerError(f"파일 저장 실패: {e}")
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """파일이 존재하는지 확인합니다."""
        return Path(path).exists() 