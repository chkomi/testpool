#!/usr/bin/env python3
"""
Fix JavaScript syntax errors caused by Hanja span tags in JS files.
Remove span tags from JavaScript code comments and strings where they break syntax.
"""

import os
import re

def fix_js_syntax_in_file(file_path):
    """Fix JavaScript syntax by removing span tags from comments and code."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix span tags in JavaScript comments (starting with //)
        comment_pattern = r'(//[^\n]*)<span[^>]*>([^<]*)</span>([^\n]*)'
        
        def fix_comment(match):
            before = match.group(1)
            text = match.group(2)  # The content inside span tags
            after = match.group(3)
            return before + text + after
        
        # Keep applying the pattern until no more matches
        while re.search(comment_pattern, content):
            content = re.sub(comment_pattern, fix_comment, content)
        
        # Fix span tags that are inside JavaScript string literals or identifiers
        # This is more complex - look for span tags that are not inside quoted strings
        # but are breaking JavaScript syntax
        
        # Pattern for span tags in variable names or identifiers (like "사<span>用</span>")
        js_identifier_pattern = r'([a-zA-Z가-힣_$][a-zA-Z0-9가-힣_$]*)<span[^>]*>([^<]*)</span>([a-zA-Z0-9가-힣_$]*)'
        
        def fix_js_identifier(match):
            before = match.group(1)
            text = match.group(2)
            after = match.group(3)
            return before + text + after
        
        # Apply identifier fix
        while re.search(js_identifier_pattern, content):
            content = re.sub(js_identifier_pattern, fix_js_identifier, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Focus on core JavaScript files that might have syntax issues
    js_files = [
        'quiz-logic.js',
        'script.js', 
        'user-manager.js',
        'preview-script.js'
    ]
    
    # Add any other JS files in root directory
    for file in os.listdir('.'):
        if file.endswith('.js') and file not in js_files:
            js_files.append(file)
    
    files_fixed = 0
    
    print("Fixing JavaScript syntax errors caused by Hanja span tags...")
    
    for file_path in js_files:
        if os.path.exists(file_path):
            if fix_js_syntax_in_file(file_path):
                files_fixed += 1
                print(f"  {file_path}: Fixed JavaScript syntax")
    
    print(f"\nSummary:")
    print(f"  Files checked: {len(js_files)}")
    print(f"  Files with syntax fixes: {files_fixed}")

if __name__ == "__main__":
    main()