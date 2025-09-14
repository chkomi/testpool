#!/usr/bin/env python3
import os
import re
import glob

# Comprehensive list of all Hanja characters found in the codebase
all_hanja_replacements = {
    # Previously missed characters
    '保': "<span class='hanja'>保</span>",
    '全': "<span class='hanja'>全</span>", 
    '告': "<span class='hanja'>告</span>",
    '土': "<span class='hanja'>土</span>",
    '地': "<span class='hanja'>地</span>",
    '基': "<span class='hanja'>基</span>",
    '決': "<span class='hanja'>決</span>",
    '營': "<span class='hanja'>營</span>",
    '용': "<span class='hanja'>用</span>",  # Korean pronunciation
    '用': "<span class='hanja'>用</span>",
    '管': "<span class='hanja'>管</span>",
    '補': "<span class='hanja'>補</span>",
    '農': "<span class='hanja'>農</span>",
    '院': "<span class='hanja'>院</span>",
    '법': "<span class='hanja'>법</span>",  # Korean for 法
    '査': "<span class='hanja'>査</span>",
    '監': "<span class='hanja'>監</span>",
    '下': "<span class='hanja'>下</span>",
    '水': "<span class='hanja'>水</span>",
    '生': "<span class='hanja'>生</span>",
    '計': "<span class='hanja'>計</span>",
    '設': "<span class='hanja'>設</span>",
    
    # Also include previously identified characters to ensure they stay wrapped
    '流下距離': "<span class='hanja'>流下距離</span>",
    '連名': "<span class='hanja'>連名</span>",
    '時價': "<span class='hanja'>時價</span>",
    '支院': "<span class='hanja'>支院</span>",
    '預受金': "<span class='hanja'>預受金</span>",
    '流用': "<span class='hanja'>流用</span>",
    '工事': "<span class='hanja'>工事</span>",
    '再開': "<span class='hanja'>再開</span>",
    '無資力': "<span class='hanja'>無資力</span>",
    '監事': "<span class='hanja'>監事</span>",
    '監査': "<span class='hanja'>監査</span>",
    '複數': "<span class='hanja'>複數</span>",
    '價': "<span class='hanja'>價</span>",
    '取入洑': "<span class='hanja'>取入洑</span>",
    '浚渫': "<span class='hanja'>浚渫</span>",
    '遊漁基盤': "<span class='hanja'>遊漁基盤</span>",
    '裁決': "<span class='hanja'>裁決</span>",
    '洑': "<span class='hanja'>洑</span>",
}

def fix_all_hanja(file_path):
    """Fix all hanja characters that aren't wrapped properly"""
    print(f"Checking {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    original_content = content
    changes_made = 0
    
    # Apply replacements, but only if the character is not already wrapped
    for hanja, replacement in all_hanja_replacements.items():
        # Don't replace if it's already wrapped in span tags
        pattern = f'(?<!<span class=\'hanja\'>){re.escape(hanja)}(?!</span>)'
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes_made += len(matches)
            print(f"  Fixed {len(matches)} instances of {hanja}")
    
    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Total fixes: {changes_made}")
        return changes_made
    else:
        print(f"  No fixes needed")
        return 0

def main():
    # Get all JavaScript files
    js_files = []
    js_files.extend(glob.glob('*.js'))
    js_files.extend(glob.glob('2025/*.js'))
    
    # Filter out backup files
    js_files = [f for f in js_files if not f.endswith('.backup')]
    
    total_changes = 0
    processed_files = 0
    
    for js_file in js_files:
        changes = fix_all_hanja(js_file)
        if changes > 0:
            processed_files += 1
            total_changes += changes
    
    print(f"\nSummary:")
    print(f"Files fixed: {processed_files}")
    print(f"Total fixes made: {total_changes}")

if __name__ == "__main__":
    main()