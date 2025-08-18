#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
법령집 폴더의 근거법령 텍스트를 기반으로 더욱 상세하고 논리적인 해설을 작성하는 스크립트
"""

import json
import re
import os

def load_law_texts():
    """법령집 폴더에서 법령 텍스트들을 로드"""
    law_texts = {}
    
    # 농어촌정비법
    try:
        with open("법령집/(법령) 1-1. 농어촌정비법.txt", 'r', encoding='utf-8') as f:
            law_texts["농어촌정비법"] = f.read()
    except:
        law_texts["농어촌정비법"] = ""
    
    try:
        with open("법령집/(법령) 1-2. 농어촌정비법 시행령.txt", 'r', encoding='utf-8') as f:
            law_texts["농어촌정비법_시행령"] = f.read()
    except:
        law_texts["농어촌정비법_시행령"] = ""
    
    # 공운법
    try:
        with open("법령집/(법령) 2-1 공운법.txt", 'r', encoding='utf-8') as f:
            law_texts["공운법"] = f.read()
    except:
        law_texts["공운법"] = ""
    
    try:
        with open("법령집/(법령) 2-2. 공운법 시행령.txt", 'r', encoding='utf-8') as f:
            law_texts["공운법_시행령"] = f.read()
    except:
        law_texts["공운법_시행령"] = ""
    
    # 공사법
    try:
        with open("법령집/(법령) 3-1. 공사법.txt", 'r', encoding='utf-8') as f:
            law_texts["공사법"] = f.read()
    except:
        law_texts["공사법"] = ""
    
    try:
        with open("법령집/(법령) 3-2. 공사법 시행령.txt", 'r', encoding='utf-8') as f:
            law_texts["공사법_시행령"] = f.read()
    except:
        law_texts["공사법_시행령"] = ""
    
    # 직제규정
    try:
        with open("법령집/(법령) 4. 직제규정.txt", 'r', encoding='utf-8') as f:
            law_texts["직제규정"] = f.read()
    except:
        law_texts["직제규정"] = ""
    
    # 취업규칙
    try:
        with open("법령집/(법령) 5. 취업규칙.txt", 'r', encoding='utf-8') as f:
            law_texts["취업규칙"] = f.read()
    except:
        law_texts["취업규칙"] = ""
    
    # 인사규정
    try:
        with open("법령집/(법령) 6. 인사규정.txt", 'r', encoding='utf-8') as f:
            law_texts["인사규정"] = f.read()
    except:
        law_texts["인사규정"] = ""
    
    # 행동강령
    try:
        with open("법령집/(법령) 7. 행동강령.txt", 'r', encoding='utf-8') as f:
            law_texts["행동강령"] = f.read()
    except:
        law_texts["행동강령"] = ""
    
    # 회계기준
    try:
        with open("법령집/(법령) 8. 회계기준.txt", 'r', encoding='utf-8') as f:
            law_texts["회계기준"] = f.read()
    except:
        law_texts["회계기준"] = ""
    
    return law_texts

def find_law_article(law_text, article_pattern):
    """법령 텍스트에서 특정 조항을 찾기"""
    if not law_text:
        return ""
    
    # 조항 패턴 매칭
    patterns = [
        rf"제{article_pattern}조[^\n]*\n(.*?)(?=제\d+조|$)",
        rf"제{article_pattern}조[^\n]*\n(.*?)(?=\n제\d+조|$)",
        rf"제{article_pattern}조[^\n]*\n(.*?)(?=\n\n|$)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, law_text, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return ""

def create_detailed_farm_law_explanation(question_data, law_texts):
    """농어촌정비법 상세 해설 생성"""
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
            # 시행령 제9조 내용 찾기
            article_9 = find_law_article(law_texts.get("농어촌정비법_시행령", ""), "9")
            if article_9:
                explanation += f"농어촌정비법 시행령 제9조에 따르면:\n{article_9}\n\n"
            
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
            # 제14조 내용 찾기
            article_14 = find_law_article(law_texts.get("농어촌정비법", ""), "14")
            if article_14:
                explanation += f"농어촌정비법 제14조에 따르면:\n{article_14}\n\n"
            
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
            # 제58조 내용 찾기
            article_58 = find_law_article(law_texts.get("농어촌정비법", ""), "58")
            if article_58:
                explanation += f"농어촌정비법 제58조에 따르면:\n{article_58}\n\n"
            
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
            # 시행령 제52조 내용 찾기
            article_52 = find_law_article(law_texts.get("농어촌정비법_시행령", ""), "52")
            if article_52:
                explanation += f"농어촌정비법 시행령 제52조에 따르면:\n{article_52}\n\n"
            
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
        # 시행령 제32조, 제94조 내용 찾기
        article_32 = find_law_article(law_texts.get("농어촌정비법_시행령", ""), "32")
        article_94 = find_law_article(law_texts.get("농어촌정비법_시행령", ""), "94")
        
        if article_32:
            explanation += f"농어촌정비법 시행령 제32조(사용료의 징수)에 따르면:\n{article_32}\n\n"
        
        if article_94:
            explanation += f"농어촌정비법 시행령 제94조(무단점용료의 징수)에 따르면:\n{article_94}\n\n"
        
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
        # 제108조 내용 찾기
        article_108 = find_law_article(law_texts.get("농어촌정비법", ""), "108")
        if article_108:
            explanation += f"농어촌정비법 제108조(자금지원)에 따르면:\n{article_108}\n\n"
        
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
        # 제110조의3 내용 찾기
        article_110_3 = find_law_article(law_texts.get("농어촌정비법", ""), "110의3")
        if article_110_3:
            explanation += f"농어촌정비법 제110조의3(구분지상권의 설정등기 등)에 따르면:\n{article_110_3}\n\n"
        
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
    
    elif "자원 조사" in question:
        # 제3조 내용 찾기
        article_3 = find_law_article(law_texts.get("농어촌정비법", ""), "3")
        if article_3:
            explanation += f"농어촌정비법 제3조(자원 조사)에 따르면:\n{article_3}\n\n"
        
        # 시행령 제3조 내용 찾기
        article_3_enforcement = find_law_article(law_texts.get("농어촌정비법_시행령", ""), "3")
        if article_3_enforcement:
            explanation += f"농어촌정비법 시행령 제3조(자원 조사의 대상 항목)에 따르면:\n{article_3_enforcement}\n\n"
        
        if correct == "d":
            explanation += f"정답 이유:\n"
            explanation += f"④번이 정답인 이유:\n"
            explanation += f"- '농식품의 유통구조 개선에 관한 사항'은 시행령 제3조의 조사 대상 항목에 포함되지 않음\n\n"
            explanation += f"올바른 조사 대상 항목:\n"
            explanation += f"- ① 농지의 분포상태와 이용에 관한 사항: 시행령 제3조 제1호에 해당\n"
            explanation += f"- ② 농업생산 기반 정비에 관한 사항: 시행령 제3조 제2호에 해당\n"
            explanation += f"- ③ 농어촌 관광휴양자원에 관한 사항: 시행령 제3조 제4호에 해당\n"
    
    else:
        explanation += "농어촌정비법은 농어촌의 정비와 개발을 위한 기본법입니다.\n\n"
        explanation += f"정답 이유:\n"
        explanation += f"{correct}번이 정답인 이유는 해당 법령 조항에 근거합니다.\n\n"
        explanation += "법령 근거: 농어촌정비법 및 시행령 관련 조항"
    
    return explanation

def create_detailed_explanation(question_data, subject, law_texts):
    """과목별 상세 해설 생성"""
    if subject == "농어촌정비법":
        return create_detailed_farm_law_explanation(question_data, law_texts)
    elif subject == "공운법":
        return create_detailed_public_operation_explanation(question_data, law_texts)
    elif subject == "공사법":
        return create_detailed_public_corp_explanation(question_data, law_texts)
    elif subject in ["직제규정", "취업규칙", "인사규정", "행동강령"]:
        return create_detailed_regulation_explanation(question_data, subject, law_texts)
    elif subject == "회계기준":
        return create_detailed_accounting_explanation(question_data, law_texts)
    
    return "정답: " + question_data.get("correct", "") + "\n\n해당 법령 조항에 근거합니다."

def create_detailed_public_operation_explanation(question_data, law_texts):
    """공공기관운영법 상세 해설 생성"""
    question = question_data.get("question", "")
    correct = question_data.get("correct", "")
    
    explanation = f"정답: {correct}\n\n"
    explanation += "공공기관의 운영에 관한 법률은 공공기관의 운영과 관리에 관한 기본법입니다.\n\n"
    
    # 문제 내용에 따라 관련 조항 찾기
    if "공공기관" in question:
        article_2 = find_law_article(law_texts.get("공운법", ""), "2")
        article_3 = find_law_article(law_texts.get("공운법", ""), "3")
        article_4 = find_law_article(law_texts.get("공운법", ""), "4")
        
        if article_2:
            explanation += f"공공기관의 운영에 관한 법률 제2조(정의)에 따르면:\n{article_2}\n\n"
        if article_3:
            explanation += f"공공기관의 운영에 관한 법률 제3조(공공기관의 분류)에 따르면:\n{article_3}\n\n"
        if article_4:
            explanation += f"공공기관의 운영에 관한 법률 제4조(공공기관의 운영원칙)에 따르면:\n{article_4}\n\n"
    
    elif "이사회" in question:
        article_15 = find_law_article(law_texts.get("공운법", ""), "15")
        article_16 = find_law_article(law_texts.get("공운법", ""), "16")
        article_17 = find_law_article(law_texts.get("공운법", ""), "17")
        
        if article_15:
            explanation += f"공공기관의 운영에 관한 법률 제15조(이사회의 구성)에 따르면:\n{article_15}\n\n"
        if article_16:
            explanation += f"공공기관의 운영에 관한 법률 제16조(이사회의 기능)에 따르면:\n{article_16}\n\n"
        if article_17:
            explanation += f"공공기관의 운영에 관한 법률 제17조(이사회의 운영)에 따르면:\n{article_17}\n\n"
    
    explanation += f"정답 이유:\n"
    explanation += f"{correct}번이 정답인 이유는 공공기관운영법의 관련 조항에 근거합니다.\n\n"
    explanation += "법령 근거: 공공기관의 운영에 관한 법률 관련 조항"
    
    return explanation

def create_detailed_public_corp_explanation(question_data, law_texts):
    """한국농어촌공사법 상세 해설 생성"""
    question = question_data.get("question", "")
    correct = question_data.get("correct", "")
    
    explanation = f"정답: {correct}\n\n"
    explanation += "한국농어촌공사 및 농지관리기금법은 한국농어촌공사의 설립과 운영에 관한 법률입니다.\n\n"
    
    if "한국농어촌공사" in question:
        article_3 = find_law_article(law_texts.get("공사법", ""), "3")
        article_4 = find_law_article(law_texts.get("공사법", ""), "4")
        article_5 = find_law_article(law_texts.get("공사법", ""), "5")
        
        if article_3:
            explanation += f"한국농어촌공사 및 농지관리기금법 제3조(한국농어촌공사의 설립)에 따르면:\n{article_3}\n\n"
        if article_4:
            explanation += f"한국농어촌공사 및 농지관리기금법 제4조(한국농어촌공사의 사업)에 따르면:\n{article_4}\n\n"
        if article_5:
            explanation += f"한국농어촌공사 및 농지관리기금법 제5조(한국농어촌공사의 조직)에 따르면:\n{article_5}\n\n"
    
    elif "농지관리기금" in question:
        article_31 = find_law_article(law_texts.get("공사법", ""), "31")
        article_32 = find_law_article(law_texts.get("공사법", ""), "32")
        article_33 = find_law_article(law_texts.get("공사법", ""), "33")
        
        if article_31:
            explanation += f"한국농어촌공사 및 농지관리기금법 제31조(농지관리기금의 설치)에 따르면:\n{article_31}\n\n"
        if article_32:
            explanation += f"한국농어촌공사 및 농지관리기금법 제32조(농지관리기금의 조성)에 따르면:\n{article_32}\n\n"
        if article_33:
            explanation += f"한국농어촌공사 및 농지관리기금법 제33조(농지관리기금의 운용)에 따르면:\n{article_33}\n\n"
    
    explanation += f"정답 이유:\n"
    explanation += f"{correct}번이 정답인 이유는 한국농어촌공사법의 관련 조항에 근거합니다.\n\n"
    explanation += "법령 근거: 한국농어촌공사 및 농지관리기금법 관련 조항"
    
    return explanation

def create_detailed_regulation_explanation(question_data, subject, law_texts):
    """규정 상세 해설 생성"""
    question = question_data.get("question", "")
    correct = question_data.get("correct", "")
    
    explanation = f"정답: {correct}\n\n"
    explanation += f"{subject}는 한국농어촌공사의 내부 운영 규정입니다.\n\n"
    
    # 해당 규정의 전체 내용을 참조
    regulation_text = law_texts.get(subject, "")
    if regulation_text:
        explanation += f"{subject}의 주요 내용:\n"
        explanation += regulation_text[:500] + "...\n\n"  # 처음 500자만 표시
    
    explanation += f"정답 이유:\n"
    explanation += f"{correct}번이 정답인 이유는 {subject}의 관련 조항에 근거합니다.\n\n"
    explanation += f"법령 근거: {subject} 관련 조항"
    
    return explanation

def create_detailed_accounting_explanation(question_data, law_texts):
    """회계기준 상세 해설 생성"""
    question = question_data.get("question", "")
    correct = question_data.get("correct", "")
    
    explanation = f"정답: {correct}\n\n"
    explanation += "공기업준정부기관회계기준시행세칙은 공기업의 회계 처리 기준입니다.\n\n"
    
    # 회계기준의 전체 내용을 참조
    accounting_text = law_texts.get("회계기준", "")
    if accounting_text:
        explanation += f"공기업준정부기관회계기준시행세칙의 주요 내용:\n"
        explanation += accounting_text[:500] + "...\n\n"  # 처음 500자만 표시
    
    explanation += f"정답 이유:\n"
    explanation += f"{correct}번이 정답인 이유는 공기업준정부기관회계기준시행세칙의 관련 조항에 근거합니다.\n\n"
    explanation += "법령 근거: 공기업준정부기관회계기준시행세칙 관련 조항"
    
    return explanation

def enhance_all_files_with_law_texts():
    """법령 텍스트를 기반으로 모든 파일의 상세 해설 개선"""
    print("📚 법령 텍스트 로딩 중...")
    law_texts = load_law_texts()
    print(f"✅ {len(law_texts)}개 법령 텍스트 로드 완료")
    
    subjects = {
        "1.농어촌정비법.js": "농어촌정비법",
        "2.공운법.js": "공운법", 
        "3.공사법.js": "공사법",
        "4.직제규정.js": "직제규정",
        "5.취업규칙.js": "취업규칙",
        "6.인사규정.js": "인사규정",
        "7.행동강령.js": "행동강령",
        "8.회계기준.js": "회계기준"
    }
    
    success_count = 0
    total_count = len(subjects)
    
    for filename, subject in subjects.items():
        if os.path.exists(filename):
            print(f"🔄 {subject} 상세 해설 개선 중...")
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # quizData 배열 추출
                match = re.search(r'const quizData = (\[.*?\]);', content, re.DOTALL)
                if not match:
                    print(f"❌ {filename}에서 quizData를 찾을 수 없습니다.")
                    continue
                
                quiz_data_str = match.group(1)
                quiz_data = json.loads(quiz_data_str)
                
                # 각 문제의 해설 개선
                updated_count = 0
                for question in quiz_data:
                    original_explanation = question.get("explanation", "")
                    new_explanation = create_detailed_explanation(question, subject, law_texts)
                    
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
                success_count += 1
                
            except Exception as e:
                print(f"❌ {filename} 처리 중 오류 발생: {e}")
        else:
            print(f"⚠️ {filename} 파일이 존재하지 않습니다.")
    
    print(f"\n📊 작업 완료: {success_count}/{total_count} 과목 처리 완료")
    
    if success_count == total_count:
        print("🎉 모든 과목의 상세 해설 작성이 완료되었습니다!")
    else:
        print("⚠️ 일부 과목 처리에 실패했습니다.")

if __name__ == "__main__":
    enhance_all_files_with_law_texts() 