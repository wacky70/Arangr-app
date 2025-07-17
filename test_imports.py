#!/usr/bin/env python3
"""
Minimal test to check if imports work correctly
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    from utils.file_utils import get_file_icon, format_file_size, is_text_file
    print("✓ utils.file_utils imported successfully")
    
    from config.themes import get_theme
    print("✓ config.themes imported successfully")
    
    from ui.animated_logo import AnimatedLogo
    print("✓ ui.animated_logo imported successfully")
    
    from core.office_reader import OfficeFileReader
    print("✓ core.office_reader imported successfully")
    
    from core.ai_assistant import AIAssistant, AIDialog
    print("✓ core.ai_assistant imported successfully")
    
    # Test basic functionality
    test_path = "C:\\Windows\\System32\\notepad.exe"
    if os.path.exists(test_path):
        icon = get_file_icon(test_path)
        size = format_file_size(1024)
        print(f"✓ File utilities work: icon={icon}, size={size}")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
