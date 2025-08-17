#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def find_missing_questions(txt_file, js_file, subject_name):
    """txt 파일과 js 파일을 비교해서 누락된 문제 번호를 찾습니다."""
    
    print(f"\n=== {subject_name} 누락 문제 조사 ===")
    
    # txt 파일에서 문제 번호 추출
    with open(txt_file, 'r', encoding='utf-8') as f:
        txt_content = f.read()
    
    txt_questions = set()
    txt_pattern = r'^(\d+)\.\s'
    for match in re.finditer(txt_pattern, txt_content, re.MULTILINE):
        txt_questions.add(int(match.group(1)))
    
    print(f"txt 파일 문제 수: {len(txt_questions)}")
    print(f"txt 파일 문제 범위: {min(txt_questions)} ~ {max(txt_questions)}")
    
    # js 파일에서 문제 수 확인
    with open(js_file, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    js_question_count = js_content.count('"question":')
    print(f"js 파일 문제 수: {js_question_count}")
    
    # 누락된 문제 찾기
    if len(txt_questions) > js_question_count:
        missing_count = len(txt_questions) - js_question_count
        print(f"누락된 문제 수: {missing_count}")
        
        # txt 파일에서 문제 내용 확인 (처음 5개)
        print("\n처음 5개 문제:")
        for i in range(1, 6):
            if i in txt_questions:
                # 해당 문제 주변 내용 찾기
                pattern = rf'{i}\.\s*(.*?)(?=\d+\.|$)'
                match = re.search(pattern, txt_content, re.DOTALL)
                if match:
                    question_text = match.group(1).strip()[:100] + "..."
                    print(f"{i}. {question_text}")
        
        # 마지막 5개 문제
        print("\n마지막 5개 문제:")
        for i in range(max(txt_questions)-4, max(txt_questions)+1):
            if i in txt_questions:
                pattern = rf'{i}\.\s*(.*?)(?=\d+\.|$)'
                match = re.search(pattern, txt_content, re.DOTALL)
                if match:
                    question_text = match.group(1).strip()[:100] + "..."
                    print(f"{i}. {question_text}")
    else:
        print("모든 문제가 정상적으로 생성되었습니다.")

def main():
    subjects = {
        "농어촌정비법": {
            "txt_file": "2025/1. 농어촌정비법.txt",
            "js_file": "2025-nongchon.js"
        },
        "공운법": {
            "txt_file": "2025/2. 공운법.txt",
            "js_file": "2025-gongun.js"
        },
        "공사법": {
            "txt_file": "2025/3. 공사법.txt",
            "js_file": "2025-gongsa.js"
        },
        "직제규정": {
            "txt_file": "2025/4. 직제규정.txt",
            "js_file": "2025-jikje.js"
        },
        "취업규칙": {
            "txt_file": "2025/5. 취업규칙.txt",
            "js_file": "2025-chwip.js"
        },
        "인사규정": {
            "txt_file": "2025/6. 인사규정.txt",
            "js_file": "2025-insa.js"
        },
        "행동강령": {
            "txt_file": "2025/7. 행동강령.txt",
            "js_file": "2025-haengdong.js"
        },
        "회계기준": {
            "txt_file": "2025/8. 회계기준.txt",
            "js_file": "2025-hoegye.js"
        }
    }
    
    for subject_name, config in subjects.items():
        if os.path.exists(config["txt_file"]) and os.path.exists(config["js_file"]):
            find_missing_questions(config["txt_file"], config["js_file"], subject_name)
        else:
            print(f"\n=== {subject_name} ===")
            if not os.path.exists(config["txt_file"]):
                print(f"❌ txt 파일 없음: {config['txt_file']}")
            if not os.path.exists(config["js_file"]):
                print(f"❌ js 파일 없음: {config['js_file']}")

if __name__ == "__main__":
    main() 