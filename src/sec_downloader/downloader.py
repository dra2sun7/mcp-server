"""
SEC Filing 다운로더
"""
from pathlib import Path
from typing import Optional, Dict, Any
from src.sec_downloader.api_client import SECAPIClient
from src.utils.file_manager import FileManager
from src.utils.exceptions import SECDownloadError


class SECDownloader:
    """SEC Filing 다운로더 클래스"""
    
    def __init__(self, user_agent: Optional[str] = None, rate_limit_delay: float = 0.1):
        self.user_agent = user_agent or "MCP-Server/1.0 dra2sun7@gmail.com"
        self.rate_limit_delay = rate_limit_delay
        self.api_client = SECAPIClient(
            user_agent=self.user_agent,
            rate_limit_delay=self.rate_limit_delay
        )
    
    def download_filing(self, cik: str, year: str, filing_type: str) -> Dict[str, Any]:
        """
        SEC EDGAR에서 회사 Filing을 다운로드합니다.
        
        Args:
            cik: 회사 CIK 번호
            year: 다운로드할 년도
            filing_type: Filing 타입 (8-K, 10-Q, 10-K, DEF 14A)
        
        Returns:
            다운로드 결과 정보
        """
        try:
            # 임시 디렉토리 사용 (권한 문제 해결)
            import tempfile
            temp_dir = tempfile.gettempdir()
            output_dir = Path(temp_dir) / "sec_filings" / "html"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 입력 검증
            self.api_client.validate_inputs(year, filing_type)
            
            print(f"📊 SEC Filing 다운로드 시작: CIK={cik}, Year={year}, Type={filing_type}")
            
            # 회사 정보 및 Filing 목록 조회
            company_info = self.api_client.get_company_filings(cik)
            company_data = company_info['company_data']
            filings = company_info['filings']
            
            # 대상 Filing 찾기
            target_filings = self.api_client.find_target_filings(filings, year, filing_type)
            
            # 최신 Filing 선택
            latest_filing = self.api_client.get_latest_filing(target_filings)
            
            print(f"🎯 선택된 Filing: {latest_filing['report_date']} - {latest_filing['form_type']}")
            
            # Filing 문서 다운로드
            document_content = self.api_client.download_filing_document(
                cik=self.api_client._normalize_cik(cik),
                accession_number=latest_filing['accession_number'],
                primary_doc=latest_filing['primary_document']
            )
            
            # 파일 저장
            company_name = company_data.get('name', 'unknown')
            filename = FileManager.create_filename(company_name, year, filing_type)
            file_path = output_dir / filename
            
            FileManager.save_file(document_content, file_path)
            
            print(f"✅ 다운로드 완료: {filename}")
            print(f"📁 저장 위치: {file_path}")
            
            return {
                "success": True,
                "file_path": str(file_path),
                "company_name": company_name,
                "filing_date": latest_filing['report_date'],
                "form_type": latest_filing['form_type']
            }
            
        except (SECDownloadError, ValueError) as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"다운로드 실패: {e}"
            }
        except Exception as e:
            print(f"❌ 예상치 못한 오류 발생: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"예상치 못한 오류: {e}"
            }


def download_sec_filing(
    cik: str,
    year: str,
    filing_type: str,
    output_dir_path: str,
    user_agent: Optional[str] = None,
    rate_limit_delay: float = 0.1
) -> str:
    """
    SEC EDGAR에서 회사 Filing을 다운로드합니다. (기존 함수 호환성 유지)
    
    Args:
        cik: 회사 CIK 번호
        year: 다운로드할 년도
        filing_type: Filing 타입 (8-K, 10-Q, 10-K, DEF 14A)
        output_dir_path: 출력 디렉토리 경로
        user_agent: User-Agent 문자열
        rate_limit_delay: 요청 간 지연 시간 (초)
    
    Returns:
        다운로드된 파일 경로
    """
    downloader = SECDownloader(user_agent, rate_limit_delay)
    result = downloader.download_filing(cik, year, filing_type)
    
    if result["success"]:
        return result["file_path"]
    else:
        raise SECDownloadError(result["error"])


 