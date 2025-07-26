# 🧠 MCP Server

> Model Context Protocol 기반 문서 처리 파이프라인  
> SEC EDGAR Filing 다운로드부터 Markdown 변환까지

---

## 📌 개요

이 프로젝트는 MCP (Model Context Protocol) 기반의 문서 처리 파이프라인을 구현합니다.  
SEC EDGAR에서 회사 Filing을 다운로드하고, HTML을 PDF로 변환한 후, 최종적으로 Markdown으로 변환하는 완전한 워크플로우를 제공합니다.

---

## 🚀 주요 기능

### 📊 download_sec_filing
- SEC EDGAR API를 통한 회사 Filing 자동 다운로드
- 8-K, 10-Q, 10-K, DEF 14A 지원
- CIK 기반 회사 검색 및 최신 Filing 선택

### 📄 html_to_pdf  
- HTML 파일을 PDF로 변환
- Playwright를 활용한 실제 브라우저 렌더링
- 배치 처리 지원

### 📝 read_me_markdown
- PDF를 Markdown으로 변환
- Docling 프레임워크 활용
- 문서 구조 보존

---

## 📂 프로젝트 구조

```
mcp-server/
├── download_sec_filing/     # SEC Filing 다운로드 도구
│   ├── main.py
│   ├── requirements.txt
│   ├── tests/
│   └── README.md
├── html_to_pdf/            # HTML to PDF 변환 도구
│   ├── main.py
│   ├── requirements.txt
│   ├── tests/
│   └── README.md
├── read_me_markdown/       # PDF to Markdown 변환 도구
│   ├── main.py
│   ├── requirements.txt
│   ├── tests/
│   └── README.md
├── requirements.txt        # 메인 프로젝트 의존성
└── README.md              # 이 파일
```

---

## 🔄 워크플로우

```
1. download_sec_filing → HTML 파일 다운로드
2. html_to_pdf → HTML을 PDF로 변환  
3. read_me_markdown → PDF를 Markdown으로 변환
```

---

## 🛠️ 설치 및 설정

### 1. 기본 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Playwright 브라우저 설치 (html_to_pdf용)

```bash
pip install playwright
playwright install
```

### 3. 각 도구별 의존성 설치

```bash
# download_sec_filing
cd download_sec_filing
pip install -r requirements.txt

# html_to_pdf  
cd ../html_to_pdf
pip install -r requirements.txt

# read_me_markdown
cd ../read_me_markdown
pip install -r requirements.txt
```

---

## 🚀 사용 예시

### 1. SEC Filing 다운로드

```bash
cd download_sec_filing
python main.py
```

### 2. HTML을 PDF로 변환

```bash
cd html_to_pdf
python main.py
```

### 3. PDF를 Markdown으로 변환

```bash
cd read_me_markdown
python main.py
```

---

## 🧪 테스트

각 도구별로 테스트를 실행할 수 있습니다:

```bash
# download_sec_filing 테스트
cd download_sec_filing
pytest tests/

# html_to_pdf 테스트
cd ../html_to_pdf
pytest tests/

# read_me_markdown 테스트
cd ../read_me_markdown
pytest tests/
```

---

## 📚 참고 자료

- [SEC EDGAR API 문서](https://www.sec.gov/edgar/sec-api-documentation)
- [Playwright 공식 문서](https://playwright.dev/python/docs/intro)
- [Docling 프레임워크](https://github.com/docling-ai/docling)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

> 본 프로젝트는 MCP 기반 문서 처리 파이프라인의 완전한 구현체입니다.

