#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def create_optimized_2025_exam():
    """최적화된 2025-exam.js 생성 - lazy loading 지원"""
    
    subjects = [
        "농어촌정비법", "공사법", "공운법", "직제규정", 
        "취업규칙", "인사규정", "행동강령", "회계기준"
    ]
    
    # 각 과목별 메타데이터만 포함하는 경량화된 구조
    js_content = """// 2025년 시험 최적화된 메인 파일
// Lazy loading 지원으로 성능 개선
// 생성일: 2025-08-17

console.log('2025년 시험 시스템 초기화 중...');

// 과목별 메타데이터 (경량화)
window.exam2025 = {
    metadata: {
        year: 2025,
        version: "2.0-optimized",
        total_subjects: 8,
        supports_lazy_loading: true,
        last_updated: "2025-08-17"
    },
    subjects: {
"""
    
    # 각 과목별 메타데이터 추가
    for i, subject in enumerate(subjects):
        # 실제 파일에서 문제 수 계산
        unified_file = f"/Users/hyungchangyoun/Documents/project/testpool/2025-{subject}-unified.js"
        question_count = 0
        
        if os.path.exists(unified_file):
            with open(unified_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # total_questions 값 추출
                import re
                match = re.search(r'"total_questions":\s*(\d+)', content)
                if match:
                    question_count = int(match.group(1))
        
        js_content += f"""        "{subject}": {{
            name: "{subject}",
            total_questions: {question_count},
            file: "2025-{subject}-unified.js",
            loaded: false,
            data: null
        }}"""
        
        if i < len(subjects) - 1:
            js_content += ","
        js_content += "\n"
    
    js_content += """    }
};

// Lazy Loading 함수들
window.loadSubject2025 = async function(subjectName) {
    console.log(`Loading subject: ${subjectName}`);
    
    const subjectInfo = window.exam2025.subjects[subjectName];
    if (!subjectInfo) {
        throw new Error(`Unknown subject: ${subjectName}`);
    }
    
    // 이미 로드된 경우 캐시된 데이터 반환
    if (subjectInfo.loaded && subjectInfo.data) {
        console.log(`Subject ${subjectName} already loaded from cache`);
        return subjectInfo.data;
    }
    
    try {
        // 동적 스크립트 로딩
        await loadScript(subjectInfo.file);
        
        // 로드된 데이터 확인
        if (window.subjects2025 && window.subjects2025[subjectName]) {
            subjectInfo.data = window.subjects2025[subjectName];
            subjectInfo.loaded = true;
            
            console.log(`✅ ${subjectName} loaded: ${subjectInfo.data.metadata.total_questions} questions`);
            return subjectInfo.data;
        } else {
            throw new Error(`Failed to load subject data: ${subjectName}`);
        }
    } catch (error) {
        console.error(`Error loading subject ${subjectName}:`, error);
        throw error;
    }
};

// 스크립트 동적 로딩 헬퍼
function loadScript(filename) {
    return new Promise((resolve, reject) => {
        // 이미 로드된 스크립트인지 확인
        const existingScript = document.querySelector(`script[src*="${filename}"]`);
        if (existingScript) {
            resolve();
            return;
        }
        
        const script = document.createElement('script');
        script.src = filename;
        script.onload = resolve;
        script.onerror = () => reject(new Error(`Failed to load script: ${filename}`));
        document.head.appendChild(script);
    });
}

// 과목별 문제 데이터 가져오기 (하위 호환성)
window.getQuestionsForSubject2025 = async function(subjectName) {
    try {
        const subjectData = await window.loadSubject2025(subjectName);
        
        // 기존 형식으로 변환하여 반환
        return subjectData.questions.map(q => ({
            question: q.question,
            a: q.choices.a,
            b: q.choices.b,
            c: q.choices.c,
            d: q.choices.d,
            correct: q.answer.correct,
            explanation: q.answer.explanation.brief,
            detailedExplanation: q.answer.explanation.detailed,
            urls: q.answer.explanation.references.law_links
        }));
    } catch (error) {
        console.error(`Error getting questions for ${subjectName}:`, error);
        return [];
    }
};

// 모든 과목 목록 반환
window.getAllSubjects2025 = function() {
    return Object.keys(window.exam2025.subjects);
};

// 과목별 메타데이터 반환
window.getSubjectMetadata2025 = function(subjectName) {
    const subject = window.exam2025.subjects[subjectName];
    return subject ? {
        name: subject.name,
        total_questions: subject.total_questions,
        loaded: subject.loaded
    } : null;
};

// 전체 통계 정보
window.getExamStats2025 = function() {
    const subjects = window.exam2025.subjects;
    const totalQuestions = Object.values(subjects).reduce((sum, subject) => sum + subject.total_questions, 0);
    const loadedSubjects = Object.values(subjects).filter(s => s.loaded).length;
    
    return {
        total_subjects: Object.keys(subjects).length,
        total_questions: totalQuestions,
        loaded_subjects: loadedSubjects,
        loading_progress: `${loadedSubjects}/${Object.keys(subjects).length}`
    };
};

// 성능 모니터링
window.exam2025Performance = {
    start_time: Date.now(),
    load_times: {},
    
    recordLoadTime: function(subject, startTime) {
        this.load_times[subject] = Date.now() - startTime;
        console.log(`📊 ${subject} load time: ${this.load_times[subject]}ms`);
    },
    
    getStats: function() {
        return {
            session_duration: Date.now() - this.start_time,
            load_times: this.load_times,
            average_load_time: Object.values(this.load_times).reduce((a, b) => a + b, 0) / Object.values(this.load_times).length || 0
        };
    }
};

// 사용법 안내
console.log(`
🎓 2025년 시험 시스템 사용법:
- 과목 로드: await loadSubject2025('농어촌정비법')
- 문제 가져오기: await getQuestionsForSubject2025('농어촌정비법')  
- 과목 목록: getAllSubjects2025()
- 통계 정보: getExamStats2025()

📊 현재 상태: ${Object.keys(window.exam2025.subjects).length}개 과목 등록됨
`);

// 초기화 완료
window.exam2025.initialized = true;
console.log('✅ 2025년 시험 시스템 초기화 완료');
"""
    
    # 파일 저장
    output_path = "/Users/hyungchangyoun/Documents/project/testpool/2025-exam-optimized.js"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    return output_path

def create_demo_html():
    """새로운 시스템 테스트용 HTML 생성"""
    
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2025년 시험 시스템 테스트</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .subject-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .subject-card { border: 1px solid #ddd; padding: 15px; border-radius: 8px; cursor: pointer; }
        .subject-card:hover { background: #f5f5f5; }
        .subject-card.loaded { background: #e8f5e8; border-color: #4caf50; }
        .stats { background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }
        .questions { margin-top: 20px; }
        .question { background: white; border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .loading { text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 2025년 시험 시스템 테스트</h1>
        
        <div class="stats" id="stats">
            <h3>📊 시스템 통계</h3>
            <div id="statsContent">로딩 중...</div>
        </div>
        
        <h3>📚 과목별 로드 테스트</h3>
        <div class="subject-grid" id="subjectGrid">
            <!-- 동적으로 생성됨 -->
        </div>
        
        <div class="questions" id="questions">
            <!-- 선택된 과목의 문제들이 여기에 표시됨 -->
        </div>
    </div>

    <script src="2025-exam-optimized.js"></script>
    <script>
        // DOM 로드 후 초기화
        document.addEventListener('DOMContentLoaded', function() {
            initializeTestPage();
        });
        
        function initializeTestPage() {
            updateStats();
            createSubjectCards();
        }
        
        function updateStats() {
            const stats = window.getExamStats2025();
            const performance = window.exam2025Performance.getStats();
            
            document.getElementById('statsContent').innerHTML = `
                <p><strong>총 과목 수:</strong> ${stats.total_subjects}</p>
                <p><strong>총 문제 수:</strong> ${stats.total_questions}</p>
                <p><strong>로드된 과목:</strong> ${stats.loading_progress}</p>
                <p><strong>세션 시간:</strong> ${Math.round(performance.session_duration / 1000)}초</p>
                <p><strong>평균 로드 시간:</strong> ${Math.round(performance.average_load_time || 0)}ms</p>
            `;
        }
        
        function createSubjectCards() {
            const subjects = window.getAllSubjects2025();
            const grid = document.getElementById('subjectGrid');
            
            grid.innerHTML = subjects.map(subject => {
                const metadata = window.getSubjectMetadata2025(subject);
                return `
                    <div class="subject-card" data-subject="${subject}" onclick="loadSubjectTest('${subject}')">
                        <h4>${subject}</h4>
                        <p>문제 수: ${metadata.total_questions}개</p>
                        <p>상태: <span id="status-${subject}">${metadata.loaded ? '로드됨' : '대기중'}</span></p>
                    </div>
                `;
            }).join('');
        }
        
        async function loadSubjectTest(subjectName) {
            const statusEl = document.getElementById(`status-${subjectName}`);
            const card = document.querySelector(`[data-subject="${subjectName}"]`);
            
            try {
                statusEl.textContent = '로딩중...';
                
                const startTime = Date.now();
                const questions = await window.getQuestionsForSubject2025(subjectName);
                window.exam2025Performance.recordLoadTime(subjectName, startTime);
                
                statusEl.textContent = '로드됨';
                card.classList.add('loaded');
                
                displayQuestions(subjectName, questions.slice(0, 3)); // 처음 3문제만 표시
                updateStats();
                
            } catch (error) {
                statusEl.textContent = '실패';
                console.error('로드 실패:', error);
                alert(`${subjectName} 로드 실패: ${error.message}`);
            }
        }
        
        function displayQuestions(subjectName, questions) {
            const questionsEl = document.getElementById('questions');
            
            questionsEl.innerHTML = `
                <h3>📋 ${subjectName} (샘플 ${questions.length}문제)</h3>
                ${questions.map((q, index) => `
                    <div class="question">
                        <h4>문제 ${index + 1}</h4>
                        <p><strong>Q:</strong> ${q.question}</p>
                        <p><strong>정답:</strong> ${q.correct}</p>
                        <p><strong>해설:</strong> ${q.explanation}</p>
                        ${q.detailedExplanation ? `<p><strong>상세해설:</strong> ${q.detailedExplanation.substring(0, 200)}...</p>` : ''}
                    </div>
                `).join('')}
            `;
        }
    </script>
</body>
</html>"""
    
    demo_path = "/Users/hyungchangyoun/Documents/project/testpool/2025-test-demo.html"
    with open(demo_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return demo_path

if __name__ == "__main__":
    print("🚀 최적화된 2025년 시험 시스템 생성 중...")
    
    # 최적화된 메인 파일 생성
    main_file = create_optimized_2025_exam()
    print(f"✅ 메인 파일 생성: {main_file}")
    
    # 테스트 데모 페이지 생성
    demo_file = create_demo_html()
    print(f"✅ 테스트 페이지 생성: {demo_file}")
    
    print(f"""
📊 작업 완료!

생성된 파일:
1. 2025-exam-optimized.js - 최적화된 메인 파일 (lazy loading 지원)
2. 2025-test-demo.html - 새 시스템 테스트용 페이지

새로운 구조의 장점:
✅ Lazy Loading - 필요한 과목만 동적 로드
✅ 표준화된 데이터 구조 - 일관된 형식
✅ 성능 최적화 - 초기 로드 시간 단축  
✅ 캐싱 지원 - 한번 로드한 데이터 재사용
✅ 하위 호환성 - 기존 코드와 호환

테스트 방법:
브라우저에서 2025-test-demo.html 열어서 테스트하세요!
""")