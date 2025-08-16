function startQuizEngine(quizData) {
    // --- 에러 핸들링 및 검증 ---
    if (!quizData || !Array.isArray(quizData) || quizData.length === 0) {
        console.error('유효하지 않은 퀴즈 데이터:', quizData);
        showError('문제 데이터를 불러올 수 없습니다. 페이지를 새로고침해주세요.');
        return;
    }

    // --- DOM Element References ---
    const quiz = document.getElementById('quiz');
    const question = document.getElementById('question');
    const aText = document.getElementById('a_text');
    const bText = document.getElementById('b_text');
    const cText = document.getElementById('c_text');
    const dText = document.getElementById('d_text');
    const submitBtn = document.getElementById('submit');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const questionCounter = document.getElementById('question-counter');
    const progressBadge = document.getElementById('progress-badge');
    const answerList = document.querySelector('#quiz ul');

    // DOM 요소 검증
    const requiredElements = { quiz, question, aText, bText, cText, dText, submitBtn, prevBtn, nextBtn, questionCounter };
    const missingElements = Object.entries(requiredElements).filter(([name, element]) => !element).map(([name]) => name);
    
    if (missingElements.length > 0) {
        console.error('필수 DOM 요소가 누락됨:', missingElements);
        showError(`페이지 구조에 문제가 있습니다. 누락된 요소: ${missingElements.join(', ')}`);
        return;
    }

    // --- State Variables ---
    let shuffledQuizData, currentQuiz, score, userAnswers, questionAnswered;
    let isRandomMode = localStorage.getItem('quizRandomMode') !== 'false';

    // --- Helper Functions ---
    const shuffleArray = (array) => {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    };

    const createSequentialArray = (array) => array.map((q, index) => ({...q, originalIndex: index + 1}));

    // --- Error Handling Functions ---
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            background: #fee; 
            border: 1px solid #fcc; 
            color: #c00; 
            padding: 15px; 
            margin: 10px; 
            border-radius: 5px; 
            text-align: center;
            font-weight: bold;
        `;
        errorDiv.innerHTML = `
            <p>${message}</p>
            <button onclick="location.reload()" style="margin-top: 10px; padding: 8px 16px; background: #007cba; color: white; border: none; border-radius: 4px; cursor: pointer;">
                페이지 새로고침
            </button>
        `;
        
        // 기존 에러 메시지 제거
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();
        
        // 퀴즈 컨테이너 앞에 에러 메시지 추가
        const container = document.querySelector('.quiz-container') || document.body;
        container.insertBefore(errorDiv, container.firstChild);
    }

    function handleStorageError(error, fallbackAction) {
        console.warn('Storage error:', error);
        if (typeof fallbackAction === 'function') {
            fallbackAction();
        }
    }

    // --- Progress Management Functions ---
    function getProgressKey(subject) {
        // URL에서 년도 정보 추출
        const pathSegments = window.location.pathname.split('/');
        const currentPage = pathSegments[pathSegments.length - 1];
        
        // 2025년 시험인지 확인
        if (currentPage.includes('2025-exam.html')) {
            // URL에서 과목명 추출 또는 전역 변수 사용
            if (!subject) {
                const urlParams = new URLSearchParams(window.location.search);
                subject = urlParams.get('subject') || 'unknown';
            }
            return `exam_2025_${subject}_progress`;
        } else {
            // 2021-2024년 시험의 경우 년도만 추출
            const yearMatch = currentPage.match(/(\d{4})-exam\.html/);
            if (yearMatch) {
                const year = yearMatch[1];
                return `exam_${year}_progress`;
            }
        }
        
        // 기본값 (fallback)
        return 'exam_unknown_progress';
    }

    function saveProgress(subject = null) {
        try {
            const progressKey = getProgressKey(subject);
            const progressData = {
                shuffledData: shuffledQuizData,
                currentIndex: currentQuiz,
                userAnswers: userAnswers,
                score: score,
                total: shuffledQuizData.length,
                answered: userAnswers.filter(Boolean).length,
                correct: userAnswers.filter((answer, index) => answer && answer === shuffledQuizData[index]?.correct).length,
                timestamp: Date.now(),
                isRandomMode: isRandomMode
            };
            localStorage.setItem(progressKey, JSON.stringify(progressData));
            // console.log(`진행률 저장: ${progressKey}`, progressData.answered, '/', progressData.total);
        } catch (error) {
            console.warn('Progress save error:', error);
        }
    }

    function loadProgress(subject = null) {
        try {
            const progressKey = getProgressKey(subject);
            const savedProgress = localStorage.getItem(progressKey);
            if (savedProgress) {
                const progressData = JSON.parse(savedProgress);
                // console.log(`진행률 로드: ${progressKey}`, progressData.answered, '/', progressData.total);
                return progressData;
            }
        } catch (error) {
            console.warn('Progress load error:', error);
        }
        return null;
    }

    function clearProgress(subject = null) {
        try {
            const progressKey = getProgressKey(subject);
            localStorage.removeItem(progressKey);
            // console.log(`진행률 삭제: ${progressKey}`);
        } catch (error) {
            console.warn('Progress clear error:', error);
        }
    }

    // --- Core Functions ---
    function initializeQuiz() {
        try {
            // 진행상태 복원 시도
            const savedProgress = loadProgress();
            
            // URL 파라미터에서 resume 여부 확인
            const urlParams = new URLSearchParams(window.location.search);
            const shouldResume = urlParams.get('resume') === 'true';
            
            if (savedProgress && savedProgress.shuffledData && savedProgress.shuffledData.length > 0) {
                // 저장된 진행상태가 있으면 복원
                shuffledQuizData = savedProgress.shuffledData;
                currentQuiz = savedProgress.currentIndex || 0;
                userAnswers = savedProgress.userAnswers || [];
                score = savedProgress.score || 0;
                isRandomMode = savedProgress.isRandomMode !== undefined ? savedProgress.isRandomMode : isRandomMode;
                
                // 진행상태 복원 알림 (URL에 resume=true가 없는 경우에만)
                if (savedProgress.answered > 0 && !shouldResume) {
                    const resumeMessage = `이전 진행상태를 발견했습니다.\n진행률: ${savedProgress.answered}/${savedProgress.total} (${Math.round((savedProgress.answered/savedProgress.total)*100)}%)\n\n계속하시겠습니까?`;
                    if (confirm(resumeMessage)) {
                        // console.log('진행상태 복원 완료');
                    } else {
                        // 새로 시작하기로 선택한 경우
                        clearProgress();
                        shuffledQuizData = isRandomMode ? shuffleArray(quizData) : createSequentialArray(quizData);
                        currentQuiz = 0;
                        score = 0;
                        userAnswers = [];
                    }
                } else if (shouldResume) {
                    // console.log('URL 파라미터로 진행상태 자동 복원');
                }
            } else {
                // 저장된 진행상태가 없으면 새로 시작
                shuffledQuizData = isRandomMode ? shuffleArray(quizData) : createSequentialArray(quizData);
                currentQuiz = 0;
                score = 0;
                userAnswers = [];
            }
            
            questionAnswered = false;
            // Clear any previous results
            const resultDiv = document.getElementById('result');
            if(resultDiv) resultDiv.innerHTML = '';
            loadQuiz();
        } catch (error) {
            console.error('Quiz initialization error:', error);
            showError('퀴즈 초기화 중 오류가 발생했습니다.');
        }
    }

    function loadQuiz() {
        try {
            if (!shuffledQuizData || currentQuiz >= shuffledQuizData.length || currentQuiz < 0) {
                throw new Error(`Invalid quiz state: currentQuiz=${currentQuiz}, length=${shuffledQuizData?.length}`);
            }

            deselectAnswers();
            hideFeedback();
            questionAnswered = false;
            const currentQuizData = shuffledQuizData[currentQuiz];

            if (!currentQuizData || !currentQuizData.question) {
                throw new Error(`Invalid question data at index ${currentQuiz}`);
            }

            question.innerHTML = `${currentQuiz + 1}. ${currentQuizData.question}`;
            aText.innerText = currentQuizData.a || '';
            bText.innerText = currentQuizData.b || '';
            cText.innerText = currentQuizData.c || '';
            dText.innerText = currentQuizData.d || '';
            questionCounter.innerText = `${currentQuiz + 1} / ${shuffledQuizData.length}`;

            // 참조 버튼 추가 (질문 로드시에는 불필요 - 해설에서만 표시)

            resetOptionStyles();
            if (userAnswers[currentQuiz]) {
                const letterToId = {'a': '1', 'b': '2', 'c': '3', 'd': '4'};
                const elementId = letterToId[userAnswers[currentQuiz]];
                const answerElement = document.getElementById(elementId);
                if (answerElement) {
                    answerElement.checked = true;
                    showFeedback(userAnswers[currentQuiz]);
                }
            }

            prevBtn.disabled = currentQuiz === 0;
            nextBtn.style.display = 'inline-block';
            submitBtn.style.display = currentQuiz === shuffledQuizData.length - 1 ? 'inline-block' : 'none';
            updateNextButtonState();
            updateProgressBadge();
        } catch (error) {
            console.error('Load quiz error:', error);
            showError('문제를 불러오는 중 오류가 발생했습니다.');
        }
    }

    function getSelected() {
        let answer;
        document.querySelectorAll('.answer').forEach(answerEl => {
            if (answerEl.checked) {
                const idToLetter = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'};
                answer = idToLetter[answerEl.id];
            }
        });
        return answer;
    }

    function showFeedback(selectedAnswer) {
        const currentQuizData = shuffledQuizData[currentQuiz];
        const correctAnswer = currentQuizData.correct;
        const isCorrect = selectedAnswer === correctAnswer;

        hideFeedback();
        resetOptionStyles();

        document.querySelectorAll('ul li label').forEach((label, index) => {
            const optionLetter = ['a', 'b', 'c', 'd'][index];
            const li = label.parentElement;
            if (optionLetter === selectedAnswer) {
                li.classList.add(isCorrect ? 'selected-correct' : 'selected-incorrect');
            } else if (optionLetter === correctAnswer) {
                li.classList.add('correct-answer');
            }
        });

        const feedbackDiv = document.createElement('div');
        feedbackDiv.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
        
        // 참조 버튼 HTML 생성
        let referenceButtonsHtml = '';
        if (currentQuizData.urls && currentQuizData.urls.length > 0) {
            const buttons = currentQuizData.urls.map((url, index) => {
                // URL에서 조문 추출
                const articleMatch = url.match(/제(\d+(?:조의?\d*)?(?:조)?)/);
                const chapterMatch = url.match(/제(\d+장)/);
                let buttonText = '';
                
                if (articleMatch) {
                    buttonText = articleMatch[1].includes('조') ? articleMatch[1] : `${articleMatch[1]}조`;
                } else if (chapterMatch) {
                    buttonText = chapterMatch[1];
                } else {
                    buttonText = `참조${index + 1}`;
                }
                
                return `<button class="reference-btn" onclick="openLawModal('${url}', '${buttonText}')">📖 ${buttonText}</button>`;
            }).join('');
            
            referenceButtonsHtml = `<div class="reference-buttons" style="margin-top: 10px;">${buttons}</div>`;
        }
        
        feedbackDiv.innerHTML = `
            <div class="feedback-content">
                <span class="feedback-icon">${isCorrect ? '✓' : '✗'}</span>
                <span class="feedback-text">${isCorrect ? '정답입니다!' : `오답입니다. 정답: ${correctAnswer.toUpperCase()}`}</span>
            </div>
            <div class="explanation-content">
                <p><strong>해설:</strong> ${currentQuizData.explanation || '해설이 없습니다.'}</p>
                ${referenceButtonsHtml}
            </div>
        `;
        question.parentNode.insertBefore(feedbackDiv, question.nextSibling);
        questionAnswered = true;
    }
    
    function hideFeedback() {
        const existingFeedback = document.querySelector('.feedback');
        if (existingFeedback) existingFeedback.remove();
    }

    function resetOptionStyles() {
        document.querySelectorAll('ul li').forEach(li => {
            li.classList.remove('selected-correct', 'selected-incorrect', 'correct-answer');
        });
    }

    function updateNextButtonState() {
        nextBtn.disabled = !questionAnswered;
        nextBtn.textContent = currentQuiz === shuffledQuizData.length - 1 ? '결과 보기' : '다음';
    }
    
    function updateProgressBadge() {
        if (!progressBadge) return;
        
        let correctCount = userAnswers.filter((answer, index) => answer && answer === shuffledQuizData[index]?.correct).length;
        let answeredCount = userAnswers.filter(Boolean).length;
        let totalQuestions = shuffledQuizData.length;
        const percentage = answeredCount > 0 ? Math.round((correctCount / answeredCount) * 100) : 0;
        
        progressBadge.textContent = `${answeredCount}/${totalQuestions} 진행 | ${correctCount}/${answeredCount} 정답 (${percentage}%)`;
    }

    function showResults() {
        // 퀴즈 완료 시 진행상태 삭제
        clearProgress();
        
        calculateScore();
        let detailedHTML = '';
        shuffledQuizData.forEach((questionData, i) => {
            const userAnswer = userAnswers[i];
            const isCorrect = userAnswer === questionData.correct;
            const options = { a: questionData.a, b: questionData.b, c: questionData.c, d: questionData.d };
            detailedHTML += `
                <div class="question-result ${isCorrect ? 'correct' : 'incorrect'}">
                    <p><strong>문제 ${i + 1} (원래 ${questionData.originalIndex}번):</strong> ${isCorrect ? '정답' : '오답'}</p>
                    <p><strong>정답:</strong> ${questionData.correct.toUpperCase()}. ${options[questionData.correct]}</p>
                    ${userAnswer ? `<p><strong>선택한 답:</strong> ${userAnswer.toUpperCase()}. ${options[userAnswer]}</p>` : '<p><strong>선택한 답:</strong> 미선택</p>'}
                    <p><strong>해설:</strong> ${questionData.explanation || '해설이 없습니다.'}</p>
                </div>
            `;
        });

        quiz.innerHTML = `
            <div class="result">
                <h2>시험 결과</h2>
                <p>총 ${shuffledQuizData.length}문제 중 ${score}문제 정답</p>
                <p>정답률: ${(score / shuffledQuizData.length * 100).toFixed(1)}%</p>
                <div class="detailed-results"><h3>상세 결과</h3>${detailedHTML}</div>
                <button onclick="location.reload()">다시 풀기</button>
                <button onclick="location.href='index.html'">메인으로</button>
            </div>
        `;
    }

    function calculateScore() {
        score = userAnswers.reduce((acc, answer, i) => acc + (answer === shuffledQuizData[i].correct ? 1 : 0), 0);
    }

    function deselectAnswers() {
        document.querySelectorAll('.answer').forEach(answerEl => answerEl.checked = false);
    }

    // --- Event Handlers ---
    function handleAnswerChange(e) {
        if (e.target.classList.contains('answer') && !questionAnswered) {
            const selectedAnswer = getSelected();
            if (selectedAnswer) {
                userAnswers[currentQuiz] = selectedAnswer;
                showFeedback(selectedAnswer);
                updateNextButtonState();
                updateProgressBadge();
                
                // 진행상태 저장
                saveProgress();
            }
        }
    }

    function handlePrevClick() {
        if (currentQuiz > 0) {
            currentQuiz--;
            loadQuiz();
            
            // 진행상태 저장
            saveProgress();
        }
    }

    function handleNextClick() {
        if (questionAnswered) {
            if (currentQuiz < shuffledQuizData.length - 1) {
                currentQuiz++;
                loadQuiz();
                
                // 진행상태 저장
                saveProgress();
            } else {
                showResults();
            }
        } else {
            alert('답안을 선택해주세요.');
        }
    }

    function handleSubmitClick() {
        if (questionAnswered) {
            showResults();
        } else {
            alert('답안을 선택해주세요.');
        }
    }

    // --- Event Listener Management ---
    function removeAllEventListeners() {
        answerList.removeEventListener('change', handleAnswerChange);
        prevBtn.removeEventListener('click', handlePrevClick);
        nextBtn.removeEventListener('click', handleNextClick);
        submitBtn.removeEventListener('click', handleSubmitClick);
    }

    function addAllEventListeners() {
        answerList.addEventListener('change', handleAnswerChange);
        prevBtn.addEventListener('click', handlePrevClick);
        nextBtn.addEventListener('click', handleNextClick);
        submitBtn.addEventListener('click', handleSubmitClick);
    }

    // --- Initialization ---
    removeAllEventListeners(); // Clean up listeners from any previous initializations
    addAllEventListeners();
    initializeQuiz();
}

// 전역 에러 핸들러 (퀴즈 실행 중 발생하는 예상치 못한 오류 처리)
window.addEventListener('error', (event) => {
    console.error('=== 전역 JavaScript 오류 ===');
    console.error('오류 객체:', event.error);
    console.error('메시지:', event.message);
    console.error('파일명:', event.filename);
    console.error('라인:', event.lineno);
    console.error('컬럼:', event.colno);
    console.error('스택 트레이스:', event.error?.stack);
    console.error('=========================');
    
    const errorMessage = `예상치 못한 오류가 발생했습니다: ${event.error?.message || event.message || '알 수 없는 오류'}`;
    
    // 이미 에러 메시지가 표시되어 있지 않다면 표시
    if (!document.querySelector('.error-message')) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: #fee;
            border: 1px solid #fcc;
            color: #c00;
            padding: 15px;
            border-radius: 5px;
            z-index: 10000;
            max-width: 90%;
            text-align: center;
        `;
        errorDiv.innerHTML = `
            <p>${errorMessage}</p>
            <p style="font-size: 12px; margin-top: 5px;">파일: ${event.filename || '알 수 없음'}, 라인: ${event.lineno || '알 수 없음'}</p>
            <button onclick="this.parentElement.remove()" style="margin-top: 10px; margin-right: 10px; padding: 5px 10px;">닫기</button>
            <button onclick="location.reload()" style="margin-top: 10px; padding: 5px 10px; background: #007cba; color: white; border: none; border-radius: 3px;">새로고침</button>
        `;
        document.body.appendChild(errorDiv);
    }
});

// LocalStorage 오류 처리
window.addEventListener('storage', (event) => {
    if (event.storageArea === localStorage) {
        console.log('LocalStorage changed:', event.key);
        // 필요시 상태 동기화 로직 추가
    }
});

// 전역 모달 관련 함수들
function openLawModal(url, title) {
    // 모달이 이미 존재하는지 확인
    let modal = document.getElementById('law-modal');
    if (!modal) {
        modal = createLawModal();
        document.body.appendChild(modal);
    }

    // 배경 스크롤 방지
    document.body.style.overflow = 'hidden';

    // 모달 내용 업데이트
    const modalTitle = modal.querySelector('.law-modal-title');
    const modalBody = modal.querySelector('.law-modal-body');
    
    modalTitle.textContent = `법령 참조: ${title}`;
    modalBody.innerHTML = '<div class="law-loading">법령 내용을 불러오는 중...</div>';
    
    // 모달 표시
    modal.classList.add('active');
    
    // iframe 로드 (안정화)
    setTimeout(() => {
        console.log('법령 URL 로딩 시작:', url);
        modalBody.innerHTML = `<iframe class="law-iframe" 
                                     src="${url}" 
                                     title="법령 참조" 
                                     frameborder="0"
                                     scrolling="auto"
                                     loading="eager"></iframe>`;
        
        // iframe 로드 완료 후 스크롤 강제 활성화
        const iframe = modalBody.querySelector('.law-iframe');
        if (iframe) {
            console.log('iframe 생성됨, URL:', url);
            
            // 즉시 기본 스타일만 설정
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.minWidth = '1200px'; // 기본 최소 너비 설정
            iframe.style.border = 'none';
            
            // 로드 완료 이벤트
            iframe.onload = function() {
                console.log('iframe 로딩 완료');
                // 로딩 완료 후 간단한 확인만
                setTimeout(() => {
                    console.log('iframe 콘텐츠 로드 확인 완료');
                }, 500);
            };
            
            // 에러 이벤트
            iframe.onerror = function(e) {
                console.error('iframe 로딩 실패:', e);
                modalBody.innerHTML = '<div class="law-loading">법령 내용을 불러올 수 없습니다. 네트워크를 확인해주세요.</div>';
            };
        }
    }, 500);
}

function createLawModal() {
    const modal = document.createElement('div');
    modal.id = 'law-modal';
    modal.className = 'law-modal';
    
    modal.innerHTML = `
        <div class="law-modal-content">
            <div class="law-modal-header">
                <h3 class="law-modal-title">법령 참조</h3>
                <div class="law-modal-controls">
                    <button class="zoom-btn" onclick="zoomLawFrame(-0.1)" title="축소">🔍−</button>
                    <button class="zoom-btn" onclick="resetZoomLawFrame()" title="원본크기">🔄</button>
                    <button class="zoom-btn" onclick="zoomLawFrame(0.1)" title="확대">🔍+</button>
                    <button class="law-modal-close" onclick="closeLawModal()" title="닫기">×</button>
                </div>
            </div>
            <div class="law-modal-body">
                <div class="law-loading">법령 내용을 불러오는 중...</div>
            </div>
        </div>
    `;
    
    // 모달 배경 클릭 시 닫기 (터치 친화적)
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeLawModal();
        }
    });
    
    // 터치 이벤트 처리 (모바일 최적화)
    modal.addEventListener('touchstart', (e) => {
        if (e.target === modal) {
            e.preventDefault();
        }
    });
    
    modal.addEventListener('touchend', (e) => {
        if (e.target === modal) {
            e.preventDefault();
            closeLawModal();
        }
    });
    
    return modal;
}

function closeLawModal() {
    const modal = document.getElementById('law-modal');
    if (modal) {
        modal.classList.remove('active');
        // 줌 레벨 초기화
        currentZoomLevel = 1.0;
        // 배경 스크롤 복원
        document.body.style.overflow = '';
    }
}

// 줌 기능을 위한 전역 변수
let currentZoomLevel = 1.0;

function zoomLawFrame(delta) {
    const iframe = document.querySelector('.law-iframe');
    if (iframe) {
        currentZoomLevel = Math.max(0.5, Math.min(3.0, currentZoomLevel + delta));
        iframe.style.transform = `scale(${currentZoomLevel})`;
        iframe.style.transformOrigin = '0 0';
        
        console.log(`줌 레벨: ${currentZoomLevel}`);
    }
}

function resetZoomLawFrame() {
    const iframe = document.querySelector('.law-iframe');
    if (iframe) {
        currentZoomLevel = 1.0;
        iframe.style.transform = 'scale(1)';
        iframe.style.transformOrigin = '0 0';
        
        console.log('줌 리셋: 기본 크기로 복원');
    }
}

// ESC 키로 모달 닫기
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeLawModal();
    }
});

// 모바일 스와이프 제스처로 모달 닫기 (위에서 아래로 스와이프)
let startY = 0;
let startX = 0;

document.addEventListener('touchstart', (e) => {
    const modal = document.getElementById('law-modal');
    if (modal && modal.classList.contains('active')) {
        startY = e.touches[0].clientY;
        startX = e.touches[0].clientX;
    }
});

document.addEventListener('touchmove', (e) => {
    const modal = document.getElementById('law-modal');
    if (modal && modal.classList.contains('active')) {
        const currentY = e.touches[0].clientY;
        const currentX = e.touches[0].clientX;
        const diffY = currentY - startY;
        const diffX = currentX - startX;
        
        // 위에서 아래로 스와이프하고, 수직 이동이 수평 이동보다 클 때
        if (diffY > 100 && Math.abs(diffY) > Math.abs(diffX)) {
            // 모달 헤더 영역에서 시작한 스와이프만 처리
            const modalHeader = modal.querySelector('.law-modal-header');
            const headerRect = modalHeader.getBoundingClientRect();
            if (startY >= headerRect.top && startY <= headerRect.bottom) {
                closeLawModal();
            }
        }
    }
});

// For backward compatibility with older exam pages that define a global `quizData`
document.addEventListener('DOMContentLoaded', () => {
    try {
        if (typeof quizData !== 'undefined' && typeof startQuizEngine === 'function') {
            const is2025Exam = window.location.pathname.includes('2025-exam.html');
            if (!is2025Exam && quizData.length > 0) {
                startQuizEngine(quizData);
            }
        }
    } catch (error) {
        console.error('Quiz initialization error:', error);
    }
});