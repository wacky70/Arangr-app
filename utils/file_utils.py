"""
Enhanced File Utilities with better UX and performance
"""

import os
import mimetypes
from datetime import datetime

# Enhanced file icons with better visual hierarchy and thumbnails
ENHANCED_FILE_ICONS = {
    # Programming & Development - More specific icons
    '.py': '🐍', '.js': '🟨', '.ts': '🔷', '.html': '🌐', '.css': '🎨', 
    '.json': '📋', '.xml': '🗂️', '.yaml': '⚙️', '.yml': '⚙️',
    '.cpp': '⚡', '.c': '🔧', '.java': '☕', '.php': '🐘', '.go': '🐹',
    '.rs': '🦀', '.swift': '🐦', '.kt': '🔶', '.rb': '💎', '.sql': '🗄️',
    
    # Documents & Text - More descriptive
    '.txt': '📄', '.md': '📝', '.doc': '📘', '.docx': '📘', 
    '.rtf': '📝', '.pdf': '📕', '.odt': '📄', '.pages': '📄',
    
    # Spreadsheets & Data - Enhanced
    '.xls': '📊', '.xlsx': '📊', '.csv': '📈', '.ods': '📊',
    '.numbers': '📊', '.tsv': '📋',
    
    # Presentations - More detailed
    '.ppt': '📽️', '.pptx': '📽️', '.odp': '🎞️', '.key': '📽️',
    
    # Images - Format-specific icons for better identification
    '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🎞️',
    '.bmp': '🖼️', '.svg': '🎨', '.ico': '🔷', '.webp': '🖼️',
    '.tiff': '🖼️', '.raw': '📷', '.psd': '🎨', '.ai': '🎨',
    
    # Audio & Video - Enhanced with quality indicators
    '.mp3': '🎵', '.wav': '🎼', '.flac': '🎼', '.aac': '🎵',
    '.ogg': '🎵', '.m4a': '🎵', '.wma': '🎵',
    '.mp4': '🎬', '.avi': '📹', '.mov': '🎬', '.mkv': '🎬',
    '.wmv': '📹', '.webm': '🎬', '.flv': '📹', '.m4v': '🎬',
    
    # Archives & Compression - More specific
    '.zip': '🗜️', '.rar': '📦', '.7z': '🗜️', '.tar': '📦',
    '.gz': '📦', '.bz2': '📦', '.xz': '📦', '.dmg': '💿',
    
    # Executables & System - OS specific
    '.exe': '⚙️', '.msi': '📦', '.bat': '⚙️', '.sh': '🐚',
    '.app': '📱', '.deb': '📦', '.rpm': '📦', '.pkg': '📦',
    
    # Development files - More detailed
    '.log': '📋', '.ini': '⚙️', '.cfg': '⚙️', '.conf': '⚙️',
    '.dll': '🔧', '.so': '🔧', '.dylib': '🔧', '.lib': '📚',
    '.gitignore': '🚫', '.env': '🔐', '.dockerfile': '🐳',
    
    # Special folders with enhanced hierarchy
    'folder': '📁',
    'folder_open': '📂',
    'folder_code': '📁',
    'folder_images': '🖼️',
    'folder_music': '🎵',
    'folder_videos': '🎬',
    'folder_documents': '📂',
    'folder_downloads': '📥',
    'folder_desktop': '🖥️',
    
    # Default with size indicators
    'default': '📄',
    'large_file': '📄',
    'empty_file': '📝'
}

def get_file_icon(file_path):
    """Get enhanced file icon with thumbnails and visual hierarchy"""
    if os.path.isdir(file_path):
        # Enhanced folder icons with content hints
        folder_name = os.path.basename(file_path).lower()
        
        # Check folder content to provide better icons
        try:
            files_in_folder = os.listdir(file_path)
            has_images = any(f.lower().endswith(('.jpg', '.png', '.gif', '.jpeg')) for f in files_in_folder[:10])
            has_videos = any(f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')) for f in files_in_folder[:10])
            has_music = any(f.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')) for f in files_in_folder[:10])
            has_code = any(f.lower().endswith(('.py', '.js', '.html', '.css', '.java')) for f in files_in_folder[:10])
            
            # Return content-aware folder icons
            if has_images and len([f for f in files_in_folder if f.lower().endswith(('.jpg', '.png', '.gif', '.jpeg'))]) > 5:
                return '🖼️'  # Image-heavy folder
            elif has_videos:
                return '🎬'  # Video folder
            elif has_music:
                return '🎵'  # Music folder
            elif has_code:
                return '💻'  # Code folder
        except (PermissionError, OSError):
            pass
        
        # Special system folders
        special_folders = {
            'documents': '📂',
            'downloads': '📥',
            'pictures': '🖼️',
            'music': '🎵',
            'videos': '🎬',
            'desktop': '🖥️',
            'trash': '🗑️',
            'recycle bin': '🗑️',
            '.git': '📚',
            'node_modules': '📦',
            'build': '🔨',
            'dist': '📦',
            'src': '💻',
            'assets': '🎨',
            'images': '🖼️',
            'img': '🖼️',
            'photos': '📷',
            'videos': '🎬',
            'audio': '🎵',
            'docs': '📚',
            'config': '⚙️',
            'backup': '💾',
            'temp': '🗂️',
            'cache': '💾'
        }
        return special_folders.get(folder_name, ENHANCED_FILE_ICONS['folder'])
    
    # Enhanced file detection with size consideration
    try:
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Size-based icon modifications
        if file_size == 0:
            return '📝'  # Empty file
        elif file_size > 100 * 1024 * 1024:  # > 100MB
            base_icon = ENHANCED_FILE_ICONS.get(file_ext, ENHANCED_FILE_ICONS['default'])
            return f"{base_icon}"  # Could add size indicator in future
        
        return ENHANCED_FILE_ICONS.get(file_ext, ENHANCED_FILE_ICONS['default'])
        
    except (OSError, PermissionError):
        file_ext = os.path.splitext(file_path)[1].lower()
        return ENHANCED_FILE_ICONS.get(file_ext, ENHANCED_FILE_ICONS['default'])

def get_file_type_description(file_path):
    """Get user-friendly file type description with enhanced details"""
    if os.path.isdir(file_path):
        try:
            # Count items in folder for better description
            items = os.listdir(file_path)
            item_count = len(items)
            if item_count == 0:
                return "Empty Folder"
            elif item_count == 1:
                return "Folder (1 item)"
            else:
                return f"Folder ({item_count} items)"
        except (PermissionError, OSError):
            return "Folder"
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Enhanced type descriptions with more context
    enhanced_descriptions = {
        # Programming
        '.py': 'Python Script',
        '.js': 'JavaScript File',
        '.ts': 'TypeScript File',
        '.html': 'HTML Document',
        '.css': 'CSS Stylesheet',
        '.json': 'JSON Data',
        '.xml': 'XML Document',
        '.yaml': 'YAML Configuration',
        '.yml': 'YAML Configuration',
        
        # Documents
        '.txt': 'Text Document',
        '.md': 'Markdown Document',
        '.pdf': 'PDF Document',
        '.docx': 'Word Document',
        '.doc': 'Word Document (Legacy)',
        '.rtf': 'Rich Text Document',
        
        # Spreadsheets
        '.xlsx': 'Excel Spreadsheet',
        '.xls': 'Excel Spreadsheet (Legacy)',
        '.csv': 'CSV Data File',
        '.ods': 'OpenDocument Spreadsheet',
        
        # Presentations
        '.pptx': 'PowerPoint Presentation',
        '.ppt': 'PowerPoint Presentation (Legacy)',
        '.odp': 'OpenDocument Presentation',
        
        # Media
        '.jpg': 'JPEG Image',
        '.jpeg': 'JPEG Image',
        '.png': 'PNG Image',
        '.gif': 'GIF Animation',
        '.svg': 'SVG Vector Image',
        '.mp3': 'MP3 Audio',
        '.wav': 'WAV Audio',
        '.flac': 'FLAC Audio (Lossless)',
        '.mp4': 'MP4 Video',
        '.avi': 'AVI Video',
        '.mov': 'QuickTime Video',
        
        # Archives
        '.zip': 'ZIP Archive',
        '.rar': 'RAR Archive',
        '.7z': '7-Zip Archive',
        '.tar': 'TAR Archive',
        
        # Executables
        '.exe': 'Windows Executable',
        '.msi': 'Windows Installer',
        '.app': 'macOS Application',
        '.deb': 'Debian Package',
        '.rpm': 'RPM Package'
    }
    
    return enhanced_descriptions.get(file_ext, f"{file_ext.upper()[1:]} File" if file_ext else "File")

def format_file_size(size_bytes):
    """Format file size with better readability"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 1)
    
    # Remove unnecessary decimal for whole numbers
    if s == int(s):
        s = int(s)
    
    return f"{s} {size_names[i]}"

def is_text_file(file_path):
    """Enhanced text file detection with better heuristics"""
    # First check by extension
    text_extensions = {
        '.txt', '.md', '.py', '.js', '.html', '.css', '.json', 
        '.xml', '.csv', '.log', '.ini', '.cfg', '.conf', '.yaml', 
        '.yml', '.sql', '.sh', '.bat', '.c', '.cpp', '.h', '.php',
        '.rb', '.go', '.rs', '.swift', '.kt', '.ts', '.vue', '.jsx',
        '.tsx', '.scss', '.less', '.sass', '.coffee', '.pl', '.r',
        '.m', '.scala', '.clj', '.hs', '.lua', '.dart', '.vb',
        '.cs', '.java', '.gradle', '.maven', '.properties',
        '.toml', '.env', '.gitignore', '.dockerfile', '.makefile',
        '.readme', '.license', '.changelog', '.authors'
    }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext in text_extensions:
        return True
    
    # Check files without extensions that are commonly text
    file_name = os.path.basename(file_path).lower()
    text_filenames = {
        'readme', 'license', 'changelog', 'authors', 'contributors',
        'makefile', 'dockerfile', 'vagrantfile', 'gemfile', 'rakefile'
    }
    
    if file_name in text_filenames:
        return True
    
    # For other files, try to detect if they're text by reading a sample
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return True  # Empty files are considered text
        
        # Don't try to detect text for very large files
        if file_size > 10 * 1024 * 1024:  # 10MB
            return False
            
        # Read a sample and check for text characteristics
        sample_size = min(1024, file_size)  # Read up to 1KB
        
        with open(file_path, 'rb') as f:
            sample = f.read(sample_size)
        
        # Check for null bytes (strong indicator of binary)
        if b'\x00' in sample:
            return False
        
        # Try to decode as text
        try:
            sample.decode('utf-8')
            return True
        except UnicodeDecodeError:
            try:
                sample.decode('latin-1')
                return True
            except UnicodeDecodeError:
                return False
                
    except (OSError, IOError, PermissionError):
        return False

def read_text_file(file_path):
    """Enhanced text file reading with better encoding detection and error handling"""
    try:
        file_size = os.path.getsize(file_path)
        
        # Handle very large files
        if file_size > 10 * 1024 * 1024:  # 10MB
            return _read_large_text_file(file_path, file_size)
        
        # Try different encodings in order of likelihood
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                    content = file.read()
                    return content, None
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                return None, f"Error reading file: {str(e)}"
        
        # If all encodings fail, try binary mode with error replacement
        try:
            with open(file_path, 'rb') as file:
                raw_content = file.read()
                content = raw_content.decode('utf-8', errors='replace')
                return content, None
        except Exception as e:
            return None, f"Could not read file with any encoding: {str(e)}"
            
    except Exception as e:
        return None, str(e)

def _read_large_text_file(file_path, file_size):
    """Handle large text files by reading only a portion"""
    try:
        # Read first 1MB of large files
        max_read_size = 1024 * 1024  # 1MB
        
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read(max_read_size)
            
        # Add truncation notice
        if file_size > max_read_size:
            content += f"\n\n... [File truncated - showing first {format_file_size(max_read_size)} of {format_file_size(file_size)}]"
            
        return content, None
        
    except Exception as e:
        return None, f"Error reading large file: {str(e)}"

def is_image_file(file_path):
    """Enhanced image file detection"""
    image_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', 
        '.ico', '.webp', '.tiff', '.tif', '.raw', '.cr2', '.nef',
        '.dng', '.orf', '.srw', '.arw', '.pef', '.rw2', '.rwl',
        '.heic', '.heif', '.avif', '.jxl'
    }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    return file_ext in image_extensions