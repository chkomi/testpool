const fs = require('fs');

// Read the new questions with explanations
const newQuestions = require('./취업규칙_47_with_explanations.json');

// Read the original file
let content = fs.readFileSync('2025-exam.js', 'utf8');

// Find the start and end of the 취업규칙 section
const startPattern = /"취업규칙":\s*\[/;
const endPattern = /\],\s*"인사규정"/;

const startMatch = content.match(startPattern);
const endMatch = content.match(endPattern);

if (!startMatch || !endMatch) {
    console.error('Could not find 취업규칙 section boundaries');
    process.exit(1);
}

const startIndex = startMatch.index + startMatch[0].length;
const endIndex = endMatch.index;

console.log(`Found 취업규칙 section from index ${startIndex} to ${endIndex}`);

// Create the new content
const newSectionContent = JSON.stringify(newQuestions, null, 4);

// Replace the section
const newContent = content.substring(0, startIndex) + '\n' + newSectionContent + '\n    ' + content.substring(endIndex);

// Write back to file
fs.writeFileSync('2025-exam.js', newContent, 'utf8');

console.log('Successfully updated 2025-exam.js with new 취업규칙 questions including explanations and URLs');
console.log(`Updated ${newQuestions.length} questions`); 