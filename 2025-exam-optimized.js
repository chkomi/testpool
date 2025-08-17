// 2025년 시험 최적화된 메인 파일
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
        "농어촌정비법": {
            name: "농어촌정비법",
            total_questions: 102,
            file: "2025-농어촌정비법-unified.js",
            loaded: false,
            data: null
        },
        "공사법": {
            name: "공사법",
            total_questions: 99,
            file: "2025-공사법-unified.js",
            loaded: false,
            data: null
        },
        "공운법": {
            name: "공운법",
            total_questions: 0,
            file: "2025-공운법-unified.js",
            loaded: false,
            data: null
        },
        "직제규정": {
            name: "직제규정",
            total_questions: 27,
            file: "2025-직제규정-unified.js",
            loaded: false,
            data: null
        },
        "취업규칙": {
            name: "취업규칙",
            total_questions: 47,
            file: "2025-취업규칙-unified.js",
            loaded: false,
            data: null
        },
        "인사규정": {
            name: "인사규정",
            total_questions: 56,
            file: "2025-인사규정-unified.js",
            loaded: false,
            data: null
        },
        "행동강령": {
            name: "행동강령",
            total_questions: 21,
            file: "2025-행동강령-unified.js",
            loaded: false,
            data: null
        },
        "회계기준": {
            name: "회계기준",
            total_questions: 53,
            file: "2025-회계기준-unified.js",
            loaded: false,
            data: null
        }
    }
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
