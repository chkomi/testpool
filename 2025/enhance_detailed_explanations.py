#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
각 문제의 구체적인 정답 이유를 자세히 설명하는 상세 해설 작성 스크립트
"""

import json
import re
import os

def create_detailed_farm_law_explanation(question_data):
    """농어촌정비법 상세 해설 생성"""
    question_num = question_data.get("questionNumber", "")
    question = question_data.get("question", "")
    correct = question_data.get("correct", "")
    choices = {
        "a": question_data.get("a", ""),
        "b": question_data.get("b", ""),
        "c": question_data.get("c", ""),
        "d": question_data.get("d", "")
    }
    
    explanation = f"정답: {correct}\n\n"
    
    # 문제 유형별 상세 해설 생성
    if "농업생산기반" in question:
        explanation += "농어촌정비법에서 농업생산기반 정비사업은 농업생산의 기반이 되는 시설을 정비하는 사업입니다.\n\n"
        
        if "시행계획" in question:
            explanation += "농어촌정비법 시행령 제9조에 따르면, 농업생산기반 정비사업 시행계획에는 다음 사항이 포함되어야 합니다:\n"
            explanation += "제1호: 농업생산기반 정비사업 시행계획의 개요\n"
            explanation += "제2호: 세부 설계도서\n"
            explanation += "제3호: 사업비 명세서\n"
            explanation += "제4호: 사업 시행 지역의 위치도\n"
            explanation += "제5호: 사업별 추진계획\n"
            explanation += "제6호: 그 밖에 농림축산식품부장관이 정하는 사항\n\n"
            
            if correct == "a":
                explanation += f"정답 이유:\n"
                explanation += f"①번이 정답인 이유:\n"
                explanation += f"- ㉠ 농업생산기반 정비사업 시행계획의 개요: 시행령 제9조 제1호에 해당\n"
                explanation += f"- ㉡ 세부 설계도서: 시행령 제9조 제2호에 해당\n"
                explanation += f"- ㉤ 사업비 명세서: 시행령 제9조 제3호에 해당\n"
                explanation += f"- ㉥ 사업 시행 지역의 위치도: 시행령 제9조 제4호에 해당\n\n"
                explanation += f"오답 이유:\n"
                explanation += f"- ㉢ 참여 인력 현황: 시행령 제9조에 명시되지 않음\n"
                explanation += f"- ㉣ 인건비 지출예산서: 시행령 제9조에 명시되지 않음\n"
        
        elif "재산의 관리와 처분" in question or "간척지" in question:
            explanation += "농어촌정비법 제14조에 따르면, 농업생산기반 정비사업 시행으로 조성된 재산의 처분에 대한 명확한 규정이 있습니다.\n\n"
            explanation += "주요 규정:\n"
            explanation += "- 제14조 제1항: 농업생산기반 정비사업 시행으로 조성된 재산은 매각할 수 있음\n"
            explanation += "- 제14조 제1항: 매각 시 농림축산식품부장관의 승인을 받아야 함\n"
            explanation += "- 제14조 제2항: 국가가 시행한 농업생산기반 정비사업으로 조성된 간척지의 매각대금은 농지관리기금에 납입\n"
            explanation += "- 제14조 제3항: 매각대금은 농업생산기반시설의 유지·관리, 다른 농업생산기반 정비사업, 농지관리기금 납입 용도로만 사용 가능\n\n"
            
            if correct == "d":
                explanation += f"정답 이유:\n"
                explanation += f"④번이 정답인 이유:\n"
                explanation += f"- '간척지를 매각한 대금은 사용에 제한이 없다'는 설명이 틀림\n"
                explanation += f"- 실제로는 제14조 제3항에 따라 매각대금의 사용 용도가 제한됨\n"
                explanation += f"- 농어촌산업 활성화를 위한 기부금으로 사용하는 것은 허용되지 않음\n\n"
                explanation += f"올바른 설명들:\n"
                explanation += f"- ① 간척지 매각 처분: 제14조 제1항에 따라 가능\n"
                explanation += f"- ② 농림축산식품부장관 승인: 제14조 제1항에 따라 필요\n"
                explanation += f"- ③ 농지관리기금 납입: 제14조 제2항에 따라 국가가 시행한 사업의 경우 필요\n"
    
    elif "생활환경정비" in question:
        explanation += "생활환경정비사업은 농어촌 주민의 생활환경을 개선하기 위한 사업입니다.\n\n"
        
        if "기본계획" in question and "경미한 사항" in question:
            explanation += "농어촌정비법 제58조 제2항에 따르면:\n"
            explanation += "- 생활환경정비사업 기본계획 수립·변경 시 주민 의견 청취 및 협의 필요\n"
            explanation += "- 다만, 농림축산식품부령으로 정하는 경미한 사항 변경 시에는 예외\n\n"
            
            if correct == "d":
                explanation += f"정답 이유:\n"
                explanation += f"④번이 정답인 이유:\n"
                explanation += f"- '경미한 사항을 변경하는 경우라도 주민 의견과 협의가 필요하다'고 했으나\n"
                explanation += f"- 실제로는 제58조 제2항에서 '다만' 조항으로 경미한 사항 변경 시 예외 규정을 두고 있음\n"
                explanation += f"- 경미한 사항 변경 시에는 주민 의견 청취 및 협의를 생략할 수 있음\n\n"
                explanation += f"올바른 설명들:\n"
                explanation += f"- ① 세부 사업별 기본계획 수립: 제58조 제1항에 따라 가능\n"
                explanation += f"- ② 기본계획 고시: 제58조 제3항에 따라 필요\n"
                explanation += f"- ③ 주민 의견 청취 및 협의: 제58조 제2항에 따라 일반적인 경우 필요\n"
        
        elif "총괄계획가" in question:
            explanation += "농어촌정비법 시행령 제52조에 따르면, 생활환경정비 총괄계획가의 자격 요건이 명시되어 있습니다.\n\n"
            explanation += "자격 요건:\n"
            explanation += "제1호: 농어촌지역개발 관련 학과의 교수\n"
            explanation += "제2호: 농어촌지역개발 분야 박사학위 취득 후 연구경력이 3년 이상인 사람\n"
            explanation += "제3호: 농어촌계획 분야에 종사하는 건축사\n"
            explanation += "제4호: 농어촌계획 분야에 종사하여 기술사 수준의 전문지식과 실무경력을 가지고 있다고 시장·군수·구청장이 인정한 사람\n\n"
            
            if correct == "b":
                explanation += f"정답 이유:\n"
                explanation += f"②번이 정답인 이유:\n"
                explanation += f"- '농어촌지역개발 분야 박사 학위 취득 후 연구경력이 1년 이상인 사람'은 자격 요건에 미달\n"
                explanation += f"- 시행령 제52조 제1항 제2호에서는 연구경력이 '3년 이상'이어야 한다고 규정\n"
                explanation += f"- 1년 이상으로는 자격 요건에 미달하여 위촉할 수 없음\n\n"
                explanation += f"올바른 자격 요건들:\n"
                explanation += f"- ① 농어촌지역개발 관련 학과 교수: 시행령 제52조 제1항 제1호에 해당\n"
                explanation += f"- ③ 농어촌계획 분야에 종사하는 건축사: 시행령 제52조 제1항 제3호에 해당\n"
                explanation += f"- ④ 기술사 수준의 전문지식과 실무경력을 가지고 있다고 시장이 인정한 사람: 시행령 제52조 제1항 제4호에 해당\n"
    
    elif "사용료" in question or "무단점용료" in question:
        explanation += "농어촌정비법 시행령 제32조와 제94조에 따른 사용료 및 무단점용료 산정과 징수 절차입니다.\n\n"
        explanation += "주요 계산 기준:\n"
        explanation += "- 신·재생에너지 설비 설치·운영 목적 사용료: 총수입금의 10% (시행령 제32조 제1항 제3호)\n"
        explanation += "- 무단점용료: 해당 사용료의 110% (시행령 제94조 제1항)\n"
        explanation += "- 납부기한: 고지일로부터 30일 이내 (시행령 제94조 제3항)\n"
        explanation += "- 연체 시: 연체이자를 붙여 15일 이내 기한으로 납부 고지 (시행령 제94조 제5항)\n\n"
        
        if correct == "d":
            explanation += f"정답 이유:\n"
            explanation += f"④번이 정답인 이유:\n"
            explanation += f"- 'A법인이 무단점용료를 납부하지 않으면 국가는 납부하여야 할 무단점용료에 연체이자를 붙여 15일 이내의 기한을 정하여 납부를 고지하여야 한다'\n"
            explanation += f"- 시행령 제94조 제5항에 따라 연체이자를 붙여 15일 이내 기한으로 납부 고지하는 것이 올바름\n\n"
            explanation += f"오답 이유:\n"
            explanation += f"- ① 사용료는 500만원이 맞으나, 이것만으로는 완전한 설명이 아님\n"
            explanation += f"- ② 무단점용료는 550만원이 맞지만, '기간을 곱한 금액'이라는 설명이 틀림\n"
            explanation += f"- ③ 납부기한은 고지일로부터 30일 이내이지, 90일이 아님\n"
    
    elif "자금지원" in question:
        explanation += "농어촌정비법 제108조(자금지원)에 따른 농어촌정비사업 자금지원 규정입니다.\n\n"
        explanation += "주요 규정:\n"
        explanation += "- 제108조 제1항: 국가와 지방자치단체는 농어촌정비사업에 필요한 자금의 전부 또는 일부를 보조하거나 융자할 수 있음\n"
        explanation += "- 제108조 제2항: 관계 중앙행정기관의 장과 지방자치단체의 장은 사업비를 예산에 계상하여야 함\n"
        explanation += "- 제108조 제3항: 농어촌정비사업의 시행자는 사업 시행을 위탁한 경우 국가등으로부터 지원받은 자금의 일부를 사업을 끝내기 전에 위탁 사업자에게 내줄 수 있음\n\n"
        
        if correct == "d":
            explanation += f"정답 이유:\n"
            explanation += f"④번이 정답인 이유:\n"
            explanation += f"- '국가와 지방자치단체는 농어촌정비법에 따른 농어촌정비사업에 필요한 자금의 전부를 보조하거나 융자할 수 있다'\n"
            explanation += f"- 제108조 제1항에서 '전부 또는 일부'를 보조하거나 융자할 수 있다고 명시하여 올바른 설명\n\n"
            explanation += f"오답 이유:\n"
            explanation += f"- ① 보조자금 상환 의무: 제108조에서는 보조금의 상환 의무에 대한 규정이 없음\n"
            explanation += f"- ② 예산 계상 예외 처리: 제108조 제2항에서 예산 계상 의무가 있음\n"
            explanation += f"- ③ 위탁 사업자에 대한 자금 지급 제한: 제108조 제3항에서 지급이 가능함\n"
    
    elif "구분지상권" in question:
        explanation += "농어촌정비법 제110조의3(구분지상권의 설정등기 등) 관련 규정입니다.\n\n"
        explanation += "주요 규정:\n"
        explanation += "- 제110조의3 제1항: 농업생산기반시설의 지상 또는 지하 공간을 사용할 수 있는 구분지상권을 설정할 수 있음\n"
        explanation += "- 제110조의3 제2항: 구분지상권의 설정등기는 농업생산기반시설관리자가 신청함\n"
        explanation += "- 제110조의3 제3항: 토지의 지상 또는 지하 공간 사용에 따른 구분지상권의 등기절차에 관하여 필요한 사항은 대법원규칙으로 정함\n"
        explanation += "- 제110조의3 제4항: 구분지상권의 존속기간은 민법 제280조 및 제281조에도 불구하고 농업생산기반시설이 존속하는 날까지로 함\n\n"
        
        if correct == "d":
            explanation += f"정답 이유:\n"
            explanation += f"④번이 정답인 이유:\n"
            explanation += f"- '구분지상권의 존속기간은 민법 제280조 및 제281조에 따른다'고 했으나\n"
            explanation += f"- 실제로는 제110조의3 제4항에서 '민법 제280조 및 제281조에도 불구하고'라고 명시하여 민법 규정을 배제함\n"
            explanation += f"- 존속기간을 '농업생산기반시설이 존속하는 날까지'로 특별 규정함\n\n"
            explanation += f"올바른 설명들:\n"
            explanation += f"- ① 구분지상권 설정: 제110조의3 제1항에 따라 가능\n"
            explanation += f"- ② 설정등기 신청: 제110조의3 제2항에 따라 농업생산기반시설관리자가 신청\n"
            explanation += f"- ③ 등기절차: 제110조의3 제3항에 따라 대법원규칙으로 정함\n"
    
    else:
        explanation += "농어촌정비법은 농어촌의 정비와 개발을 위한 기본법입니다.\n\n"
        explanation += f"정답 이유:\n"
        explanation += f"{correct}번이 정답인 이유는 해당 법령 조항에 근거합니다.\n\n"
        explanation += "법령 근거: 농어촌정비법 및 시행령 관련 조항"
    
    return explanation

def enhance_farm_law_detailed():
    """농어촌정비법 상세 해설 개선"""
    filename = "1.농어촌정비법.js"
    print(f"🔄 농어촌정비법 상세 해설 개선 중...")
    
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
            new_explanation = create_detailed_farm_law_explanation(question)
            
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
        
        print(f"✅ {filename} 상세 해설 업데이트 완료 ({updated_count}개 문제 개선)")
        return True
        
    except Exception as e:
        print(f"❌ {filename} 처리 중 오류 발생: {e}")
        return False

if __name__ == "__main__":
    enhance_farm_law_detailed() 