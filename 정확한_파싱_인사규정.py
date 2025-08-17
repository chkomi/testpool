#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def extract_questions_precisely(content):
    """정확한 문제 추출을 위한 개선된 파싱"""
    
    questions = []
    
    # 문제 번호로 시작하는 라인들 찾기
    question_lines = []
    for i, line in enumerate(content.split('\n')):
        if re.match(r'^\d+\.\s+', line.strip()):
            question_lines.append((i, line.strip()))
    
    print(f"발견된 문제 번호 라인 수: {len(question_lines)}")
    
    for idx, (line_num, question_line) in enumerate(question_lines):
        try:
            # 문제 번호 추출
            question_num = int(re.match(r'^(\d+)\.', question_line).group(1))
            
            # 다음 문제의 시작점 찾기
            if idx + 1 < len(question_lines):
                next_line_num = question_lines[idx + 1][0]
            else:
                next_line_num = len(content.split('\n'))
            
            # 현재 문제의 전체 텍스트 추출
            content_lines = content.split('\n')
            question_content = '\n'.join(content_lines[line_num:next_line_num])
            
            # 문제 텍스트에서 선택지 분리
            question_text = re.sub(r'^(\d+\.\s+)', '', question_content, count=1)
            
            # 선택지 패턴 찾기 (①②③④ 또는 ① ② ③ ④)
            choice_pattern = r'[①②③④]\s*[^①②③④\n]*'
            choices = re.findall(choice_pattern, question_text, re.DOTALL)
            
            if len(choices) >= 4:
                # 문제 본문 (선택지 제거)
                question_only = re.split(r'[①②③④]', question_text)[0].strip()
                
                # 선택지 정리
                clean_choices = []
                for choice in choices[:4]:
                    clean_choice = re.sub(r'^[①②③④]\s*', '', choice.strip())
                    clean_choice = clean_choice.replace('\n', ' ').strip()
                    clean_choices.append(clean_choice)
                
                question_obj = {
                    'question': question_only,
                    'a': clean_choices[0],
                    'b': clean_choices[1],
                    'c': clean_choices[2],
                    'd': clean_choices[3],
                    'correct': 'a'  # 나중에 업데이트
                }
                
                questions.append(question_obj)
                print(f"문제 {question_num}: 성공적으로 파싱됨")
                
            else:
                print(f"문제 {question_num}: 선택지 부족 ({len(choices)}개) - 내용을 자세히 확인 필요")
                print(f"문제 내용 시작: {question_text[:200]}...")
                
        except Exception as e:
            print(f"문제 {idx+1} 파싱 중 오류: {e}")
    
    return questions

# 원본 텍스트 읽기
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/6. 인사규정.txt', 'r', encoding='utf-8') as f:
    content = f.read()

questions = extract_questions_precisely(content)

print(f"\n총 파싱된 문제 수: {len(questions)}")

# 답안 데이터 로드
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/답안.txt', 'r', encoding='utf-8') as f:
    answer_content = f.read()

answer_data = json.loads(answer_content)
인사규정_answers = answer_data.get('인사규정', {})

# 해설 데이터 로드
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/해설.txt', 'r', encoding='utf-8') as f:
    explanation_content = f.read()

explanation_data = json.loads(explanation_content)
인사규정_explanations = {}
for item in explanation_data:
    if item.get('과목') == '인사규정':
        인사규정_explanations[str(item['문항'])] = {
            'explanation': item['해설'],
            'url': item.get('url', '')
        }

# 답안과 해설 적용
answer_map = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

for i, question in enumerate(questions):
    question_num = i + 1
    
    # 답안 적용
    if str(question_num) in 인사규정_answers:
        answer_value = 인사규정_answers[str(question_num)]
        question['correct'] = answer_map.get(answer_value, 'a')
    
    # 해설 적용
    if str(question_num) in 인사규정_explanations:
        exp_data = 인사규정_explanations[str(question_num)]
        question['explanation'] = exp_data['explanation']
        question['urls'] = [exp_data['url']] if exp_data['url'] else [f"https://www.law.go.kr/학칙공단/한국농어촌공사 인사규정/(9999,20241231)/관련조항"]
    else:
        question['explanation'] = "인사규정 관련 조항"
        question['urls'] = [f"https://www.law.go.kr/학칙공단/한국농어촌공사 인사규정/(9999,20241231)/관련조항"]

# JS 파일 생성
js_content = """// 인사규정 문제 데이터

window.currentSubjectQuestions = [
"""

for i, q in enumerate(questions):
    if i > 0:
        js_content += ",\n"
    
    js_content += f"""        {{
            "question": {json.dumps(q['question'], ensure_ascii=False)},
            "a": {json.dumps(q['a'], ensure_ascii=False)},
            "b": {json.dumps(q['b'], ensure_ascii=False)},
            "c": {json.dumps(q['c'], ensure_ascii=False)},
            "d": {json.dumps(q['d'], ensure_ascii=False)},
            "correct": {json.dumps(q['correct'], ensure_ascii=False)},
            "explanation": {json.dumps(q['explanation'], ensure_ascii=False)},
            "urls": {json.dumps(q['urls'], ensure_ascii=False)}
        }}"""

js_content += """
];
"""

# 파일 저장
with open('/Users/hyungchangyoun/Documents/project/testpool/2025-data-인사규정.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ 인사규정 완료: {len(questions)}개 문제 (목표: 56개)")