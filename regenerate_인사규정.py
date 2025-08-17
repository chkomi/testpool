#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def parse_questions_from_text(content):
    """Parse questions from the original text file"""
    
    # Find all questions using pattern
    question_pattern = r'(\d+)\.\s*(.*?)(?=\d+\.\s*|$)'
    matches = re.findall(question_pattern, content, re.DOTALL)
    
    questions = []
    for num, question_text in matches:
        question_text = question_text.strip()
        
        # Look for choice patterns
        choices_pattern = r'[①②③④].*?(?=[①②③④]|$)'
        choices = re.findall(choices_pattern, question_text, re.DOTALL)
        
        if len(choices) >= 4:
            # Extract main question (before choices)
            question_only = re.split(r'[①②③④]', question_text)[0].strip()
            
            # Clean up choices
            clean_choices = []
            for choice in choices[:4]:
                clean_choice = re.sub(r'^[①②③④]\s*', '', choice.strip())
                clean_choices.append(clean_choice)
            
            question_obj = {
                'question': question_only,
                'a': clean_choices[0],
                'b': clean_choices[1], 
                'c': clean_choices[2],
                'd': clean_choices[3],
                'correct': 'a'  # Will be updated with actual answers
            }
            questions.append(question_obj)
            print(f"문제 {num}: 파싱 완료")
        else:
            print(f"문제 {num}: 선택지 부족 ({len(choices)}개)")
    
    return questions

# Load answer data
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/답안.txt', 'r', encoding='utf-8') as f:
    answer_content = f.read()

answer_data = json.loads(answer_content)
인사규정_answers = answer_data.get('인사규정', {})

# Load explanation data  
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/해설.txt', 'r', encoding='utf-8') as f:
    explanation_content = f.read()

explanation_data = json.loads(explanation_content)
# Filter for 인사규정 explanations
인사규정_explanations = {}
for item in explanation_data:
    if item.get('과목') == '인사규정':
        인사규정_explanations[str(item['문항'])] = {
            'explanation': item['해설'],
            'url': item.get('url', '')
        }

# Parse original text
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/6. 인사규정.txt', 'r', encoding='utf-8') as f:
    content = f.read()

questions = parse_questions_from_text(content)

# Apply answers and explanations
answer_map = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

for i, question in enumerate(questions):
    question_num = i + 1
    
    # Apply answer
    if str(question_num) in 인사규정_answers:
        answer_value = 인사규정_answers[str(question_num)]
        question['correct'] = answer_map.get(answer_value, 'a')
    
    # Apply explanation  
    if str(question_num) in 인사규정_explanations:
        exp_data = 인사규정_explanations[str(question_num)]
        question['explanation'] = exp_data['explanation']
        question['urls'] = [exp_data['url']] if exp_data['url'] else [f"https://www.law.go.kr/학칙공단/한국농어촌공사 인사규정/(9999,20241231)/관련조항"]
    else:
        question['explanation'] = "인사규정 관련 조항"
        question['urls'] = [f"https://www.law.go.kr/학칙공단/한국농어촌공사 인사규정/(9999,20241231)/관련조항"]

print(f"\n총 {len(questions)}개 문제 파싱 완료")
print(f"목표: 56개 문제")

if len(questions) >= 56:
    questions = questions[:56]  # Take first 56 questions
    print(f"56개 문제로 제한")

# Generate JS file content
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

# Write new file
with open('/Users/hyungchangyoun/Documents/project/testpool/2025-data-인사규정.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ 인사규정 데이터 재생성 완료: {len(questions)}개 문제")