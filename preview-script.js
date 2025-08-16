// 사전공개문제 페이지 기능
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
    updatePreviewProgressIndicators();
});

// 각 사전공개문제별 진행 상황을 버튼에 표시 (사용자별)
function updatePreviewProgressIndicators() {
    if (!userManager.currentUser) return;
    
    for (let i = 1; i <= 8; i++) {
        const progressKey = userManager.getUserProgressKey(`preview_${i}`);
        const progress = localStorage.getItem(progressKey);
        const button = document.querySelector(`button[onclick="startPreviewQuestion(${i})"]`);
        
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
    }
}

// 사전공개문제 시작 전 확인 및 이어하기 옵션 (사용자별)
function startPreviewQuestion(questionNumber) {
    if (!userManager.currentUser) {
        alert('사용자를 먼저 선택해주세요.');
        return;
    }
    
    const progressKey = userManager.getUserProgressKey(`preview_${questionNumber}`);
    const progress = localStorage.getItem(progressKey);
    
    if (progress) {
        const progressData = JSON.parse(progress);
        if (progressData.answered > 0) {
            const resumeChoice = confirm(`사전공개문제 ${questionNumber}번에 진행 중인 내용이 있습니다.\\n\\n이어서 풀기: 확인\\n처음부터 시작: 취소`);
            
            if (resumeChoice) {
                // 이어하기
                location.href = `preview-${questionNumber}-exam.html?resume=true`;
            } else {
                // 처음부터 시작 - 진행 상황 삭제
                localStorage.removeItem(progressKey);
                location.href = `preview-${questionNumber}-exam.html`;
            }
            return;
        }
    }
    
    // 첫 시작
    location.href = `preview-${questionNumber}-exam.html`;
}