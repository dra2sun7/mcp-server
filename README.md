# 🧠 MCP Server.

> Model Context Protocol 기반의 선택형 응답 API 서버  
> FastAPI + Python으로 개발된 지능형 컨텍스트 선택 서버

---

## 📌 개요

MCP (Model Context Protocol)는 사용자 요청을 수집하여 **문맥(Context)**을 구성하고, 이에 기반해 **다중 선택지 응답(Choices)**을 제공하는 프로토콜입니다.  
이 프로젝트는 MCP를 구현한 **RESTful API 서버**로, 외부 모델 API와 연동하여 동적인 선택지 제공이 가능합니다.

---

## 🚀 주요 기능

- 사용자 발화를 분석해 문맥(Context) 구성
- 선택 가능한 응답(Choices) 생성
- 외부 AI 모델과 연동 (OpenAI GPT 등)
- 문맥 초기화 및 갱신 기능 제공
- RESTful API + Swagger UI 제공

---

## �� 프로젝트 구조


```

# mcp-server

## Playwright 설치 및 사용 안내

이 프로젝트는 [Playwright](https://playwright.dev/python/)를 사용하여 HTML 파일을 PDF로 변환하는 기능을 포함합니다.

### 1. 파이썬 라이브러리 설치

```bash
pip install playwright
```

### 2. Playwright 브라우저 실행 파일 설치 (필수!)

Playwright는 파이썬 라이브러리만 설치하면 동작하지 않습니다. 
**아래 명령어로 브라우저 실행 파일을 반드시 설치해야 합니다.**

```bash
playwright install
```

- 이 명령어는 Chromium, Firefox, WebKit 등 Playwright가 사용할 브라우저를 자동으로 다운로드합니다.
- 한 번만 실행하면 됩니다.

#### (선택) 특정 브라우저만 설치하고 싶다면

```bash
playwright install chromium
playwright install firefox
playwright install webkit
```

> **중요:**  
> `playwright install`을 실행하지 않으면  
> "BrowserType.launch: Executable doesn't exist ..."  
> 와 같은 에러가 발생합니다.

---

## 프로젝트 실행 예시

```bash
python html_to_pdf/main.py
```

---

## 참고

- [Playwright 공식 문서 (Python)](https://playwright.dev/python/docs/intro)

