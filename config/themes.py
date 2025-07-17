"""
Theme Configuration for Organizer Application - Monokai Theme
"""

def get_theme(is_dark_mode=False):
    """Get enhanced Monokai theme configuration with better UX colors"""
    
    if is_dark_mode:
        # Monokai Dark Theme
        return {
            'bg': '#272822',           # Monokai background
            'fg': '#F8F8F2',           # Monokai foreground
            'header_bg': '#3E3D32',    # Darker monokai
            'header_fg': '#F8F8F2',    # Monokai foreground
            'button_bg': '#49483E',    # Monokai comment background
            'button_fg': '#F8F8F2',    # Monokai foreground
            'button_hover': '#66D9EF', # Monokai cyan
            'button_active': '#FD971F', # Monokai orange
            'entry_bg': '#49483E',     # Monokai comment background
            'entry_fg': '#F8F8F2',     # Monokai foreground
            'text_bg': '#272822',      # Monokai background
            'text_fg': '#F8F8F2',      # Monokai foreground
            'tree_bg': '#272822',      # Monokai background
            'tree_fg': '#F8F8F2',      # Monokai foreground
            'select_bg': '#66D9EF',    # Monokai cyan
            'select_fg': '#272822',    # Dark text on cyan
            'separator': '#49483E',    # Monokai comment background
            'accent': '#66D9EF',       # Monokai cyan
            'highlight': '#FD971F',    # Monokai orange
            'success': '#A6E22E',      # Monokai green
            'warning': '#E6DB74',      # Monokai yellow
            'error': '#F92672',        # Monokai pink/red
            'comment': '#75715E',      # Monokai comment
            'code_bg': '#272822',      # Code background
            'code_fg': '#F8F8F2'       # Code foreground
        }
    else:
        # Light Monokai variant
        return {
            'bg': '#FAFAFA',
            'fg': '#272822',
            'header_bg': '#FFFFFF',
            'header_fg': '#272822',
            'button_bg': '#E8E8E8',
            'button_fg': '#272822',
            'button_hover': '#66D9EF',
            'button_active': '#FD971F',
            'entry_bg': '#FFFFFF',
            'entry_fg': '#272822',
            'text_bg': '#FFFFFF',
            'text_fg': '#272822',
            'tree_bg': '#FFFFFF',
            'tree_fg': '#272822',
            'select_bg': '#66D9EF',
            'select_fg': '#FFFFFF',
            'separator': '#E0E0E0',
            'accent': '#66D9EF',
            'highlight': '#FD971F',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336',
            'comment': '#9E9E9E',
            'code_bg': '#F8F8F8',
            'code_fg': '#272822'
        }

# Monokai Theme Constants
MONOKAI_COLORS = {
    'background': '#272822',
    'foreground': '#F8F8F2',
    'comment': '#75715E',
    'red': '#F92672',
    'orange': '#FD971F',
    'yellow': '#E6DB74',
    'green': '#A6E22E',
    'cyan': '#66D9EF',
    'purple': '#AE81FF',
    'selection': '#49483E',
    'line_highlight': '#3E3D32'
}