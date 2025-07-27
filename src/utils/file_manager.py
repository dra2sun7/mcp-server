"""
파일 관리 유틸리티
"""
import tempfile
import os
from pathlib import Path
from .exceptions import FileManagerError


class FileManager:
    """파일 및 디렉토리 관리 클래스"""
    
    @staticmethod
    def create_output_directories() -> None:
        """필요한 출력 디렉토리들을 생성합니다."""
        # 임시 디렉토리 사용
        temp_dir = tempfile.gettempdir()
        directories = [
            os.path.join(temp_dir, "mcp_server", "html"),
            os.path.join(temp_dir, "mcp_server", "pdf"),
            os.path.join(temp_dir, "mcp_server", "markdown")
        ]
        for directory in directories:
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
            except (PermissionError, OSError) as e:
                # 권한 오류나 파일 시스템 오류는 무시
                print(f"⚠️  디렉토리 생성 실패 (무시됨): {directory} - {e}")
    
    @staticmethod
    def ensure_directory(directory_path: str) -> Path:
        """디렉토리가 존재하는지 확인하고, 없으면 생성합니다."""
        try:
            path = Path(directory_path)
            path.mkdir(parents=True, exist_ok=True)
            return path
        except (PermissionError, OSError) as e:
            # 권한 오류 시 임시 디렉토리 사용
            temp_dir = tempfile.gettempdir()
            fallback_dir = os.path.join(temp_dir, "mcp_server", "fallback")
            print(f"⚠️  디렉토리 생성 실패, 임시 디렉토리 사용: {directory_path} - {e}")
            Path(fallback_dir).mkdir(parents=True, exist_ok=True)
            return Path(fallback_dir)
    
    @staticmethod
    def create_filename(company_name: str, year: str, filing_type: str) -> str:
        """파일명을 생성합니다."""
        # 특수문자 제거 및 공백을 언더스코어로 변경
        safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_company_name = safe_company_name.replace(' ', '_')
        
        return f"{safe_company_name}_{year}_{filing_type}.html"
    
    @staticmethod
    def save_file(content: str, file_path: Path) -> None:
        """파일을 저장합니다."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except (PermissionError, OSError) as e:
            # 권한 오류 시 임시 디렉토리에 저장
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, "mcp_server", file_path.name)
            print(f"⚠️  원본 위치 저장 실패, 임시 위치에 저장: {temp_file}")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """파일이 존재하는지 확인합니다."""
        return Path(file_path).exists() 