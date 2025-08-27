#!/usr/bin/env python3
# Script to update specific question explanations in 2025-gongsa.js

import re
import sys

def update_question_9(content):
    """Update question 9 explanation"""
    pattern = r'(\s+"questionNumber": 9,.*?"explanation": ")(정답: c\n\n.*?법령 근거: 한국농어촌공사 및 농지관리기금법 관련 조항)(")'
    
    new_explanation = """문제 9 — 【정답】 c — 【해설】

관련 법령: 「한국농어촌공사 및 농지관리기금법」 제34조제1항

정답 이유:
c번이 정답입니다. 농지관리기금은 은퇴하려는 농업인의 농지를 매입하여 '농업에 종사하려는 자'에게 우선 매도하는 것이 목적이며, 일반인에게 우선적으로 매도하는 것은 법령에 규정되지 않은 부적절한 활용입니다.

오답 분석:
① 직업전환 농업인의 농지 임차 자금 융자는 「한국농어촌공사 및 농지관리기금법」 제34조제1항에 따라 적절한 활용입니다.
② 병충해로 인한 경영위기 농업인 지원을 위한 농지매입사업 자금 융자는 동법에 따라 적절합니다.
④ 농지의 재개발사업 필요 자금의 투자는 동법 제34조에 규정된 적절한 활용입니다."""
    
    return re.sub(pattern, r'\1' + new_explanation + r'\3', content, flags=re.DOTALL)

def update_question_11(content):
    """Update question 11 explanation"""
    # Find question 11 specifically
    pattern = r'(\s+"questionNumber": 11,.*?"explanation": ")(정답: d\n\n.*?법령 근거: 한국농어촌공사 및 농지관리기금법 관련 조항)(")'
    
    new_explanation = """문제 11 — 【정답】 d — 【해설】

관련 법령: 「한국농어촌공사 및 농지관리기금법 시행령」 제17조

정답 이유:
d번 (㉡, ㉣)이 정답입니다. 농지관리기금에서 융자를 받아 사업을 시행한 결과 발생하는 손익 중 기금에 귀속되는 것은 농지의 임차료와 임대료의 차액(㉡)과 농지의 임대료(㉣)입니다.

오답 분석:
㉠ 농지연금 위험부담금은 기금에 귀속되는 손익에 해당하지 않습니다.
㉢ 농지연금채권에 대한 이자는 기금에 귀속되는 손익 항목이 아닙니다.
따라서 ① (㉠, ㉡), ② (㉡, ㉢), ③ (㉢, ㉣)는 모두 부정확한 조합입니다."""
    
    return re.sub(pattern, r'\1' + new_explanation + r'\3', content, flags=re.DOTALL)

def update_question_12(content):
    """Update question 12 explanation and correct answer"""
    # First, change the correct answer from "a" to "b"
    pattern_correct = r'(\s+"questionNumber": 12,.*?"correct": ")(a)(")'
    content = re.sub(pattern_correct, r'\1b\3', content, flags=re.DOTALL)
    
    # Then update the explanation
    pattern_explanation = r'(\s+"questionNumber": 12,.*?"explanation": ")(정답: a\n\n.*?법령 근거: 한국농어촌공사 및 농지관리기금법 관련 조항)(")'
    
    new_explanation = """문제 12 — 【정답】 b — 【해설】

관련 법령: 「한국농어촌공사 및 농지관리기금법」 제12조

정답 이유:
b번이 정답입니다. 공사가 (가)를 발행하는 경우에는 발행목적과 발행방법에 관하여 이사회의 의결을 거쳐야 합니다.

오답 분석:
① (가)의 발행액은 공사의 자본금에서 적립금을 차감한 금액의 2배를 초과하지 못한다는 것은 부정확합니다.
③ 정부는 공사가 발행하는 (가)의 원리금 상환을 보증하지 않는다는 것은 사실이 아닙니다.
④ 공사는 농림축산식품부장관의 승인을 거쳐 (가)의 발행을 최종 결정한다는 것은 부정확합니다."""
    
    return re.sub(pattern_explanation, r'\1' + new_explanation + r'\3', content, flags=re.DOTALL)

def update_question_13(content):
    """Update question 13 explanation and correct answer"""
    # First, change the correct answer from "b" to "c"  
    pattern_correct = r'(\s+"questionNumber": 13,.*?"correct": ")(b)(")'
    content = re.sub(pattern_correct, r'\1c\3', content, flags=re.DOTALL)
    
    # Then update the explanation
    pattern_explanation = r'(\s+"questionNumber": 13,.*?"explanation": ")(정답: b\n\n.*?법령 근거: 한국농어촌공사 및 농지관리기금법 관련 조항)(")'
    
    new_explanation = """문제 13 — 【정답】 c — 【해설】

관련 법령: 「한국농어촌공사 및 농지관리기금법」 제11조

정답 이유:
c번이 정답입니다. 국고 납입과 관련된 조항에 따라 이월손실금, 자본금, 20/100, 이익준비금, 자본금, 사업확장적립금의 순서가 올바른 조합입니다.

오답 분석:
① 부채, 자산, 10/100, 적립금, 자본금, 자본금의 조합은 법령 규정과 일치하지 않습니다.
② 이월손실금, 자본금, 20/100, 적립금, 적립금, 자본금의 조합은 부분적으로 부정확합니다.
④ 이월손실금, 자산, 10/100, 이익준비금, 자본금, 사업확장적립금의 조합은 법령 규정에 맞지 않습니다."""
    
    return re.sub(pattern_explanation, r'\1' + new_explanation + r'\3', content, flags=re.DOTALL)

def main():
    file_path = '/Users/yunhyungchang/Documents/project/testpool/testpool/2025-gongsa.js'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Original file size: {len(content)} characters")
    
    # Update each question
    content = update_question_9(content)
    print("Updated question 9")
    
    content = update_question_11(content)
    print("Updated question 11")
    
    content = update_question_12(content)
    print("Updated question 12 (changed answer to 'b' and explanation)")
    
    content = update_question_13(content)
    print("Updated question 13 (changed answer to 'c' and explanation)")
    
    # Write the updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated file size: {len(content)} characters")
    print("Successfully updated questions 9, 11, 12, and 13")

if __name__ == "__main__":
    main()