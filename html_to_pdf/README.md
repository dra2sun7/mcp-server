# 📄 html_to_pdf

HTML 파일을 PDF로 변환하는 자동화 도구입니다.  
[Playwright](https://playwright.dev/python/)를 활용하여 실제 브라우저 렌더링 결과를 PDF로 저장합니다.

---

## 🛠️ 설치 방법

1. **필수 패키지 설치**
    ```bash
    pip install playwright
    ```

2. **Playwright 브라우저 실행 파일 설치 (필수)**
    ```bash
    playwright install
    ```
    - 이 명령어는 Chromium, Firefox, WebKit 등 Playwright가 사용할 브라우저를 자동으로 다운로드합니다.
    - 한 번만 실행하면 됩니다.

---

## 📂 폴더 구조

```
html_to_pdf/
├── main.py           # 변환 실행 파일
├── html/             # 변환할 HTML 파일을 넣는 폴더
├── pdf/              # 변환된 PDF 파일이 저장되는 폴더
├── tests/            # 테스트 코드
│   ├── __init__.py
│   └── test_main.py
└── requirements.txt  # (필요시)
```

---

필요에 따라 예시 코드, 옵션, 추가 설명 등을 더 넣을 수 있습니다.  
원하는 내용이나 강조하고 싶은 부분이 있으면 말씀해 주세요!

---

## 🚀 사용법

1. **html 폴더에 변환할 .html/.htm 파일을 넣으세요.**
2. 아래 명령어로 변환을 실행하세요.
    ```bash
    python main.py
    ```
    - 모든 HTML 파일이 `pdf/` 폴더에 같은 이름의 PDF로 저장됩니다.
    - 이미 PDF가 존재하면 경고 메시지와 함께 덮어씁니다.

---

## 🧪 테스트

테스트는 pytest로 실행할 수 있습니다.

```bash
pytest tests/
```

- 테스트 환경에서는 실제 PDF 파일이 생성되지 않습니다.
- 다양한 예외 상황(빈 폴더, 잘못된 HTML 등)도 자동으로 검증합니다.

---

## ⚠️ 주의사항

- **Playwright 브라우저 실행 파일을 반드시 설치해야 합니다.**
    - `playwright install`을 실행하지 않으면  
      `"BrowserType.launch: Executable doesn't exist ..."`  
      와 같은 에러가 발생합니다.
- 입력 폴더(`html/`)와 출력 폴더(`pdf/`)는 고정되어 있습니다.
- 변환 결과는 항상 `pdf/` 폴더에 저장됩니다.

---

## 📚 참고

- [Playwright 공식 문서 (Python)](https://playwright.dev/python/docs/intro)
- [pytest 공식 문서](https://docs.pytest.org/)

---

> 본 도구는 MCP 기반 문서 처리 파이프라인의 전처리 단계로 활용할 수 있습니다.
