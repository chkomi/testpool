// 사용자 관리 시스템 (로그인 없음)
class UserManager {
    constructor() {
        this.currentUser = null;
        this.initializeUser();
    }

    // 사용자 초기화
    initializeUser() {
        const savedUser = localStorage.getItem('current_user');
        if (savedUser) {
            this.currentUser = JSON.parse(savedUser);
        }
    }

    // 새 사용자 등록 또는 기존 사용자 선택
    async setupUser() {
        return new Promise((resolve) => {
            const modal = this.createUserModal();
            document.body.appendChild(modal);
            
            // 기존 사용자 목록 로드
            this.loadExistingUsers();
            
            resolve();
        });
    }

    // 사용자 선택/생성 모달 생성
    createUserModal() {
        const modal = document.createElement('div');
        modal.className = 'user-modal';
        modal.innerHTML = `
            <div class="user-modal-content">
                <h2>사용자 정보</h2>
                <div class="user-options">
                    <div class="new-user-section">
                        <h3>새 사용자로 시작</h3>
                        <input type="text" id="user-name" placeholder="이름 (예: 홍길동)" required>
                        <input type="text" id="user-dept" placeholder="부서 (예: 총무팀)" required>
                        <button id="create-user-btn">시작하기</button>
                    </div>
                    <div class="existing-user-section">
                        <h3>기존 사용자로 계속</h3>
                        <select id="existing-users">
                            <option value="">사용자 선택...</option>
                        </select>
                        <button id="select-user-btn">선택</button>
                        <button id="clear-users-btn" class="danger-btn">전체 기록 삭제</button>
                    </div>
                </div>
            </div>
        `;

        // 이벤트 리스너 추가
        this.addModalEventListeners(modal);
        
        return modal;
    }

    // 모달 이벤트 리스너
    addModalEventListeners(modal) {
        const createBtn = modal.querySelector('#create-user-btn');
        const selectBtn = modal.querySelector('#select-user-btn');
        const clearBtn = modal.querySelector('#clear-users-btn');

        createBtn.addEventListener('click', () => {
            this.createNewUser(modal);
        });

        selectBtn.addEventListener('click', () => {
            this.selectExistingUser(modal);
        });

        clearBtn.addEventListener('click', () => {
            this.clearAllUsers(modal);
        });
    }

    // 새 사용자 생성
    createNewUser(modal) {
        const name = modal.querySelector('#user-name').value.trim();
        const dept = modal.querySelector('#user-dept').value.trim();

        if (!name || !dept) {
            alert('이름과 부서를 모두 입력해주세요.');
            return;
        }

        const userId = this.generateUserId();
        const user = {
            id: userId,
            name: name,
            department: dept,
            createdAt: Date.now(),
            lastAccess: Date.now()
        };

        this.currentUser = user;
        this.saveUser(user);
        this.closeModal(modal);
    }

    // 기존 사용자 선택
    selectExistingUser(modal) {
        const select = modal.querySelector('#existing-users');
        const userId = select.value;

        if (!userId) {
            alert('사용자를 선택해주세요.');
            return;
        }

        const users = this.getAllUsers();
        const user = users.find(u => u.id === userId);
        
        if (user) {
            user.lastAccess = Date.now();
            this.currentUser = user;
            this.saveUser(user);
            this.closeModal(modal);
        }
    }

    // 사용자 ID 생성 (시간 기반)
    generateUserId() {
        return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // 사용자 저장
    saveUser(user) {
        // 현재 사용자 저장
        localStorage.setItem('current_user', JSON.stringify(user));
        
        // 전체 사용자 목록에 추가
        const users = this.getAllUsers();
        const existingIndex = users.findIndex(u => u.id === user.id);
        
        if (existingIndex >= 0) {
            users[existingIndex] = user;
        } else {
            users.push(user);
        }
        
        localStorage.setItem('all_users', JSON.stringify(users));
    }

    // 모든 사용자 조회
    getAllUsers() {
        const users = localStorage.getItem('all_users');
        return users ? JSON.parse(users) : [];
    }

    // 기존 사용자 목록 로드
    loadExistingUsers() {
        const users = this.getAllUsers();
        const select = document.querySelector('#existing-users');
        
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user.id;
            option.textContent = `${user.name} (${user.department})`;
            select.appendChild(option);
        });
    }

    // 전체 사용자 기록 삭제
    clearAllUsers(modal) {
        if (confirm('모든 사용자의 기록을 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다.')) {
            localStorage.clear();
            alert('모든 기록이 삭제되었습니다.');
            location.reload();
        }
    }

    // 모달 닫기
    closeModal(modal) {
        document.body.removeChild(modal);
        this.updateUserDisplay();
    }

    // 현재 사용자 표시 업데이트
    updateUserDisplay() {
        if (this.currentUser) {
            const userInfo = document.createElement('div');
            userInfo.className = 'current-user-info';
            userInfo.innerHTML = `
                <span>현재 사용자: <strong>${this.currentUser.name}</strong> (${this.currentUser.department})</span>
                <button onclick="userManager.changeUser()">사용자 변경</button>
            `;
            
            // 기존 사용자 정보 제거 후 새로 추가
            const existing = document.querySelector('.current-user-info');
            if (existing) existing.remove();
            
            const header = document.querySelector('.quiz-header');
            if (header) {
                header.insertBefore(userInfo, header.firstChild);
            }
        }
    }

    // 사용자 변경
    changeUser() {
        this.setupUser();
    }

    // 사용자별 진행상황 키 생성
    getUserProgressKey(examYear) {
        return `exam_${examYear}_progress_${this.currentUser.id}`;
    }

    // 사용자별 결과 저장
    saveUserResult(examYear, result) {
        const resultKey = `exam_${examYear}_result_${this.currentUser.id}`;
        const resultData = {
            ...result,
            user: this.currentUser,
            completedAt: Date.now()
        };
        localStorage.setItem(resultKey, JSON.stringify(resultData));
    }

    // 관리자용 전체 결과 조회
    getAllResults() {
        const results = [];
        const users = this.getAllUsers();
        
        users.forEach(user => {
            ['2021', '2022', '2023', '2024'].forEach(year => {
                const resultKey = `exam_${year}_result_${user.id}`;
                const result = localStorage.getItem(resultKey);
                if (result) {
                    results.push(JSON.parse(result));
                }
            });
        });
        
        return results;
    }
}

// 전역 사용자 관리자 인스턴스
const userManager = new UserManager();