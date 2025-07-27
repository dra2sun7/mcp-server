"""
SEC Filing 다운로더
"""
from typing import Optional

from .api_client import SECAPIClient
from ..utils.file_manager import FileManager
from ..utils.exceptions import SECDownloadError


def download_sec_filing(
    cik: str, 
    year: str, 
    filing_type: str, 
    output_dir_path: str,
    user_agent: Optional[str] = None,
    rate_limit_delay: float = 0.1
) -> str:
    """
    SEC EDGAR에서 특정 회사의 Filing을 다운로드합니다.
    
    Args:
        cik: 회사의 CIK 번호 (예: '0001018724' 또는 '1018724')
        year: 다운로드할 Filing의 년도 (2021-2025)
        filing_type: Filing 타입 ("8-K", "10-Q", "10-K", "DEF 14A")
        output_dir_path: 다운로드할 폴더 경로
        user_agent: User-Agent 헤더 (기본값: "MCP-Server/1.0 dra2sun7@gmail.com")
        rate_limit_delay: Rate limiting을 위한 대기 시간 (초)
    
    Returns:
        다운로드된 HTML 파일의 경로
        
    Raises:
        SECDownloadError: 다운로드 실패 시
        ValueError: 잘못된 입력값일 때
    """
    try:
        # API 클라이언트 초기화
        api_client = SECAPIClient(
            user_agent=user_agent or "MCP-Server/1.0 dra2sun7@gmail.com",
            rate_limit_delay=rate_limit_delay
        )
        
        # 입력값 검증
        api_client.validate_inputs(year, filing_type)
        
        # 출력 디렉토리 생성
        output_path = FileManager.ensure_directory(output_dir_path)
        
        print(f"📊 SEC Filing 다운로드 시작: CIK={cik}, Year={year}, Type={filing_type}")
        
        # 회사 Filing 정보 가져오기
        company_info = api_client.get_company_filings(cik)
        company_data = company_info['company_data']
        filings = company_info['filings']
        
        # 대상 Filing 찾기
        target_filings = api_client.find_target_filings(filings, year, filing_type)
        
        # 가장 최근 Filing 선택
        latest_filing = api_client.get_latest_filing(target_filings)
        
        print(f"🎯 선택된 Filing: {latest_filing['report_date']} - {latest_filing['form_type']}")
        
        # Filing 문서 다운로드
        document_content = api_client.download_filing_document(
            cik=api_client._normalize_cik(cik),
            accession_number=latest_filing['accession_number'],
            primary_doc=latest_filing['primary_document']
        )
        
        # 파일명 생성
        company_name = company_data.get('name', 'unknown')
        filename = FileManager.create_filename(company_name, year, filing_type)
        file_path = output_path / filename
        
        # HTML 파일 저장
        FileManager.save_file(document_content, file_path)
        
        print(f"✅ 다운로드 완료: {filename}")
        print(f"📁 저장 위치: {file_path}")
        
        return str(file_path)
        
    except (SECDownloadError, ValueError) as e:
        # 이미 적절한 예외 타입이므로 그대로 재발생
        raise
    except Exception as e:
        # 예상치 못한 오류는 SECDownloadError로 래핑
        print(f"❌ 예상치 못한 오류 발생: {e}")
        raise SECDownloadError(f"다운로드 중 오류 발생: {e}")


 