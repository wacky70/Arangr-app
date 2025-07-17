#!/usr/bin/env python3
"""
Quick test script to debug the Arangr application
"""

import tkinter as tk
import sys
import os

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import ArangrExplorer

def main():
    """Test the application with debugging"""
    root = tk.Tk()
    
    try:
        app = ArangrExplorer(root)
        print(f"Application initialized successfully")
        print(f"Current directory: {app.current_dir}")
        root.mainloop()
    except Exception as e:
        print(f"Error initializing application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
