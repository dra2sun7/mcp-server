import requests
import json
import time

def debug_company_info():
    """SEC EDGAR API 응답 구조를 확인하여 회사명 필드를 찾습니다."""
    
    cik = "0001018724"  # Amazon
    base_url = "https://data.sec.gov/submissions/CIK"
    filings_url = f"{base_url}{cik}.json"
    
    print(f"🔍 CIK {cik}의 API 응답 구조 확인")
    print("=" * 50)
    
    try:
        headers = {
            'User-Agent': 'MCP-Server/1.0 dra2sun7@gmail.com'
        }
        
        time.sleep(0.1)
        response = requests.get(filings_url, headers=headers)
        response.raise_for_status()
        
        company_data = response.json()
        
        print("📋 최상위 키들:")
        for key in company_data.keys():
            print(f"   - {key}")
        
        print("\n🏢 회사명 관련 필드들:")
        
        # 가능한 회사명 필드들 확인
        possible_name_fields = [
            'entityName', 'name', 'companyName', 'registrantName', 
            'filerName', 'entity', 'company', 'registrant'
        ]
        
        for field in possible_name_fields:
            if field in company_data:
                print(f"   ✅ {field}: {company_data[field]}")
            else:
                print(f"   ❌ {field}: 없음")
        
        print("\n📊 전체 응답 구조 (첫 10개 키):")
        for i, (key, value) in enumerate(company_data.items()):
            if i >= 10:
                break
            print(f"   {key}: {type(value).__name__}")
            if isinstance(value, str) and len(value) < 100:
                print(f"      값: {value}")
        
        print("\n🔍 'entityName' 필드 상세:")
        entity_name = company_data.get('entityName')
        print(f"   타입: {type(entity_name)}")
        print(f"   값: {entity_name}")
        
        if entity_name is None:
            print("   ⚠️ entityName이 None입니다!")
        
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    debug_company_info() 