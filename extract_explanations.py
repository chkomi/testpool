#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def extract_explanations_from_js(file_path):
    """Extract explanations and URLs from the existing 2025-exam.js file for the 취업규칙 section"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the 취업규칙 section
    start_pattern = r'"취업규칙":\s*\['
    end_pattern = r'\],\s*"인사규정"'
    
    start_match = re.search(start_pattern, content)
    if not start_match:
        print("취업규칙 section not found")
        return []
    
    start_pos = start_match.end()
    
    # Find the end of the section
    end_match = re.search(end_pattern, content[start_pos:])
    if not end_match:
        print("End of 취업규칙 section not found")
        return []
    
    end_pos = start_pos + end_match.start()
    section_content = content[start_pos:end_pos]
    
    # Extract questions, explanations and URLs
    questions = []
    
    # Pattern to match each question object
    question_pattern = r'\{[^{}]*"question"[^{}]*"a"[^{}]*"b"[^{}]*"c"[^{}]*"d"[^{}]*"correct"[^{}]*"explanation"[^{}]*\}'
    
    matches = re.findall(question_pattern, section_content, re.DOTALL)
    
    for match in matches:
        # Extract question text
        question_match = re.search(r'"question":\s*"([^"]*)"', match)
        question_text = question_match.group(1) if question_match else ""
        
        # Extract explanation
        explanation_match = re.search(r'"explanation":\s*"([^"]*)"', match)
        explanation = explanation_match.group(1) if explanation_match else ""
        
        # Extract URL if exists
        url_match = re.search(r'"url":\s*"([^"]*)"', match)
        url = url_match.group(1) if url_match else ""
        
        if question_text:
            questions.append({
                "question": question_text,
                "explanation": explanation,
                "url": url
            })
    
    return questions

def main():
    # Extract explanations from the existing file
    existing_questions = extract_explanations_from_js('2025-exam.js')
    
    print(f"Extracted {len(existing_questions)} questions with explanations")
    
    # Print first few for verification
    for i, q in enumerate(existing_questions[:5]):
        print(f"\nQuestion {i+1}:")
        print(f"Text: {q['question'][:100]}...")
        print(f"Explanation: {q['explanation']}")
        print(f"URL: {q['url']}")
    
    # Save to file
    with open('existing_explanations.json', 'w', encoding='utf-8') as f:
        json.dump(existing_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(existing_questions)} existing questions to existing_explanations.json")

if __name__ == "__main__":
    main() 