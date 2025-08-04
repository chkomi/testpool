// 메인 페이지 기능
document.addEventListener('DOMContentLoaded', function() {
    // 페이지 로드 애니메이션
    const examButtons = document.querySelectorAll('.exam-btn');
    
    examButtons.forEach((button, index) => {
        setTimeout(() => {
            button.style.opacity = '0';
            button.style.transform = 'translateY(20px)';
            button.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                button.style.opacity = '1';
                button.style.transform = 'translateY(0)';
            }, 100);
        }, index * 150);
    });

    // 로컬 스토리지에서 진행 상황 확인하여 표시
    updateProgressIndicators();
    
    // 랜덤 모드 토글 초기화
    initializeRandomModeToggle();
    
    // 스크롤 애니메이션 초기화
    initializeScrollAnimations();
    
});

// 랜덤 모드 토글 기능 초기화
function initializeRandomModeToggle() {
    const randomModeToggle = document.getElementById('randomModeHome');
    const modeStatusText = document.getElementById('modeStatusText');
    
    if (randomModeToggle && modeStatusText) {
        // 저장된 설정 불러오기 (기본값: true - 랜덤 모드)
        const isRandomMode = localStorage.getItem('quizRandomMode') !== 'false';
        randomModeToggle.checked = isRandomMode;
        
        // 초기 상태 텍스트 설정
        updateModeStatusText(isRandomMode);
        
        // 토글 이벤트 리스너
        randomModeToggle.addEventListener('change', function() {
            const newRandomMode = this.checked;
            localStorage.setItem('quizRandomMode', newRandomMode.toString());
            
            // 상태 텍스트 업데이트
            updateModeStatusText(newRandomMode);
            
            // 사용자에게 변경 안내
            const modeText = newRandomMode ? '랜덤 모드' : '일반 모드';
            console.log(`문제 출제 방식이 ${modeText}로 변경되었습니다.`);
        });
    }
}

// 모드 상태 텍스트 업데이트 함수
function updateModeStatusText(isRandomMode) {
    const modeStatusText = document.getElementById('modeStatusText');
    if (modeStatusText) {
        modeStatusText.textContent = isRandomMode ? '랜덤모드' : '일반모드';
    }
}

// 각 시험별 진행 상황을 버튼에 표시
function updateProgressIndicators() {
    const years = ['2021', '2022', '2023', '2024'];
    
    years.forEach(year => {
        const progressKey = `exam_${year}_progress`;
        const progress = localStorage.getItem(progressKey);
        const button = document.querySelector(`button[onclick="startExam('${year}')"]`);
        
        if (progress && button) {
            const progressData = JSON.parse(progress);
            const totalQuestions = progressData.total || 0;
            const answeredQuestions = progressData.answered || 0;
            const correctAnswers = progressData.correct || 0;
            
            if (answeredQuestions > 0) {
                const percentage = Math.round((correctAnswers / answeredQuestions) * 100);
                
                // 기존 진행 상황 제거
                const existingProgress = button.querySelector('.progress-indicator');
                if (existingProgress) {
                    existingProgress.remove();
                }
                
                // 진행 상황 표시 요소 추가
                const progressSpan = document.createElement('span');
                progressSpan.className = 'progress-indicator';
                progressSpan.innerHTML = `<br><small>진행률: ${answeredQuestions}/${totalQuestions} (${percentage}%)</small>`;
                button.appendChild(progressSpan);
            }
        }
    });
}

// 사전공개문제 페이지로 이동
function startPreviewExam() {
    location.href = 'preview-exam.html';
}

// 시험 시작 전 확인 및 이어하기 옵션
function startExam(year) {
    const progressKey = `exam_${year}_progress`;
    const progress = localStorage.getItem(progressKey);
    
    if (progress) {
        const progressData = JSON.parse(progress);
        if (progressData.answered > 0) {
            const resumeChoice = confirm(`${year}년 시험에 진행 중인 내용이 있습니다.\n\n이어서 풀기: 확인\n처음부터 시작: 취소`);
            
            if (resumeChoice) {
                // 이어하기
                location.href = `${year}-exam.html?resume=true`;
            } else {
                // 처음부터 시작 - 진행 상황 삭제
                localStorage.removeItem(progressKey);
                location.href = `${year}-exam.html`;
            }
            return;
        }
    }
    
    // 첫 시작
    location.href = `${year}-exam.html`;
}

// 스크롤 애니메이션 초기화
function initializeScrollAnimations() {
    // 애니메이션할 요소들에 클래스 추가
    const elementsToAnimate = document.querySelectorAll('.exam-selection, .mode-setting, .exam-btn');
    elementsToAnimate.forEach(element => {
        element.classList.add('animate-on-scroll');
    });
    
    // Intersection Observer 설정
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // 요소들을 관찰 시작
    elementsToAnimate.forEach(element => {
        observer.observe(element);
    });
    
    // 페이지 로드 시 즉시 보이는 요소들은 바로 애니메이션 적용
    setTimeout(() => {
        const visibleElements = document.querySelectorAll('.animate-on-scroll');
        visibleElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                element.classList.add('visible');
            }
        });
    }, 100);
}

