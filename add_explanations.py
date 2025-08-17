#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def add_explanations_to_questions():
    """Add explanations and URLs to the existing 47 questions"""
    
    # Load the existing questions
    with open('취업규칙_47_complete.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # Load the explanation data
    with open('explanation_data.json', 'r', encoding='utf-8') as f:
        explanations = json.load(f)
    
    print(f"Loaded {len(questions)} questions and {len(explanations)} explanations")
    
    # Add explanations and URLs to each question
    for i, question in enumerate(questions):
        if i < len(explanations):
            exp_data = explanations[i]
            question['explanation'] = exp_data['explanation']
            
            # Add URLs - handle multiple URLs
            urls = exp_data['urls']
            if len(urls) == 1:
                question['url'] = urls[0]
            elif len(urls) > 1:
                question['url'] = urls[0]  # Primary URL
                for j, url in enumerate(urls[1:], 2):
                    question[f'url{j}'] = url
    
    # Save the updated questions
    with open('취업규칙_47_with_explanations.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {len(questions)} questions with explanations and URLs")
    print("Saved to 취업규칙_47_with_explanations.json")
    
    # Print first few for verification
    for i, q in enumerate(questions[:3]):
        print(f"\nQuestion {i+1}:")
        print(f"Explanation: {q.get('explanation', 'N/A')}")
        print(f"URL: {q.get('url', 'N/A')}")
        if 'url2' in q:
            print(f"URL2: {q['url2']}")

if __name__ == "__main__":
    add_explanations_to_questions() 