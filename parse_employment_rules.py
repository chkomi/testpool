import re
import json

def parse_employment_rules():
    """5. 취업규칙.txt 파일을 파싱해서 47문제를 만듭니다."""
    
    with open('2025/5. 취업규칙.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 문제 번호 패턴 찾기
    question_numbers = re.findall(r'(\d+)\.', content)
    unique_numbers = sorted(set([int(num) for num in question_numbers]))
    
    print(f"발견된 문제 번호: {unique_numbers}")
    print(f"총 문제 수: {len(unique_numbers)}")
    
    questions = []
    
    for num in unique_numbers:
        # 각 문제의 시작과 끝 찾기
        start_pattern = rf'{num}\.'
        start_match = re.search(start_pattern, content)
        if not start_match:
            continue
            
        start_pos = start_match.end()
        
        # 다음 문제 번호 찾기
        if num < max(unique_numbers):
            next_num = num + 1
            end_pattern = rf'\n\s*{next_num}\.'
            end_match = re.search(end_pattern, content[start_pos:])
            if end_match:
                end_pos = start_pos + end_match.start()
            else:
                end_pos = len(content)
        else:
            end_pos = len(content)
        
        question_content = content[start_pos:end_pos].strip()
        
        # 문제 텍스트와 보기 추출
        lines = question_content.split('\n')
        question_text = ""
        options = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 보기 패턴 찾기 (①, ②, ③, ④)
            if re.match(r'^[①②③④]', line):
                option_text = re.sub(r'^[①②③④]\s*', '', line)
                options.append(option_text)
            elif not options:
                # 보기가 나오기 전까지는 문제 텍스트
                question_text += line + " "
            else:
                # 보기 이후는 문제 텍스트의 연속
                question_text += line + " "
        
        question_text = question_text.strip()
        
        if len(options) == 4:
            # 기본 답안은 'a'로 설정 (나중에 수정 필요)
            correct_answer = "a"
            
            question_obj = {
                "question": question_text,
                "a": options[0],
                "b": options[1], 
                "c": options[2],
                "d": options[3],
                "correct": correct_answer,
                "explanation": "",
                "url": ""
            }
            questions.append(question_obj)
            print(f"문제 {num}: {len(options)}개 보기 추출 완료")
        else:
            print(f"문제 {num}: 보기 수가 4개가 아님 ({len(options)}개)")
    
    return questions

def save_questions_to_js(questions):
    """문제를 JavaScript 파일로 저장합니다."""
    
    js_content = "// 취업규칙 47문제 데이터\n\n"
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
    
    with open('취업규칙_47_questions.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"취업규칙_47_questions.js 파일이 생성되었습니다. (총 {len(questions)}문제)")

if __name__ == "__main__":
    questions = parse_employment_rules()
    save_questions_to_js(questions) 