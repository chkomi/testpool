const fs = require('fs');

// 새로 만든 47문제 데이터 읽기
const content = fs.readFileSync('취업규칙_47_complete.js', 'utf8');

// window.currentSubjectQuestions = [ 부분에서 실제 문제 데이터 추출
const questionsMatch = content.match(/window\.currentSubjectQuestions\s*=\s*(\[[\s\S]*\]);/);
if (!questionsMatch) {
    console.log('문제 데이터를 찾을 수 없습니다.');
    process.exit(1);
}

// JavaScript 배열을 JSON으로 변환
const questionsString = questionsMatch[1];
const newQuestions = eval(questionsString);

// 2025-exam.js 파일 읽기
let examContent = fs.readFileSync('2025-exam.js', 'utf8');

// 취업규칙 섹션의 시작과 끝 찾기
const startPattern = /"취업규칙":\s*\[/;
const endPattern = /\],\s*"인사규정"/;

const startMatch = examContent.match(startPattern);
const endMatch = examContent.match(endPattern);

if (startMatch && endMatch) {
    const startIndex = startMatch.index + startMatch[0].length;
    const endIndex = endMatch.index;
    
    // 새 문제 데이터를 JSON 문자열로 변환
    const newSectionContent = JSON.stringify(newQuestions, null, 4);
    
    // 기존 섹션을 새 섹션으로 교체
    const newContent = examContent.substring(0, startIndex) + '\n' + newSectionContent + '\n    ' + examContent.substring(endIndex);
    
    // 파일에 저장
    fs.writeFileSync('2025-exam.js', newContent, 'utf8');
    
    console.log('취업규칙 섹션이 47문제로 성공적으로 교체되었습니다!');
    console.log(`새로 추가된 문제 수: ${newQuestions.length}`);
} else {
    console.log('취업규칙 섹션을 찾을 수 없습니다.');
} 