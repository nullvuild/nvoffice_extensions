import os
import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("markitdown 패키지가 설치되지 않았습니다.")
    print("다음 명령어로 설치해주세요: pip install markitdown")
    sys.exit(1)

def convert_files_to_markdown():
    """현재 폴더의 docs/ 디렉토리에 있는 모든 파일을 Markdown으로 변환"""
    
    # 현재 스크립트가 있는 디렉토리
    current_dir = Path(__file__).parent
    docs_dir = current_dir / "docs"
    output_dir = current_dir / "docs_output"
    
    print(f"ex_py_markitdown 시작~~")
    print(f"현재 디렉토리: {current_dir}")
    print(f"docs 폴더 경로: {docs_dir}")
    
    # docs 폴더가 존재하는지 확인
    if not docs_dir.exists():
        print(f"❌ docs 폴더를 찾을 수 없습니다: {docs_dir}")
        print("docs 폴더를 생성하고 변환할 파일들을 넣어주세요.")
        return
    
    # 출력 폴더 생성
    output_dir.mkdir(exist_ok=True)
    print(f"📁 출력 폴더: {output_dir}")
    
    # MarkItDown 인스턴스 생성
    md = MarkItDown()
    
    # 변환할 파일 확장자 목록
    supported_extensions = {'.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.txt', '.html', '.htm'}
    
    # docs 폴더의 모든 파일 처리
    converted_count = 0
    skipped_count = 0
    
    for file_path in docs_dir.rglob('*'):
        if file_path.is_file():
            file_extension = file_path.suffix.lower()
            
            if file_extension in supported_extensions:
                try:
                    print(f"🔄 변환 중: {file_path.name}")
                    
                    # 파일을 Markdown으로 변환
                    result = md.convert(str(file_path))
                    
                    # 출력 파일명 생성 (원본 파일명 + .md)
                    output_filename = file_path.stem + '.md'
                    output_path = output_dir / output_filename
                    
                    # 중복 파일명 처리
                    counter = 1
                    while output_path.exists():
                        output_filename = f"{file_path.stem}_{counter}.md"
                        output_path = output_dir / output_filename
                        counter += 1
                    
                    # Markdown 파일로 저장
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(result.text_content)
                    
                    print(f"✅ 변환 완료: {output_filename}")
                    converted_count += 1
                    
                except Exception as e:
                    print(f"❌ 변환 실패 ({file_path.name}): {str(e)}")
                    skipped_count += 1
            else:
                print(f"⏭️  지원하지 않는 형식: {file_path.name} ({file_extension})")
                skipped_count += 1
    
    print(f"\n📊 변환 결과:")
    print(f"   - 변환 성공: {converted_count}개 파일")
    print(f"   - 건너뛴 파일: {skipped_count}개 파일")
    print(f"   - 출력 위치: {output_dir}")
    print("ex_py_markitdown 완료")

if __name__ == "__main__":
    convert_files_to_markdown()
