"""
SEC EDGAR API 클라이언트
"""
import time
import requests
import json
from typing import Dict, List
from src.utils.exceptions import APIError, SECDownloadError


class SECAPIClient:
    """SEC EDGAR API 클라이언트"""
    
    def __init__(self, user_agent: str = "MCP-Server/1.0 dra2sun7@gmail.com", rate_limit_delay: float = 0.1):
        self.base_url = "https://data.sec.gov/submissions/CIK"
        self.user_agent = user_agent
        self.rate_limit_delay = rate_limit_delay
        self.headers = {'User-Agent': user_agent}
    
    def _normalize_cik(self, cik: str) -> str:
        """CIK를 10자리 형식으로 정규화"""
        # 숫자만 추출
        cik_digits = ''.join(filter(str.isdigit, cik))
        
        # 10자리로 패딩
        normalized_cik = cik_digits.zfill(10)
        
        return normalized_cik
    
    def _make_request(self, url: str) -> Dict:
        """API 요청 수행"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"API 요청 실패: {e}")
    
    def get_company_filings(self, cik: str) -> Dict:
        """회사 정보 및 Filing 목록 조회"""
        normalized_cik = self._normalize_cik(cik)
        url = f"{self.base_url}{normalized_cik}.json"
        
        try:
            data = self._make_request(url)
            
            return {
                'company_data': data.get('entityName', {}),
                'filings': data.get('filings', {}).get('recent', {})
            }
            
        except Exception as e:
            raise SECDownloadError(f"회사 정보 조회 실패: {e}")
    
    def find_target_filings(self, filings: Dict, year: str, filing_type: str) -> List[Dict]:
        """대상 Filing 찾기"""
        try:
            # Filing 데이터 추출
            form_types = filings.get('form', [])
            report_dates = filings.get('reportDate', [])
            accession_numbers = filings.get('accessionNumber', [])
            primary_docs = filings.get('primaryDocument', [])
            
            target_filings = []
            
            for i, form_type in enumerate(form_types):
                if (form_type == filing_type and 
                    i < len(report_dates) and 
                    report_dates[i].startswith(year)):
                    
                    target_filings.append({
                        'form_type': form_type,
                        'report_date': report_dates[i],
                        'accession_number': accession_numbers[i] if i < len(accession_numbers) else '',
                        'primary_document': primary_docs[i] if i < len(primary_docs) else ''
                    })
            
            if not target_filings:
                raise SECDownloadError(f"{year}년 {filing_type} Filing을 찾을 수 없습니다.")
            
            return target_filings
            
        except Exception as e:
            raise SECDownloadError(f"대상 Filing 검색 실패: {e}")
    
    def get_latest_filing(self, filings: List[Dict]) -> Dict:
        """최신 Filing 선택"""
        if not filings:
            raise SECDownloadError("Filing 목록이 비어있습니다.")
        
        # 날짜순으로 정렬하여 최신 것 선택
        sorted_filings = sorted(filings, key=lambda x: x['report_date'], reverse=True)
        return sorted_filings[0]
    
    def download_filing_document(self, cik: str, accession_number: str, primary_doc: str) -> str:
        """Filing 문서 다운로드"""
        try:
            # Accession number에서 하이픈 제거
            clean_accession = accession_number.replace('-', '')
            
            # 문서 URL 생성
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{clean_accession}/{primary_doc}"
            
            # 문서 다운로드
            response = requests.get(doc_url, headers=self.headers)
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            raise SECDownloadError(f"문서 다운로드 실패: {e}")
    
    def validate_inputs(self, year: str, filing_type: str) -> None:
        """입력값 검증"""
        # 년도 검증
        if not year.isdigit() or len(year) != 4:
            raise ValueError("년도는 4자리 숫자여야 합니다.")
        
        year_int = int(year)
        if year_int < 1990 or year_int > 2025:
            raise ValueError("년도는 1990-2025 사이여야 합니다.")
        
        # Filing 타입 검증
        valid_types = ["8-K", "10-Q", "10-K", "DEF 14A"]
        if filing_type not in valid_types:
            raise ValueError(f"Filing 타입은 다음 중 하나여야 합니다: {', '.join(valid_types)}") 