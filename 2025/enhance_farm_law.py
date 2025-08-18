#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
농어촌정비법 상세 해설 작성 스크립트
"""

import json
import re
import os

def create_farm_law_explanation(question_data):
    """농어촌정비법 상세 해설 생성"""
    question_num = question_data.get("questionNumber", "")
    question = question_data.get("question", "")
    correct = question_data.get("correct", "")
    current_explanation = question_data.get("explanation", "")
    
    # 이미 상세한 해설이 있는 경우 스킵
    if "정답:" in current_explanation and "법령 근거:" in current_explanation:
        return current_explanation
    
    explanation = f"정답: {correct}\n\n"
    
    # 문제 유형별 상세 해설 생성
    if "농업생산기반" in question:
        explanation += "농어촌정비법에서 농업생산기반 정비사업은 농업생산의 기반이 되는 시설을 정비하는 사업입니다.\n\n"
        explanation += "주요 관련 조항:\n"
        explanation += "- 제6조: 농업생산기반 정비사업의 원칙\n"
        explanation += "- 제7조: 농업생산기반 정비계획의 수립\n"
        explanation += "- 제8조: 농업생산기반 정비사업의 시행\n"
        explanation += "- 제14조: 농업생산기반 정비사업 시행으로 조성된 재산의 관리와 처분\n"
        explanation += "- 제16조: 농업생산기반시설의 인수\n\n"
        
        if "시행계획" in question:
            explanation += "시행계획 관련:\n"
            explanation += "- 시행령 제9조: 농업생산기반 정비사업 시행계획의 수립\n"
            explanation += "- 시행령 제6조: 농업생산기반 정비계획의 수립\n\n"
    
    elif "생활환경정비" in question:
        explanation += "생활환경정비사업은 농어촌 주민의 생활환경을 개선하기 위한 사업입니다.\n\n"
        explanation += "주요 관련 조항:\n"
        explanation += "- 제54조: 생활환경정비계획의 수립\n"
        explanation += "- 제55조: 생활환경정비계획의 내용\n"
        explanation += "- 제58조: 생활환경정비사업 기본계획의 수립\n\n"
        
        if "고시" in question:
            explanation += "고시 관련:\n"
            explanation += "- 시행령 제50조: 생활환경정비계획의 고시\n"
            explanation += "- 시행령 제52조: 생활환경정비 총괄계획가의 자격 요건\n\n"
    
    elif "벌칙" in question:
        explanation += "농어촌정비법 제130조(벌칙)에 따른 처벌 규정입니다.\n\n"
        explanation += "주요 벌칙 사항:\n"
        explanation += "- 농업생산기반시설 불법 점용·사용\n"
        explanation += "- 농어촌용수 이용·관리 지장\n"
        explanation += "- 사업정지명령 위반\n"
        explanation += "- 조성용지 전매\n\n"
    
    elif "자원 조사" in question:
        explanation += "농어촌정비법 제3조(자원 조사)에 따른 조사 규정입니다.\n\n"
        explanation += "주요 내용:\n"
        explanation += "- 농림축산식품부장관 또는 해양수산부장관이 조사 실시\n"
        explanation += "- 농어촌지역을 대상으로 조사\n"
        explanation += "- 시행령 제3조: 자원 조사의 대상 항목\n\n"
    
    elif "사용료" in question or "무단점용료" in question:
        explanation += "농업생산기반시설 사용료 및 무단점용료 관련 규정입니다.\n\n"
        explanation += "주요 조항:\n"
        explanation += "- 제23조: 농업생산기반시설이나 용수의 사용허가\n"
        explanation += "- 시행령 제32조: 사용료의 징수\n"
        explanation += "- 시행령 제94조: 무단점용료의 징수\n\n"
    
    elif "자금지원" in question or "자금" in question:
        explanation += "농어촌정비사업 자금지원 관련 규정입니다.\n\n"
        explanation += "주요 조항:\n"
        explanation += "- 제108조: 자금지원\n"
        explanation += "- 국가와 지방자치단체의 보조 또는 융자\n"
        explanation += "- 위탁 사업자에 대한 자금 지급 가능\n\n"
    
    elif "구분지상권" in question:
        explanation += "농어촌정비법 제110조의3(구분지상권의 설정등기 등) 관련 규정입니다.\n\n"
        explanation += "주요 내용:\n"
        explanation += "- 농업생산기반시설의 지상 또는 지하 공간 사용\n"
        explanation += "- 구분지상권의 존속기간: 농업생산기반시설이 존속하는 날까지\n"
        explanation += "- 민법 규정에도 불구하고 특별 규정 적용\n\n"
    
    else:
        explanation += "농어촌정비법은 농어촌의 정비와 개발을 위한 기본법입니다.\n\n"
        explanation += "주요 내용:\n"
        explanation += "- 농업생산기반 정비사업\n"
        explanation += "- 생활환경정비사업\n"
        explanation += "- 농어촌 관광휴양지사업\n"
        explanation += "- 농어촌산업 육성\n\n"
    
    explanation += f"정답 이유:\n"
    explanation += f"{correct}번이 정답인 이유는 해당 법령 조항에 근거합니다.\n\n"
    explanation += "법령 근거: 농어촌정비법 및 시행령 관련 조항"
    
    return explanation

def enhance_farm_law_file():
    """농어촌정비법 파일 해설 개선"""
    filename = "1.농어촌정비법.js"
    print(f"🔄 농어촌정비법 해설 개선 중...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # quizData 배열 추출
        match = re.search(r'const quizData = (\[.*?\]);', content, re.DOTALL)
        if not match:
            print(f"❌ {filename}에서 quizData를 찾을 수 없습니다.")
            return False
        
        quiz_data_str = match.group(1)
        quiz_data = json.loads(quiz_data_str)
        
        # 각 문제의 해설 개선
        updated_count = 0
        for question in quiz_data:
            original_explanation = question.get("explanation", "")
            new_explanation = create_farm_law_explanation(question)
            
            if new_explanation != original_explanation:
                question["explanation"] = new_explanation
                updated_count += 1
        
        # 개선된 내용으로 파일 업데이트
        updated_content = content.replace(
            match.group(0),
            f"const quizData = {json.dumps(quiz_data, ensure_ascii=False, indent=4)};"
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ {filename} 업데이트 완료 ({updated_count}개 문제 개선)")
        return True
        
    except Exception as e:
        print(f"❌ {filename} 처리 중 오류 발생: {e}")
        return False

if __name__ == "__main__":
    enhance_farm_law_file() 