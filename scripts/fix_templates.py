import os
import re

def fix_file(filepath):
    # Try different encodings to read the file
    encodings = ['utf-8', 'utf-16', 'windows-1252', 'iso-8859-1']
    content = None
    
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
            
    if content is None:
        print(f"Skipping {filepath}: Could not decode")
        return

    # List of broken patterns to fix (Currency and common symbols)
    replacements = {
        'â‚¦': '$',  # Mojibake for ₦
        '₦': '$',    # The actual symbol
        'ðŸ”¥': '🔥', # Mojibake for flame emoji
        'a,;': '$',   # The user's reported artifact
    }
    
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if content != original_content:
        # Save as clean UTF-8
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")

def main():
    root_dir = os.getcwd()
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
