import re

def parse_nongchon():
    with open('2025/1. 농어촌정비법.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 문제 번호와 보기를 모두 찾기
    questions = []
    
    # 문제 번호 패턴: "숫자." 다음에 "①"이 나오기 전까지
    question_pattern = r'(\d+)\.\s*(.*?)(?=①)'
    question_matches = re.findall(question_pattern, content, re.DOTALL)
    
    print(f"문제 번호 패턴으로 {len(question_matches)}개 발견")
    
    # 각 문제에 대해 보기 찾기
    for q_num, q_content in question_matches:
        if int(q_num) > 134:  # 134문제까지만
            continue
            
        # 해당 문제 다음 부분에서 보기 찾기
        start_idx = content.find(f"{q_num}. {q_content}①")
        if start_idx == -1:
            continue
            
        # 다음 문제 번호까지의 텍스트 추출
        next_q_pattern = rf'{int(q_num)+1}\.'
        next_match = re.search(next_q_pattern, content[start_idx:])
        
        if next_match:
            question_section = content[start_idx:start_idx + next_match.start()]
        else:
            question_section = content[start_idx:]
        
        # 보기 찾기 (①, ②, ③, ④)
        options = []
        option_pattern = r'[①②③④]\s*(.*?)(?=[①②③④]|$)'
        option_matches = re.findall(option_pattern, question_section, re.DOTALL)
        
        for opt in option_matches[:4]:  # 최대 4개만
            opt = opt.strip()
            if opt:
                options.append(opt)
        
        # 4개 보기가 모두 있는지 확인
        if len(options) == 4:
            # 정답은 임시로 설정 (나중에 답안.txt에서 가져올 예정)
            correct = "a"
            
            question_data = {
                "question": q_content.strip(),
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
    parse_nongchon() 