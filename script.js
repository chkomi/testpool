// 메인 페이지 기능
document.addEventListener('DOMContentLoaded', async function() {
    // 사용자 설정이 없으면 사용자 선택 모달 표시
    if (!userManager.currentUser) {
        await userManager.setupUser();
    } else {
        userManager.updateUserDisplay();
    }
    
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
    
});

// 랜덤 모드 토글 기능 초기화
function initializeRandomModeToggle() {
    const randomModeToggle = document.getElementById('randomModeHome');
    
    if (randomModeToggle) {
        // 저장된 설정 불러오기 (기본값: true - 랜덤 모드)
        const isRandomMode = localStorage.getItem('quizRandomMode') !== 'false';
        randomModeToggle.checked = isRandomMode;
        
        // 토글 이벤트 리스너
        randomModeToggle.addEventListener('change', function() {
            const newRandomMode = this.checked;
            localStorage.setItem('quizRandomMode', newRandomMode.toString());
            
            // 사용자에게 변경 안내
            const modeText = newRandomMode ? '랜덤 모드' : '일반 모드';
            // alert 대신 더 우아한 알림으로 대체할 수 있음
            console.log(`문제 출제 방식이 ${modeText}로 변경되었습니다.`);
        });
    }
}

// 각 시험별 진행 상황을 버튼에 표시 (사용자별)
function updateProgressIndicators() {
    if (!userManager.currentUser) return;
    
    const years = ['2021', '2022', '2023', '2024'];
    
    years.forEach(year => {
        const progressKey = userManager.getUserProgressKey(year);
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

// 시험 시작 전 확인 및 이어하기 옵션 (사용자별)
function startExam(year) {
    if (!userManager.currentUser) {
        alert('사용자를 먼저 선택해주세요.');
        return;
    }
    
    const progressKey = userManager.getUserProgressKey(year);
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


// 결과 내보내기 (CSV 형식)
function exportResults() {
    const results = userManager.getAllResults();
    
    let csv = '사용자명,부서,시험년도,점수,총문제수,정답률,완료일시\n';
    
    results.forEach(result => {
        const percentage = Math.round((result.score / result.total) * 100);
        const completedDate = new Date(result.completedAt).toLocaleString('ko-KR');
        csv += `${result.user.name},${result.user.department},2024년,${result.score},${result.total},${percentage}%,${completedDate}\n`;
    });
    
    // CSV 파일 다운로드
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `시험결과_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}