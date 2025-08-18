#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os

def load_answers():
    """답안.txt에서 각 과목별 정답을 로드"""
    try:
        with open('답안.txt', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: 답안.txt file not found")
        return {}
    except json.JSONDecodeError:
        print("Error: 답안.txt is not valid JSON")
        return {}

def load_explanations():
    """해설.txt에서 각 과목별 해설을 로드"""
    try:
        with open('해설.txt', 'r', encoding='utf-8') as f:
            explanations_list = json.load(f)
            
        # 과목과 문항별로 인덱싱
        explanations = {}
        for item in explanations_list:
            subject = item['과목']
            question_num = str(item['문항'])
            
            if subject not in explanations:
                explanations[subject] = {}
            
            # URL 처리 (url, url1, url2 등 다양한 형태 지원)
            url = item.get('url') or item.get('url1') or item.get('url2') or f"https://www.law.go.kr/법령/{subject}"
            
            explanations[subject][question_num] = {
                'explanation': item['해설'],
                'url': url
            }
        
        return explanations
    except FileNotFoundError:
        print("Error: 해설.txt file not found")
        return {}
    except json.JSONDecodeError:
        print("Error: 해설.txt is not valid JSON")
        return {}

def parse_question_from_txt(file_path):
    """TXT 파일에서 문제를 파싱"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} file not found")
        return []
    
    questions = []
    
    # 문제 번호로 분할 (1., 2., 3., ... 패턴) - 더 정확한 패턴
    question_splits = re.split(r'\n(\d+)\.\s*', content)
    
    # 첫 번째 요소는 제목 부분이므로 제거
    question_splits = question_splits[1:]
    
    # 짝수 인덱스: 문제 번호, 홀수 인덱스: 문제 내용
    for i in range(0, len(question_splits), 2):
        if i + 1 >= len(question_splits):
            break
            
        question_num = int(question_splits[i])
        question_content = question_splits[i + 1].strip()
        
        # 선택지 찾기 (① ② ③ ④ 또는 ➀ ➁ ➂ ➃)
        choices = []
        choice_pattern = r'[①➀]\s*(.*?)[②➁]\s*(.*?)[③➂]\s*(.*?)[④➃]\s*(.*?)(?=\n\n|\Z)'
        match = re.search(choice_pattern, question_content, re.DOTALL)
        
        if match:
            choices = [
                match.group(1).strip(),
                match.group(2).strip(), 
                match.group(3).strip(),
                match.group(4).strip()
            ]
            
            # 문제 본문 추출 (첫 번째 ① 또는 ➀ 이전까지)
            question_text = re.split(r'[①➀]', question_content)[0].strip()
            
            questions.append({
                'questionNumber': question_num,
                'question': question_text,
                'choices': {
                    'a': choices[0],
                    'b': choices[1], 
                    'c': choices[2],
                    'd': choices[3]
                }
            })
        else:
            print(f"Warning: Question {question_num} does not have exactly 4 choices")
    
    return questions

def number_to_letter(num):
    """숫자 정답을 문자로 변환 (1->a, 2->b, 3->c, 4->d)"""
    mapping = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    return mapping.get(num, 'a')

def escape_json_string(text):
    """JSON 문자열을 안전하게 이스케이프"""
    if not text:
        return ""
    # 백슬래시, 쌍따옴표, 제어문자 이스케이프
    text = text.replace('\\', '\\\\')  # 백슬래시 먼저 처리
    text = text.replace('"', '\\"')   # 쌍따옴표 이스케이프
    text = text.replace('\n', '\\n')  # 개행문자 이스케이프
    text = text.replace('\r', '\\r')  # 캐리지 리턴 이스케이프
    text = text.replace('\t', '\\t')  # 탭 이스케이프
    return text

def process_subject(subject_name, file_number):
    """개별 과목 처리"""
    print(f"Processing {subject_name}...")
    
    # TXT 파일에서 문제 파싱
    txt_file = f"{file_number}. {subject_name}.txt"
    questions = parse_question_from_txt(txt_file)
    
    if not questions:
        print(f"  No questions found in {txt_file}")
        return
    
    # 답안과 해설 로드
    answers = load_answers()
    explanations = load_explanations()
    
    subject_answers = answers.get(subject_name, {})
    subject_explanations = explanations.get(subject_name, {})
    
    # JSON 데이터 구성
    quiz_data = []
    
    for question in questions:
        question_num = question['questionNumber']
        question_num_str = str(question_num)
        
        # 정답 찾기
        correct_num = subject_answers.get(question_num_str)
        if correct_num is None:
            print(f"  Warning: No answer found for question {question_num}")
            continue
        
        correct_letter = number_to_letter(correct_num)
        
        # 해설 찾기
        explanation_data = subject_explanations.get(question_num_str, {})
        explanation = explanation_data.get('explanation', f"{subject_name} 관련 법령")
        url = explanation_data.get('url', f"https://www.law.go.kr/법령/{subject_name}")
        
        # 최종 데이터 구성
        item = {
            "questionNumber": question_num,
            "question": question['question'],
            "a": question['choices']['a'],
            "b": question['choices']['b'],
            "c": question['choices']['c'],
            "d": question['choices']['d'],
            "correct": correct_letter,
            "explanation": explanation,
            "url": url
        }
        
        quiz_data.append(item)
    
    # JS 파일 생성
    js_content = f"// 2025년 사전공개문제 - {subject_name}\n\n"
    js_content += "const quizData = [\n"
    
    for i, item in enumerate(quiz_data):
        js_content += "    {\n"
        js_content += f'        "questionNumber": {item["questionNumber"]},\n'
        js_content += f'        "question": "{escape_json_string(item["question"])}",\n'
        js_content += f'        "a": "{escape_json_string(item["a"])}",\n'
        js_content += f'        "b": "{escape_json_string(item["b"])}",\n'
        js_content += f'        "c": "{escape_json_string(item["c"])}",\n'
        js_content += f'        "d": "{escape_json_string(item["d"])}",\n'
        js_content += f'        "correct": "{item["correct"]}",\n'
        js_content += f'        "explanation": "{escape_json_string(item["explanation"])}",\n'
        js_content += f'        "url": "{escape_json_string(item["url"])}"\n'
        js_content += "    }"
        
        if i < len(quiz_data) - 1:
            js_content += ","
        js_content += "\n"
    
    js_content += "];\n"
    
    # 파일 저장
    output_file = f"{file_number}.{subject_name}.js"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"✓ Created {output_file} with {len(quiz_data)} questions")
    except Exception as e:
        print(f"  Error writing {output_file}: {e}")

def main():
    """메인 실행 함수"""
    subjects = [
        ("1", "농어촌정비법"),
        ("2", "공운법"),
        ("3", "공사법"),
        ("4", "직제규정"),
        ("5", "취업규칙"),
        ("6", "인사규정"),
        ("7", "행동강령"),
        ("8", "회계기준")
    ]
    
    print("🔄 Starting conversion process...")
    
    for file_number, subject_name in subjects:
        process_subject(subject_name, file_number)
    
    print("\n✅ Conversion completed!")

if __name__ == "__main__":
    main()