#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import glob
import os
import json

def improve_question_readability(question_text):
    """
    문제의 가독성을 개선합니다.
    - 표제(첫 번째 문장, ?로 끝나는) 이후에 개행 두 번 추가
    - 부제 부분의 문장마다 개행 추가
    """
    if not question_text:
        return question_text
    
    # 이미 개행이 잘 되어있는 경우는 그대로 반환
    if question_text.count('\n') >= 2:
        return question_text
    
    # 첫 번째 ?를 찾아서 표제와 부제를 분리
    # 단, 긴 문장 내의 ?는 제외 (예: "100분의 ? 로 한다" 같은 경우)
    lines = question_text.split('\n')
    first_line = lines[0] if lines else question_text
    
    # 첫 번째 줄에서 ?를 찾되, 실제 문장 끝인지 확인
    question_marks = list(re.finditer(r'\?', first_line))
    
    title_end_pos = -1
    for match in question_marks:
        pos = match.start()
        # ? 다음에 오는 내용 확인
        after_question = first_line[pos+1:].strip()
        
        # ? 다음이 비어있거나 공백만 있으면 표제의 끝으로 간주
        if not after_question or after_question.startswith(' '):
            title_end_pos = pos + 1
            break
    
    if title_end_pos == -1:
        # 첫 번째 줄에 명확한 질문 끝이 없으면 원본 반환
        return question_text
    
    title = first_line[:title_end_pos].strip()
    remaining_first_line = first_line[title_end_pos:].strip()
    
    # 나머지 줄들과 첫 번째 줄의 나머지 부분을 합침
    all_remaining = []
    if remaining_first_line:
        all_remaining.append(remaining_first_line)
    if len(lines) > 1:
        all_remaining.extend(lines[1:])
    
    remaining_text = '\n'.join(all_remaining).strip()
    
    if not remaining_text:
        # 부제가 없으면 표제만 반환
        return title
    
    # 부제 부분 처리 - 문장별로 개행 추가
    # 긴 문장들을 적절히 나누어 가독성 향상
    sentences = re.split(r'([.!;](?:\s|$))', remaining_text)
    
    improved_subtitle = ""
    for i in range(0, len(sentences), 2):
        if i < len(sentences):
            sentence = sentences[i].strip()
            punctuation = sentences[i + 1].strip() if i + 1 < len(sentences) else ""
            
            if sentence:  # 빈 문장이 아닌 경우
                full_sentence = sentence + punctuation
                improved_subtitle += full_sentence
                # 마지막 문장이 아니고, 문장이 충분히 길면 개행 추가
                if i + 2 < len(sentences) and len(sentence) > 20:
                    improved_subtitle += "\n"
                elif i + 2 < len(sentences):
                    improved_subtitle += " "
    
    # 남은 부분이 있다면 추가 (마지막에 구두점이 없는 경우)
    if len(sentences) % 2 == 1 and len(sentences) > 1:
        last_part = sentences[-1].strip()
        if last_part:
            improved_subtitle += last_part
    
    # 표제 + 개행 두 번 + 개선된 부제
    if improved_subtitle.strip():
        return title + "\n\n" + improved_subtitle.strip()
    else:
        return title

def parse_js_file(file_path):
    """JS 파일에서 quizData 배열을 파싱"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 각 question 객체를 개별적으로 파싱
        questions = []
        
        # { 로 시작하는 객체들을 찾기
        question_pattern = r'(\{[^{}]*?"questionNumber":\s*(\d+).*?\})'
        
        # 중첩된 중괄호를 고려한 더 정교한 패턴
        brace_count = 0
        current_obj = ""
        in_question = False
        
        lines = content.split('\n')
        for line in lines:
            stripped = line.strip()
            
            if '"questionNumber"' in line and not in_question:
                in_question = True
                current_obj = ""
                brace_count = 0
            
            if in_question:
                current_obj += line + '\n'
                
                # 중괄호 카운트
                brace_count += line.count('{') - line.count('}')
                
                # 객체가 완성되면
                if brace_count == 0 and stripped.endswith((',', '}')):
                    # questionNumber 추출
                    q_match = re.search(r'"questionNumber":\s*(\d+)', current_obj)
                    if q_match:
                        questions.append({
                            'questionNumber': int(q_match.group(1)),
                            'object_text': current_obj.rstrip(',\n').strip()
                        })
                    in_question = False
                    current_obj = ""
        
        return questions
            
    except Exception as e:
        print(f"파일 읽기 오류 ({file_path}): {e}")
        return []

def update_js_file(file_path, questions_data):
    """JS 파일의 question 필드를 업데이트"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content
        
        for q_data in questions_data:
            question_num = q_data['questionNumber']
            object_text = q_data['object_text']
            
            # question 필드 추출
            question_match = re.search(r'"question":\s*"((?:[^"\\]|\\.)*)"', object_text)
            if question_match:
                original_question = question_match.group(1)
                # 이스케이프된 문자 처리
                decoded_question = original_question.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
                
                # 가독성 개선
                improved_question = improve_question_readability(decoded_question)
                
                # 다시 이스케이프
                encoded_question = improved_question.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                
                if encoded_question != original_question:
                    print(f"문제 {question_num}: 가독성 개선 적용")
                    # 해당 문제의 question 필드 교체
                    pattern = rf'("questionNumber":\s*{question_num}[\s\S]*?"question":\s*")([^"\\]|\\.)*(")'
                    replacement = rf'\g<1>{encoded_question}\g<3>'
                    updated_content = re.sub(pattern, replacement, updated_content)
        
        # 파일 업데이트
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        return False
            
    except Exception as e:
        print(f"파일 업데이트 오류 ({file_path}): {e}")
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
        
        # 문제 파싱
        questions = parse_js_file(file_path)
        if not questions:
            print(f"  ⚠️  문제를 찾을 수 없습니다.")
            continue
        
        print(f"  📝 총 {len(questions)}개 문제 발견")
        
        # 파일 업데이트
        if update_js_file(file_path, questions):
            print(f"  ✅ 파일 업데이트 완료")
            total_updated += 1
        else:
            print(f"  ℹ️  변경사항 없음")
    
    print(f"\n" + "=" * 80)
    print(f"작업 완료: {total_updated}개 파일 업데이트됨")
    print("=" * 80)

if __name__ == "__main__":
    main()