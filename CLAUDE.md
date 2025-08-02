# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Web-based quiz application for Korean Agricultural and Rural Infrastructure Corporation (한국농어촌공사) 3급 승진 기초역량평가 필기시험 문제풀이. Built with vanilla HTML/CSS/JavaScript for maximum compatibility and ease of deployment.

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

### Local Development
```bash
# Method 1: Direct file opening
open index.html

# Method 2: Local server (recommended for testing)
python -m http.server 8000
# or
npx serve .
# or  
php -S localhost:8000
```

### File Operations
```bash
# View exam completion status
# Check localStorage in browser dev tools for progress data

# Add new questions
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

## Legal Content Guidelines

### Question Requirements
- Based on official Korean legal documents in `backdata/`
- Include specific law article citations in explanations
- Maintain accuracy with current legal amendments
- Follow consistent Korean legal terminology

### Source Documents
- 농어촌정비법 및 시행령
- 한국농어촌공사 및 농지관리기금법
- 공공기관의 운영에 관한 법률
- 직제규정, 인사규정, 행동강령 등

## Code Conventions

### JavaScript Style
- Use camelCase for variables and functions
- Vanilla JavaScript only (no frameworks/libraries)
- Event delegation for dynamic content
- Clear function naming reflecting business logic

### Data Management
- User data: `user_` prefix in localStorage
- Progress data: `exam_{year}_progress` pattern
- Results data: `exam_results` with timestamp arrays

## Common Tasks

### Adding New Exam Year
1. Create `{year}-exam.html` (copy from existing year)
2. Create `{year}-exam.js` with question data
3. Update main page button in `index.html`
4. Test user progress isolation

### Adding Questions to Existing Exam
1. Edit corresponding `{year}-exam.js` file
2. Follow exact data structure format
3. Include detailed explanation with legal citations
4. Test question randomization and feedback

### Debugging User Issues
1. Check browser localStorage for user data
2. Verify `UserManager` initialization
3. Check console for JavaScript errors
4. Validate quiz data structure integrity