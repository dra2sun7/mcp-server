"""
SEC EDGAR API 클라이언트
"""
import time
import requests
import json
from typing import Dict, List
from ..utils.exceptions import APIError, SECDownloadError


class SECAPIClient:
    """SEC EDGAR API 클라이언트"""
    
    def __init__(self, user_agent: str = "MCP-Server/1.0 dra2sun7@gmail.com", rate_limit_delay: float = 0.1):
        """
        SEC API 클라이언트 초기화
        
        Args:
            user_agent: User-Agent 헤더
            rate_limit_delay: Rate limiting을 위한 대기 시간 (초)
        """
        self.base_url = "https://data.sec.gov/submissions/CIK"
        self.user_agent = user_agent
        self.rate_limit_delay = rate_limit_delay
        
        self.headers = {
            'User-Agent': user_agent
        }
    
    def _rate_limit(self) -> None:
        """Rate limiting을 위한 대기"""
        time.sleep(self.rate_limit_delay)
    
    def _normalize_cik(self, cik: str) -> str:
        """CIK를 10자리 형식으로 정규화"""
        return cik.zfill(10)
    
    def get_company_filings(self, cik: str) -> Dict:
        """
        회사의 Filing 정보를 가져옵니다.
        
        Args:
            cik: 회사 CIK 번호
            
        Returns:
            회사 Filing 정보
            
        Raises:
            APIError: API 호출 실패 시
            SECDownloadError: Filing 정보를 찾을 수 없을 때
        """
        normalized_cik = self._normalize_cik(cik)
        filings_url = f"{self.base_url}{normalized_cik}.json"
        
        try:
            self._rate_limit()
            print(f"📡 SEC API 호출: {filings_url}")
            
            response = requests.get(filings_url, headers=self.headers)
            response.raise_for_status()
            
            company_data = response.json()
            
            # Filing 정보 추출
            filings = company_data.get('filings', {}).get('recent', {})
            
            if not filings:
                raise SECDownloadError(f"CIK {normalized_cik}에 대한 Filing 정보를 찾을 수 없습니다.")
            
            return {
                'company_data': company_data,
                'filings': filings
            }
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"SEC EDGAR API 호출 중 오류 발생: {e}")
        except json.JSONDecodeError as e:
            raise APIError(f"JSON 파싱 오류: {e}")
    
    def find_target_filings(self, filings: Dict, year: str, filing_type: str) -> List[Dict]:
        """
        특정 년도와 타입의 Filing을 찾습니다.
        
        Args:
            filings: Filing 정보
            year: 년도
            filing_type: Filing 타입
            
        Returns:
            대상 Filing 목록
            
        Raises:
            SECDownloadError: 해당 Filing을 찾을 수 없을 때
        """
        target_filings = []
        
        for i, (form_type, report_date) in enumerate(zip(filings.get('form', []), filings.get('reportDate', []))):
            if form_type == filing_type and report_date.startswith(str(year)):
                target_filings.append({
                    'index': i,
                    'form_type': form_type,
                    'report_date': report_date,
                    'accession_number': filings.get('accessionNumber', [])[i],
                    'primary_document': filings.get('primaryDocument', [])[i]
                })
        
        if not target_filings:
            raise SECDownloadError(f"{year}년 {filing_type} Filing을 찾을 수 없습니다.")
        
        return target_filings
    
    def get_latest_filing(self, target_filings: List[Dict]) -> Dict:
        """가장 최근 Filing을 반환합니다."""
        return max(target_filings, key=lambda x: x['report_date'])
    
    def download_filing_document(self, cik: str, accession_number: str, primary_doc: str) -> str:
        """
        Filing 문서를 다운로드합니다.
        
        Args:
            cik: 회사 CIK 번호
            accession_number: 접근 번호
            primary_doc: 주요 문서명
            
        Returns:
            다운로드된 문서 내용
            
        Raises:
            APIError: 다운로드 실패 시
        """
        try:
            # CIK에서 앞의 0 제거
            clean_cik = cik.lstrip('0')
            # 접근 번호에서 하이픈 제거
            clean_accession = accession_number.replace('-', '')
            
            # SEC EDGAR 문서 URL
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{clean_cik}/{clean_accession}/{primary_doc}"
            
            self._rate_limit()
            print(f"📄 문서 다운로드: {doc_url}")
            
            doc_response = requests.get(doc_url, headers=self.headers)
            doc_response.raise_for_status()
            
            return doc_response.text
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"문서 다운로드 실패: {e}")
    
    def validate_inputs(self, year: str, filing_type: str) -> None:
        """
        입력값을 검증합니다.
        
        Args:
            year: 년도
            filing_type: Filing 타입
            
        Raises:
            ValueError: 잘못된 입력값일 때
        """
        if not (2021 <= int(year) <= 2025):
            raise ValueError("년도는 2021부터 2025까지만 지원됩니다.")
        
        if filing_type not in ["8-K", "10-Q", "10-K", "DEF 14A"]:
            raise ValueError("지원되지 않는 filing_type입니다. '8-K', '10-Q', '10-K', 'DEF 14A' 중 선택하세요.") 