import os
import requests
import json
from datetime import datetime
from pathlib import Path
import time


def download_sec_filing(cik, year, filing_type, output_dir_path):
    """
    SEC EDGAR에서 특정 회사의 Filing을 다운로드합니다.
    
    Args:
        cik (str): 회사의 CIK 번호 (예: '0001018724' 또는 '1018724')
        year (str): 다운로드할 Filing의 년도 (2021-2025)
        filing_type (str): Filing 타입 ("8-K", "10-Q", "10-K", "DEF 14A")
        output_dir_path (str): 다운로드할 폴더 경로 (html 폴더 하위)
    
    Returns:
        str: 다운로드된 대표 HTML 파일의 경로
    """
    
    # 입력 검증
    if not (2021 <= int(year) <= 2025):
        raise ValueError("년도는 2021부터 2025까지만 지원됩니다.")
    
    if filing_type not in ["8-K", "10-Q", "10-K", "DEF 14A"]:
        raise ValueError("지원되지 않는 filing_type입니다. '8-K', '10-Q', '10-K', 'DEF 14A' 중 선택하세요.")
    
    # CIK 형식 정규화 (10자리로 패딩, 10자리로 고정)
    cik = cik.zfill(10)
    
    # 출력 디렉토리 생성
    output_path = Path(output_dir_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # SEC EDGAR API 엔드포인트
    base_url = "https://data.sec.gov/submissions/CIK"
    filings_url = f"{base_url}{cik}.json"
    
    try:
        # SEC EDGAR API 호출 (Rate limiting 준수)
        headers = {
            'User-Agent': 'MCP-Server/1.0 dra2sun7@gmail.com'
        }
        
        # Rate limiting을 위한 대기
        time.sleep(0.1)
        
        response = requests.get(filings_url, headers=headers)
        response.raise_for_status()
        
        company_data = response.json()
        
        # Filing 정보 추출
        filings = company_data.get('filings', {}).get('recent', {})
        
        if not filings:
            raise ValueError(f"CIK {cik}에 대한 Filing 정보를 찾을 수 없습니다.")
        
        # # filings 정보 출력 (디버깅용)
        # print("🔍 filings 정보:")
        # print(f"   - filings 타입: {type(filings)}")
        # print(f"   - filings 키들: {list(filings.keys())}")
        # print(f"   - 총 Filing 수: {len(filings.get('form', []))}")
        # print()
        # print("📋 form 배열 직접 출력:")
        # print(f"   - form: {filings['form']}")
        # print()
        # print("📅 reportDate 배열 직접 출력:")
        # print(f"   - reportDate: {filings['reportDate']}")
        # print()
        # print("🔢 accessionNumber 배열 직접 출력:")
        # print(f"   - accessionNumber: {filings['accessionNumber']}")
        # print()
        # print("📄 primaryDocument 배열 직접 출력:")
        # print(f"   - primaryDocument: {filings['primaryDocument']}")
        # print("-" * 50)
        
        # 해당 년도와 타입의 Filing 찾기
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
            raise ValueError(f"{year}년 {filing_type} Filing을 찾을 수 없습니다.")
        
        # # target_filings 결과 출력 (디버깅용)
        # print(f"🎯 {year}년 {filing_type} Filing 찾기 결과:")
        # for i, filing in enumerate(target_filings):
        #     print(f"   {i+1}. {filing['report_date']} - {filing['form_type']} - {filing['accession_number']}")
        # print("-" * 50)
        
        # 가장 최근 Filing 선택 (report_date 기준)
        latest_filing = max(target_filings, key=lambda x: x['report_date'])
        
        # Filing 다운로드
        accession_number = latest_filing['accession_number'].replace('-', '')
        primary_doc = latest_filing['primary_document']
        
        # SEC EDGAR 문서 URL
        doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{accession_number}/{primary_doc}"
        
        # Rate limiting을 위한 대기
        time.sleep(0.1)
        
        doc_response = requests.get(doc_url, headers=headers)
        doc_response.raise_for_status()
        
        # 파일명 생성 (회사명_년도_타입.html)
        company_name = company_data.get('name', 'unknown').replace(' ', '_').replace('.', '')
        filename = f"{company_name}_{year}_{filing_type.replace(' ', '_')}.html"
        file_path = output_path / filename
        
        # HTML 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc_response.text)
        
        print(f"✅ {filename} 다운로드 완료")
        print(f"📁 저장 위치: {file_path}")
        
        return str(file_path)
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"SEC EDGAR API 호출 중 오류 발생: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"JSON 파싱 오류: {e}")
    except Exception as e:
        raise Exception(f"다운로드 중 오류 발생: {e}")


def main():
    """메인 실행 함수"""
    # 테스트 환경에서는 파일 생성 방지
    if os.getenv('TESTING') == 'true':
        print("🧪 테스트 환경: 파일 다운로드가 비활성화되었습니다.")
        return
    
    # 예시 사용법
    try:
        # Amazon (CIK: 0001018724)의 2024년 8-K Filing 다운로드
        result = download_sec_filing(
            cik="0001018724",
            year="2024",
            filing_type="8-K",
            output_dir_path="html/amzn_2024_8_k"
        )
        print(f"🎯 다운로드 완료: {result}")
        
    except Exception as e:
        print(f"❌ 오류: {e}")


if __name__ == "__main__":
    main() 
