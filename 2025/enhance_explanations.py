#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os
import sys

def load_current_explanations():
    """해설.txt에서 기존 해설을 로드"""
    try:
        with open('해설.txt', 'r', encoding='utf-8') as f:
            explanations_list = json.load(f)
            
        # 과목과 문항별로 인덱싱
        explanations = {}
        for item in explanations_list:
            subject = item['과목']
            question_num = str(item['문항'])
            
            if subject not in explanations:
                explanations[subject] = {}
            
            explanations[subject][question_num] = {
                'explanation': item['해설'],
                'url': item.get('url') or item.get('url1') or item.get('url2') or ""
            }
        
        return explanations
    except FileNotFoundError:
        print("Error: 해설.txt file not found")
        return {}
    except json.JSONDecodeError:
        print("Error: 해설.txt is not valid JSON")
        return {}

def enhance_explanation_with_ai(subject, question_num, question_text, choices, correct_answer, current_explanation):
    """AI를 사용해 해설을 개선"""
    # 여기서는 시뮬레이션으로 개선된 해설을 반환
    # 실제로는 각 과목별 법령을 참조해서 상세한 해설을 생성해야 함
    
    answer_mapping = {'a': '①', 'b': '②', 'c': '③', 'd': '④'}
    correct_korean = answer_mapping.get(correct_answer, correct_answer)
    
    enhanced = f"정답: {correct_korean}\\n\\n"
    
    # 기존 해설이 있다면 보존
    if current_explanation and current_explanation.strip() and current_explanation != f"{subject} 관련 법령":
        enhanced += f"{current_explanation}\\n\\n"
    
    # 과목별 특화된 해설 패턴 추가
    if subject == "농어촌정비법":
        enhanced += "농어촌정비법 관련 조문을 정확히 확인하여 답을 선택해야 합니다. 법령의 세부 조항과 예외 규정을 주의깊게 살펴보세요."
    elif subject == "공운법":
        enhanced += "공공기관의 운영에 관한 법률의 세부 규정을 확인하여 공공기관 운영의 원칙과 절차를 정확히 파악해야 합니다."
    elif subject == "공사법":
        enhanced += "한국농어촌공사 및 농지관리기금법의 조문을 근거로 공사의 역할과 기금 운영 방식을 정확히 이해해야 합니다."
    elif subject == "직제규정":
        enhanced += "조직구조와 직급체계, 각 부서의 역할과 권한을 정확히 구분하여 이해해야 합니다."
    elif subject == "취업규칙":
        enhanced += "근무조건, 복무규정, 징계 및 보상 체계의 세부 규정을 정확히 파악해야 합니다."
    elif subject == "인사규정":
        enhanced += "채용, 승진, 전보, 평가 등 인사관리 전반의 절차와 기준을 정확히 이해해야 합니다."
    elif subject == "행동강령":
        enhanced += "공직자의 윤리기준과 행동규범, 이해충돌 방지 등의 구체적 적용 사례를 파악해야 합니다."
    elif subject == "회계기준":
        enhanced += "회계처리 원칙, 재무관리 절차, 감사 및 보고 체계의 세부 규정을 정확히 적용해야 합니다."
    
    return enhanced

def update_js_file_explanations(subject_name, file_number):
    """JS 파일의 해설을 업데이트"""
    js_file = f"{file_number}.{subject_name}.js"
    
    if not os.path.exists(js_file):
        print(f"Warning: {js_file} not found")
        return
    
    print(f"Updating explanations for {subject_name}...")
    
    # 현재 해설 데이터 로드
    current_explanations = load_current_explanations()
    subject_explanations = current_explanations.get(subject_name, {})
    
    # JS 파일 읽기
    try:
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {js_file} not found")
        return
    
    # 문제별로 해설 업데이트
    # 정규식으로 각 문제 블록을 찾아서 해설 부분을 교체
    def replace_explanation(match):
        question_block = match.group(0)
        
        # questionNumber 추출
        question_num_match = re.search(r'"questionNumber":\s*(\d+)', question_block)
        if not question_num_match:
            return question_block
        
        question_num = question_num_match.group(1)
        
        # 현재 explanation 추출
        current_exp_match = re.search(r'"explanation":\s*"([^"]*)"', question_block)
        if not current_exp_match:
            return question_block
        
        current_exp = current_exp_match.group(1)
        
        # 문제 텍스트와 선택지 추출 (해설 개선에 활용)
        question_match = re.search(r'"question":\s*"([^"]*)"', question_block)
        question_text = question_match.group(1) if question_match else ""
        
        correct_match = re.search(r'"correct":\s*"([^"]*)"', question_block)
        correct_answer = correct_match.group(1) if correct_match else ""
        
        # 해설.txt에서 해당 문제의 해설 찾기
        enhanced_explanation = subject_explanations.get(question_num, {}).get('explanation', current_exp)
        
        # 기본적인 해설만 있는 경우 개선
        if enhanced_explanation == f"{subject_name} 관련 법령" or len(enhanced_explanation.strip()) < 20:
            enhanced_explanation = enhance_explanation_with_ai(
                subject_name, question_num, question_text, {}, correct_answer, enhanced_explanation
            )
        
        # 해설 교체
        new_explanation = enhanced_explanation.replace('"', '\\"').replace('\n', '\\n')
        new_block = re.sub(
            r'"explanation":\s*"[^"]*"',
            f'"explanation": "{new_explanation}"',
            question_block
        )
        
        return new_block
    
    # 모든 문제 블록에 대해 해설 업데이트
    pattern = r'\{\s*"questionNumber":[^}]+\}'
    updated_content = re.sub(pattern, replace_explanation, content, flags=re.DOTALL)
    
    # 파일 저장
    try:
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✓ Updated explanations in {js_file}")
    except Exception as e:
        print(f"Error writing {js_file}: {e}")

def main():
    """메인 실행 함수"""
    subjects = [
        ("1", "농어촌정비법"),
        ("2", "공운법"),
        ("3", "공사법"),
        ("4", "직제규정"),
        ("5", "취업규칙"),
        ("6", "인사규정"),
        ("7", "행동강령"),
        ("8", "회계기준")
    ]
    
    print("🔄 Starting explanation enhancement...")
    
    # 특정 과목만 처리하고 싶다면 여기서 필터링
    if len(sys.argv) > 1:
        target_subject = sys.argv[1]
        subjects = [(num, name) for num, name in subjects if name == target_subject]
    
    for file_number, subject_name in subjects:
        update_js_file_explanations(subject_name, file_number)
    
    print("\n✅ Explanation enhancement completed!")

if __name__ == "__main__":
    main()