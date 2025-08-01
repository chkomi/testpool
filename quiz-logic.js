
// 문제 순서를 랜덤으로 섞기
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// 문제 순서를 랜덤으로 섞어서 저장
const shuffledQuizData = shuffleArray(quizData.map((q, index) => ({...q, originalIndex: index + 1})));

let currentQuiz = 0;
let score = 0;
let userAnswers = [];
let questionAnswered = false;

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
const result = document.getElementById('result');
const progressBadge = document.getElementById('progress-badge');

loadQuiz();

// 진행률 뱃지 업데이트 함수
function updateProgressBadge() {
    let correctCount = 0;
    let answeredCount = 0;
    
    for (let i = 0; i < shuffledQuizData.length; i++) {
        if (userAnswers[i]) {
            answeredCount++;
            if (userAnswers[i] === shuffledQuizData[i].correct) {
                correctCount++;
            }
        }
    }
    
    const percentage = answeredCount > 0 ? Math.round((correctCount / answeredCount) * 100) : 0;
    progressBadge.textContent = `${correctCount}/${answeredCount} (${percentage}%)`;
}

function loadQuiz() {
    deselectAnswers();
    questionAnswered = false;
    
    const currentQuizData = shuffledQuizData[currentQuiz];
    
    question.innerHTML = `${currentQuiz + 1}. ${currentQuizData.question}`;
    aText.innerText = currentQuizData.a;
    bText.innerText = currentQuizData.b;
    cText.innerText = currentQuizData.c;
    dText.innerText = currentQuizData.d;
    
    questionCounter.innerText = `${currentQuiz + 1} / ${shuffledQuizData.length}`;
    
    // 피드백 메시지 숨기기
    hideFeedback();
    
    // 모든 선택지의 스타일 초기화
    resetOptionStyles();
    
    // 이전에 선택한 답안이 있으면 복원하고 피드백 표시
    if (userAnswers[currentQuiz]) {
        // 알파벳을 ID로 변환 (a->1, b->2, c->3, d->4)
        const letterToId = {'a': '1', 'b': '2', 'c': '3', 'd': '4'};
        const elementId = letterToId[userAnswers[currentQuiz]];
        const selectedAnswer = document.getElementById(elementId);
        if (selectedAnswer) {
            selectedAnswer.checked = true;
            showFeedback(userAnswers[currentQuiz]);
            questionAnswered = true;
        }
    }
    
    // 버튼 상태 업데이트
    prevBtn.disabled = currentQuiz === 0;
    nextBtn.style.display = 'inline-block';
    submitBtn.style.display = currentQuiz === shuffledQuizData.length - 1 ? 'inline-block' : 'none';
    
    // 답변이 완료된 경우 다음 버튼 활성화
    updateNextButtonState();
    
    // 진행률 뱃지 업데이트
    updateProgressBadge();
}

function deselectAnswers() {
    const answerElements = document.querySelectorAll('.answer');
    answerElements.forEach(answerEl => answerEl.checked = false);
}

function getSelected() {
    const answerElements = document.querySelectorAll('.answer');
    let answer;
    answerElements.forEach(answerEl => {
        if (answerEl.checked) {
            // ID를 알파벳으로 변환 (1->a, 2->b, 3->c, 4->d)
            const idToLetter = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'};
            answer = idToLetter[answerEl.id];
        }
    });
    return answer;
}

// 피드백 표시 함수
function showFeedback(selectedAnswer) {
    const currentQuizData = shuffledQuizData[currentQuiz];
    const correctAnswer = currentQuizData.correct;
    const isCorrect = selectedAnswer === correctAnswer;
    
    // 기존 피드백 제거
    hideFeedback();
    
    // 선택지들에 스타일 적용
    const allLabels = document.querySelectorAll('ul li label');
    allLabels.forEach((label, index) => {
        const optionLetter = ['a', 'b', 'c', 'd'][index];
        const li = label.parentElement;
        
        if (optionLetter === selectedAnswer) {
            // 선택한 답안
            if (isCorrect) {
                li.classList.add('selected-correct');
            } else {
                li.classList.add('selected-incorrect');
            }
        } else if (optionLetter === correctAnswer) {
            // 정답 표시
            li.classList.add('correct-answer');
        }
    });
    
    // 피드백 메시지 생성
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
    feedbackDiv.innerHTML = `
        <div class="feedback-content">
            <span class="feedback-icon">${isCorrect ? '✓' : '✗'}</span>
            <span class="feedback-text">
                ${isCorrect ? '정답입니다!' : `오답입니다. 정답: ${correctAnswer.toUpperCase()}`}
            </span>
        </div>
        <div class="explanation-content">
            <p><strong>해설:</strong> ${currentQuizData.explanation || '해설이 없습니다.'}</p>
        </div>
    `;
    
    // 문제 영역 바로 아래에 피드백 추가
    const questionDiv = document.getElementById('question');
    questionDiv.parentNode.insertBefore(feedbackDiv, questionDiv.nextSibling);
    
    questionAnswered = true;
}

// 피드백 숨기기 함수
function hideFeedback() {
    const existingFeedback = document.querySelector('.feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
}

// 선택지 스타일 초기화 함수
function resetOptionStyles() {
    const allLis = document.querySelectorAll('ul li');
    allLis.forEach(li => {
        li.classList.remove('selected-correct', 'selected-incorrect', 'correct-answer');
    });
}

// 다음 버튼 상태 업데이트
function updateNextButtonState() {
    if (questionAnswered) {
        nextBtn.disabled = false;
        nextBtn.textContent = currentQuiz === shuffledQuizData.length - 1 ? '결과 보기' : '다음';
    } else {
        nextBtn.disabled = true;
        nextBtn.textContent = '다음';
    }
}

// 답안 선택 시 즉시 피드백 표시 (이벤트 위임 사용)
document.addEventListener('change', (e) => {
    if (e.target.classList.contains('answer') && !questionAnswered) {
        const selectedAnswer = getSelected();
        if (selectedAnswer) {
            userAnswers[currentQuiz] = selectedAnswer;
            showFeedback(selectedAnswer);
            updateNextButtonState();
            updateProgressBadge();
        }
    }
});

prevBtn.addEventListener('click', () => {
    const answer = getSelected();
    if (answer) {
        userAnswers[currentQuiz] = answer;
    }
    
    if (currentQuiz > 0) {
        currentQuiz--;
        loadQuiz();
    }
});

nextBtn.addEventListener('click', () => {
    if (questionAnswered) {
        if (currentQuiz === shuffledQuizData.length - 1) {
            // 마지막 문제인 경우 결과 표시
            calculateScore();
            showResults();
        } else {
            currentQuiz++;
            loadQuiz();
        }
    } else {
        alert('답안을 선택해주세요.');
    }
});

submitBtn.addEventListener('click', () => {
    if (questionAnswered) {
        calculateScore();
        showResults();
    } else {
        alert('답안을 선택해주세요.');
    }
});

// 점수 계산 함수
function calculateScore() {
    score = 0;
    for (let i = 0; i < shuffledQuizData.length; i++) {
        if (userAnswers[i]) {
            const correctAnswer = shuffledQuizData[i].correct;
            if (userAnswers[i] === correctAnswer) {
                score++;
            }
        }
    }
}

function showResults() {
    quiz.innerHTML = `
        <div class="result">
            <h2>시험 결과</h2>
            <p>총 ${shuffledQuizData.length}문제 중 ${score}문제 정답</p>
            <p>정답률: ${(score / shuffledQuizData.length * 100).toFixed(1)}%</p>
            <div class="detailed-results">
                <h3>상세 결과</h3>
                ${getDetailedResults()}
            </div>
            <button onclick="location.reload()">다시 풀기</button>
            <button onclick="location.href='index.html'">메인으로</button>
        </div>
    `;
}

function getDetailedResults() {
    let detailedHTML = '';
    for (let i = 0; i < shuffledQuizData.length; i++) {
        const userAnswer = userAnswers[i];
        const questionData = shuffledQuizData[i];
        const correctAnswer = questionData.correct;
        const isCorrect = userAnswer === correctAnswer;
        
        const options = {
            'a': questionData.a,
            'b': questionData.b,
            'c': questionData.c,
            'd': questionData.d
        };
        
        detailedHTML += `
            <div class="question-result ${isCorrect ? 'correct' : 'incorrect'}">
                <p><strong>문제 ${i + 1} (원래 ${questionData.originalIndex}번):</strong> ${isCorrect ? '정답' : '오답'}</p>
                <p><strong>정답:</strong> ${correctAnswer.toUpperCase()}. ${options[correctAnswer]}</p>
                ${userAnswer ? `<p><strong>선택한 답:</strong> ${userAnswer.toUpperCase()}. ${options[userAnswer]}</p>` : '<p><strong>선택한 답:</strong> 미선택</p>'}
                <p><strong>해설:</strong> ${questionData.explanation || '해설이 없습니다.'}</p>
            </div>
        `;
    }
    return detailedHTML;
}
