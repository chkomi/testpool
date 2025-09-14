#!/usr/bin/env python3
"""
Fix URLs that were broken by Hanja span tag processing.
URLs should not contain HTML tags - they need clean text.
"""

import os
import re

def fix_urls_in_file(file_path):
    """Fix URLs in a single file by removing span tags from URL fields."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match URL fields with span tags
        url_pattern = r'"url":\s*"([^"]*<span[^>]*>[^<]*</span>[^"]*)"'
        
        def clean_url(match):
            url_with_tags = match.group(1)
            # Remove all span tags from URL
            clean_url = re.sub(r'<span[^>]*>([^<]*)</span>', r'\1', url_with_tags)
            return f'"url": "{clean_url}"'
        
        # Fix single URLs
        content = re.sub(url_pattern, clean_url, content)
        
        # Pattern to match URLs array fields with span tags
        urls_pattern = r'"urls":\s*\[((?:[^[\]]*<span[^>]*>[^<]*</span>[^[\]]*)*)\]'
        
        def clean_urls_array(match):
            urls_content = match.group(1)
            # Remove all span tags from URLs array content
            clean_urls = re.sub(r'<span[^>]*>([^<]*)</span>', r'\1', urls_content)
            return f'"urls": [{clean_urls}]'
        
        # Fix URLs arrays
        content = re.sub(urls_pattern, clean_urls_array, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Count fixes
            fixes = len(re.findall(r'<span[^>]*>[^<]*</span>', original_content)) - len(re.findall(r'<span[^>]*>[^<]*</span>', content))
            return fixes
        
        return 0
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    # Find all JS files that might contain quiz data
    js_files = []
    
    # Root level exam files
    for file in os.listdir('.'):
        if file.endswith('.js') and ('exam' in file or '2025-' in file):
            js_files.append(file)
    
    # 2025 directory files
    if os.path.exists('2025'):
        for file in os.listdir('2025'):
            if file.endswith('.js'):
                js_files.append(os.path.join('2025', file))
    
    total_fixes = 0
    files_fixed = 0
    
    print("Fixing URLs broken by Hanja span tags...")
    
    for file_path in js_files:
        if os.path.exists(file_path):
            fixes = fix_urls_in_file(file_path)
            if fixes > 0:
                files_fixed += 1
                total_fixes += fixes
                print(f"  {file_path}: {fixes} URL fixes")
    
    print(f"\nSummary:")
    print(f"  Files processed: {len(js_files)}")
    print(f"  Files with URL fixes: {files_fixed}")
    print(f"  Total URL fixes: {total_fixes}")

if __name__ == "__main__":
    main()