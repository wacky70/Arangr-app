"""
Arangr Application - Main Application Entry Point
"""

import tkinter as tk
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import ArangrExplorer


def main():
    """Initialize and run the application"""
    root = tk.Tk()
    
    # Set window icon if available
    try:
        if os.path.exists("logo.ico"):
            root.iconbitmap("logo.ico")
    except (tk.TclError, FileNotFoundError):
        pass
    
    # Initialize application
    try:
        app = ArangrExplorer(root)
        
        # Handle graceful shutdown
        def on_closing():
            try:
                if hasattr(app, 'logo') and app.logo:
                    app.logo.animation_enabled = False
            except:
                pass
            root.quit()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())