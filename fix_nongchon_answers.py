import re
import json

def fix_nongchon_answers():
    # 답안.txt에서 농어촌정비법 답안 읽기
    with open('2025/답안.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 농어촌정비법 답안 추출
    nongchon_match = re.search(r'"농어촌정비법":\s*\{([^}]+)\}', content)
    if not nongchon_match:
        print("농어촌정비법 답안을 찾을 수 없습니다.")
        return
    
    answers_text = nongchon_match.group(1)
    
    # 답안 파싱 (예: "1": 4, "2": 3, ...)
    answers = {}
    answer_pattern = r'"(\d+)":\s*(\d+)'
    answer_matches = re.findall(answer_pattern, answers_text)
    
    for q_num, answer in answer_matches:
        # 1->a, 2->b, 3->c, 4->d로 변환
        answer_letter = chr(ord('a') + int(answer) - 1)
        answers[int(q_num)] = answer_letter
    
    print(f"농어촌정비법 답안 {len(answers)}개 로드 완료")
    
    # 2025-nongchon.js 파일 읽기
    with open('2025-nongchon.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # 각 문제의 correct 필드 수정
    current_question = 1
    modified_content = js_content
    
    # correct 필드 찾아서 수정
    correct_pattern = r'"correct":\s*"[^"]*"'
    
    def replace_correct(match):
        nonlocal current_question
        if current_question in answers:
            result = f'"correct": "{answers[current_question]}"'
            current_question += 1
            return result
        else:
            current_question += 1
            return match.group(0)
    
    modified_content = re.sub(correct_pattern, replace_correct, modified_content)
    
    # 수정된 내용 저장
    with open('2025-nongchon.js', 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print("2025-nongchon.js 답안 수정 완료!")

if __name__ == "__main__":
    fix_nongchon_answers() 