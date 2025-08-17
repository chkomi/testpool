#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def parse_questions(file_path):
    """Parse the questions from the text file and convert to JSON format"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into questions
    questions = []
    
    # Pattern to match question blocks
    question_pattern = r'(\d+)\.\s*(.*?)(?=\d+\.|$)'
    
    matches = re.findall(question_pattern, content, re.DOTALL)
    
    for i, (qnum, qcontent) in enumerate(matches, 1):
        if not qcontent.strip():
            continue
            
        # Clean up the question content
        qcontent = qcontent.strip()
        
        # Split into question text and options
        lines = qcontent.split('\n')
        question_text = ""
        options = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line contains option markers (①, ②, ③, ④)
            if re.match(r'^[①②③④]', line):
                # Remove the option marker and clean up
                option_text = re.sub(r'^[①②③④]\s*', '', line)
                options.append(option_text)
            elif not options:  # This is question text
                question_text += line + " "
            else:  # This is continuation of question text
                question_text += line + " "
        
        # Clean up question text
        question_text = question_text.strip()
        
        # For now, we'll set a default answer (this should be updated with correct answers)
        # We'll use the first option as default, but this needs to be corrected manually
        correct_answer = "a"  # Default to first option
        
        # Create question object in the format used in 2025-exam.js
        question_obj = {
            "question": question_text,
            "a": options[0] if len(options) > 0 else "",
            "b": options[1] if len(options) > 1 else "",
            "c": options[2] if len(options) > 2 else "",
            "d": options[3] if len(options) > 3 else "",
            "correct": correct_answer,
            "explanation": ""
        }
        
        questions.append(question_obj)
    
    return questions

def main():
    # Parse the questions
    questions = parse_questions('2025/5. 취업규칙.txt')
    
    print(f"Parsed {len(questions)} questions")
    
    # Print first few questions for verification
    for i, q in enumerate(questions[:3]):
        print(f"\nQuestion {i+1}:")
        print(f"Text: {q['question'][:100]}...")
        print(f"Option A: {q['a'][:50]}...")
        print(f"Option B: {q['b'][:50]}...")
        print(f"Option C: {q['c'][:50]}...")
        print(f"Option D: {q['d'][:50]}...")
        print(f"Answer: {q['correct']}")
    
    # Save to JSON file
    with open('취업규칙_questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(questions)} questions to 취업규칙_questions.json")
    
    # Also save as JavaScript array format
    js_content = "const 취업규칙_questions = " + json.dumps(questions, ensure_ascii=False, indent=2) + ";"
    with open('취업규칙_questions.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("Saved JavaScript format to 취업규칙_questions.js")

if __name__ == "__main__":
    main() 