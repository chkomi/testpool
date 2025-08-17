import json
import re

def count_questions_by_subject():
    """2025-exam.js 파일에서 각 과목별 문제 수를 정확히 셉니다."""
    
    with open('2025-exam.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 각 과목별 문제 수를 세기
    subjects = ["농어촌정비법", "공운법", "공사법", "직제규정", "취업규칙", "인사규정", "행동강령", "회계기준"]
    
    for subject in subjects:
        # 해당 과목 섹션 찾기
        subject_pattern = rf'"{subject}":\s*\[(.*?)\]'
        subject_match = re.search(subject_pattern, content, re.DOTALL)
        
        if subject_match:
            subject_content = subject_match.group(1)
            
            # 문제 패턴 찾기 (더 정확한 패턴)
            question_pattern = r'\{[^}]*"question"[^}]*\}'
            questions_found = re.findall(question_pattern, subject_content)
            
            print(f"{subject}: {len(questions_found)}문제")
        else:
            print(f"{subject}: 찾을 수 없음")

if __name__ == "__main__":
    count_questions_by_subject() 