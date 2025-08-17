#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def extract_questions_improved(content):
    """개선된 파싱 - 복잡한 다중구조 문제 처리"""
    
    questions = []
    
    # 전체 텍스트를 문제별로 분할
    # 더 정확한 문제 구분을 위해 패턴 개선
    question_pattern = r'(\d+\.)\s*([^①②③④]*?)(?=[①②③④])'
    choice_pattern = r'([①②③④])\s*([^①②③④\n]+?)(?=[①②③④]|\n\d+\.|\Z)'
    
    # 전체 내용에서 문제를 추출
    content_parts = re.split(r'\n\d+\.\s+', content)
    
    for i, part in enumerate(content_parts[1:], 1):  # 첫 번째는 빈 문자열이므로 제외
        try:
            # 현재 부분에서 선택지 찾기
            choices = re.findall(r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|\Z)', part, re.DOTALL)
            
            if len(choices) >= 4:
                # 문제 텍스트 추출 (선택지 이전 부분)
                question_text = re.split(r'[①②③④]', part)[0].strip()
                
                # 선택지 정리
                clean_choices = []
                for choice in choices[:4]:
                    clean_choice = choice.strip().replace('\n', ' ')
                    # 불필요한 공백 제거
                    clean_choice = re.sub(r'\s+', ' ', clean_choice)
                    clean_choices.append(clean_choice)
                
                question_obj = {
                    'question': question_text,
                    'a': clean_choices[0],
                    'b': clean_choices[1],
                    'c': clean_choices[2],
                    'd': clean_choices[3],
                    'correct': 'a'  # 나중에 업데이트
                }
                
                questions.append(question_obj)
                print(f"문제 {i}: 성공적으로 파싱됨")
                
            else:
                print(f"문제 {i}: 선택지 부족 ({len(choices)}개)")
                print(f"내용: {part[:200]}...")
                
        except Exception as e:
            print(f"문제 {i} 파싱 중 오류: {e}")
    
    return questions

def clean_question_text(text):
    """문제 텍스트 정리"""
    # 불필요한 공백과 줄바꿈 정리
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

# 원본 텍스트 읽기
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/5. 취업규칙.txt', 'r', encoding='utf-8') as f:
    content = f.read()

questions = extract_questions_improved(content)

print(f"\n총 파싱된 문제 수: {len(questions)}")

# 답안 데이터 로드
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/답안.txt', 'r', encoding='utf-8') as f:
    answer_content = f.read()

answer_data = json.loads(answer_content)
취업규칙_answers = answer_data.get('취업규칙', {})

# 해설 데이터 로드
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/해설.txt', 'r', encoding='utf-8') as f:
    explanation_content = f.read()

explanation_data = json.loads(explanation_content)
취업규칙_explanations = {}
for item in explanation_data:
    if item.get('과목') == '취업규칙':
        취업규칙_explanations[str(item['문항'])] = {
            'explanation': item['해설'],
            'url': item.get('url', '')
        }

# 답안과 해설 적용
answer_map = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

for i, question in enumerate(questions):
    question_num = i + 1
    
    # 답안 적용
    if str(question_num) in 취업규칙_answers:
        answer_value = 취업규칙_answers[str(question_num)]
        question['correct'] = answer_map.get(answer_value, 'a')
    
    # 해설 적용
    if str(question_num) in 취업규칙_explanations:
        exp_data = 취업규칙_explanations[str(question_num)]
        question['explanation'] = exp_data['explanation']
        question['urls'] = [exp_data['url']] if exp_data['url'] else [f"https://www.law.go.kr/학칙공단/한국농어촌공사 취업규칙/(9999,20241231)/관련조항"]
    else:
        question['explanation'] = "취업규칙 관련 조항"
        question['urls'] = [f"https://www.law.go.kr/학칙공단/한국농어촌공사 취업규칙/(9999,20241231)/관련조항"]

# JS 파일 생성
js_content = """// 취업규칙 문제 데이터

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
with open('/Users/hyungchangyoun/Documents/project/testpool/2025-data-취업규칙.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ 취업규칙 완료: {len(questions)}개 문제 (목표: 47개)")