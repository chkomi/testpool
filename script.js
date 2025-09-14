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

    // 테스트용 진행상태 데이터 생성을 비활성화 (실제 진행률만 표시)
    // createTestProgressData();
    
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
        // 저장된 설정 불러오기 (기본값: false - 일반 모드)
        const isRandomMode = localStorage.getItem('quizRandomMode') === 'true';
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
            // console.log(`문제 출제 방식이 ${modeText}로 변경되었습니다.`);
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
            try {
                const progressData = JSON.parse(progress);
                const totalQuestions = progressData.total || 0;
                const answeredQuestions = progressData.answered || 0;
                const correctAnswers = progressData.correct || 0;
                
                if (answeredQuestions > 0 && totalQuestions > 0) {
                    const percentage = Math.round((correctAnswers / answeredQuestions) * 100);
                    
                    // 기존 진행 상황 표시 제거 (텍스트/뱃지 모두)
                    const existingProgressText = button.querySelector('.progress-indicator');
                    if (existingProgressText) existingProgressText.remove();
                    const existingBadge = button.querySelector('.completion-badge');
                    if (existingBadge) existingBadge.remove();

                    // 진행률 뱃지로 표시
                    const badge = document.createElement('span');
                    badge.className = 'completion-badge';
                    badge.textContent = `${answeredQuestions}/${totalQuestions} (${percentage}%)`;
                    button.appendChild(badge);
                } else {
                    // 데이터가 있지만 answeredQuestions가 0인 경우 표시 제거
                    const existingProgressText = button.querySelector('.progress-indicator');
                    if (existingProgressText) existingProgressText.remove();
                    const existingBadge = button.querySelector('.completion-badge');
                    if (existingBadge) existingBadge.remove();
                }
            } catch (error) {
                console.warn(`${year}년 진행률 데이터 파싱 오류:`, error);
                // 잘못된 데이터가 있는 경우 제거
                localStorage.removeItem(progressKey);
            }
        } else {
            // 진행 상황 데이터가 없는 경우 기존 진행률 표시 제거
            if (button) {
                const existingProgressText = button.querySelector('.progress-indicator');
                if (existingProgressText) existingProgressText.remove();
                const existingBadge = button.querySelector('.completion-badge');
                if (existingBadge) existingBadge.remove();
            }
        }
    });

    // 2025년 문제 총 개수 표시
    update2025QuestionCount();
}

// 2025년 총 문제수 표시 함수
function update2025QuestionCount() {
    const button2025 = document.getElementById('exam-btn-2025');
    if (button2025) {
        // 2025-exam.js에서 문제수 정보를 가져오기 위해 fetch 사용
        fetch('2025-exam.js')
            .then(response => response.text())
            .then(scriptContent => {
                // examQuestions 객체에서 총 문제수 계산
                const matches = scriptContent.match(/examQuestions\s*=\s*\{[\s\S]*?\};/);
                if (matches) {
                    try {
                        // 임시로 함수 생성해서 문제수 계산
                        const tempFunc = new Function(`
                            ${matches[0]}
                            let total = 0;
                            for (const subject in examQuestions) {
                                if (examQuestions[subject] && Array.isArray(examQuestions[subject])) {
                                    total += examQuestions[subject].length;
                                }
                            }
                            return total;
                        `);
                        
                        const totalQuestions = tempFunc();
                        
                        // 기존 문제수 표시 제거
                        const existingCount = button2025.querySelector('.question-count-2025');
                        if (existingCount) {
                            existingCount.remove();
                        }
                        
                        // 2025년 과목별 진행률 확인
                        const subjects = ['농어촌정비법', '공운법', '공사법', '직제규정', '취업규칙', '인사규정', '행동강령', '회계기준'];
                        let totalAnswered = 0;
                        let totalCorrect = 0;
                        let hasProgress = false;

                        subjects.forEach(subject => {
                            const progressKey = `exam_2025_${subject}_progress`;
                            const savedProgress = localStorage.getItem(progressKey);
                            if (savedProgress) {
                                try {
                                    const progressData = JSON.parse(savedProgress);
                                    if (progressData.answered > 0) {
                                        totalAnswered += progressData.answered;
                                        totalCorrect += progressData.correct || 0;
                                        hasProgress = true;
                                    }
                                } catch (error) {
                                    console.warn(`2025년 ${subject} 진행률 로드 오류:`, error);
                                }
                            }
                        });

                        // 새로운 문제수 및 진행률 표시 추가
                        const countSpan = document.createElement('span');
                        countSpan.className = 'question-count-2025 progress-indicator';
                        
                        let displayText = `<br><small>총 ${totalQuestions}문제 (8과목)</small>`;
                        
                        if (hasProgress && totalAnswered > 0) {
                            const percentage = Math.round((totalCorrect / totalAnswered) * 100);
                            displayText += `<br><small>전체 진행률: ${totalAnswered}/${totalQuestions} (${percentage}%)</small>`;
                        }
                        
                        countSpan.innerHTML = displayText;
                        button2025.appendChild(countSpan);
                        
                        // console.log(`2025년 총 문제수: ${totalQuestions}문제${hasProgress ? `, 진행률: ${totalAnswered}/${totalQuestions}` : ''}`);
                    } catch (error) {
                        console.error('2025년 문제수 계산 중 오류:', error);
                    }
                }
            })
            .catch(error => {
                console.error('2025년 문제 파일 로드 오류:', error);
            });
    }
}

// 사전공개문제 페이지로 이동
function startPreviewExam() {
    location.href = 'preview-exam.html';
}

// 컴팩트 확인 모달 함수
function showCompactConfirm(title, message, confirmText = '확인', cancelText = '취소') {
    return new Promise((resolve) => {
        // 기존 모달이 있다면 제거
        const existingModal = document.querySelector('.compact-confirm-overlay');
        if (existingModal) {
            existingModal.remove();
        }

        // 모달 HTML 생성
        const modalHTML = `
            <div class="compact-confirm-overlay">
                <div class="compact-confirm-modal">
                    <div class="compact-confirm-title">${title}</div>
                    <div class="compact-confirm-message">${message}</div>
                    <div class="compact-confirm-buttons">
                        <button class="compact-confirm-btn primary" data-action="confirm">${confirmText}</button>
                        <button class="compact-confirm-btn secondary" data-action="cancel">${cancelText}</button>
                    </div>
                </div>
            </div>
        `;

        // 모달을 body에 추가
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const overlay = document.querySelector('.compact-confirm-overlay');

        // 애니메이션을 위해 약간의 지연 후 active 클래스 추가
        setTimeout(() => {
            overlay.classList.add('active');
        }, 10);

        // 버튼 이벤트 리스너
        overlay.addEventListener('click', (e) => {
            if (e.target.closest('[data-action="confirm"]')) {
                closeModal(true);
            } else if (e.target.closest('[data-action="cancel"]') || e.target === overlay) {
                closeModal(false);
            }
        });

        // 모달 닫기 함수
        function closeModal(result) {
            overlay.classList.remove('active');
            setTimeout(() => {
                overlay.remove();
                resolve(result);
            }, 300);
        }

        // ESC 키로 닫기
        function handleKeyDown(e) {
            if (e.key === 'Escape') {
                document.removeEventListener('keydown', handleKeyDown);
                closeModal(false);
            }
        }
        document.addEventListener('keydown', handleKeyDown);
    });
}

// 시험 시작 전 확인 및 이어하기 옵션
async function startExam(year) {
    const progressKey = `exam_${year}_progress`;
    const progress = localStorage.getItem(progressKey);
    
    if (progress) {
        const progressData = JSON.parse(progress);
        if (progressData.answered > 0) {
            const resumeChoice = await showCompactConfirm(
                `${year}년 시험 진행 중`,
                '진행 중인 내용이 있습니다.',
                '이어서 풀기',
                '처음부터'
            );
            
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
