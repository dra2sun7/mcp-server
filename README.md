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

## 📁 프로젝트 구조

