#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os

# 과목 매핑
SUBJECT_MAPPING = {
    "1. 농어촌정비법.txt": "농어촌정비법",
    "2. 공운법.txt": "공운법", 
    "3. 공사법.txt": "공사법",
    "4. 직제규정.txt": "직제규정",
    "5. 취업규칙.txt": "취업규칙",
    "6. 인사규정.txt": "인사규정",
    "7. 행동강령.txt": "행동강령",
    "8. 회계기준.txt": "회계기준"
}

def load_answers():
    """답안 파일 로드"""
    with open('답안.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # JSON 파싱
    answers_data = json.loads(content)
    return answers_data

def load_explanations():
    """해설 파일 로드"""
    with open('해설.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # JSON 배열 파싱
    explanations_data = json.loads(content)
    
    # 과목별로 정리
    explanations_by_subject = {}
    for item in explanations_data:
        subject = item['과목']
        question_num = item['문항']
        if subject not in explanations_by_subject:
            explanations_by_subject[subject] = {}
        
        # URL 정보 수집 (url, url1, url2, url3 등)
        urls = []
        for key in item:
            if key.startswith('url'):
                urls.append(item[key])
        
        # 첫 번째 URL 사용, 없으면 기본값
        primary_url = urls[0] if urls else f"https://www.law.go.kr/법령/{subject}"
        
        explanations_by_subject[subject][question_num] = {
            '해설': item['해설'],
            'url': primary_url,
            'urls': urls  # 모든 URL 보관
        }
    
    return explanations_by_subject

def parse_question_file(filename):
    """문제 파일 파싱"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 문제별로 분리 (숫자로 시작하는 줄을 기준으로)
    questions = []
    current_question = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 숫자로 시작하는 줄이면 새로운 문제 시작
        if re.match(r'^\d+\.', line):
            if current_question:
                questions.append('\n'.join(current_question))
            current_question = [line]
        else:
            if current_question:
                current_question.append(line)
    
    # 마지막 문제 추가
    if current_question:
        questions.append('\n'.join(current_question))
    
    return questions

def parse_single_question(question_text):
    """개별 문제 파싱"""
    lines = question_text.strip().split('\n')
    
    # 문제 번호 추출
    first_line = lines[0]
    question_num_match = re.match(r'^(\d+)\.', first_line)
    if not question_num_match:
        return None
    
    question_num = int(question_num_match.group(1))
    
    # 문제 내용과 선택지 분리
    question_content = []
    choices = {'a': '', 'b': '', 'c': '', 'd': ''}
    choice_pattern = re.compile(r'^[①②③④]')
    
    current_choice = None
    
    for line in lines[1:]:  # 첫 번째 줄(문제번호) 제외
        line = line.strip()
        if not line:
            continue
            
        # 선택지 시작 확인
        if line.startswith('①'):
            current_choice = 'a'
            choices['a'] = line[1:].strip()
        elif line.startswith('②'):
            current_choice = 'b' 
            choices['b'] = line[1:].strip()
        elif line.startswith('③'):
            current_choice = 'c'
            choices['c'] = line[1:].strip()
        elif line.startswith('④'):
            current_choice = 'd'
            choices['d'] = line[1:].strip()
        else:
            # 선택지가 시작되기 전이면 문제 내용
            if current_choice is None:
                question_content.append(line)
            else:
                # 선택지 내용이 여러 줄인 경우
                if current_choice and current_choice in choices:
                    choices[current_choice] += ' ' + line
    
    # 모든 선택지가 있는지 확인
    if not all(choices[key].strip() for key in ['a', 'b', 'c', 'd']):
        print(f"  Warning: Question {question_num} missing choices: {choices}")
        return None
    
    # 문제 텍스트에서 번호 제거하고 정리
    question_text_clean = first_line[first_line.find('.') + 1:].strip()
    if question_content:
        question_text_clean += '\n' + '\n'.join(question_content)
    
    return {
        'question_num': question_num,
        'question': question_text_clean,
        'choices': choices
    }

def convert_answer_number_to_letter(num):
    """숫자 답안을 문자로 변환 (1->a, 2->b, 3->c, 4->d)"""
    mapping = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    return mapping.get(num, 'a')

def process_subject(filename, subject_name, answers_data, explanations_data):
    """과목별 처리"""
    print(f"Processing {subject_name}...")
    
    # 답안 데이터에서 해당 과목의 문제 번호들 가져오기
    subject_answers = answers_data.get(subject_name, {})
    available_questions = [int(q) for q in subject_answers.keys()]
    available_questions.sort()
    
    print(f"  Available answers: {len(available_questions)} questions (1-{max(available_questions) if available_questions else 0})")
    
    # 문제 파일 파싱
    questions = parse_question_file(filename)
    print(f"  Parsed questions from TXT: {len(questions)}")
    
    quiz_data = []
    
    for question_text in questions:
        parsed = parse_single_question(question_text)
        if not parsed:
            continue
            
        question_num = parsed['question_num']
        
        # 답안이 있는 문제만 처리
        if question_num not in available_questions:
            print(f"  Skipping question {question_num} (no answer available)")
            continue
            
        correct_num = subject_answers[str(question_num)]
        correct_letter = convert_answer_number_to_letter(correct_num)
        
        # 해설 가져오기
        explanation_info = explanations_data.get(subject_name, {}).get(question_num, {})
        explanation = explanation_info.get('해설', f"{subject_name} 관련 법령에 따른 정답입니다.")
        url = explanation_info.get('url', f"https://www.law.go.kr/법령/{subject_name}")
        
        # JSON 객체 생성
        question_obj = {
            "questionNumber": question_num,
            "question": parsed['question'],
            "a": parsed['choices']['a'],
            "b": parsed['choices']['b'], 
            "c": parsed['choices']['c'],
            "d": parsed['choices']['d'],
            "correct": correct_letter,
            "explanation": explanation,
            "url": url
        }
        
        quiz_data.append(question_obj)
    
    return quiz_data

def main():
    # 답안과 해설 데이터 로드
    answers_data = load_answers()
    explanations_data = load_explanations()
    
    # 각 과목별 처리
    for filename, subject_name in SUBJECT_MAPPING.items():
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found")
            continue
            
        # 과목 처리
        quiz_data = process_subject(filename, subject_name, answers_data, explanations_data)
        
        # JS 파일 생성 (파일명에서 숫자 추출)
        file_number = filename.split('.')[0]
        output_filename = f"{file_number}.{subject_name}.js"
        
        js_content = f"""// 2025년 사전공개문제 - {subject_name}

const quizData = {json.dumps(quiz_data, ensure_ascii=False, indent=4)};
"""
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"✓ Created {output_filename} with {len(quiz_data)} questions")

if __name__ == "__main__":
    main()