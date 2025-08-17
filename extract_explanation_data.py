#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def extract_explanation_data(file_path):
    """Extract explanation data and URLs from 2025-data-취업규칙.js"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the explanationData array
    start_pattern = r'const explanationData = \['
    end_pattern = r'\];'
    
    start_match = re.search(start_pattern, content)
    if not start_match:
        print("explanationData array not found")
        return []
    
    start_pos = start_match.end()
    
    # Find the end of the array
    end_match = re.search(end_pattern, content[start_pos:])
    if not end_match:
        print("End of explanationData array not found")
        return []
    
    end_pos = start_pos + end_match.start()
    array_content = content[start_pos:end_pos]
    
    # Extract each explanation entry
    explanations = []
    
    # Pattern to match each explanation object
    entry_pattern = r'\{[^{}]*explanation[^{}]*urls[^{}]*\}'
    
    matches = re.findall(entry_pattern, array_content, re.DOTALL)
    
    for match in matches:
        # Extract explanation
        explanation_match = re.search(r'explanation:\s*"([^"]*)"', match)
        explanation = explanation_match.group(1) if explanation_match else ""
        
        # Extract URLs
        urls_match = re.search(r'urls:\s*\[(.*?)\]', match, re.DOTALL)
        if urls_match:
            urls_content = urls_match.group(1)
            # Extract individual URLs
            url_pattern = r'"([^"]*)"'
            urls = re.findall(url_pattern, urls_content)
        else:
            urls = []
        
        if explanation:
            explanations.append({
                "explanation": explanation,
                "urls": urls
            })
    
    return explanations

def main():
    # Extract explanation data from the data file
    explanations = extract_explanation_data('2025-data-취업규칙.js')
    
    print(f"Extracted {len(explanations)} explanation entries")
    
    # Print first few for verification
    for i, exp in enumerate(explanations[:5]):
        print(f"\nExplanation {i+1}:")
        print(f"Text: {exp['explanation']}")
        print(f"URLs: {exp['urls']}")
    
    # Save to file
    with open('explanation_data.json', 'w', encoding='utf-8') as f:
        json.dump(explanations, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(explanations)} explanation entries to explanation_data.json")

if __name__ == "__main__":
    main() 