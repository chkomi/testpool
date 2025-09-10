# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**⚠️ CRITICAL: Read AGENTS.md first - it contains the latest project guidelines and is the primary contributor guide.**

## Repository Overview

Web-based quiz application for Korean Agricultural and Rural Infrastructure Corporation (한국농어촌공사) 3급 승진 기초역량평가 필리시험 문제풀이. Built with vanilla HTML/CSS/JavaScript for maximum compatibility and ease of deployment.

### Latest Project Structure (2025)
- **Root**: `index.html`, `styles.css`, shared logic `quiz-logic.js`
- **Legacy Years**: `2021-2024` use `YYYY-exam.{html,js}` format
- **2025 Subjects**: Individual `2025-<과목>.{html,js}` files + modular data in `2025/n.과목명.js`
- **Reference Materials**: `2025/근거`, `2025/법령집` (PDFs), `backdata/` (supplementary), `font/`

## Architecture

### Core System Design
- **Multi-user Support**: User management system with progress isolation per user
- **State Management**: LocalStorage-based persistence with user-specific keys
- **Modular Quiz Engine**: Shared quiz logic (`quiz-logic.js`) across all exam years
- **Progress Tracking**: Real-time progress updates with resume capability
- **Admin Dashboard**: Built-in analytics and user management

### Key Architectural Patterns
1. **Shared Logic Pattern**: Core quiz functionality centralized in `quiz-logic.js`
2. **User Isolation**: Progress data separated by user via `UserManager` class
3. **Event-Driven UI**: DOM event delegation for dynamic content handling
4. **State Persistence**: Automatic save/restore of quiz progress and user data

## Project Structure

```
testpool/
├── index.html              # Main landing page with exam selection
├── script.js              # Main page logic and progress indicators
├── user-manager.js         # User management system (multi-user support)
├── quiz-logic.js           # Shared quiz engine (question shuffling, progress, feedback)
├── styles.css              # Global responsive styling
├── {year}-exam.html        # Individual exam pages (2021-2024)
├── {year}-exam.js          # Quiz data for each year
├── backdata/               # Legal document PDFs (laws and regulations)
└── pro_pool/              # Question pool PDFs for reference
```

## Data Structures

### Quiz Data Format
```javascript
const quizData = [
    {
        question: "Question text",
        a: "Option A",
        b: "Option B", 
        c: "Option C",
        d: "Option D",
        correct: "a",           // Answer key
        explanation: "Detailed explanation with legal citations"
    }
];
```

### User Progress Storage
- Key Pattern: `user_{userId}_exam_{year}_progress`
- Contains: shuffled questions, current position, answers, scores
- Automatically cleared on exam completion

## Development Commands

### Local Development (Updated for 2025)
```bash
# Primary method: Local server for 2025 subjects
python3 -m http.server 8000
# Then navigate to: http://localhost:8000/2025-subjects.html

# Direct file opening
open 2025-subjects.html  # macOS
xdg-open 2025-subjects.html  # Linux

# Git synchronization
git pull --ff-only
```

### File Operations
```bash
# View exam completion status
# Check localStorage in browser dev tools for progress data

# Add new questions (2025)
# Edit corresponding 2025/<과목>.js or 2025/n.과목명.js file

# Legacy years (2021-2024)
# Edit corresponding {year}-exam.js file following existing format
```

## Key Components

### UserManager Class (`user-manager.js`)
- Handles multi-user functionality without authentication
- Manages user creation, selection, and data isolation
- Provides admin dashboard with statistics and CSV export
- Methods: `setupUser()`, `getUserProgressKey()`, `getAllResults()`

### Quiz Engine (`quiz-logic.js`)
- Question randomization with original index tracking
- Real-time feedback system with visual indicators
- Progress persistence across browser sessions
- Navigation controls with validation

### Progress System
- User-specific localStorage keys prevent data conflicts
- Automatic save on every answer selection
- Resume capability from exact last position
- Progress indicators on main page showing completion rates

## Testing Strategy

### Manual Testing Checklist
1. **Multi-user Flow**: Create users, switch between them, verify data isolation
2. **Quiz Navigation**: Test previous/next buttons, answer persistence
3. **Progress Persistence**: Close browser, reopen, verify resume functionality  
4. **Feedback System**: Verify immediate feedback, correct answer highlighting
5. **Results Page**: Check detailed results, explanations, score calculations
6. **Admin Dashboard**: Verify statistics, CSV export functionality

### Browser Compatibility
- Vanilla JavaScript ensures broad browser support
- CSS Grid/Flexbox for responsive design
- LocalStorage API widely supported

## 2025 Content Guidelines (CRITICAL)

### **해설 작성 핵심 원칙**
- **정확성**: 근거는 `2025/근거` 및 `2025/법령집` PDF만 사용 (외부 자료 금지)
- **체계성**: 일관된 형식으로 작성
- **완전성**: 정답·오답 근거 모두 제시

### **인용 형식**
- 필수 형식: 「법령명」 제○조제○항
- 예시: 「농어촌정비법」 제15조제1항

### **해설 구조 템플릿**
```
문제 [번호] — 【정답】 n — 【해설】
- 관련 법령: [법령명 제○조제○항]
- 정답 이유: [구체적 설명]
- 오답 분석: ① … ② … ③ … ④ …
```

### **참조 버튼 시스템 (필수)**
- 문제 객체에 `url` (단일) 또는 `urls` (배열) 필드 보존/추가
- `quiz-logic.js`가 이 필드를 읽어 법령 참조 팝업 생성
- 복수 근거 시 `urls` 배열에 모든 조문 추가

### **작업 절차**
1. 대상 파일 선택: `2025-<과목>.js` 또는 `2025/n.과목.js`
2. 정답 확인: `2025/답안.txt` 매칭 검증
3. 근거 확인: 관련 PDF에서 조문 검색·확정
4. 해설 작성: 정답 근거→오답 사유 순으로 기입
5. 검토: 정답 일치, 조문 번호·표기, 모든 선택지 설명, 논리 일관성

### Legacy Content (2021-2024)
- Based on official Korean legal documents in `backdata/`
- Include specific law article citations in explanations

## Code Conventions

### JavaScript Style (Updated Standards)
- **Indentation**: 4 spaces (not tabs)
- **Semicolons**: Required for all statements
- **Naming**: `camelCase` for variables/functions, `kebab-case` for filenames
- **Prefix**: Year prefix for 2025 files (e.g., `2025-haengdong.js`)
- **Frameworks**: Vanilla JavaScript only - NO build tools or frameworks
- **Event delegation**: For dynamic content handling

### Data Management
- User data: `user_` prefix in localStorage
- Progress data: `exam_{year}_progress` pattern
- Results data: `exam_results` with timestamp arrays
- **2025 Structure**: Modular data files in `2025/n.과목명.js` format

## Common Tasks

### Working with 2025 Subjects (Primary)
1. **Adding/Editing Questions**: Edit `2025-<과목>.js` or `2025/n.과목명.js`
2. **Answer Verification**: Check against `2025/답안.txt`
3. **Reference Citations**: Use only PDFs in `2025/근거` and `2025/법령집`
4. **Testing**: Navigate to `2025-subjects.html` → select subject → test functionality

### Testing Checklist (2025)
- Navigate: `2025-subjects.html` → subject selection → question solving
- Verify: No console errors, localStorage progress, reference button popups
- Check: Answer feedback, scoring, navigation controls

### Legacy Years (2021-2024)
1. **Adding New Year**: Create `{year}-exam.html` and `{year}-exam.js`
2. **Adding Questions**: Edit corresponding `{year}-exam.js` file
3. **Testing**: Standard quiz functionality and user progress

### Debugging
1. Check browser localStorage for user data
2. Verify `UserManager` initialization  
3. Check console for JavaScript errors
4. Validate quiz data structure integrity
5. **2025 Specific**: Verify `url`/`urls` fields for reference buttons
