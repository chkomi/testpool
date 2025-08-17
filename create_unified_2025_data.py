#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os
from pathlib import Path

def read_js_file(file_path):
    """JS 파일에서 데이터 추출"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # window.currentSubjectQuestions = [...] 패턴 찾기
        match = re.search(r'window\.currentSubjectQuestions\s*=\s*(\[.*?\]);', content, re.DOTALL)
        if match:
            questions_str = match.group(1)
            # eval 대신 json으로 파싱 시도
            try:
                # JavaScript 배열을 JSON으로 변환
                questions_str = questions_str.replace("'", '"')
                return json.loads(questions_str)
            except:
                # 실패시 수동 파싱
                return parse_questions_manually(questions_str)
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def parse_questions_manually(content):
    """수동으로 문제 데이터 파싱"""
    questions = []
    # 간단한 정규식 파싱
    question_blocks = re.findall(r'\{[^}]*"question"[^}]*\}', content, re.DOTALL)
    for block in question_blocks:
        try:
            # 기본 JSON 파싱 시도
            question = json.loads(block.replace("'", '"'))
            questions.append(question)
        except:
            continue
    return questions

def standardize_question_format(question):
    """문제 데이터 표준화"""
    standardized = {
        "question": question.get("question", ""),
        "choices": {
            "a": question.get("a", ""),
            "b": question.get("b", ""),
            "c": question.get("c", ""),
            "d": question.get("d", "")
        },
        "answer": {
            "correct": question.get("correct", "a"),
            "explanation": {
                "brief": question.get("explanation", ""),
                "detailed": question.get("detailedExplanation", ""),
                "references": {
                    "law_links": question.get("urls", []),
                    "articles": extract_articles(question.get("explanation", ""))
                }
            }
        }
    }
    return standardized

def extract_articles(explanation):
    """설명에서 법조문 정보 추출"""
    articles = []
    # 제XX조 패턴 찾기
    patterns = [
        r'제(\d+)조',
        r'제(\d+)조의(\d+)',
        r'제(\d+)조\s*\([^)]+\)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, explanation)
        articles.extend(matches)
    
    return list(set(articles))

def create_unified_subject_data():
    """과목별 통합 데이터 생성"""
    
    subjects = {
        "농어촌정비법": "2025-data-농어촌정비법.js",
        "공사법": "2025-data-공사법.js", 
        "공운법": "2025-data-공운법.js",
        "직제규정": "2025-data-직제규정.js",
        "취업규칙": "2025-data-취업규칙.js",
        "인사규정": "2025-data-인사규정.js",
        "행동강령": "2025-data-행동강령.js",
        "회계기준": "2025-data-회계기준.js"
    }
    
    unified_data = {}
    
    for subject_name, file_name in subjects.items():
        file_path = f"/Users/hyungchangyoun/Documents/project/testpool/{file_name}"
        
        if os.path.exists(file_path):
            print(f"Processing {subject_name}...")
            
            raw_questions = read_js_file(file_path)
            standardized_questions = []
            
            for q in raw_questions:
                try:
                    standardized = standardize_question_format(q)
                    standardized_questions.append(standardized)
                except Exception as e:
                    print(f"Error standardizing question in {subject_name}: {e}")
                    continue
            
            unified_data[subject_name] = {
                "metadata": {
                    "subject": subject_name,
                    "total_questions": len(standardized_questions),
                    "source_file": file_name,
                    "last_updated": "2025-08-17"
                },
                "questions": standardized_questions
            }
            
            print(f"✅ {subject_name}: {len(standardized_questions)}개 문제 처리 완료")
        else:
            print(f"❌ {subject_name}: 파일 없음 ({file_name})")
    
    return unified_data

def generate_unified_js_files(unified_data):
    """통합된 JS 파일들 생성"""
    
    # 1. 개별 과목별 JS 파일 생성
    for subject, data in unified_data.items():
        file_name = f"2025-{subject}-unified.js"
        file_path = f"/Users/hyungchangyoun/Documents/project/testpool/{file_name}"
        
        js_content = f"""// {subject} 통합 데이터 (표준화된 구조)
// 마지막 업데이트: {data['metadata']['last_updated']}

window.subjects2025 = window.subjects2025 || {{}};

window.subjects2025['{subject}'] = {{
    metadata: {json.dumps(data['metadata'], ensure_ascii=False, indent=8)},
    questions: {json.dumps(data['questions'], ensure_ascii=False, indent=8)}
}};

// 하위 호환성을 위한 기존 형식 유지
window.currentSubjectQuestions = window.subjects2025['{subject}'].questions.map(q => ({{
    question: q.question,
    a: q.choices.a,
    b: q.choices.b, 
    c: q.choices.c,
    d: q.choices.d,
    correct: q.answer.correct,
    explanation: q.answer.explanation.brief,
    detailedExplanation: q.answer.explanation.detailed,
    urls: q.answer.explanation.references.law_links
}}));
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"✅ 생성됨: {file_name}")
    
    # 2. 전체 통합 파일 생성
    master_file_path = "/Users/hyungchangyoun/Documents/project/testpool/2025-exam-unified.js"
    
    master_content = f"""// 2025년 시험 전체 통합 데이터
// 표준화된 구조로 모든 과목 데이터 포함
// 생성일: 2025-08-17

window.exam2025 = {{
    metadata: {{
        year: 2025,
        total_subjects: {len(unified_data)},
        total_questions: {sum(data['metadata']['total_questions'] for data in unified_data.values())},
        structure_version: "1.0",
        last_updated: "2025-08-17"
    }},
    subjects: {json.dumps(unified_data, ensure_ascii=False, indent=4)}
}};

// 과목별 접근 함수들
window.getSubject2025 = function(subjectName) {{
    return window.exam2025.subjects[subjectName];
}};

window.getQuestions2025 = function(subjectName) {{
    const subject = window.getSubject2025(subjectName);
    return subject ? subject.questions : [];
}};

window.getAllSubjects2025 = function() {{
    return Object.keys(window.exam2025.subjects);
}};

// 하위 호환성 함수
window.loadSubject2025 = function(subjectName) {{
    const questions = window.getQuestions2025(subjectName);
    return questions.map(q => ({{
        question: q.question,
        a: q.choices.a,
        b: q.choices.b,
        c: q.choices.c, 
        d: q.choices.d,
        correct: q.answer.correct,
        explanation: q.answer.explanation.brief,
        detailedExplanation: q.answer.explanation.detailed,
        urls: q.answer.explanation.references.law_links
    }}));
}};

console.log('2025년 시험 데이터 로드 완료:', window.exam2025.metadata);
"""
    
    with open(master_file_path, 'w', encoding='utf-8') as f:
        f.write(master_content)
    
    print(f"✅ 마스터 파일 생성됨: 2025-exam-unified.js")

if __name__ == "__main__":
    print("🚀 2025년 시험 데이터 통합 작업 시작...")
    
    # 통합 데이터 생성
    unified_data = create_unified_subject_data()
    
    # JS 파일들 생성
    generate_unified_js_files(unified_data)
    
    print(f"\n📊 작업 완료 요약:")
    print(f"- 처리된 과목 수: {len(unified_data)}")
    print(f"- 총 문제 수: {sum(data['metadata']['total_questions'] for data in unified_data.values())}")
    print("\n생성된 파일들:")
    print("- 개별 과목별 통합 파일: 2025-{과목명}-unified.js")
    print("- 전체 마스터 파일: 2025-exam-unified.js")