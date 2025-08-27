#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import glob
import os

def improve_question_readability(question_text):
    """
    문제의 가독성을 개선합니다.
    - 표제(첫 번째 문장, ?로 끝나는) 이후에 개행 두 번 추가
    - 부제 부분의 긴 문장들도 적절히 개행 추가
    """
    if not question_text:
        return question_text
    
    # 이미 개행이 충분히 있는 경우는 건드리지 않음
    if question_text.count('\\n') >= 3:
        return question_text
    
    # 첫 번째 ?를 찾아서 표제와 부제를 분리
    # ? 다음에 바로 다른 내용이 이어지는 경우만 처리
    match = re.search(r'^(.+?\?)(\s*)(.*)$', question_text, re.DOTALL)
    
    if not match:
        return question_text
    
    title = match.group(1).strip()
    space_after = match.group(2)
    remaining = match.group(3).strip()
    
    if not remaining:
        return question_text  # 부제가 없으면 원본 반환
    
    # 부제가 있고, 표제 바로 다음에 붙어있으면 개행 추가
    if not space_after or space_after == ' ':
        # 부제 부분도 개선
        improved_remaining = improve_subtitle(remaining)
        return title + '\\n\\n' + improved_remaining
    
    return question_text

def improve_subtitle(text):
    """부제 부분의 가독성 개선"""
    if not text:
        return text
    
    # 긴 문장들을 적절히 나누어 개행 추가
    # 마침표나 세미콜론 다음에 개행 추가
    improved = text
    
    # ". " 패턴을 찾아서 개행으로 변경 (단, 숫자.숫자 같은 경우는 제외)
    improved = re.sub(r'\.(\s+)(?=[A-Z가-힣])', '.\\n', improved)
    improved = re.sub(r';(\s+)', ';\\n', improved)
    
    # 너무 긴 문장은 적절한 지점에서 개행 (단, 기존 구조 유지)
    lines = improved.split('\\n')
    final_lines = []
    
    for line in lines:
        line = line.strip()
        if len(line) > 100:
            # 쉼표나 접속사 등에서 적절히 나누기
            parts = re.split(r'(,\s*(?=그리고|그러나|또한|따라서|하지만))', line)
            if len(parts) > 1:
                current_line = ""
                for part in parts:
                    if current_line and len(current_line + part) > 80:
                        final_lines.append(current_line.strip())
                        current_line = part.strip()
                    else:
                        current_line += part
                if current_line.strip():
                    final_lines.append(current_line.strip())
            else:
                final_lines.append(line)
        else:
            final_lines.append(line)
    
    return '\\n'.join(final_lines)

def process_js_file(file_path):
    """JS 파일 처리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content
        changes_made = 0
        
        # "question": "..." 패턴을 찾아서 처리
        def replace_question(match):
            nonlocal changes_made
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
            print(f"  ✅ {changes_made}개 문제 개선")
            return True
        else:
            print(f"  ℹ️  개선 대상 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False

def main():
    """메인 함수"""
    js_files = glob.glob('2025-*.js')
    
    print("=" * 80)
    print("문제 가독성 개선 작업 시작")
    print("=" * 80)
    
    total_updated = 0
    
    for file_path in sorted(js_files):
        subject_name = os.path.basename(file_path).replace('2025-', '').replace('.js', '')
        print(f"\n[{subject_name}] 처리 중...")
        
        if process_js_file(file_path):
            total_updated += 1
    
    print(f"\n" + "=" * 80)
    print(f"작업 완료: {total_updated}개 파일 업데이트됨")
    print("=" * 80)

if __name__ == "__main__":
    main()