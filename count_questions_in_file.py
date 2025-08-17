import re

def count_questions_in_file():
    """2025-data-취업규칙.js 파일에서 실제 문제 수를 정확히 셉니다."""
    
    with open('2025-data-취업규칙.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # explanationData 배열의 항목 수 세기
    explanation_pattern = r'\{[^}]*"explanation"[^}]*\}'
    explanations = re.findall(explanation_pattern, content)
    print(f"explanationData 배열: {len(explanations)}개")
    
    # window.currentSubjectQuestions 배열의 문제 수 세기
    questions_pattern = r'\{[^}]*"question"[^}]*\}'
    questions = re.findall(questions_pattern, content)
    print(f"window.currentSubjectQuestions 배열: {len(questions)}개")
    
    # 실제 문제 객체 수 세기 (더 정확한 패턴)
    question_objects_pattern = r'\{\s*"question":\s*"[^"]*"[^}]*"correct":\s*"[^"]*"[^}]*\}'
    question_objects = re.findall(question_objects_pattern, content)
    print(f"실제 문제 객체: {len(question_objects)}개")

if __name__ == "__main__":
    count_questions_in_file() 