const fs = require('fs');

// Read the new questions
const newQuestions = require('./취업규칙_47_complete.json');

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
const beforeSection = content.substring(0, startIndex);
const afterSection = content.substring(endIndex);

const newContent = beforeSection + '\n' + newSectionContent + '\n    ' + afterSection;

// Write the updated file
fs.writeFileSync('2025-exam.js', newContent, 'utf8');

console.log('Successfully updated 2025-exam.js with 47 questions');

// Also update the question count at the bottom of the file
const countPattern = /'취업규칙':\s*\d+,/;
const newCountLine = "'취업규칙': 47,";

if (countPattern.test(newContent)) {
    const updatedContent = newContent.replace(countPattern, newCountLine);
    fs.writeFileSync('2025-exam.js', updatedContent, 'utf8');
    console.log('Updated question count to 47');
} else {
    console.log('Could not find question count line to update');
} 