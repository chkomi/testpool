#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def fix_missing_questions():
    """문제 12번과 47번을 수동으로 추가해서 완전한 47문제를 만듭니다."""
    
    # 기존 45문제 읽기
    with open('취업규칙_47_questions.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 문제 12번 추가 (연차휴가 설명)
    question_12 = {
        "question": "다음은 연차휴가에 대한 설명 중 일부이다. 각 괄호 ㉠~㉣ 에 들어갈 숫자들을 모두 합한 값으로 알맞은 것은? ① 연차휴가는 다음 각 호에 따른다. 1. 1년간 ( ㉠ )퍼센트 이상 출근하였을 때에는 ( ㉡ )일 2. 3년 이상 계속 근로한 직원에 대해서는 제1호의 휴가일수에 최초 1년을 초과하는 계속 근로 연수 2년에 대하여 1일 을 가산한다. 3. 제2호에 따른 가산휴가를 포함한 총 휴가일수는 ( ㉢ )일을 한도로 한다. ② 계속 근로 연수가 1년 미만인 직원 또는 1년간 ( ㉣ )퍼센트 미만 출근한 직원에게 1개월 개근 시 1일의 연차휴가를 주어야 한다.",
        "a": "190",
        "b": "200", 
        "c": "210",
        "d": "220",
        "correct": "a",
        "explanation": "제19조(연차휴가)",
        "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 취업규칙/(9999,20250101)/제19조"
    }
    
    # 문제 47번 추가 (적립휴가)
    question_47 = {
        "question": "적립휴가관련 다음 빈칸에 가장 옳은 것은? 제19조의4(적립휴가) ① 제19조의2에 따라 사용을 촉진하여 보상할 의무가 없는 연차휴가의 일부는 제19조제9항에 따른 소멸 익일 적립휴가로 전환된다. 이때, 당해연도 생성된 연차휴가의 ( ㉠ )(소수점 절사)를 초과하여 전환할 수 없다. ② 적립휴가는 전환일부터 ( ㉡ ) 이내 또는 퇴직 전까지 사용하지 않으면 소멸하며, 공사는 이를 금전으로 보상하지 않는다. ③ 적립휴가는 ( ㉢ ) 단위로 분할하여 사용할 수 있다.",
        "a": "㉠ 20%,  ㉡ 퇴직 전까지,  ㉢ 30분",
        "b": "㉠ 20%,  ㉡ 퇴직 전까지,  ㉢ 1시간",
        "c": "㉠ 30%,  ㉡ 10년 이내에,   30분",
        "d": "㉠ 30%,  ㉡ 10년 이내에,  ㉢ 1시간",
        "correct": "a",
        "explanation": "제19조의4(적립휴가)",
        "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 취업규칙/(9999,20250101)/제19조의4"
    }
    
    # 기존 문제들을 JSON 배열로 변환
    questions = []
    
    # window.currentSubjectQuestions = [ 부분 제거하고 실제 문제들만 추출
    content_lines = content.split('\n')
    in_questions = False
    
    for line in content_lines:
        if 'window.currentSubjectQuestions = [' in line:
            in_questions = True
            continue
        elif line.strip() == '];':
            break
        elif in_questions and line.strip().startswith('{'):
            # 문제 객체 시작
            question_text = ""
            for i, content_line in enumerate(content_lines[content_lines.index(line):]):
                question_text += content_line + '\n'
                if content_line.strip() == '},':
                    break
                elif content_line.strip() == '}':
                    break
            
            # JSON 파싱을 위해 임시 파일 생성
            temp_content = question_text.rstrip(',\n') + '\n'
            try:
                # JavaScript 객체를 JSON으로 변환
                temp_content = temp_content.replace("'", '"')
                question_obj = eval(temp_content)
                questions.append(question_obj)
            except:
                print(f"문제 파싱 실패: {temp_content[:100]}...")
    
    # 문제 12번을 11번 다음에 삽입
    questions.insert(11, question_12)
    
    # 문제 47번을 마지막에 추가
    questions.append(question_47)
    
    print(f"총 문제 수: {len(questions)}")
    
    # 완성된 문제들을 JavaScript 파일로 저장
    js_content = "// 취업규칙 47문제 완성 데이터\n\n"
    js_content += "window.currentSubjectQuestions = [\n"
    
    for i, question in enumerate(questions):
        js_content += "    {\n"
        js_content += f'        "question": "{question["question"]}",\n'
        js_content += f'        "a": "{question["a"]}",\n'
        js_content += f'        "b": "{question["b"]}",\n'
        js_content += f'        "c": "{question["c"]}",\n'
        js_content += f'        "d": "{question["d"]}",\n'
        js_content += f'        "correct": "{question["correct"]}",\n'
        js_content += f'        "explanation": "{question["explanation"]}",\n'
        js_content += f'        "url": "{question["url"]}"\n'
        js_content += "    }"
        
        if i < len(questions) - 1:
            js_content += ","
        js_content += "\n"
    
    js_content += "];\n"
    
    with open('취업규칙_47_complete.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("취업규칙_47_complete.js 파일이 생성되었습니다. (총 47문제)")

if __name__ == "__main__":
    fix_missing_questions() 