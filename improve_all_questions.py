#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import glob
import os

def _split_subtitle_sentences(text: str) -> str:
    """부제 문장을 문장 단위로 개행한다.
    - 한국어 서술형 종결(…다.) 뒤에 개행 추가
    - 세미콜론/콜론 뒤 선택적 개행
    - 연속 공백 정리 및 중복 개행 방지
    - 숫자 소수점(3.14)과 같은 패턴은 분리하지 않음
    """
    if not text:
        return text

    s = text

    # 기존 개행은 유지하고 과도한 공백은 한 칸으로 축약
    s = re.sub(r"\s+", lambda m: "\n" if "\n" in m.group(0) else " ", s)

    # '다.'로 끝나는 문장 뒤 개행 (이미 개행이면 유지)
    s = re.sub(r"다\.(\s*)(?!\n)", r"다.\n", s)

    # 물음표/느낌표 뒤 개행 (이미 개행이면 유지)
    s = re.sub(r"([!?])\s*(?!\n)", r"\1\n", s)

    # 세미콜론 뒤 개행은 선택적으로 처리
    s = re.sub(r";\s+(?=[가-힣A-Za-z0-9])", ";\n", s)

    # 소수점/번호 패턴 보호: 3.14, 1.2 등은 줄바꿈 대상에서 제외되어야 함
    # 위 규칙들이 개입하지 않도록 추가적인 처리는 하지 않음 (보수적)

    # 연속 개행 정리 (3개 이상 → 2개)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def improve_question_readability(question_text):
    """
    문제의 가독성을 전면적으로 개선합니다.
    - 표제(첫 번째 문장, ?로 끝나는) 이후에 개행 두 번 추가
    - 조건부/단서 조항을 별도 줄로 분리
    - 긴 문장들을 적절히 분리하여 가독성 향상
    """
    if not question_text:
        return question_text
    
    # 이미 많은 개행이 있는 경우는 추가 처리만 진행
    original_text = question_text
    
    # 패턴 1: "질문?" 바로 다음에 "(단," 이나 다른 내용이 오는 경우
    # 예: "질문?(단, 조건)" -> "질문?\n\n(단, 조건)"
    pattern1 = r'(\?)\s*(\([^)]*[단조건가정]\s*[^)]*\))'
    if re.search(pattern1, question_text):
        question_text = re.sub(pattern1, r'\1\n\n\2', question_text)
    
    # 패턴 2: "질문?" 바로 다음에 다른 설명이 오는 경우 (괄호가 아닌)
    # 예: "질문?다음은" -> "질문?\n\n다음은"
    pattern2 = r'(\?)\s*([가-힣A-Za-z][^?]*)'
    if re.search(pattern2, question_text) and '\\n' not in question_text:
        question_text = re.sub(pattern2, r'\1\n\n\2', question_text)
    
    # 패턴 3: 긴 조건부나 설명이 포함된 경우 적절히 분리
    # 예: "(단, 조건1, 조건2)" -> "(단, 조건1,\n조건2)"
    def improve_parentheses(match):
        content = match.group(0)
        # 괄호 안의 내용이 길면 쉼표 뒤에서 개행
        if len(content) > 50 and ',' in content:
            # 쉼표 뒤에 개행 추가 (단, 숫자,숫자 패턴은 제외)
            improved = re.sub(r',\s*(?![0-9])', ',\n', content)
            return improved
        return content
    
    question_text = re.sub(r'\([^)]{30,}\)', improve_parentheses, question_text)
    
    # 패턴 4: "다음" 으로 시작하는 부분들을 적절히 분리
    # 예: "질문?다음 중" -> "질문?\n\n다음 중"
    if '다음' in question_text and not re.search(r'\?\s*\n', question_text):
        question_text = re.sub(r'(\?)\s*(다음[^?]*)', r'\1\n\n\2', question_text)
    
    # 패턴 5: 보기나 선택지 설명이 포함된 경우
    # 예: "질문?<보기>" -> "질문?\n\n<보기>"
    if re.search(r'\?[^?\n]*[<＜].*?[>＞]', question_text):
        question_text = re.sub(r'(\?)([^?\n]*[<＜].*?[>＞])', r'\1\n\n\2', question_text)
    
    # 패턴 6: 목록이나 항목이 포함된 경우
    # 예: "질문?㉠ 항목1" -> "질문?\n\n㉠ 항목1"
    if re.search(r'\?[^?\n]*[㉠-㉧ⓐ-ⓩ①-⑨]', question_text):
        question_text = re.sub(r'(\?)([^?\n]*[㉠-㉧ⓐ-ⓩ①-⑨])', r'\1\n\n\2', question_text)
    
    # 패턴 7: "문제 XX" 패턴이 있는 경우 분리
    if re.search(r'\?[^?\n]*문제\s*[0-9]', question_text):
        question_text = re.sub(r'(\?)([^?\n]*문제\s*[0-9][^?]*)', r'\1\n\n\2', question_text)
    
    # 첫 문장의 '?'를 기준으로 표제/부제 분리 후, 부제 문장별 개행 강제
    m = re.match(r"^(.*?\?)(\s*)(.*)$", question_text, flags=re.DOTALL)
    if m:
        title = m.group(1).strip()
        rest = m.group(3).strip()
        if rest:
            rest = _split_subtitle_sentences(rest)
            question_text = f"{title}\n\n{rest}"

    # 불필요한 연속 개행 정리 (3개 이상 → 2개)
    question_text = re.sub(r"\n{3,}", "\n\n", question_text).strip()
    return question_text

def process_js_file(file_path):
    """JS 파일 처리 - 모든 question 필드에 대해 가독성 개선 적용"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content
        changes_made = 0
        total_questions = 0
        
        # "question": "..." 패턴을 찾아서 처리
        def replace_question(match):
            nonlocal changes_made, total_questions
            total_questions += 1
            full_match = match.group(0)
            question_content = match.group(1)
            
            # 이스케이프된 문자들을 실제 문자로 변환
            decoded = question_content.replace('\\"', '"').replace('\\n', '\n')
            
            # 가독성 개선
            improved = improve_question_readability(decoded)
            
            if improved != decoded:
                changes_made += 1
                # 다시 이스케이프
                encoded = improved.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                return f'"question": "{encoded}"'
            
            return full_match
        
        # question 필드 패턴 매칭 및 교체
        pattern = r'"question":\s*"((?:[^"\\]|\\.)*)"'
        updated_content = re.sub(pattern, replace_question, updated_content)
        
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"  ✅ {changes_made}/{total_questions}개 문제 개선")
            return True
        else:
            print(f"  ℹ️  {total_questions}개 문제 중 개선 대상 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False

def main():
    """메인 함수"""
    # 루트의 2025-*.js + 하위 폴더(2025/2025-*.js) 모두 처리
    js_files = sorted(set(glob.glob('2025-*.js') + glob.glob('2025/2025-*.js')))
    
    print("=" * 80)
    print("모든 문제 가독성 전면 개선 작업 시작")
    print("=" * 80)
    
    total_updated_files = 0
    total_updated_questions = 0
    total_questions = 0
    
    for file_path in js_files:
        subject_name = os.path.basename(file_path).replace('2025-', '').replace('.js', '')
        print(f"\n[{subject_name}] 처리 중...")
        
        # 변경 전 문제 수 체크
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            question_count = len(re.findall(r'"question":', content))
            total_questions += question_count
        
        if process_js_file(file_path):
            total_updated_files += 1
            # 변경된 문제 수 추출 (출력에서)
            # 이미 위에서 처리됨
    
    print(f"\n" + "=" * 80)
    print(f"작업 완료: {total_updated_files}개 파일 업데이트됨")
    print(f"전체 문제 수: {total_questions}개")
    print("=" * 80)
    
    # 변경사항 요약
    print(f"\n📊 변경사항 요약:")
    print(f"- 업데이트된 파일: {total_updated_files}개")
    print(f"- 가독성이 개선된 문제들에는 표제와 부제 구분, 조건부 분리 등이 적용되었습니다.")

if __name__ == "__main__":
    main()
