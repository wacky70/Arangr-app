"""
Application Settings and Configuration
"""

# Application Information
APP_NAME = "Arangr ∞ Explorer"
APP_VERSION = "3.0.0"

# Window Configuration
WINDOW_GEOMETRY = "1400x900"
MIN_WINDOW_SIZE = (1000, 700)

# Font Configuration
FONTS = {
    'title': ('Segoe UI', 18, 'normal'),
    'header': ('Segoe UI', 10, 'bold'),
    'body': ('Segoe UI', 9),
    'button': ('Segoe UI', 9, 'bold'),
    'code': ('Consolas', 9),
    'fallback': ('Segoe UI', 20, 'bold')
}

# File Preview Limits
MAX_PREVIEW_SIZE = 10 * 1024 * 1024  # 10MB
MAX_TEXT_SIZE = 1024 * 1024  # 1MB
MAX_PREVIEW_CHARS = 10000

# File Icons
FILE_ICONS = {
    # Programming
    '.py': '🐍', '.js': '⚡', '.html': '🌐', '.css': '🎨', 
    '.json': '📋', '.xml': '📋',
    
    # Documents
    '.txt': '📄', '.md': '📝', '.doc': '📄', '.docx': '📄', 
    '.rtf': '📄', '.pdf': '📕',
    
    # Spreadsheets
    '.xls': '📊', '.xlsx': '📊', '.csv': '📊',
    
    # Presentations
    '.ppt': '📽️', '.pptx': '📽️',
    
    # Media
    '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
    '.mp3': '🎵', '.mp4': '🎬', '.avi': '🎬', '.mov': '🎬',
    
    # Archives
    '.zip': '🗜️', '.rar': '🗜️', '.7z': '🗜️',
    
    # Executables
    '.exe': '⚙️', '.bat': '⚙️', '.sh': '⚙️',
    
    # Default
    'folder': '📁',
    'default': '📄'
}

# Text Encodings
TEXT_ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

# Text File Extensions
TEXT_EXTENSIONS = {
    '.txt', '.md', '.py', '.js', '.html', '.css', '.json', 
    '.xml', '.csv', '.log', '.ini', '.cfg', '.conf'
}

# Office File Extensions
OFFICE_EXTENSIONS = {
    'word': ['.docx', '.doc'],
    'excel': ['.xlsx', '.xls'],
    'powerpoint': ['.pptx', '.ppt'],
    'pdf': ['.pdf']
}
