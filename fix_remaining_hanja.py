#!/usr/bin/env python3
import os
import re
import glob

# Additional hanja characters that were missed
additional_hanja_replacements = {
    '流下距離': "<span class='hanja'>流下距離</span>",
    '連名': "<span class='hanja'>連名</span>",
    '時價': "<span class='hanja'>時價</span>",
    '支院': "<span class='hanja'>支院</span>",
    '預受金': "<span class='hanja'>預受金</span>",
    '流用': "<span class='hanja'>流用</span>"  # This might have been missed in some files
}

def fix_remaining_hanja(file_path):
    """Fix remaining hanja that weren't wrapped properly"""
    print(f"Checking {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    original_content = content
    changes_made = 0
    
    # Apply replacements, but only if the character is not already wrapped
    for hanja, replacement in additional_hanja_replacements.items():
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
        changes = fix_remaining_hanja(js_file)
        if changes > 0:
            processed_files += 1
            total_changes += changes
    
    print(f"\nSummary:")
    print(f"Files fixed: {processed_files}")
    print(f"Total fixes made: {total_changes}")

if __name__ == "__main__":
    main()