import json

def create_complete_47_questions():
    """문제 12번, 15번, 47번을 수동으로 수정해서 완전한 47문제를 만듭니다."""
    
    # 기존 44문제 읽기
    with open('취업규칙_47_questions_fixed.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 문제들을 JSON 배열로 변환
    questions = []
    
    # window.currentSubjectQuestions = [ 부분 제거하고 실제 문제들만 추출
    content_lines = content.split('\n')
    in_questions = False
    current_question = {}
    
    for line in content_lines:
        if 'window.currentSubjectQuestions = [' in line:
            in_questions = True
            continue
        elif line.strip() == '];':
            break
        elif in_questions:
            line = line.strip()
            if line.startswith('"question":'):
                if current_question:
                    questions.append(current_question)
                current_question = {}
                current_question['question'] = line.split('"question":')[1].strip().strip('",')
            elif line.startswith('"a":'):
                current_question['a'] = line.split('"a":')[1].strip().strip('",')
            elif line.startswith('"b":'):
                current_question['b'] = line.split('"b":')[1].strip().strip('",')
            elif line.startswith('"c":'):
                current_question['c'] = line.split('"c":')[1].strip().strip('",')
            elif line.startswith('"d":'):
                current_question['d'] = line.split('"d":')[1].strip().strip('",')
            elif line.startswith('"correct":'):
                current_question['correct'] = line.split('"correct":')[1].strip().strip('",')
            elif line.startswith('"explanation":'):
                current_question['explanation'] = line.split('"explanation":')[1].strip().strip('",')
            elif line.startswith('"url":'):
                current_question['url'] = line.split('"url":')[1].strip().strip('",')
    
    # 마지막 문제 추가
    if current_question:
        questions.append(current_question)
    
    print(f"기존 문제 수: {len(questions)}")
    
    # 문제 12번 수정 (연차휴가 설명)
    question_12 = {
        "question": "다음은 연차휴가에 대한 설명 중 일부이다. 각 괄호 ㉠~㉣ 에 들어갈 숫자들을 모두 합한 값으로 알맞은 것은? ① 연차휴가는 다음 각 호에 따른다. 1. 1년간 ( ㉠ )퍼센트 이상 출근하였을 때에는 ( ㉡ )일 2. 3년 이상 계속 근로한 직원에 대해서는 제1호의 휴가일수에 최초 1년을 초과하는 계속 근로 연수 2년에 대하여 1일을 가산한다. 3. 제2호에 따른 가산휴가를 포함한 총 휴가일수는 ( ㉢ )일을 한도로 한다. ② 계속 근로 연수가 1년 미만인 직원 또는 1년간 ( ㉣ )퍼센트 미만 출근한 직원에게 1개월 개근 시 1일의 연차휴가를 주어야 한다.",
        "a": "190",
        "b": "200",
        "c": "210", 
        "d": "220",
        "correct": "a",
        "explanation": "제19조(연차휴가)",
        "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 취업규칙/(9999,20250101)/제19조"
    }
    
    # 문제 15번 수정 (특별휴가 설명)
    question_15 = {
        "question": "다음은 특별휴가에 대한 설명 중 일부이다. 각 괄호에 들어갈 내용으로 알맞은 것은? 3. 그 밖의 특별휴가 가. 배우자 출산휴가 1) 단태아인 경우: 20일(출산일로부터 120일 이내에 사용하며, 3회까지 분할 사용 가능) 2) 다태아인 경우: ( ㉠ )일(출산일로부터 120일 이내에 사용하며, 3회까지 분할 사용 가능) 다. 출산전후휴가 1) 출산 전과 출산 후를 통하여 90일(미숙아를 출산한 경우에는 100일), 배정은 출산 후에 ( ㉡ )일 이상(한 번에 둘 이상 자녀를 임신한 경우 ( ㉢ )일, 배정은 출산 후에 60일 이상)이 되어야 한다. 2) 임신 중인 직원이 유산ㆍ사산의 경험이 있거나 출산전후휴가를 청구할 당시 연령이 만 ( ㉣ )세 이상인 경우, 유산ㆍ사산의 위험이 있다는 의료기관의 진단서를 제출한 경우에는 출산 전 어느 때라도 휴가를 나누어 사용할 수 있으며, 이 경우 출산 후의 휴가 기간은 연속하여 ( ㉤ )일 이상(한 번에 둘 이상의 자녀를 임신한 경우에는 60일 이상)이 되어야 한다.",
        "a": "㉠ 25, ㉡ 45, ㉢ 120, ㉣ 40, ㉤ 45",
        "b": "㉠ 25, ㉡ 50, ㉢ 120, ㉣ 45, ㉤ 45",
        "c": "㉠ 25, ㉡ 45, ㉢ 100, ㉣ 45, ㉤ 40",
        "d": "㉠ 30, ㉡ 50, ㉢ 100, ㉣ 40, ㉤ 45",
        "correct": "a",
        "explanation": "제20조(특별휴가)",
        "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 취업규칙/(9999,20250101)/제20조"
    }
    
    # 문제 47번 수정 (적립휴가)
    question_47 = {
        "question": "적립휴가관련 다음 빈칸에 가장 옳은 것은? 제19조의4(적립휴가) ① 제19조의2에 따라 사용을 촉진하여 보상할 의무가 없는 연차휴가의 일부는 제19조제9항에 따른 소멸 익일 적립휴가로 전환된다. 이때, 당해연도 생성된 연차휴가의 ( ㉠ )(소수점 절사)를 초과하여 전환할 수 없다. ② 적립휴가는 전환일부터 ( ㉡ ) 이내 또는 퇴직 전까지 사용하지 않으면 소멸하며, 공사는 이를 금전으로 보상하지 않는다. ③ 적립휴가는 ( ㉢ ) 단위로 분할하여 사용할 수 있다.",
        "a": "㉠ 20%, ㉡ 퇴직 전까지, ㉢ 30분",
        "b": "㉠ 20%, ㉡ 퇴직 전까지, ㉢ 1시간",
        "c": "㉠ 30%, ㉡ 10년 이내에, ㉢ 30분",
        "d": "㉠ 30%, ㉡ 10년 이내에, ㉢ 1시간",
        "correct": "a",
        "explanation": "제19조의4(적립휴가)",
        "url": "https://www.law.go.kr/학칙공단/(한국농어촌공사) 취업규칙/(9999,20250101)/제19조의4"
    }
    
    # 문제 12번을 11번 다음에 삽입
    questions.insert(11, question_12)
    
    # 문제 15번을 14번 다음에 삽입 (기존 15번은 16번이 됨)
    questions.insert(14, question_15)
    
    # 문제 47번을 마지막에 추가
    questions.append(question_47)
    
    print(f"완성된 문제 수: {len(questions)}")
    
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
    create_complete_47_questions() 