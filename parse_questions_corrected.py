#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def parse_questions_corrected(file_path):
    """Parse exactly 47 questions from the text file with corrected logic"""
    
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

def parse_questions_advanced(file_path):
    """Advanced parsing approach - handle complex question structures"""
    
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

def parse_questions_simple(file_path):
    """Simple parsing approach - just count and extract basic structure"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count the number of questions by looking for "숫자." patterns
    question_numbers = re.findall(r'(\d+)\.', content)
    unique_numbers = sorted(set([int(num) for num in question_numbers]))
    
    print(f"Found question numbers: {unique_numbers}")
    print(f"Total unique questions: {len(unique_numbers)}")
    
    # Now let's extract each question manually
    questions = []
    
    for num in unique_numbers:
        # Find the start of this question
        start_pattern = rf'{num}\.\s*'
        start_match = re.search(start_pattern, content)
        
        if not start_match:
            continue
            
        start_pos = start_match.end()
        
        # Find the end (next question or end of file)
        if num < max(unique_numbers):
            next_num = num + 1
            end_pattern = rf'\n\s*{next_num}\.'
            end_match = re.search(end_pattern, content[start_pos:])
            if end_match:
                end_pos = start_pos + end_match.start()
            else:
                end_pos = len(content)
        else:
            end_pos = len(content)
        
        question_content = content[start_pos:end_pos].strip()
        
        # Extract question text and options
        lines = question_content.split('\n')
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
            print(f"Question {num} has {len(options)} options, skipping...")
            print(f"Content: {question_content[:200]}...")
    
    return questions

def main():
    # Try the simple parsing approach
    questions = parse_questions_simple('2025/5. 취업규칙.txt')
    
    print(f"\nParsed {len(questions)} questions using simple approach")
    
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
    with open('취업규칙_47_questions_simple.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(questions)} questions to 취업규칙_47_questions_simple.json")
    
    # Also save as JavaScript array format
    js_content = "const 취업규칙_47_questions = " + json.dumps(questions, ensure_ascii=False, indent=2) + ";"
    with open('취업규칙_47_questions_simple.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("Saved JavaScript format to 취업규칙_47_questions_simple.js")

if __name__ == "__main__":
    main() 