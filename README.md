# SEC Filing Processor MCP Server for Claude Desktop

SEC EDGAR에서 회사 공시를 다운로드하고, HTML을 PDF로 변환한 후, Markdown으로 변환하여 LLM이 이해할 수 있는 형태로 제공하는 FastMCP 기반 MCP (Model Context Protocol) 서버입니다.

## 🚀 주요 기능

1. **SEC Filing 다운로드**: 회사 CIK를 입력하여 SEC EDGAR에서 공시 파일 다운로드
2. **HTML to PDF 변환**: Playwright를 사용한 정확한 HTML to PDF 변환
3. **PDF to Markdown 변환**: Docling을 사용한 PDF to Markdown 변환
4. **LLM 질의**: 변환된 Markdown 파일에 대한 질의 처리
5. **Claude Desktop 통합**: FastMCP를 통한 Claude Desktop 직접 연동

## 📁 프로젝트 구조

```
mcp-server/
├── src/
│   ├── sec_downloader/          # SEC 다운로더 모듈
│   │   ├── __init__.py
│   │   ├── api_client.py        # SEC API 클라이언트
│   │   └── downloader.py        # 다운로드 비즈니스 로직
│   ├── html_converter/          # HTML to PDF 변환 모듈
│   │   ├── __init__.py
│   │   ├── browser_manager.py   # Playwright 브라우저 관리
│   │   └── html_converter.py    # 변환 비즈니스 로직
│   ├── markdown_converter/      # PDF to Markdown 변환 모듈
│   │   ├── __init__.py
│   │   ├── docling_wrapper.py   # Docling 라이브러리 래퍼
│   │   └── markdown_converter.py # 변환 및 질의 비즈니스 로직
│   └── utils/                   # 공통 유틸리티
│       ├── __init__.py
│       ├── exceptions.py        # 커스텀 예외 클래스
│       └── file_manager.py      # 파일 관리 유틸리티
├── data/                        # 데이터 저장 디렉토리
│   ├── html/                    # 다운로드된 HTML 파일
│   ├── pdf/                     # 변환된 PDF 파일
│   └── markdown/                # 변환된 Markdown 파일
├── main.py                      # FastMCP 서버 메인 파일
├── requirements.txt             # 프로젝트 의존성
└── README.md                    # 프로젝트 문서
```

## 🛠️ Claude Desktop 설치

### **1. 사전 요구사항**

- **uv 설치**: `brew install uv` (macOS) 또는 [uv 공식 사이트](https://docs.astral.sh/uv/getting-started/installation/)에서 설치
- **Claude Desktop**: 최신 버전 설치

### **2. FastMCP CLI 설치**

```bash
# FastMCP CLI 설치
pip install fastmcp

# 또는 uv 사용
uv pip install fastmcp
```

### **3. MCP 서버 설치**

```bash
# 프로젝트 디렉토리로 이동
cd /path/to/mcp-server

# Claude Desktop에 MCP 서버 설치
fastmcp install claude-desktop main.py --with-requirements requirements.txt
```

### **4. 환경 변수 설정 (필요시)**

```bash
# API 키나 기타 환경 변수가 필요한 경우
fastmcp install claude-desktop main.py \
  --with-requirements requirements.txt \
  --env API_KEY=your-api-key \
  --env DEBUG=true
```

### **5. Claude Desktop 재시작**

Claude Desktop을 완전히 종료하고 다시 실행합니다. 입력창 하단에 🔨 아이콘이 나타나면 MCP 도구가 성공적으로 로드된 것입니다.

## 🚀 사용법

### Claude Desktop에서 사용

설치가 완료되면 Claude Desktop에서 다음과 같이 사용할 수 있습니다:

```
"Amazon의 2024년 8-K 공시를 다운로드하고 주요 내용을 요약해줘"
```

### 로컬 테스트

```bash
# 로컬에서 서버 테스트
python3 main.py
```

## 🔧 MCP 도구

### 1. `download_sec_filing`
SEC EDGAR에서 회사 Filing을 다운로드합니다.

**매개변수:**
- `cik`: 회사 CIK 번호 (예: 0001018724)
- `year`: 다운로드할 년도 (2021-2025)
- `filing_type`: Filing 타입 (8-K, 10-Q, 10-K, DEF 14A)

### 2. `convert_html_to_pdf`
HTML 파일을 PDF로 변환합니다.

**매개변수:**
- `html_path`: 변환할 HTML 파일 경로

### 3. `convert_pdf_to_markdown`
PDF 파일을 Markdown으로 변환합니다.

**매개변수:**
- `pdf_path`: 변환할 PDF 파일 경로

### 4. `query_markdown_file`
Markdown 파일에 질의합니다.

**매개변수:**
- `markdown_path`: 질의할 Markdown 파일 경로
- `question`: 질문 내용

### 5. `process_sec_filing_pipeline`
SEC Filing을 다운로드하고 Markdown으로 변환하는 전체 파이프라인을 실행합니다.

**매개변수:**
- `cik`: 회사 CIK 번호
- `year`: 다운로드할 년도
- `filing_type`: Filing 타입

### 6. `list_available_companies`
주요 회사들의 CIK 번호 목록을 제공합니다.

## 📋 지원하는 Filing 타입

- **8-K**: 주요 이벤트 보고서
- **10-Q**: 분기 보고서
- **10-K**: 연간 보고서
- **DEF 14A**: 대리인 권유서

## 🔍 주요 회사 CIK 예시

- **Amazon**: 0001018724
- **Apple**: 0000320193
- **Microsoft**: 0000789019
- **Google**: 0001652044
- **Tesla**: 0001318605

## 🛡️ 에러 처리

프로젝트는 다음과 같은 커스텀 예외를 사용합니다:

- `SECDownloadError`: SEC 다운로드 관련 오류
- `ConversionError`: 변환 관련 오류
- `FileManagerError`: 파일 관리 관련 오류
- `APIError`: API 호출 관련 오류
- `ConfigError`: 설정 관련 오류

## 🧪 테스트

```bash
# 테스트 실행
pytest tests/
```

## 🔧 문제 해결

### MCP 서버가 로드되지 않는 경우

1. **uv 설치 확인**: `uv --version`
2. **FastMCP 버전 확인**: `fastmcp --version`
3. **Claude Desktop 재시작**: 완전히 종료 후 재시작
4. **설치 로그 확인**: 터미널에서 설치 과정 확인

### 의존성 문제

```bash
# 의존성 재설치
fastmcp install claude-desktop main.py --with-requirements requirements.txt --force
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

