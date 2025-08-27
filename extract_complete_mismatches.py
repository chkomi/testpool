#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import glob
import os
from urllib.parse import urlparse, parse_qs

def extract_articles_from_explanation(explanation):
    """해설에서 조문 번호를 추출"""
    if not explanation:
        return []
    
    # 「법령명」 제○조제○항 또는 제○조 패턴 매칭
    patterns = [
        r'제(\d+)조제(\d+)항',  # 제15조제1항
        r'제(\d+)조(?!제)',     # 제15조 (뒤에 제가 오지 않는 경우)
    ]
    
    articles = []
    for pattern in patterns:
        matches = re.findall(pattern, explanation)
        for match in matches:
            if isinstance(match, tuple):
                if len(match) == 2:  # 조+항
                    articles.append(f"{match[0]}조{match[1]}항")
                else:  # 조만
                    articles.append(f"{match[0]}조")
            else:  # 조만
                articles.append(f"{match}조")
    
    return list(set(articles))  # 중복 제거

def extract_articles_from_url(url):
    """URL에서 조문 번호를 추출"""
    if not url:
        return []
    
    articles = []
    
    # URL 파라미터에서 jo= 값 추출
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    if 'jo' in params:
        jo_value = params['jo'][0]
        articles.append(f"{jo_value}조")
    
    # URL 경로에서 조문 번호 패턴 매칭
    path_patterns = [
        r'/제(\d+)조/?$',  # /제109조
        r'/제(\d+)조제\d+항/?$',  # /제109조제1항
        r'/(\d+)/?$',  # 경로 끝의 숫자
        r'_(\d+)\.pdf',  # 파일명의 숫자
        r'제(\d+)조',  # 제109조 패턴
    ]
    
    for pattern in path_patterns:
        match = re.search(pattern, url)
        if match:
            articles.append(f"{match.group(1)}조")
    
    return list(set(articles))

def parse_js_file(file_path):
    """JS 파일에서 quizData 배열을 파싱"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 각 question 객체를 개별적으로 파싱
        questions = []
        
        # { 로 시작하는 객체들을 찾기
        question_pattern = r'\{\s*"questionNumber":\s*(\d+),.*?\}'
        question_matches = re.finditer(question_pattern, content, re.DOTALL)
        
        for match in question_matches:
            question_obj = match.group(0)
            
            # explanation 필드 추출
            exp_match = re.search(r'"explanation":\s*"(.*?)"(?=\s*,\s*"url)', question_obj, re.DOTALL)
            explanation = exp_match.group(1) if exp_match else ""
            
            # URL 필드들 추출
            url_match = re.search(r'"url":\s*"([^"]*)"', question_obj)
            urls_match = re.search(r'"urls":\s*\[(.*?)\]', question_obj, re.DOTALL)
            
            urls = []
            if url_match:
                urls.append(url_match.group(1))
            if urls_match:
                url_list_str = urls_match.group(1)
                url_items = re.findall(r'"([^"]*)"', url_list_str)
                urls.extend(url_items)
            
            questions.append({
                'questionNumber': int(match.group(1)),
                'explanation': explanation.replace('\\"', '"').replace('\\n', '\n'),
                'urls': urls
            })
        
        return questions
            
    except Exception as e:
        print(f"파일 읽기 오류 ({file_path}): {e}")
        return []

def is_complete_mismatch(explanation_jos, url_jos):
    """완전히 다른 조문인지 판단"""
    # 두 집합의 교집합이 없으면 완전히 다른 것
    return len(set(explanation_jos) & set(url_jos)) == 0

def analyze_file(file_path):
    """파일 분석하여 완전 불일치 항목 찾기"""
    subject_name = os.path.basename(file_path).replace('2025-', '').replace('.js', '')
    quiz_data = parse_js_file(file_path)
    
    complete_mismatches = []
    
    for question in quiz_data:
        question_num = question.get('questionNumber', 0)
        explanation = question.get('explanation', '')
        urls = question.get('urls', [])
        
        # 해설에서 조문 추출
        explanation_articles = extract_articles_from_explanation(explanation)
        
        # URL에서 조문 추출
        url_articles = []
        for url in urls:
            url_articles.extend(extract_articles_from_url(url))
        url_articles = list(set(url_articles))
        
        # 완전 불일치 체크
        if explanation_articles and url_articles:
            # 조문 번호만 비교 (항은 제외)
            exp_jos = list(set(art.split('조')[0] + '조' for art in explanation_articles))
            url_jos = list(set(art.split('조')[0] + '조' for art in url_articles))
            
            if is_complete_mismatch(exp_jos, url_jos):
                complete_mismatches.append({
                    'subject': subject_name,
                    'question': question_num,
                    'explanation_articles': explanation_articles,
                    'url_articles': url_articles,
                    'explanation_jos': exp_jos,
                    'url_jos': url_jos
                })
    
    return complete_mismatches

def main():
    """메인 함수"""
    js_files = glob.glob('2025-*.js')
    
    all_complete_mismatches = []
    
    print("=" * 80)
    print("해설과 URL의 조문이 완전히 다른 경우들")
    print("=" * 80)
    
    for file_path in sorted(js_files):
        complete_mismatches = analyze_file(file_path)
        all_complete_mismatches.extend(complete_mismatches)
        
        if complete_mismatches:
            print(f"\n[{file_path}] - {len(complete_mismatches)}개 발견")
    
    print(f"\n" + "=" * 80)
    print(f"전체 완전 불일치: {len(all_complete_mismatches)}개")
    print("=" * 80)
    
    if all_complete_mismatches:
        for mismatch in all_complete_mismatches:
            print(f"\n📌 {mismatch['subject']} - {mismatch['question']}번")
            print(f"   해설 조문: {', '.join(mismatch['explanation_jos'])}")
            print(f"   URL 조문:  {', '.join(mismatch['url_jos'])}")
            print(f"   ⚠️  완전 불일치: 공통 조문 없음")
    else:
        print("\n✅ 완전 불일치 사례가 발견되지 않았습니다.")

if __name__ == "__main__":
    main()