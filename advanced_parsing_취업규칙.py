#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def advanced_extract_questions(content):
    """고급 파싱 - 복잡한 구조 문제 처리 개선"""
    
    questions = []
    
    # 전체 텍스트를 문제 단위로 분할 
    # 패턴: 숫자. 으로 시작하는 라인을 기준으로 분할
    parts = re.split(r'\n(\d+\.)\s*', content)
    
    for i in range(1, len(parts), 2):  # 홀수 인덱스만 처리 (문제 번호 부분)
        if i + 1 < len(parts):
            question_num = parts[i].strip('.')
            question_content = parts[i + 1]
            
            try:
                # 선택지 패턴 찾기 - 더 정확한 패턴 사용
                choice_matches = re.findall(r'[①②③④]\s*([^①②③④\n]+?)(?=[①②③④]|\n\d+\.|\Z)', question_content, re.DOTALL)
                
                if len(choice_matches) >= 4:
                    # 문제 본문 추출 - 첫 번째 선택지 이전까지
                    question_text = re.split(r'[①②③④]', question_content)[0].strip()
                    
                    # 선택지 정리
                    clean_choices = []
                    for choice in choice_matches[:4]:
                        clean_choice = choice.strip().replace('\n', ' ')
                        clean_choice = re.sub(r'\s+', ' ', clean_choice)
                        clean_choices.append(clean_choice)
                    
                    # 문제 텍스트가 너무 짧거나 선택지 내용이 포함된 경우 스킵
                    if len(question_text) < 10 or any('㉠' in choice or '㉡' in choice for choice in clean_choices):
                        print(f"문제 {question_num}: 구조적 문제로 스킵")
                        continue
                    
                    question_obj = {
                        'question': question_text,
                        'a': clean_choices[0],
                        'b': clean_choices[1], 
                        'c': clean_choices[2],
                        'd': clean_choices[3],
                        'correct': 'a'  # 나중에 업데이트
                    }
                    
                    questions.append(question_obj)
                    print(f"문제 {question_num}: 성공적으로 파싱됨")
                    
                else:
                    print(f"문제 {question_num}: 선택지 부족 ({len(choice_matches)}개)")
                    
            except Exception as e:
                print(f"문제 {question_num} 파싱 중 오류: {e}")
    
    return questions

# 수동으로 문제가 있는 문제들을 고정
def fix_manual_questions():
    """수동으로 문제가 있는 문제들 수정"""
    
    manual_questions = [
        {
            'question': "다음은 연차휴가에 대한 설명 중 일부이다. 각 괄호 ㉠~㉣ 에 들어갈 숫자들을 모두 합한 값으로 알맞은 것은?\n\n① 연차휴가는 다음 각 호에 따른다.\n 1. 1년간 ( ㉠ )퍼센트 이상 출근하였을 때에는 ( ㉡ )일\n 2. 3년 이상 계속 근로한 직원에 대해서는 제1호의 휴가일수에 최초 1년을 초과하는 계속 근로 연수 2년에 대하여 1일을 가산한다.\n 3. 제2호에 따른 가산휴가를 포함한 총 휴가일수는 ( ㉢ )일을 한도로 한다.\n 4. 계속 근로 연수가 1년 미만인 직원 또는 1년간 ( ㉣ )퍼센트 미만 출근한 직원에게 1개월 개근 시 1일의 연차휴가를 주어야 한다.",
            'a': "190",
            'b': "200", 
            'c': "210",
            'd': "220",
            'correct': 'a'
        }
    ]
    
    return manual_questions

# 원본 텍스트 읽기
with open('/Users/hyungchangyoun/Documents/project/testpool/2025/5. 취업규칙.txt', 'r', encoding='utf-8') as f:
    content = f.read()

questions = advanced_extract_questions(content)

# 수동 수정 문제들 추가
manual_questions = fix_manual_questions()

print(f"\n자동 파싱된 문제 수: {len(questions)}")
print(f"수동 수정 문제 수: {len(manual_questions)}")

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

all_questions = questions + manual_questions

for i, question in enumerate(all_questions):
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

for i, q in enumerate(all_questions):
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

print(f"✅ 취업규칙 완료: {len(all_questions)}개 문제 (목표: 47개)")