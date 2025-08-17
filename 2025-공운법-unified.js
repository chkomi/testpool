// 공운법 통합 데이터 (표준화된 구조)
// 마지막 업데이트: 2025-08-17

window.subjects2025 = window.subjects2025 || {};

window.subjects2025['공운법'] = {
    metadata: {
        "subject": "공운법",
        "total_questions": 0,
        "source_file": "2025-data-공운법.js",
        "last_updated": "2025-08-17"
},
    questions: []
};

// 하위 호환성을 위한 기존 형식 유지
window.currentSubjectQuestions = window.subjects2025['공운법'].questions.map(q => ({
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
