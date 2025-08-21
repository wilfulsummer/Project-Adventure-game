#!/usr/bin/env python3
"""
Simple syntax checker for the modified game files
"""

import ast
import sys

def check_syntax(filename):
    """Check if a Python file has valid syntax"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the source code
        ast.parse(source)
        print(f"✅ {filename}: Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {filename}: Syntax Error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filename}: Error reading file: {e}")
        return False

def main():
    """Check syntax of modified files"""
    files_to_check = [
        "main.py",
        "world_generation.py"
    ]
    
    print("🔍 Checking syntax of modified files...")
    print("=" * 50)
    
    all_good = True
    for filename in files_to_check:
        if not check_syntax(filename):
            all_good = False
    
    print("=" * 50)
    if all_good:
        print("🎉 All files have valid syntax!")
    else:
        print("⚠️  Some files have syntax errors that need fixing.")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
