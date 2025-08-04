import os
import sys
from pathlib import Path

try:
    import PyPDF2
    import pdfplumber
except ImportError as e:
    print("필요한 패키지가 설치되지 않았습니다.")
    print("다음 명령어로 설치해주세요:")
    print("pip install PyPDF2 pdfplumber")
    sys.exit(1)

def convert_pdf_to_markdown_pypdf2(pdf_path):
    """PyPDF2를 사용한 PDF 텍스트 추출"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            page_count = len(pdf_reader.pages)
            
            for i, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n## 페이지 {i}/{page_count}\n\n"
                    text += page_text + "\n\n"
                    
        return text
    except Exception as e:
        print(f"PyPDF2 오류: {e}")
        return None

def convert_pdf_to_markdown_pdfplumber(pdf_path):
    """pdfplumber를 사용한 PDF 텍스트 추출"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            page_count = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n## 페이지 {i}/{page_count}\n\n"
                    text += page_text + "\n\n"
                    
                # 표가 있는 경우 표 정보도 추출
                tables = page.extract_tables()
                if tables:
                    text += "### 표 정보\n\n"
                    for j, table in enumerate(tables, 1):
                        text += f"**표 {j}:**\n\n"
                        for row in table:
                            if row:
                                text += "| " + " | ".join(str(cell) if cell else "" for cell in row) + " |\n"
                        text += "\n"
                        
        return text
    except Exception as e:
        print(f"pdfplumber 오류: {e}")
        return None

def process_pdf_files():
    """현재 디렉터리와 docs 폴더의 PDF 파일들을 처리"""
    print("ex_py_pdf_converter 시작~~")
    
    current_dir = Path(__file__).parent
    docs_dir = current_dir / "docs"
    output_dir = current_dir / "docs_output"
    
    # 출력 폴더 생성
    output_dir.mkdir(exist_ok=True)
    
    # 처리할 디렉터리 목록
    directories_to_process = [current_dir]
    if docs_dir.exists():
        directories_to_process.append(docs_dir)
        print(f"📁 docs 폴더 발견: {docs_dir}")
    
    converted_count = 0
    failed_count = 0
    
    for directory in directories_to_process:
        print(f"\n🔍 {directory} 디렉터리 스캔 중...")
        
        for file_path in directory.glob("*.pdf"):
            if file_path.is_file():
                print(f"📄 {file_path.name} 처리 중...")
                
                # 먼저 pdfplumber 시도 (더 정확한 추출)
                text = convert_pdf_to_markdown_pdfplumber(file_path)
                method_used = "pdfplumber"
                
                # pdfplumber 실패시 PyPDF2 시도
                if not text:
                    print(f"   pdfplumber 실패, PyPDF2로 재시도...")
                    text = convert_pdf_to_markdown_pypdf2(file_path)
                    method_used = "PyPDF2"
                
                if text:
                    # 출력 파일명 생성
                    md_filename = file_path.stem + ".md"
                    output_path = output_dir / md_filename
                    
                    # 중복 파일명 처리
                    counter = 1
                    while output_path.exists():
                        md_filename = f"{file_path.stem}_{counter}.md"
                        output_path = output_dir / md_filename
                        counter += 1
                    
                    # 마크다운 파일로 저장
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(f"# {file_path.name}\n\n")
                        f.write(f"*변환 방법: {method_used}*\n\n")
                        f.write(f"*변환 시간: {Path(__file__).stat().st_mtime}*\n\n")
                        f.write("---\n\n")
                        f.write(text)
                    
                    print(f"✅ {file_path.name} → {md_filename} 변환 완료 ({method_used})")
                    converted_count += 1
                else:
                    print(f"❌ {file_path.name} 변환 실패 (모든 방법 시도함)")
                    failed_count += 1
    
    print(f"\n📊 변환 결과:")
    print(f"   - 변환 성공: {converted_count}개 파일")
    print(f"   - 변환 실패: {failed_count}개 파일")
    print(f"   - 출력 위치: {output_dir}")
    print("ex_py_pdf_converter 완료")

if __name__ == "__main__":
    process_pdf_files()
