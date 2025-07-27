# 📊 download_sec_filing

SEC EDGAR에서 회사의 Filing을 자동으로 다운로드하는 도구입니다.  
SEC의 공식 API를 활용하여 회사의 8-K, 10-Q, 10-K, DEF 14A 등의 Filing을 HTML 형태로 다운로드합니다.

---

## 🎯 주요 기능

- **SEC EDGAR API 연동**: SEC의 공식 API를 사용하여 정확한 데이터 수집
- **다양한 Filing 타입 지원**: 8-K, 10-Q, 10-K, DEF 14A
- **자동 최신 Filing 선택**: 지정된 년도의 가장 최근 Filing 자동 선택
- **Rate Limiting 준수**: SEC API 사용 제한을 준수하는 안전한 요청
- **파일명 자동 생성**: 회사명_년도_타입.html 형식으로 자동 명명

---

## 🛠️ 설치 방법

1. **필수 패키지 설치**
    ```bash
    pip install -r requirements.txt
    ```

2. **의존성 확인**
    - `requests`: HTTP 요청 처리
    - `pytest`: 테스트 실행 (개발용)

---

## 📂 폴더 구조

```
download_sec_filing/
├── main.py              # 메인 실행 파일
├── requirements.txt     # 의존성 목록
├── tests/              # 테스트 코드
│   ├── __init__.py
│   └── test_main.py
└── README.md           # 이 파일
```

---

## 🚀 사용법

### 기본 사용법

```python
from main import download_sec_filing

# Amazon (CIK: 0001018724)의 2024년 8-K Filing 다운로드
result = download_sec_filing(
    cik="0001018724",
    year="2024", 
    filing_type="8-K",
    output_dir_path="html/amzn_2024_8_k"
)
print(f"다운로드 완료: {result}")
```

### 명령줄 실행

```bash
python main.py
```

---

## 📋 입력 파라미터

| 파라미터 | 타입 | 설명 | 예시 |
|---------|------|------|------|
| `cik` | str | 회사의 CIK 번호 | `"0001018724"` 또는 `"1018724"` |
| `year` | str | 다운로드할 Filing의 년도 | `"2024"` (2021-2025만 지원) |
| `filing_type` | str | Filing 타입 | `"8-K"`, `"10-Q"`, `"10-K"`, `"DEF 14A"` |
| `output_dir_path` | str | 다운로드할 폴더 경로 | `"html/amzn_2024_8_k"` |

---

## 📤 출력 결과

- **반환값**: 다운로드된 HTML 파일의 전체 경로
- **파일명 형식**: `{회사명}_{년도}_{타입}.html`
- **예시**: `AMAZON.COM_INC_2024_8-K.html`

---

## 🧪 테스트

### 테스트 실행

```bash
# 전체 테스트 실행
pytest tests/

# 특정 테스트만 실행
pytest tests/test_main.py::TestDownloadSecFiling::test_successful_download
```

### 테스트 범위

- ✅ 입력 파라미터 검증
- ✅ API 응답 처리
- ✅ 파일 다운로드 및 저장
- ✅ 오류 상황 처리
- ✅ CIK 정규화
- ✅ 최신 Filing 선택 로직

---

## ⚠️ 주의사항

### SEC API 제한사항

- **Rate Limiting**: 요청 간 0.1초 대기 시간 적용
- **User-Agent**: 적절한 User-Agent 헤더 설정
- **API 엔드포인트**: SEC의 공식 API만 사용

### 입력 제한사항

- **년도**: 2021년부터 2025년까지만 지원
- **Filing 타입**: 8-K, 10-Q, 10-K, DEF 14A만 지원
- **CIK**: 10자리 이하의 숫자 문자열

### 네트워크 요구사항

- 인터넷 연결 필요
- SEC EDGAR 웹사이트 접근 가능해야 함

---

## 🔧 고급 사용법

### 여러 회사 동시 처리

```python
companies = [
    ("0001018724", "Amazon"),
    ("0000320187", "Apple"),
    ("0001067983", "Microsoft")
]

for cik, name in companies:
    try:
        result = download_sec_filing(
            cik=cik,
            year="2024",
            filing_type="10-K",
            output_dir_path=f"html/{name.lower()}_2024_10k"
        )
        print(f"{name}: {result}")
    except Exception as e:
        print(f"{name}: 오류 - {e}")
```

### 오류 처리

```python
try:
    result = download_sec_filing("0001018724", "2024", "8-K", "html/test")
except ValueError as e:
    print(f"입력 오류: {e}")
except Exception as e:
    print(f"다운로드 오류: {e}")
```

---

## 📚 참고 자료

- [SEC EDGAR API 문서](https://www.sec.gov/edgar/sec-api-documentation)
- [SEC Filing 타입 설명](https://www.sec.gov/fast-answers/answersform8khtm.html)
- [CIK 번호 검색](https://www.sec.gov/edgar/searchedgar/cik)

---

## 🔗 연계 도구

이 도구는 다음과 같은 파이프라인에서 활용할 수 있습니다:

1. **download_sec_filing** → HTML 파일 다운로드
2. **html_to_pdf** → HTML을 PDF로 변환  
3. **read_me_markdown** → PDF를 Markdown으로 변환

---

> 본 도구는 MCP 기반 문서 처리 파이프라인의 첫 번째 단계로 활용됩니다. 