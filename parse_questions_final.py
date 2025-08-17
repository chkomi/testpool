#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def parse_questions_final(file_path):
    """Parse exactly 47 questions from the text file with better logic"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into questions more carefully
    questions = []
    
    # Pattern to match question blocks - look for numbered questions
    # This pattern looks for "숫자." followed by content until the next "숫자." or end of file
    question_pattern = r'(\d+)\.\s*(.*?)(?=\n\s*\d+\.|$)'
    
    matches = re.findall(question_pattern, content, re.DOTALL)
    
    print(f"Found {len(matches)} potential questions")
    
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
        
        # Only add if we have exactly 4 options
        if len(options) == 4:
            # For now, we'll set a default answer (this should be updated with correct answers)
            correct_answer = "a"  # Default to first option
            
            # Create question object in the format used in 2025-exam.js
            question_obj = {
                "question": question_text,
                "a": options[0],
                "b": options[1],
                "c": options[2],
                "d": options[3],
                "correct": correct_answer,
                "explanation": ""
            }
            
            questions.append(question_obj)
        else:
            print(f"Question {qnum} has {len(options)} options, skipping...")
            print(f"Content: {qcontent[:200]}...")
    
    return questions

def parse_questions_manual(file_path):
    """Manual parsing approach - read the file line by line"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    questions = []
    current_question = None
    current_options = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if this is a new question (starts with number.)
        if re.match(r'^\d+\.', line):
            # Save previous question if exists
            if current_question and len(current_options) == 4:
                current_question["a"] = current_options[0]
                current_question["b"] = current_options[1]
                current_question["c"] = current_options[2]
                current_question["d"] = current_options[3]
                current_question["correct"] = "a"  # Default
                current_question["explanation"] = ""
                questions.append(current_question)
            
            # Start new question
            question_text = re.sub(r'^\d+\.\s*', '', line)
            current_question = {"question": question_text}
            current_options = []
            
        # Check if this is an option line
        elif re.match(r'^[①②③④]', line):
            option_text = re.sub(r'^[①②③④]\s*', '', line)
            current_options.append(option_text)
            
        # This is continuation of question text
        elif current_question and not current_options:
            current_question["question"] += " " + line
    
    # Don't forget the last question
    if current_question and len(current_options) == 4:
        current_question["a"] = current_options[0]
        current_question["b"] = current_options[1]
        current_question["c"] = current_options[2]
        current_question["d"] = current_options[3]
        current_question["correct"] = "a"  # Default
        current_question["explanation"] = ""
        questions.append(current_question)
    
    return questions

def main():
    # Try the manual parsing approach
    questions = parse_questions_manual('2025/5. 취업규칙.txt')
    
    print(f"\nParsed {len(questions)} questions using manual approach")
    
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
    with open('취업규칙_47_questions_final.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(questions)} questions to 취업규칙_47_questions_final.json")
    
    # Also save as JavaScript array format
    js_content = "const 취업규칙_47_questions = " + json.dumps(questions, ensure_ascii=False, indent=2) + ";"
    with open('취업규칙_47_questions_final.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("Saved JavaScript format to 취업규칙_47_questions_final.js")

if __name__ == "__main__":
    main() 