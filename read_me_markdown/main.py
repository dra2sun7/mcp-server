import os
from docling.document_converter import DocumentConverter

def convert_all_pdfs_to_markdown(input_file_path="pdf"):
    converter = DocumentConverter()
    for filename in os.listdir(input_file_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_file_path, filename)
            print(f"변환 중: {pdf_path}")
            try:
                doc = converter.convert(pdf_path).document
                markdown_text = doc.export_to_markdown()
                # 결과를 화면에 출력
                print(f"===== {filename} =====")
                print(markdown_text)
                print("\n\n")
                # 또는 파일로 저장하려면 아래 주석 해제
                md_path = os.path.splitext(pdf_path)[0] + ".md"
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
            except Exception as e:
                print(f"에러 발생: {filename} - {e}")

if __name__ == "__main__":
    convert_all_pdfs_to_markdown()
