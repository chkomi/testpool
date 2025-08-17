#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from pathlib import Path

def cleanup_old_2025_files():
    """기존 분산된 2025 파일들 정리"""
    
    base_dir = "/Users/hyungchangyoun/Documents/project/testpool"
    
    # 백업 디렉토리 생성
    backup_dir = os.path.join(base_dir, "backup_old_2025_files")
    os.makedirs(backup_dir, exist_ok=True)
    
    # 정리할 파일들 (기존 분산 파일들)
    files_to_backup = [
        "2025-data-농어촌정비법-explanations.js",  # 중복된 해설 파일
        "2025-exam.js",  # 5000+ 라인의 거대 파일
        # 기타 임시/중복 파일들
        "취업규칙_questions.json",
        "취업규칙_questions.js", 
        "existing_answers.json",
        "취업규칙_47_questions.json",
        "취업규칙_47_questions_final.json",
        "취업규칙_47_questions_final.js",
        "취업규칙_47_questions_simple.json",
        "취업규칙_47_questions_simple.js",
        "취업규칙_47_complete.json",
        "existing_explanations.json",
        "explanation_data.json",
        "취업규칙_47_with_explanations.json",
        "replace_questions.js",
        "replace_with_explanations.js",
        "취업규칙_47_questions.js",
        "취업규칙_47_questions_fixed.js",
        "취업규칙_47_complete.js",
        "replace_employment_rules.js"
    ]
    
    backed_up_files = []
    
    for file_name in files_to_backup:
        file_path = os.path.join(base_dir, file_name)
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, file_name)
            try:
                shutil.move(file_path, backup_path)
                backed_up_files.append(file_name)
                print(f"✅ 백업됨: {file_name}")
            except Exception as e:
                print(f"❌ 백업 실패 {file_name}: {e}")
    
    return backed_up_files, backup_dir

def create_file_structure_doc():
    """새로운 파일 구조 문서화"""
    
    doc_content = """# 2025년 시험 데이터 구조 개선 완료

## 📊 개선 사항 요약

### ❌ 기존 문제점
1. **데이터 구조 불일치**: 과목마다 다른 필드명과 구조 사용
2. **분산된 파일들**: 해설이 별도 파일로 분리되어 유지보수 어려움  
3. **거대한 메인 파일**: 2025-exam.js (5000+ 라인) 로딩 성능 저하
4. **중복 및 임시 파일**: 20+ 개의 중복/임시 파일들이 산재

### ✅ 개선 결과

#### 1. 표준화된 데이터 구조
```javascript
{
    "question": "문제 내용",
    "choices": {
        "a": "선택지 A",
        "b": "선택지 B", 
        "c": "선택지 C",
        "d": "선택지 D"
    },
    "answer": {
        "correct": "정답",
        "explanation": {
            "brief": "간단 해설",
            "detailed": "상세 해설",
            "references": {
                "law_links": ["법령 링크들"],
                "articles": ["관련 조문들"]
            }
        }
    }
}
```

#### 2. 체계적인 파일 구조
```
📁 2025년 시험 데이터 (새로운 구조)
├── 2025-exam-optimized.js          # 최적화된 메인 파일 (lazy loading)
├── 2025-{과목명}-unified.js        # 과목별 통합 데이터 (8개 파일)
├── 2025-exam-unified.js            # 전체 통합 파일 (선택적 사용)
└── 2025-test-demo.html             # 테스트/데모 페이지

📁 백업 (기존 파일들)
└── backup_old_2025_files/          # 기존 분산 파일들 백업
```

#### 3. 성능 최적화
- **Lazy Loading**: 필요한 과목만 동적 로드
- **캐싱**: 한번 로드한 데이터 메모리 캐시
- **초기 로드 시간**: 5000+ 라인 → 경량 메타데이터만
- **메모리 효율**: 사용하지 않는 과목 데이터 로드 안함

## 📚 과목별 데이터 현황

| 과목명 | 문제 수 | 상태 | 특이사항 |
|--------|---------|------|----------|
| 농어촌정비법 | 102개 | ✅ 완료 | 상세해설 포함 |
| 공사법 | 99개 | ✅ 완료 | 표준 구조 |
| 공운법 | 0개 | ⚠️ 데이터 없음 | 파일 확인 필요 |
| 직제규정 | 27개 | ✅ 완료 | 표준 구조 |
| 취업규칙 | 47개 | ✅ 완료 | 파싱 이슈 일부 존재 |
| 인사규정 | 56개 | ✅ 완료 | 완벽 파싱 |
| 행동강령 | 21개 | ✅ 완료 | 표준 구조 |
| 회계기준 | 53개 | ✅ 완료 | 56개 목표에서 3개 차이 |

**총계**: 405개 문제 (공운법 제외)

## 🚀 사용법

### 기본 사용법 (하위 호환성)
```javascript
// 기존 방식과 동일하게 사용 가능
const questions = await getQuestionsForSubject2025('농어촌정비법');
```

### 새로운 고급 기능
```javascript
// 과목 메타데이터 확인
const metadata = getSubjectMetadata2025('농어촌정비법');

// 전체 통계
const stats = getExamStats2025();

// 성능 모니터링
const performance = window.exam2025Performance.getStats();
```

### 통합 HTML 적용 방법
```html
<!-- 기존 방식 -->
<script src="2025-exam.js"></script>

<!-- 새로운 최적화된 방식 -->
<script src="2025-exam-optimized.js"></script>
```

## 🔧 개발자 가이드

### 새 과목 추가
1. 원본 텍스트를 `2025/{과목명}.txt`에 저장
2. `create_unified_2025_data.py` 스크립트의 subjects 딕셔너리에 추가
3. 스크립트 실행하여 통합 파일 생성

### 데이터 수정
1. `2025-{과목명}-unified.js` 파일에서 직접 수정
2. 또는 원본 데이터 수정 후 스크립트 재실행

### 성능 모니터링
- 브라우저 개발자 도구 콘솔에서 로드 시간 확인
- `window.exam2025Performance.getStats()` 활용

## 📋 향후 개선 계획

1. **공운법 데이터 보완** - 현재 0개 문제 해결
2. **회계기준 완성** - 53개 → 56개 목표 달성  
3. **취업규칙 파싱 개선** - 복잡한 다중구조 문제 해결
4. **자동화 스크립트** - 데이터 업데이트 자동화
5. **타입스크립트 적용** - 타입 안정성 향상

---
*문서 생성일: 2025-08-17*
*마지막 업데이트: 2025-08-17*
"""
    
    doc_path = "/Users/hyungchangyoun/Documents/project/testpool/2025-DATA-STRUCTURE-IMPROVEMENT.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    return doc_path

if __name__ == "__main__":
    print("🧹 2025년 파일 정리 작업 시작...")
    
    # 기존 파일들 백업
    backed_up_files, backup_dir = cleanup_old_2025_files()
    
    # 문서화
    doc_path = create_file_structure_doc()
    
    print(f"""
✅ 정리 작업 완료!

📦 백업된 파일: {len(backed_up_files)}개
📁 백업 위치: {backup_dir}

📄 생성된 문서: 2025-DATA-STRUCTURE-IMPROVEMENT.md

🎯 결과 요약:
- 분산된 파일들 → 체계적 구조로 통합
- 5000+ 라인 메인 파일 → 경량 lazy loading 시스템  
- 일관성 없는 데이터 → 표준화된 구조
- 20+ 중복 파일들 → 8개 과목별 통합 파일

다음 단계:
1. 2025-test-demo.html에서 새 시스템 테스트
2. 기존 2025-exam.html을 새 시스템으로 업데이트
3. 공운법 데이터 보완 작업
""")