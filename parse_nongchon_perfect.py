import re
import json

def parse_nongchon_perfect():
    with open('2025/1. 농어촌정비법.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = []
    
    # 1~134번까지 순차적으로 처리
    for q_num in range(1, 135):
        # 해당 문제 번호 찾기
        start_pattern = rf'{q_num}\.'
        start_match = re.search(start_pattern, content)
        
        if not start_match:
            print(f"⚠️ 문제 {q_num}번을 찾을 수 없음")
            continue
            
        start_idx = start_match.start()
        
        # 다음 문제 번호까지의 텍스트 추출
        next_pattern = rf'{q_num+1}\.'
        next_match = re.search(next_pattern, content[start_idx:])
        
        if next_match:
            question_section = content[start_idx:start_idx + next_match.start()]
        else:
            question_section = content[start_idx:]
        
        # 문제 내용 추출 (문제 번호 제거)
        question_content = question_section.replace(f"{q_num}. ", "").strip()
        
        # 보기 찾기 (①, ②, ③, ④)
        options = []
        option_pattern = r'[①②③④]\s*(.*?)(?=[①②③④]|$)'
        option_matches = re.findall(option_pattern, question_section, re.DOTALL)
        
        # 보기 개수 확인 및 수정
        if len(option_matches) >= 4:
            # 처음 4개만 사용
            for i in range(4):
                opt = option_matches[i].strip()
                if opt:
                    options.append(opt)
        else:
            print(f"⚠️ 문제 {q_num}번에 보기 부족: {len(option_matches)}개")
            continue
        
        # 4개 보기가 모두 있는지 확인
        if len(options) == 4:
            # 정답은 임시로 설정 (나중에 답안.txt에서 가져올 예정)
            correct = "a"
            
            # JSON 문자열 내 모든 특수 문자를 이스케이프 처리
            def escape_json_string(text):
                # 모든 제어 문자 처리
                result = ""
                for char in text:
                    if char == '\n':
                        result += '\\n'
                    elif char == '\r':
                        result += '\\r'
                    elif char == '\t':
                        result += '\\t'
                    elif char == '\b':
                        result += '\\b'
                    elif char == '\f':
                        result += '\\f'
                    elif char == '"':
                        result += '\\"'
                    elif char == '\\':
                        result += '\\\\'
                    elif ord(char) < 32:  # 기타 제어 문자
                        result += f'\\u{ord(char):04x}'
                    else:
                        result += char
                return result
            
            question_content = escape_json_string(question_content)
            options = [escape_json_string(opt) for opt in options]
            
            question_data = {
                "question": question_content,
                "a": options[0],
                "b": options[1], 
                "c": options[2],
                "d": options[3],
                "correct": correct,
                "explanation": "농어촌정비법 관련 법령에 따른 정답입니다.",
                "url": "https://www.law.go.kr/법령/농어촌정비법"
            }
            
            questions.append(question_data)
            print(f"문제 {q_num}: {len(options)}개 보기")
        else:
            print(f"❌ 문제 {q_num}번 파싱 실패: {len(options)}개 보기")
    
    print(f"\n총 {len(questions)}개 문제 파싱 완료")
    
    # JavaScript 파일 생성
    js_content = "// 2025년 사전공개문제 - 농어촌정비법\n\n"
    js_content += "const quizData = [\n"
    
    for q in questions:
        js_content += "    {\n"
        js_content += f'        "question": "{q["question"]}",\n'
        js_content += f'        "a": "{q["a"]}",\n'
        js_content += f'        "b": "{q["b"]}",\n'
        js_content += f'        "c": "{q["c"]}",\n'
        js_content += f'        "d": "{q["d"]}",\n'
        js_content += f'        "correct": "{q["correct"]}",\n'
        js_content += f'        "explanation": "{q["explanation"]}",\n'
        js_content += f'        "url": "{q["url"]}"\n'
        js_content += "    },\n"
    
    js_content += "];\n\n"
    js_content += "// 퀴즈 시작\n"
    js_content += "startQuizEngine(quizData);\n"
    
    # 파일 저장
    with open('2025-nongchon.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("2025-nongchon.js 파일 생성 완료!")

if __name__ == "__main__":
    parse_nongchon_perfect() 