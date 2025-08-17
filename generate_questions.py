#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os

def parse_questions_from_txt(txt_file_path, subject_name, answers):
    """txt 파일에서 문제를 파싱하여 구조화된 데이터로 변환"""
    
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 문제 번호 패턴: "1.", "2.", "3." 등
    question_pattern = r'(\d+)\.\s*(.*?)(?=\d+\.|$)'
    
    questions = []
    matches = re.findall(question_pattern, content, re.DOTALL)
    
    for match in matches:
        question_num = int(match[0])
        question_text = match[1].strip()
        
        # 4지선다 보기 추출
        choices = []
        choice_pattern = r'[①②③④]\s*(.*?)(?=[①②③④]|$)'
        choice_matches = re.findall(choice_pattern, question_text, re.DOTALL)
        
        if len(choice_matches) >= 4:
            # 문제 본문과 보기 분리
            question_body = question_text.split('①')[0].strip()
            
            # 보기들 정리
            for i, choice in enumerate(choice_matches[:4]):
                choice = choice.strip()
                if choice:
                    choices.append(choice)
            
            # 답안 확인
            correct_answer = None
            if str(question_num) in answers:
                correct_num = answers[str(question_num)]
                if correct_num == 1:
                    correct_answer = "a"
                elif correct_num == 2:
                    correct_answer = "b"
                elif correct_num == 3:
                    correct_answer = "c"
                elif correct_num == 4:
                    correct_answer = "d"
            
            if correct_answer and len(choices) == 4:
                question_data = {
                    "question": question_body,
                    "a": choices[0],
                    "b": choices[1],
                    "c": choices[2],
                    "d": choices[3],
                    "correct": correct_answer,
                    "explanation": f"{subject_name} 관련 법령에 따른 정답입니다.",
                    "url": f"https://www.law.go.kr/법령/{subject_name}"
                }
                questions.append(question_data)
    
    return questions

def generate_js_file(subject_name, questions, output_file):
    """문제 데이터를 js 파일로 생성"""
    
    js_content = f"""// 2025년 사전공개문제 - {subject_name}

const quizData = {json.dumps(questions, ensure_ascii=False, indent=4)};
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"{output_file} 생성 완료! 총 {len(questions)}문제")

def main():
    # 답안 파일 읽기
    with open('2025/답안.txt', 'r', encoding='utf-8') as f:
        answers_content = f.read()
    
    # 답안 파싱
    answers_data = json.loads(answers_content)
    
    # 과목별 설정
    subjects = {
        "농어촌정비법": {
            "txt_file": "2025/1. 농어촌정비법.txt",
            "output_file": "2025-nongchon.js",
            "question_count": 134
        },
        "공운법": {
            "txt_file": "2025/2. 공운법.txt",
            "output_file": "2025-gongun.js",
            "question_count": 91
        },
        "공사법": {
            "txt_file": "2025/3. 공사법.txt",
            "output_file": "2025-gongsa.js",
            "question_count": 102
        },
        "직제규정": {
            "txt_file": "2025/4. 직제규정.txt",
            "output_file": "2025-jikje.js",
            "question_count": 27
        },
        "취업규칙": {
            "txt_file": "2025/5. 취업규칙.txt",
            "output_file": "2025-chwip.js",
            "question_count": 47
        },
        "인사규정": {
            "txt_file": "2025/6. 인사규정.txt",
            "output_file": "2025-insa.js",
            "question_count": 56
        },
        "행동강령": {
            "txt_file": "2025/7. 행동강령.txt",
            "output_file": "2025-haengdong.js",
            "question_count": 21
        },
        "회계기준": {
            "txt_file": "2025/8. 회계기준.txt",
            "output_file": "2025-hoegye.js",
            "question_count": 56
        }
    }
    
    # 각 과목별로 문제 생성
    for subject_name, config in subjects.items():
        print(f"\n{subject_name} 처리 중...")
        
        if os.path.exists(config["txt_file"]):
            try:
                # 문제 파싱
                questions = parse_questions_from_txt(
                    config["txt_file"], 
                    subject_name, 
                    answers_data.get(subject_name, {})
                )
                
                print(f"파싱된 문제 수: {len(questions)}")
                
                # js 파일 생성
                generate_js_file(subject_name, questions, config["output_file"])
                
                # 문제 수 확인
                if len(questions) != config["question_count"]:
                    print(f"⚠️  경고: 예상 문제 수 {config['question_count']}개와 실제 파싱된 문제 수 {len(questions)}개가 다릅니다.")
                
            except Exception as e:
                print(f"❌ {subject_name} 처리 중 오류 발생: {e}")
        else:
            print(f"❌ {config['txt_file']} 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    main() 