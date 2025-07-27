import os
import sys
from playwright.sync_api import sync_playwright

def convert_all_htmls_to_pdf(input_file_path="html", output_file_path="pdf"):
    if not os.path.exists(input_file_path):
        print(f"입력 폴더가 존재하지 않습니다: {input_file_path}")
        sys.exit(1)
    if not os.path.exists(output_file_path) and not os.environ.get('TESTING'):
        os.makedirs(output_file_path, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for filename in os.listdir(input_file_path):
            if filename.lower().endswith((".html", ".htm")):
                html_path = os.path.join(input_file_path, filename)
                pdf_filename = os.path.splitext(filename)[0] + ".pdf"
                pdf_path = os.path.join(output_file_path, pdf_filename)
                print(f"변환 중: {html_path}")
                try:
                    page = browser.new_page()
                    page.goto(f"file://{os.path.abspath(html_path)}")
                    if not os.environ.get('TESTING'):
                        # 이미 존재하는 PDF 파일인지 점검
                        if os.path.exists(pdf_path):
                            print(f"⚠️  이미 존재하는 파일: {pdf_path}")
                            print(f"   기존 파일을 덮어씁니다.")
                        
                        # PDF 생성
                        page.pdf(path=pdf_path, format='A4', print_background=True)
                        print(f"✅ PDF 파일 저장 완료: {pdf_path}")
                    else:
                        print(f"(테스트 환경) PDF 파일 생성 생략: {pdf_path}")
                    page.close()
                except Exception as e:
                    print(f"에러 발생: {filename} - {e}")
        browser.close()

if __name__ == "__main__":
    convert_all_htmls_to_pdf()
