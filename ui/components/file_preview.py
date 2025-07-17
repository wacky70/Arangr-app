"""
File Preview Component
"""

import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path

from core.file_operations import FileOperations
from core.office_reader import OfficeFileReader
from config.settings import MAX_PREVIEW_SIZE, MAX_PREVIEW_CHARS, OFFICE_EXTENSIONS


class FilePreviewComponent:
    """File preview widget component"""
    
    def __init__(self, parent):
        self.parent = parent
        self.office_reader = OfficeFileReader()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the preview widget with responsive placeholder"""
        # Container frame
        self.container = tk.Frame(self.parent)
        self.container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(8, 15))
        
        # Create notebook for tabbed preview
        self.preview_notebook = ttk.Notebook(self.container)
        self.preview_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Text preview tab
        self._create_text_preview_tab()
        
        # Image preview tab (if PIL available)
        try:
            from PIL import Image
            self._create_image_preview_tab()
        except ImportError:
            pass
        
        # Properties tab
        self._create_properties_tab()
        
        # Show interactive placeholder
        self._show_interactive_placeholder()
    
    def _create_text_preview_tab(self):
        """Create enhanced text preview tab"""
        text_frame = tk.Frame(self.preview_notebook)
        self.preview_notebook.add(text_frame, text="📄 Content")
        
        # Create toolbar for text operations
        toolbar = tk.Frame(text_frame, height=30)
        toolbar.pack(fill=tk.X, padx=5, pady=2)
        toolbar.pack_propagate(False)
        
        # Text operation buttons
        tk.Button(
            toolbar, text="📋 Copy", command=self._copy_text,
            font=('Segoe UI', 8), padx=8, pady=2
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            toolbar, text="🔍 Search", command=self._search_in_text,
            font=('Segoe UI', 8), padx=8, pady=2
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            toolbar, text="📖 Wrap", command=self._toggle_word_wrap,
            font=('Segoe UI', 8), padx=8, pady=2
        ).pack(side=tk.LEFT)
        
        # Text widget with enhanced features
        text_container = tk.Frame(text_frame)
        text_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        self.text_widget = tk.Text(
            text_container,
            wrap=tk.WORD,
            font=('Consolas', 10),
            relief='flat',
            borderwidth=1,
            highlightthickness=1,
            padx=15,
            pady=15,
            undo=True,
            maxundo=20
        )
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.text_widget.yview)
        h_scroll = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        
        self.text_widget.configure(
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )
        
        # Pack text components
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_image_preview_tab(self):
        """Create enhanced image preview tab"""
        image_frame = tk.Frame(self.preview_notebook)
        self.preview_notebook.add(image_frame, text="🖼️ Image")
        
        # Image toolbar
        img_toolbar = tk.Frame(image_frame, height=35)
        img_toolbar.pack(fill=tk.X, padx=5, pady=2)
        img_toolbar.pack_propagate(False)
        
        # Image control buttons
        tk.Button(
            img_toolbar, text="🔍+ Zoom In", command=self._zoom_in,
            font=('Segoe UI', 8), padx=8, pady=2
        ).pack(side=tk.LEFT, padx=(0, 3))
        
        tk.Button(
            img_toolbar, text="🔍- Zoom Out", command=self._zoom_out,
            font=('Segoe UI', 8), padx=8, pady=2
        ).pack(side=tk.LEFT, padx=(0, 3))
        
        tk.Button(
            img_toolbar, text="📐 Fit", command=self._fit_image,
            font=('Segoe UI', 8), padx=8, pady=2
        ).pack(side=tk.LEFT, padx=(0, 3))
        
        tk.Button(
            img_toolbar, text="🔄 Rotate", command=self._rotate_image,
            font=('Segoe UI', 8), padx=8, pady=2
        ).pack(side=tk.LEFT, padx=(0, 3))
        
        # Image info label
        self.image_info = tk.Label(
            img_toolbar, text="", font=('Segoe UI', 8), fg='#666666'
        )
        self.image_info.pack(side=tk.RIGHT, padx=5)
        
        # Image canvas container
        canvas_container = tk.Frame(image_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Canvas for image display
        self.image_canvas = tk.Canvas(
            canvas_container,
            bg='#f8f9fa',
            relief='flat',
            borderwidth=1,
            highlightthickness=1
        )
        
        # Image scrollbars
        v_scroll_img = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.image_canvas.yview)
        h_scroll_img = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        
        self.image_canvas.configure(
            yscrollcommand=v_scroll_img.set,
            xscrollcommand=h_scroll_img.set
        )
        
        # Pack image components
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll_img.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll_img.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_properties_tab(self):
        """Create file properties tab"""
        props_frame = tk.Frame(self.preview_notebook)
        self.preview_notebook.add(props_frame, text="📊 Properties")
        
        # Properties text widget
        self.properties_text = tk.Text(
            props_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=1,
            highlightthickness=1,
            padx=15,
            pady=15,
            state=tk.DISABLED
        )
        
        props_scroll = ttk.Scrollbar(props_frame, orient=tk.VERTICAL, command=self.properties_text.yview)
        self.properties_text.configure(yscrollcommand=props_scroll.set)
        
        self.properties_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        props_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _show_interactive_placeholder(self):
        """Show interactive placeholder when no file is selected"""
        placeholder_content = """
🎯 Arangr File Preview

📁 SELECT A FILE to begin exploring!

✨ Available Features:
  📄 Text & Code Preview
  🖼️ Image Viewing with Zoom
  📊 Detailed File Properties
  📋 Copy & Search Functions
  🔍 Advanced File Analysis

🎮 Supported Formats:
  📝 Text: .txt, .md, .py, .js, .html, .css
  📄 Documents: .pdf, .docx, .xlsx, .pptx
  🖼️ Images: .jpg, .png, .gif, .svg, .bmp
  🎵 Audio: .mp3, .wav, .flac (info only)
  🎬 Video: .mp4, .avi, .mov (info only)

💡 Tips:
  • Double-click folders to navigate
  • Use search to find files quickly
  • Right-click for context menu
  • Drag & drop files (coming soon)

👆 Click on any file in the left panel to start!
"""
        
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, placeholder_content)
        self.text_widget.config(state=tk.DISABLED)
        
        # Add placeholder to properties tab
        self.properties_text.config(state=tk.NORMAL)
        self.properties_text.delete(1.0, tk.END)
        self.properties_text.insert(1.0, """
📊 File Properties

Select a file to view detailed information:

📋 Basic Information
📏 Size & Dimensions  
📅 Dates & Timestamps
🔐 Permissions & Security
🏷️ File Type & Format
📈 Advanced Metadata

Waiting for file selection...
""")
        self.properties_text.config(state=tk.DISABLED)

    def preview_file(self, file_path):
        """Enhanced file preview with better responsiveness"""
        if not os.path.exists(file_path):
            self._show_error("File not found")
            return
        
        # Show loading indicator
        self._show_loading()
        
        # Get comprehensive file info
        file_info = self._get_comprehensive_file_info(file_path)
        
        # Update properties tab immediately
        self._update_properties_tab(file_info)
        
        # Switch to appropriate tab and load content
        if file_info['is_image']:
            self._preview_image_file(file_path, file_info)
            self.preview_notebook.select(1)  # Image tab
        else:
            self._preview_text_file(file_path, file_info)
            self.preview_notebook.select(0)  # Text tab

    def _get_comprehensive_file_info(self, file_path):
        """Get comprehensive file information"""
        from utils.file_utils import get_file_icon, format_file_size, get_file_type_description, is_image_file
        from datetime import datetime
        import hashlib
        
        try:
            stat = os.stat(file_path)
            
            # Calculate file hash for verification
            file_hash = "Calculating..."
            if stat.st_size < 10 * 1024 * 1024:  # Only for files < 10MB
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()[:16] + "..."
                except:
                    file_hash = "Unavailable"
            
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'size_formatted': format_file_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'icon': get_file_icon(file_path),
                'type': get_file_type_description(file_path),
                'extension': os.path.splitext(file_path)[1].lower(),
                'is_image': is_image_file(file_path),
                'is_text': self._is_text_file(file_path),
                'hash': file_hash,
                'permissions': oct(stat.st_mode)[-3:]
            }
        except Exception as e:
            return {'error': str(e), 'name': os.path.basename(file_path)}

    def _update_properties_tab(self, file_info):
        """Update properties tab with comprehensive info"""
        if 'error' in file_info:
            content = f"❌ Error reading file: {file_info['error']}"
        else:
            content = f"""📊 File Properties: {file_info['name']}

📋 Basic Information:
    📁 Name: {file_info['name']}
    🏷️ Type: {file_info['type']}
    📏 Size: {file_info['size_formatted']} ({file_info['size']:,} bytes)
    🔗 Extension: {file_info['extension'] or 'None'}

📅 Timestamps:
    📝 Modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}
    📄 Created: {file_info['created'].strftime('%Y-%m-%d %H:%M:%S')}
    👁️ Accessed: {file_info['accessed'].strftime('%Y-%m-%d %H:%M:%S')}

🔐 Security:
    🔑 Permissions: {file_info['permissions']}
    🔒 Hash (MD5): {file_info['hash']}

📍 Location:
    📂 Full Path: {file_info['path']}
    📁 Directory: {os.path.dirname(file_info['path'])}

🎯 Content Type:
    🖼️ Image File: {'Yes' if file_info['is_image'] else 'No'}
    📝 Text File: {'Yes' if file_info['is_text'] else 'No'}
    📊 Preview Available: {'Yes' if file_info['is_text'] or file_info['is_image'] else 'Limited'}
"""
        
        self.properties_text.config(state=tk.NORMAL)
        self.properties_text.delete(1.0, tk.END)
        self.properties_text.insert(1.0, content)
        self.properties_text.config(state=tk.DISABLED)

    def _show_loading(self):
        """Show loading indicator"""
        loading_text = "🔄 Loading file preview...\n\nPlease wait while we analyze the file content."
        
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, loading_text)
        self.text_widget.config(state=tk.DISABLED)

    # Add new interactive methods
    def _copy_text(self):
        """Copy selected text to clipboard"""
        try:
            selected = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_widget.clipboard_clear()
            self.text_widget.clipboard_append(selected)
        except tk.TclError:
            # No selection, copy all
            content = self.text_widget.get(1.0, tk.END)
            self.text_widget.clipboard_clear()
            self.text_widget.clipboard_append(content)

    def _search_in_text(self):
        """Search within text content"""
        from tkinter import simpledialog
        search_term = simpledialog.askstring("Search", "Enter text to search:")
        if search_term:
            # Highlight search results
            content = self.text_widget.get(1.0, tk.END)
            self.text_widget.tag_remove('search', 1.0, tk.END)
            
            start = 1.0
            while True:
                start = self.text_widget.search(search_term, start, tk.END)
                if not start:
                    break
                end = f"{start}+{len(search_term)}c"
                self.text_widget.tag_add('search', start, end)
                start = end
            
            self.text_widget.tag_config('search', background='yellow', foreground='black')

    def _toggle_word_wrap(self):
        """Toggle word wrap in text widget"""
        current_wrap = self.text_widget.cget('wrap')
        new_wrap = tk.NONE if current_wrap == tk.WORD else tk.WORD
        self.text_widget.config(wrap=new_wrap)

    def _is_text_file(self, file_path):
        """Check if file is a text file"""
        from utils.file_utils import is_text_file
        return is_text_file(file_path)

    def _preview_image_file(self, file_path, file_info):
        """Preview image file in the image tab"""
        try:
            from PIL import Image
            
            # Load and display image
            img = Image.open(file_path)
            
            # Update image info
            width, height = img.size
            self.image_info.config(
                text=f"{width}×{height} | {img.format} | {img.mode}"
            )
            
            # Calculate scale to fit canvas
            canvas_width = 400  # Default canvas width
            canvas_height = 300  # Default canvas height
            
            scale_x = canvas_width / width
            scale_y = canvas_height / height
            scale = min(scale_x, scale_y) * 0.9  # 90% to leave margin
            
            # Resize image
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            if new_width > 0 and new_height > 0:
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                from tkinter import PhotoImage
                try:
                    from PIL import ImageTk
                    photo = ImageTk.PhotoImage(resized_img)
                    
                    # Clear canvas and display image
                    self.image_canvas.delete("all")
                    self.image_canvas.create_image(
                        canvas_width // 2, canvas_height // 2,
                        image=photo, anchor="center"
                    )
                    
                    # Keep reference to prevent garbage collection
                    self.image_canvas.image = photo
                    
                except ImportError:
                    self._show_error("PIL ImageTk not available for image display")
                    
        except Exception as e:
            self._show_error(f"Error loading image: {str(e)}")

    def _preview_text_file(self, file_path, file_info):
        """Preview text file content"""
        try:
            from utils.file_utils import read_text_file
            
            # Read file content
            content, error = read_text_file(file_path)
            
            if content is not None:
                # Truncate very long content
                if len(content) > 50000:  # 50KB limit for display
                    content = content[:50000] + "\n\n... [Content truncated for display]"
                
                # Display content
                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(1.0, content)
                self.text_widget.config(state=tk.DISABLED)
                
            else:
                self._show_error(f"Error reading file: {error}")
                
        except Exception as e:
            self._show_error(f"Error previewing text file: {str(e)}")

    def _show_error(self, error_message):
        """Show error message in preview area"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, f"❌ {error_message}")
        self.text_widget.config(state=tk.DISABLED)

    def _zoom_in(self):
        """Zoom in on image (placeholder)"""
        # This would be implemented with proper image scaling
        pass

    def _zoom_out(self):
        """Zoom out on image (placeholder)"""
        # This would be implemented with proper image scaling
        pass

    def _fit_image(self):
        """Fit image to canvas (placeholder)"""
        # This would be implemented with proper image fitting
        pass

    def _rotate_image(self):
        """Rotate image (placeholder)"""
        # This would be implemented with proper image rotation
        pass

    def clear(self):
        """Clear the preview area"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)
        
        if hasattr(self, 'image_canvas'):
            self.image_canvas.delete("all")
            self.image_info.config(text="")

    def get_widget(self):
        """Get the text widget for styling"""
        return self.text_widget
