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
    
    // 관리자 버튼 추가
    addAdminButton();
});

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

// 관리자 버튼 추가
function addAdminButton() {
    const examSelection = document.querySelector('.exam-selection');
    const adminBtn = document.createElement('button');
    adminBtn.textContent = '📊 관리자 현황';
    adminBtn.className = 'exam-btn admin-btn';
    adminBtn.style.marginTop = '1rem';
    adminBtn.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';
    adminBtn.onclick = showAdminDashboard;
    
    examSelection.appendChild(adminBtn);
}

// 관리자 대시보드 표시
function showAdminDashboard() {
    const results = userManager.getAllResults();
    const users = userManager.getAllUsers();
    
    // 통계 계산
    const totalUsers = users.length;
    const totalExams = results.length;
    const avgScore = results.length > 0 ? 
        Math.round(results.reduce((sum, r) => sum + ((r.score / r.total) * 100), 0) / results.length) : 0;
    
    // 연도별 통계
    const yearStats = {};
    ['2021', '2022', '2023', '2024'].forEach(year => {
        const yearResults = results.filter(r => r.shuffledQuizData?.[0]?.originalIndex && 
            window.location.pathname.includes(year));
        yearStats[year] = yearResults.length;
    });
    
    // 대시보드 HTML 생성
    const dashboardHTML = `
        <div class="admin-dashboard">
            <h2>📊 관리자 대시보드</h2>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">${totalUsers}</div>
                    <div class="stat-label">총 사용자 수</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${totalExams}</div>
                    <div class="stat-label">완료된 시험 수</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${avgScore}%</div>
                    <div class="stat-label">평균 점수</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${results.filter(r => Date.now() - r.completedAt < 86400000).length}</div>
                    <div class="stat-label">오늘 완료</div>
                </div>
            </div>
            
            <div class="results-section">
                <h3>최근 결과</h3>
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>사용자</th>
                            <th>부서</th>
                            <th>시험년도</th>
                            <th>점수</th>
                            <th>완료일시</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${results.slice(-10).reverse().map(result => `
                            <tr>
                                <td>${result.user.name}</td>
                                <td>${result.user.department}</td>
                                <td>2024년</td>
                                <td>${Math.round((result.score / result.total) * 100)}% (${result.score}/${result.total})</td>
                                <td>${new Date(result.completedAt).toLocaleString('ko-KR')}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            
            <div style="margin-top: 2rem; text-align: center;">
                <button onclick="exportResults()" style="margin-right: 1rem;">📄 결과 내보내기</button>
                <button onclick="closeAdminDashboard()">닫기</button>
            </div>
        </div>
    `;
    
    // 대시보드 표시
    const dashboardDiv = document.createElement('div');
    dashboardDiv.id = 'admin-dashboard-overlay';
    dashboardDiv.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        z-index: 1000;
        overflow-y: auto;
        padding: 2rem;
    `;
    dashboardDiv.innerHTML = dashboardHTML;
    document.body.appendChild(dashboardDiv);
}

// 관리자 대시보드 닫기
function closeAdminDashboard() {
    const dashboard = document.getElementById('admin-dashboard-overlay');
    if (dashboard) {
        document.body.removeChild(dashboard);
    }
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