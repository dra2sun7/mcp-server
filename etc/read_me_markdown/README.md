# 📄 read_me_markdown

PDF 파일을 Markdown 텍스트로 변환하는 도구입니다.  
Docling 프레임워크를 활용하여, 지정된 PDF 파일을 손쉽게 Markdown으로 변환할 수 있습니다.

---

## 🛠️ 사용 방법

1. 변환할 PDF 파일을 `pdf` 폴더에 넣어주세요.
2. 아래와 같이 main.py를 실행하여 PDF 파일명을 입력하면, 해당 파일이 Markdown으로 변환되어 출력됩니다.

```bash
python main.py "Amazon.com Inc. - Form 8-K. 2024-02-01.pdf"
```

- **입력**:  
  - `pdf` 폴더 내 PDF 파일명 (하위 폴더 미지원)
- **출력**:  
  - 변환된 Markdown 텍스트

---

## 🧩 기술 스택

- Python
- [Docling](https://github.com/docling/docling) (문서 파싱 및 변환)

---

## 📂 폴더 구조

read_me_markdown/
├── main.py
├── requirements.txt
├── README.md
├── pdf/
└── tests/

---

## 3. 구현 설계 안내

- **main.py**  
  - 입력: PDF 파일명 (명령행 인자)
  - 동작: `pdf/` 폴더에서 해당 파일을 찾아 Docling으로 파싱 → Markdown 변환 → 결과 출력
- **requirements.txt**  
  - Python, Docling 등 필요한 패키지 명시
