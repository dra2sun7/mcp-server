import os
import warnings
from docling.document_converter import DocumentConverter

# MPS 관련 경고 필터링
warnings.filterwarnings("ignore", message=".*pin_memory.*MPS.*")

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
                # print(markdown_text)
                print("\n\n")
                
                # 파일로 저장 (테스트 환경에서는 비활성화)
                if not os.environ.get('TESTING'):
                    md_path = os.path.splitext(pdf_path)[0] + ".md"
                    
                    # 이미 존재하는 .md 파일인지 점검
                    if os.path.exists(md_path):
                        print(f"⚠️  이미 존재하는 파일: {md_path}")
                        print(f"   기존 파일을 덮어씁니다.")
                    
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(markdown_text)
                    
                    print(f"✅ Markdown 파일 저장 완료: {md_path}")
            except Exception as e:
                print(f"에러 발생: {filename} - {e}")

if __name__ == "__main__":
    convert_all_pdfs_to_markdown()
