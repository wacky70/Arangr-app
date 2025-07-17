"""
Main Window UI - Professional file explorer interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import threading
from functools import lru_cache

from ui.animated_logo import AnimatedLogo
from utils.file_utils import get_file_icon, format_file_size, is_text_file, read_text_file, is_image_file
from core.office_reader import OfficeFileReader
from core.ai_assistant import AIAssistant, AIDialog
from config.themes import get_theme

# Import PIL components for image handling
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class OrganizerExplorer:
    """Main application window and file explorer"""
    
    def __init__(self, root):
        self.root = root
        self.current_dir = os.getcwd()
        self.history = [self.current_dir]
        self.history_index = 0
        self.is_dark_mode = False
        self.office_reader = OfficeFileReader()
        self.ai_assistant = AIAssistant()
        self.current_selected_file = None
        self.current_file_content = None
        
        # Performance optimization caches
        self.file_icon_cache = {}
        self.file_size_cache = {}
        self.directory_cache = {}
        self.preview_cache = {}
        
        # Background loading control
        self.loading_cancelled = False
        self.loading_thread = None
        
        # Initialize components
        self.logo = None
        
        # UX improvements
        self.last_selected_item = None
        self.hover_item = None
        self.animation_active = False
        self.progress_var = tk.StringVar(value="Ready")
        
        self._setup_window()
        self._create_ui()
        self._apply_theme()
        self._populate_tree_async()

    def _setup_window(self):
        """Configure the main window"""
        self.root.title("Organizer Application")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
    
    def _create_ui(self):
        """Create the user interface"""
        # Main container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Create sections
        self._create_header()
        self._create_toolbar()
        self._create_content_area()
        self._create_status_bar()
        
        # Bind events
        self._bind_events()
    
    def _create_header(self):
        """Create the header section with professional banner and enhanced UX"""
        self.header_frame = tk.Frame(self.main_container, height=100)  # Increased height
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Add subtle gradient effect
        header_content = tk.Frame(self.header_frame)
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Store reference for theming
        self.header_content = header_content
        
        # Professional banner logo section with improved layout
        self.logo_title_frame = tk.Frame(header_content)
        self.logo_title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Professional Banner Logo
        self._create_logo(self.logo_title_frame)
        
        # Enhanced controls section - side by side layout
        controls_frame = tk.Frame(header_content)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        # Create a horizontal container for side-by-side buttons
        buttons_container = tk.Frame(controls_frame)
        buttons_container.pack(expand=True, fill=tk.BOTH)
        
        # Professional theme toggle with enhanced 3D styling
        self.theme_toggle = tk.Button(
            buttons_container,
            text="🌙 Dark",
            command=self._toggle_theme_animated,
            font=('Segoe UI', 11, 'bold'),
            relief='raised',
            borderwidth=3,
            padx=18,
            pady=12,
            cursor='hand2',
            width=10,
            bg='#e8e8e8',
            fg='#333333',
            activebackground='#d0d0d0',
            activeforeground='#000000'
        )
        self.theme_toggle.pack(side=tk.LEFT, padx=(0, 8), pady=10)
        
        # Quick access button with matching 3D styling
        self.quick_access = tk.Button(
            buttons_container,
            text="⚡ Quick",
            command=self._show_quick_access,
            font=('Segoe UI', 11, 'bold'),
            relief='raised',
            borderwidth=3,
            padx=18,
            pady=12,
            cursor='hand2',
            width=10,
            bg='#e8e8e8',
            fg='#333333',
            activebackground='#d0d0d0',
            activeforeground='#000000'
        )
        self.quick_access.pack(side=tk.LEFT, padx=(8, 0), pady=10)
        
        # Apply enhanced 3D effects to both buttons
        self._add_3d_button_effects(self.theme_toggle)
        self._add_3d_button_effects(self.quick_access)

    def _create_logo(self, parent):
        """Create professional banner logo"""
        try:
            # Create professional banner with optimal dimensions
            self.logo = AnimatedLogo(parent, "logo.png", size=(250, 60))
        except Exception as e:
            print(f"Banner logo error: {e}")
            # Professional fallback
            self.fallback_logo = tk.Label(
                parent, 
                text="ORGANIZER", 
                font=('Segoe UI', 18, 'bold'),
                relief='flat',
                borderwidth=0,
                padx=25,
                pady=15,
                width=20,
                anchor='center'
            )
            self.fallback_logo.pack(side=tk.LEFT, padx=(20, 15), pady=8)
    
    def _create_toolbar(self):
        """Create the navigation toolbar with frame references"""
        self.toolbar_frame = tk.Frame(self.main_container, height=45)
        self.toolbar_frame.pack(fill=tk.X, padx=25, pady=(0, 8))
        self.toolbar_frame.pack_propagate(False)
        
        # Navigation buttons
        self.nav_frame = tk.Frame(self.toolbar_frame)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y, pady=5)
        
        nav_buttons = [
            ("◀ Back", self._go_back, "Go back"),
            ("▲ Up", self._go_up, "Go up"),
            ("🏠 Home", self._go_home, "Go home"),
            ("📁 Browse", self._browse_folder, "Browse folder"),
            ("📝 Current File", self._show_current_file, "Show current file info"),
            ("✏️ Rename", self._rename_file, "Rename selected file"),
            ("🤖 Ask AI", self._ask_ai, "Ask AI about files")
        ]
        
        self.nav_buttons = []
        for i, (text, command, tooltip) in enumerate(nav_buttons):
            btn = self._create_button(self.nav_frame, text, command, width=8)
            btn.pack(side=tk.LEFT, padx=(0 if i == 0 else 6, 0))
            self.nav_buttons.append(btn)
        
        # Path entry
        self._create_path_entry()
    
    def _create_path_entry(self):
        """Create the path entry widget with frame reference"""
        self.path_frame = tk.Frame(self.toolbar_frame)
        self.path_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=5)
        
        self.path_var = tk.StringVar(value=self.current_dir)
        self.path_entry = tk.Entry(
            self.path_frame,
            textvariable=self.path_var,
            font=('Segoe UI', 9),
            relief='flat',
            borderwidth=0,
            highlightthickness=1
        )
        self.path_entry.pack(fill=tk.X, ipady=6, padx=10)
    
    def _create_content_area(self):
        """Create the main content area"""
        content_container = tk.Frame(self.main_container)
        content_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 15))
        
        # Paned window
        self.paned_window = ttk.PanedWindow(content_container, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # File tree panel
        self._create_file_tree_panel()
        
        # File preview panel
        self._create_file_preview_panel()

    def _create_file_tree_panel(self):
        """Create the file tree panel with enhanced UX"""
        left_panel = tk.Frame(self.paned_window, relief='flat')
        self.paned_window.add(left_panel, weight=3)
        
        # Enhanced header with search
        header_frame = tk.Frame(left_panel)
        header_frame.pack(fill=tk.X, padx=15, pady=(8, 0))
        
        self.tree_header = tk.Label(
            header_frame,
            text="Files & Folders",
            font=('Segoe UI', 12, 'bold'),  # Larger font
            anchor='w'
        )
        self.tree_header.pack(side=tk.LEFT, fill=tk.Y)
        
        # Quick search box
        search_frame = tk.Frame(header_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 9),
            relief='flat',
            borderwidth=1,
            highlightthickness=1,
            width=15
        )
        self.search_entry.pack(side=tk.RIGHT, ipady=3)
        self.search_entry.bind('<KeyRelease>', self._on_search)
        
        search_label = tk.Label(
            search_frame,
            text="🔍",
            font=('Segoe UI', 10)
        )
        search_label.pack(side=tk.RIGHT, padx=(5, 5))
        
        # Enhanced separator with gradient effect
        self.tree_separator = tk.Frame(left_panel, height=2, relief='flat')
        self.tree_separator.pack(fill=tk.X, padx=15, pady=5)
        
        # Tree container with enhanced styling
        tree_container = tk.Frame(left_panel)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Configure enhanced tree style
        style = ttk.Style()
        style.configure("Enhanced.Treeview", 
                       font=('Segoe UI', 10),
                       rowheight=32,  # Taller rows for better touch
                       borderwidth=0,
                       relief='flat',
                       fieldbackground='white')
        style.configure("Enhanced.Treeview.Heading", 
                       font=('Segoe UI', 11, 'bold'), 
                       padding=(10, 10),
                       borderwidth=0,
                       relief='flat')
        
        # Enhanced selection colors
        style.map("Enhanced.Treeview",
                 background=[('selected', '#0078d4')],
                 foreground=[('selected', 'white')])
        
        # Create tree with enhanced features
        self.tree = ttk.Treeview(
            tree_container,
            columns=('size', 'modified', 'type'),  # Added type column
            show='tree headings',
            style="Enhanced.Treeview"
        )
        
        # Configure columns with better headers
        self.tree.heading('#0', text='📁 Name', anchor='w')
        self.tree.heading('size', text='📊 Size', anchor='center')
        self.tree.heading('modified', text='📅 Modified', anchor='center')
        self.tree.heading('type', text='🏷️ Type', anchor='center')
        
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('size', width=80, minwidth=70, anchor='center')
        self.tree.column('modified', width=130, minwidth=110, anchor='center')
        self.tree.column('type', width=100, minwidth=80, anchor='center')
        
        # Enhanced scrollbars
        v_scroll = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scroll.set)
        
        # Pack components
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_file_preview_panel(self):
        """Create the file preview panel with image and text tabs"""
        right_panel = tk.Frame(self.paned_window, relief='flat')
        self.paned_window.add(right_panel, weight=2)
        
        # Header
        self.preview_header = tk.Label(
            right_panel,
            text="File Preview",
            font=('Segoe UI', 10, 'bold'),
            anchor='w',
            padx=15,
            pady=8
        )
        self.preview_header.pack(fill=tk.X)
        
        # Separator
        self.preview_separator = tk.Frame(right_panel, height=1)
        self.preview_separator.pack(fill=tk.X, padx=15)
        
        # Preview container with notebook for tabs
        preview_container = tk.Frame(right_panel)
        preview_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(8, 15))
        
        # Create notebook for tabbed preview
        self.preview_notebook = ttk.Notebook(preview_container)
        self.preview_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Text preview tab
        text_frame = tk.Frame(self.preview_notebook)
        self.preview_notebook.add(text_frame, text="📄 Text")
        
        self.preview_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=12
        )
        
        text_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=text_scroll.set)
        
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Image preview tab
        image_frame = tk.Frame(self.preview_notebook)
        self.preview_notebook.add(image_frame, text="🖼️ Image")
        
        # Image container with scrollbars
        image_container = tk.Frame(image_frame)
        image_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for image display with scroll support
        self.image_canvas = tk.Canvas(
            image_container,
            bg='white',
            relief='flat',
            borderwidth=0,
            highlightthickness=0
        )
        
        # Scrollbars for image
        v_scroll_img = ttk.Scrollbar(image_container, orient=tk.VERTICAL, command=self.image_canvas.yview)
        h_scroll_img = ttk.Scrollbar(image_container, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        
        self.image_canvas.configure(
            yscrollcommand=v_scroll_img.set,
            xscrollcommand=h_scroll_img.set
        )
        
        # Pack image components
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll_img.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll_img.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Image controls frame
        img_controls = tk.Frame(image_frame)
        img_controls.pack(fill=tk.X, pady=(5, 0))
        
        # Zoom buttons
        tk.Button(
            img_controls,
            text="🔍+ Zoom In",
            command=self._zoom_in,
            font=('Segoe UI', 8),
            padx=8,
            pady=2
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            img_controls,
            text="🔍- Zoom Out", 
            command=self._zoom_out,
            font=('Segoe UI', 8),
            padx=8,
            pady=2
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            img_controls,
            text="📐 Fit",
            command=self._fit_image,
            font=('Segoe UI', 8),
            padx=8,
            pady=2
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            img_controls,
            text="🔄 Rotate",
            command=self._rotate_image,
            font=('Segoe UI', 8),
            padx=8,
            pady=2
        ).pack(side=tk.LEFT)
        
        # Image info label
        self.image_info_label = tk.Label(
            img_controls,
            text="",
            font=('Segoe UI', 8),
            fg='#666666'
        )
        self.image_info_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Initialize image variables
        self.current_image = None
        self.original_image = None
        self.image_scale = 1.0
        self.image_rotation = 0
        self.image_id = None

    def _create_status_bar(self):
        """Create enhanced status bar with progress indication"""
        self.status_frame = tk.Frame(self.main_container, height=35)  # Increased height
        self.status_frame.pack(fill=tk.X, padx=25, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        # Enhanced separator
        self.status_separator = tk.Frame(self.status_frame, height=2, relief='flat')
        self.status_separator.pack(fill=tk.X, pady=(0, 8))
        
        # Status content frame
        status_content = tk.Frame(self.status_frame)
        status_content.pack(fill=tk.BOTH, expand=True)
        
        # Main status label
        self.status_label = tk.Label(
            status_content,
            textvariable=self.progress_var,
            font=('Segoe UI', 9),
            anchor='w',
            padx=15
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.Y)
        
        # Progress indicator
        self.progress_indicator = tk.Label(
            status_content,
            text="",
            font=('Segoe UI', 8),
            anchor='e',
            padx=15
        )
        self.progress_indicator.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Loading animation dots
        self.loading_dots = 0

    def _create_button(self, parent, text, command, **kwargs):
        """Create a professional styled button"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 9, 'normal'),
            relief='raised',
            borderwidth=1,
            padx=12,
            pady=8,
            cursor='hand2',
            **kwargs
        )
        
        # Add professional hover effects
        self._add_button_hover_effects(button)
        return button
    
    def _add_button_hover_effects(self, button):
        """Add professional hover effects to button"""
        def on_enter(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                bg=theme['button_hover'],
                relief='raised',
                borderwidth=2
            )
        
        def on_leave(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                bg=theme['button_bg'],
                relief='raised',
                borderwidth=1
            )
        
        def on_press(e):
            button.config(relief='sunken')
        
        def on_release(e):
            button.config(relief='raised')
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)

    def _open_file(self, file_path):
        """Open file with default application"""
        try:
            normalized_path = os.path.normpath(file_path)
            
            if not os.path.exists(normalized_path):
                messagebox.showerror("Error", f"File not found: {normalized_path}")
                return
            
            import platform
            import subprocess
            
            if platform.system() == 'Windows':
                os.startfile(normalized_path)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', normalized_path])
            else:
                subprocess.run(['xdg-open', normalized_path])
                
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file: {str(e)}")

    def _add_tree_item(self, item_name, is_folder):
        """Add item to tree with enhanced information"""
        try:
            item_path = os.path.join(self.current_dir, item_name)
            normalized_path = os.path.normpath(item_path)
            
            # Get file info
            if is_folder:
                size_text = "--"
                file_type = "Folder"
            else:
                try:
                    size = os.path.getsize(normalized_path)
                    size_text = format_file_size(size)
                    file_ext = os.path.splitext(normalized_path)[1].lower()
                    file_type = file_ext.upper()[1:] if file_ext else "File"
                except (OSError, PermissionError):
                    size_text = "N/A"
                    file_type = "Unknown"
            
            try:
                from datetime import datetime
                modified = datetime.fromtimestamp(os.path.getmtime(normalized_path))
                modified_text = modified.strftime('%m/%d %H:%M')
            except (OSError, PermissionError):
                modified_text = "N/A"
            
            # Get icon
            icon = get_file_icon(normalized_path)
            display_text = f"{icon}  {item_name}"
            
            # Insert item
            self.tree.insert('', 'end', 
                           text=display_text, 
                           values=(size_text, modified_text, file_type))
            
        except Exception as e:
            print(f"Error adding tree item {item_name}: {e}")

    def _populate_tree_async(self):
        """Populate tree asynchronously"""
        if self.loading_thread and self.loading_thread.is_alive():
            self.loading_cancelled = True
            self.loading_thread.join(timeout=1.0)
        
        self.loading_cancelled = False
        self._update_progress("Loading directory...")
        
        self.loading_thread = threading.Thread(target=self._populate_tree_enhanced)
        self.loading_thread.daemon = True
        self.loading_thread.start()

    def _zoom_in(self):
        """Zoom in on the current image"""
        if hasattr(self, 'current_image') and self.current_image:
            self.image_scale *= 1.2
            self._update_image_display()

    def _zoom_out(self):
        """Zoom out on the current image"""
        if hasattr(self, 'current_image') and self.current_image:
            self.image_scale /= 1.2
            self._update_image_display()

    def _fit_image(self):
        """Fit image to canvas size"""
        if not hasattr(self, 'original_image') or not self.original_image:
            return
        
        try:
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # Canvas not ready, try again later
                self.root.after(100, self._fit_image)
                return
            
            img_width, img_height = self.original_image.size
            
            # Calculate scale to fit
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            self.image_scale = min(scale_x, scale_y) * 0.9  # 90% to leave some margin
            
            self._update_image_display()
        except Exception as e:
            print(f"Error fitting image: {e}")

    def _rotate_image(self):
        """Rotate the current image by 90 degrees"""
        if hasattr(self, 'original_image') and self.original_image:
            self.image_rotation = (self.image_rotation + 90) % 360
            self._update_image_display()

    def _update_image_display(self):
        """Update the image display with current scale and rotation"""
        if not hasattr(self, 'original_image') or not self.original_image:
            return
        
        try:
            # Apply rotation if needed
            if hasattr(self, 'image_rotation') and self.image_rotation != 0:
                rotated = self.original_image.rotate(self.image_rotation, expand=True)
            else:
                rotated = self.original_image
            
            # Apply scaling
            scale = getattr(self, 'image_scale', 1.0)
            new_width = int(rotated.size[0] * scale)
            new_height = int(rotated.size[1] * scale)
            
            if new_width > 0 and new_height > 0:
                resized = rotated.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                if PIL_AVAILABLE:
                    self.current_image = ImageTk.PhotoImage(resized)
                    
                    # Clear canvas and add image
                    self.image_canvas.delete("all")
                    self.image_id = self.image_canvas.create_image(
                        new_width // 2, new_height // 2, 
                        image=self.current_image, 
                        anchor="center"
                    )
                    
                    # Update scroll region
                    self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
                    
                    # Update info if label exists
                    if hasattr(self, 'image_info_label'):
                        rotation_text = f" | Rotation: {getattr(self, 'image_rotation', 0)}°" if hasattr(self, 'image_rotation') else ""
                        self.image_info_label.config(
                            text=f"{new_width}×{new_height} | Scale: {scale:.1f}x{rotation_text}"
                        )
        except Exception as e:
            print(f"Error updating image display: {e}")

    def _clear_image_preview(self):
        """Clear the image preview"""
        if hasattr(self, 'image_canvas'):
            self.image_canvas.delete("all")
        if hasattr(self, 'current_image'):
            self.current_image = None
        if hasattr(self, 'original_image'):
            self.original_image = None
        if hasattr(self, 'image_info_label'):
            self.image_info_label.config(text="")

    def _toggle_theme_animated(self):
        """Animated theme toggle with smooth transition"""
        self.progress_var.set("Switching theme...")
        
        # Smooth fade transition
        self._fade_transition(lambda: self._toggle_theme())
        
        self.root.after(300, lambda: self.progress_var.set("Ready"))

    def _fade_transition(self, callback):
        """Create a smooth fade transition effect"""
        # Disable interactions during transition
        self.root.config(cursor="wait")
        
        # Execute callback after short delay
        self.root.after(100, callback)
        self.root.after(200, lambda: self.root.config(cursor=""))

    def _apply_theme(self):
        """Apply the Monokai theme to all UI components including 3D buttons"""
        theme = get_theme(self.is_dark_mode)
        
        # Apply theme to main components
        self.main_container.config(bg=theme['bg'])
        self.header_frame.config(bg=theme['header_bg'])
        self.header_content.config(bg=theme['header_bg'])
        
        # Apply Monokai theme to 3D buttons
        if self.is_dark_mode:
            # Monokai dark theme button styling
            button_bg = theme['button_bg']      # #49483E
            button_fg = theme['button_fg']      # #F8F8F2
            button_hover = theme['accent']      # #66D9EF (cyan)
            button_active = theme['highlight']  # #FD971F (orange)
        else:
            # Light Monokai variant
            button_bg = theme['button_bg']
            button_fg = theme['button_fg']
            button_hover = theme['button_hover']
            button_active = theme['button_active']
        
        # Update theme toggle button with Monokai colors
        self.theme_toggle.config(
            bg=button_bg,
            fg=button_fg,
            activebackground=button_hover,
            activeforeground=theme['bg'] if self.is_dark_mode else '#FFFFFF'
        )
        
        # Update quick access button with Monokai colors
        self.quick_access.config(
            bg=button_bg,
            fg=button_fg,
            activebackground=button_hover,
            activeforeground=theme['bg'] if self.is_dark_mode else '#FFFFFF'
        )
        
        # Apply theme to navigation buttons
        for btn in self.nav_buttons:
            btn.config(
                bg=button_bg,
                fg=button_fg,
                activebackground=button_hover,
                activeforeground=theme['bg'] if self.is_dark_mode else '#FFFFFF'
            )
        
        # Apply theme to path entry
        self.path_entry.config(
            bg=theme['entry_bg'],
            fg=theme['entry_fg'],
            insertbackground=theme['accent'],  # Cursor color
            selectbackground=theme['select_bg'],
            selectforeground=theme['select_fg']
        )
        
        # Apply theme to search entry
        self.search_entry.config(
            bg=theme['entry_bg'],
            fg=theme['entry_fg'],
            insertbackground=theme['accent'],
            selectbackground=theme['select_bg'],
            selectforeground=theme['select_fg']
        )
        
        # Apply theme to tree headers and labels
        self.tree_header.config(
            bg=theme['bg'],
            fg=theme['accent']  # Use cyan for headers
        )
        
        self.preview_header.config(
            bg=theme['bg'],
            fg=theme['accent']
        )
        
        # Apply theme to separators
        self.tree_separator.config(bg=theme['separator'])
        self.preview_separator.config(bg=theme['separator'])
        self.status_separator.config(bg=theme['separator'])
        
        # Apply theme to text areas
        self.preview_text.config(
            bg=theme['code_bg'],  # Use code background
            fg=theme['code_fg'],
            insertbackground=theme['accent'],
            selectbackground=theme['select_bg'],
            selectforeground=theme['select_fg']
        )
        
        # Apply theme to status bar
        self.status_label.config(
            bg=theme['bg'],
            fg=theme['fg']
        )
        
        self.progress_indicator.config(
            bg=theme['bg'],
            fg=theme['comment']  # Use comment color for secondary text
        )
        
        # Apply theme to image canvas
        self.image_canvas.config(
            bg=theme['bg']
        )
        
        # Apply theme to image info label
        self.image_info_label.config(
            bg=theme['bg'],
            fg=theme['comment']
        )
        
        # Update tree styling with Monokai colors
        style = ttk.Style()
        
        # Configure Monokai treeview
        style.configure("Enhanced.Treeview",
                       background=theme['tree_bg'],
                       foreground=theme['tree_fg'],
                       fieldbackground=theme['tree_bg'],
                       borderwidth=0,
                       relief='flat')
        
        style.configure("Enhanced.Treeview.Heading",
                       background=theme['header_bg'],
                       foreground=theme['accent'],  # Cyan headers
                       borderwidth=0,
                       relief='flat')
        
        style.map("Enhanced.Treeview",
                 background=[('selected', theme['select_bg'])],
                 foreground=[('selected', theme['select_fg'])])
        
        # Update logo theme
        if hasattr(self, 'logo') and self.logo:
            self.logo.update_theme(self.is_dark_mode)
        
        # Update fallback logo with Monokai colors
        if hasattr(self, 'fallback_logo'):
            self.fallback_logo.config(
                bg=theme['header_bg'],
                fg=theme['accent']  # Use cyan for logo text
            )

    def _add_3d_button_effects(self, button):
        """Add enhanced 3D hover and click effects with Monokai colors"""
        def on_enter(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                bg=theme['accent'],      # Monokai cyan on hover
                fg=theme['bg'],          # Dark text on cyan
                relief='raised',
                borderwidth=4
            )
            self._animate_3d_button_hover(button, True)
        
        def on_leave(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                bg=theme['button_bg'],
                fg=theme['button_fg'],
                relief='raised',
                borderwidth=3
            )
            self._animate_3d_button_hover(button, False)
        
        def on_press(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                relief='sunken',
                borderwidth=2,
                bg=theme['highlight'],   # Monokai orange when pressed
                fg=theme['bg']
            )
            self._animate_3d_button_press(button)
        
        def on_release(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                relief='raised',
                borderwidth=4,
                bg=theme['accent'],
                fg=theme['bg']
            )
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)

    def _show_quick_access(self):
        """Show quick access menu with Monokai theme"""
        try:
            theme = get_theme(self.is_dark_mode)
            
            quick_menu = tk.Toplevel(self.root)
            quick_menu.title("Quick Access")
            quick_menu.geometry("300x400")
            quick_menu.transient(self.root)
            quick_menu.grab_set()
            
            # Apply Monokai theme to dialog
            quick_menu.config(bg=theme['bg'])
            
            # Center the menu
            quick_menu.update_idletasks()
            x = (quick_menu.winfo_screenwidth() // 2) - (300 // 2)
            y = (quick_menu.winfo_screenheight() // 2) - (400 // 2)
            quick_menu.geometry(f"300x400+{x}+{y}")
            
            # Quick access content with Monokai styling
            main_frame = tk.Frame(quick_menu, bg=theme['bg'], padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            title = tk.Label(
                main_frame,
                text="⚡ Quick Access",
                font=('Segoe UI', 16, 'bold'),
                bg=theme['bg'],
                fg=theme['accent']  # Cyan title
            )
            title.pack(pady=(0, 20))
            
            # Quick actions with Monokai styling
            actions = [
                ("📁 Documents", lambda: self._navigate_to(os.path.expanduser("~/Documents"))),
                ("💾 Downloads", lambda: self._navigate_to(os.path.expanduser("~/Downloads"))),
                ("🖼️ Pictures", lambda: self._navigate_to(os.path.expanduser("~/Pictures"))),
                ("🎵 Music", lambda: self._navigate_to(os.path.expanduser("~/Music"))),
                ("🎬 Videos", lambda: self._navigate_to(os.path.expanduser("~/Videos"))),
                ("🖥️ Desktop", lambda: self._navigate_to(os.path.expanduser("~/Desktop"))),
            ]
            
            for text, command in actions:
                btn = tk.Button(
                    main_frame,
                    text=text,
                    command=lambda cmd=command: [cmd(), quick_menu.destroy()],
                    font=('Segoe UI', 11),
                    relief='flat',
                    borderwidth=0,
                    padx=20,
                    pady=10,
                    cursor='hand2',
                    bg=theme['button_bg'],
                    fg=theme['button_fg'],
                    activebackground=theme['accent'],
                    activeforeground=theme['bg']
                )
                btn.pack(fill=tk.X, pady=2)
                self._add_monokai_button_hover(btn)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open quick access: {str(e)}")

    def _add_monokai_button_hover(self, button):
        """Add Monokai-themed hover effects to buttons"""
        def on_enter(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                bg=theme['accent'],
                fg=theme['bg']
            )
        
        def on_leave(e):
            theme = get_theme(self.is_dark_mode)
            button.config(
                bg=theme['button_bg'],
                fg=theme['button_fg']
            )
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _on_search(self, event):
        """Handle search input with live filtering"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            # Show all items
            for item in self.tree.get_children():
                self.tree.item(item, tags=())
            return
        
        # Filter items
        for item in self.tree.get_children():
            item_text = self.tree.item(item, 'text').lower()
            if search_term in item_text:
                self.tree.item(item, tags=('match',))
            else:
                self.tree.item(item, tags=('hidden',))
        
        # Configure tags for visual feedback
        self.tree.tag_configure('match', background='#e8f4fd')
        self.tree.tag_configure('hidden', foreground='#cccccc')

    def _setup_tree_item_hover(self, item_id):
        """Setup hover effects for tree items"""
        def on_item_motion(event):
            item = self.tree.identify_row(event.y)
            if item != self.hover_item:
                if self.hover_item:
                    self.tree.item(self.hover_item, tags=())
                self.hover_item = item
                if item:
                    self.tree.item(item, tags=('hover',))
        
        # Configure hover tag
        self.tree.tag_configure('hover', background='#f0f8ff')
        self.tree.bind('<Motion>', on_item_motion)

    def _update_progress(self, message, percentage=None):
        """Update progress indicator with animation"""
        self.progress_var.set(message)
        
        if percentage is not None:
            self.progress_indicator.config(text=f"{percentage}%")
        else:
            # Animated loading dots
            self.loading_dots = (self.loading_dots + 1) % 4
            dots = "." * self.loading_dots
            self.progress_indicator.config(text=f"Loading{dots}")

    def _populate_tree_enhanced(self):
        """Enhanced tree population with better performance and UX"""
        try:
            # Clear existing items
            self.root.after(0, lambda: [self.tree.delete(item) for item in self.tree.get_children()])
            
            normalized_current_dir = os.path.normpath(self.current_dir)
            
            if not os.path.exists(normalized_current_dir):
                self.root.after(0, lambda: messagebox.showerror("Error", f"Directory not found: {normalized_current_dir}"))
                return
            
            items = os.listdir(normalized_current_dir)
            folders = []
            files = []
            
            # Progress tracking
            total_items = len(items)
            processed = 0
            
            # Separate folders and files with progress updates
            for item in items:
                if self.loading_cancelled:
                    return
                    
                item_path = os.path.join(normalized_current_dir, item)
                normalized_item_path = os.path.normpath(item_path)
                
                if os.path.isdir(normalized_item_path):
                    folders.append(item)
                else:
                    files.append(item)
                
                processed += 1
                if processed % 10 == 0:  # Update progress every 10 items
                    progress = int((processed / total_items) * 100)
                    self.root.after(0, lambda p=progress: self._update_progress("Analyzing files...", p))
            
            # Sort items
            folders.sort(key=str.lower)
            files.sort(key=str.lower)
            
            # Add items with progress feedback
            all_items = folders + files
            for i, item in enumerate(all_items):
                if self.loading_cancelled:
                    return
                
                is_folder = item in folders
                self.root.after(0, lambda name=item, folder=is_folder: self._add_tree_item(name, folder))
                
                # Update progress
                if i % 5 == 0:
                    progress = int((i / len(all_items)) * 100)
                    self.root.after(0, lambda p=progress: self._update_progress("Adding items...", p))
            
            # Final status update
            total_items = len(folders) + len(files)
            status_text = f"{len(folders)} folders • {len(files)} files • {total_items} total"
            
            self.root.after(0, lambda: [
                self.progress_var.set("Ready"),
                self.progress_indicator.config(text=status_text)
            ])
            
        except Exception as e:
            self.root.after(0, lambda: [
                messagebox.showerror("Error", f"Error loading directory: {str(e)}"),
                self.progress_var.set("Error loading directory")
            ])

    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_mode = not self.is_dark_mode
        self._apply_theme()
        
        # Update theme toggle button text
        if self.is_dark_mode:
            self.theme_toggle.config(text="☀️ Light")
        else:
            self.theme_toggle.config(text="🌙 Dark")

    def _ask_ai(self):
        """Open AI assistant dialog"""
        try:
            dialog = AIDialog(self.root, self.ai_assistant)
            
            # Set context if file is selected
            if self.current_selected_file:
                dialog.set_file_context(self.current_selected_file, self.current_file_content)
            
            dialog.show()
        except Exception as e:
            messagebox.showinfo("AI Assistant", f"AI feature temporarily unavailable: {str(e)}")

    def _go_back(self):
        """Go back in history with improved path handling"""
        try:
            if self.history_index > 0:
                self.history_index -= 1
                self.current_dir = os.path.normpath(self.history[self.history_index])
                self.path_var.set(self.current_dir)
                self._populate_tree_async()
                self.preview_text.delete(1.0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error going back: {str(e)}")
    
    def _go_up(self):
        """Go to parent directory with improved path handling"""
        try:
            parent_dir = os.path.dirname(self.current_dir)
            if parent_dir != self.current_dir:
                self._navigate_to(parent_dir)
        except Exception as e:
            messagebox.showerror("Error", f"Error going up: {str(e)}")
    
    def _go_home(self):
        """Go to home directory with improved path handling"""
        try:
            home_dir = os.path.expanduser("~")
            self._navigate_to(home_dir)
        except Exception as e:
            messagebox.showerror("Error", f"Error going home: {str(e)}")
    
    def _browse_folder(self):
        """Browse for folder with improved path handling"""
        try:
            folder = filedialog.askdirectory(
                initialdir=self.current_dir,
                title="Select Folder - Organizer Application"
            )
            if folder:
                # Normalize the selected path
                normalized_folder = os.path.normpath(folder)
                self._navigate_to(normalized_folder)
        except Exception as e:
            messagebox.showerror("Error", f"Error browsing folder: {str(e)}")

    def _show_current_file(self):
        """Show current file information with improved path handling"""
        if not self.current_selected_file:
            messagebox.showinfo("Current File", "No file selected.\n\nPlease select a file from the file list to view its information.")
            return
        
        try:
            # Normalize the path
            normalized_path = os.path.normpath(self.current_selected_file)
            
            if not os.path.exists(normalized_path):
                messagebox.showerror("Error", f"File not found: {normalized_path}")
                return
            
            file_name = os.path.basename(normalized_path)
            file_dir = os.path.dirname(normalized_path)
            file_size = os.path.getsize(normalized_path)
            
            from datetime import datetime
            modified_time = datetime.fromtimestamp(os.path.getmtime(normalized_path))
            created_time = datetime.fromtimestamp(os.path.getctime(normalized_path))
            
            # Get file extension and type
            file_ext = os.path.splitext(normalized_path)[1].lower()
            file_type = "Folder" if os.path.isdir(normalized_path) else f"{file_ext.upper()} File" if file_ext else "File"
            
            info_text = f"""📄 Current File Information

📁 Name: {file_name}
📂 Location: {file_dir}
📊 Size: {format_file_size(file_size)}
🏷️ Type: {file_type}
📅 Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}
📅 Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')}

📝 Full Path:
{normalized_path}"""
            
            messagebox.showinfo("Current File Information", info_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error getting file information:\n{str(e)}")

    def _rename_file(self):
        """Rename the selected file or folder with improved path handling"""
        if not self.current_selected_file:
            messagebox.showwarning("Rename", "No file selected.\n\nPlease select a file or folder from the file list to rename it.")
            return
        
        try:
            # Normalize the file path
            normalized_path = os.path.normpath(self.current_selected_file)
            
            if not os.path.exists(normalized_path):
                messagebox.showerror("Error", f"File not found: {normalized_path}")
                return
            
            current_name = os.path.basename(normalized_path)
            parent_dir = os.path.dirname(normalized_path)
            
            # Simple rename dialog
            new_name = simpledialog.askstring(
                "Rename File", 
                f"Enter new name for:\n{current_name}",
                initialvalue=current_name
            )
            
            if new_name and new_name != current_name:
                new_path = os.path.join(parent_dir, new_name)
                new_normalized_path = os.path.normpath(new_path)
                
                if os.path.exists(new_normalized_path):
                    messagebox.showerror("Error", f"A file or folder named '{new_name}' already exists")
                    return
                
                try:
                    os.rename(normalized_path, new_normalized_path)
                    messagebox.showinfo("Success", f"Successfully renamed to:\n{new_name}")
                    
                    # Update current selected file path
                    self.current_selected_file = new_normalized_path
                    
                    # Refresh the file list
                    self._populate_tree_async()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to rename file:\n{str(e)}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error setting up rename:\n{str(e)}")

    def _bind_events(self):
        """Bind event handlers"""
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)  # Use TreeviewSelect event
        self.tree.bind('<Button-1>', self._on_click_capture)  # Capture clicks for immediate feedback
        self.path_entry.bind('<Return>', self._navigate_to_path)

    def _on_single_click(self, event):
        """Handle file selection with immediate preview update"""
        selection = self.tree.selection()
        if not selection:
            self.current_selected_file = None
            self.current_file_content = None
            # Clear preview when nothing is selected
            self._clear_preview()
            return
        
        item = self.tree.item(selection[0])
        item_name = self._extract_item_name(item['text'])
        item_path = os.path.join(self.current_dir, item_name)
        
        # Update selected file immediately
        self.current_selected_file = item_path
        
        # Clear any previous content
        self.current_file_content = None
        
        # Preview the file immediately if it's not a directory
        if not os.path.isdir(item_path):
            # Force immediate preview update
            self.root.after_idle(lambda: self._preview_file(item_path))
        else:
            # Clear preview for directories
            self._clear_preview()
            self.current_file_content = None

    def _clear_preview(self):
        """Clear all preview content"""
        # Clear text preview
        self.preview_text.delete(1.0, tk.END)
        
        # Clear image preview
        self._clear_image_preview()
        
        # Show default placeholder
        self._show_default_preview()

    def _show_default_preview(self):
        """Show default preview content when no file is selected"""
        default_content = """
📁 No File Selected

Select a file from the list to preview its content.

✨ Available Features:
  📄 Text & Code Preview
  🖼️ Image Viewing with Zoom
  📊 Detailed File Properties
  📋 Copy & Search Functions

👆 Click on any file to start!
"""
        
        self.preview_text.insert(1.0, default_content)

    def _preview_file(self, file_path):
        """Preview file content with improved synchronization"""
        # Verify this is still the selected file to prevent race conditions
        if self.current_selected_file != file_path:
            return  # Another file was selected, skip this preview
        
        # Clear existing content first
        self.preview_text.delete(1.0, tk.END)
        self._clear_image_preview()
        
        try:
            normalized_path = os.path.normpath(file_path)
            
            if not os.path.exists(normalized_path):
                error_msg = f"❌ File not found: {normalized_path}"
                self.preview_text.insert(tk.END, error_msg)
                return
            
            # Verify again that this is still the selected file
            if self.current_selected_file != file_path:
                return
            
            file_name = os.path.basename(normalized_path)
            file_size = os.path.getsize(normalized_path)
            file_ext = os.path.splitext(normalized_path)[1].lower()
            
            from datetime import datetime
            file_modified = datetime.fromtimestamp(os.path.getmtime(normalized_path))
            
            # Show file info header immediately
            header = [
                f"📋 {file_name}",
                f"📊 {format_file_size(file_size)}",
                f"📅 {file_modified.strftime('%Y-%m-%d %H:%M:%S')}",
                f"📁 {normalized_path}",
                "─" * 50,
                ""
            ]
            
            # Add size warning for large files
            if file_size > 1024 * 1024:  # 1MB
                header.insert(-1, f"⚠️ Large file detected - showing preview")
                header.insert(-1, "")
            
            self.preview_text.insert(tk.END, "\n".join(header))
            
            # Check again before processing
            if self.current_selected_file != file_path:
                return
            
            # Check if file is too large for any preview
            if file_size > 50 * 1024 * 1024:  # 50MB absolute limit
                self.preview_text.insert(tk.END, "⚠️ File too large for preview (>50MB)")
                self.current_file_content = None
                return
            
            # Handle image files - show in image tab
            if is_image_file(normalized_path):
                # Check one more time before switching tabs
                if self.current_selected_file != file_path:
                    return
                
                self._preview_image_file(normalized_path)
                self.preview_notebook.select(1)  # Switch to image tab
                
                # Add image info to text tab
                try:
                    if PIL_AVAILABLE:
                        with Image.open(normalized_path) as img:
                            width, height = img.size
                            mode = img.mode
                            format_name = img.format
                        
                        image_info = f"""🖼️ Image Information:

📏 Dimensions: {width} × {height} pixels
🎨 Color Mode: {mode}
📁 Format: {format_name}
💾 File Size: {format_file_size(file_size)}

📝 Image successfully loaded in Image tab.
Use zoom controls to adjust view."""
                        
                        self.preview_text.insert(tk.END, image_info)
                        self.current_file_content = image_info
                except Exception as e:
                    error_info = f"🖼️ Image file detected but couldn't read properties: {str(e)}"
                    self.preview_text.insert(tk.END, error_info)
                    self.current_file_content = error_info
                return
            
            # Handle other file types in text tab
            self.preview_notebook.select(0)  # Switch to text tab
            
            # Check one final time before loading content
            if self.current_selected_file != file_path:
                return
            
            # Load content based on file type
            content = None
            
            # Office files
            if file_ext in ['.docx', '.doc']:
                content = self._preview_office_file(normalized_path, 'docx')
            elif file_ext in ['.xlsx', '.xls']:
                content = self._preview_office_file(normalized_path, 'xlsx')
            elif file_ext in ['.pptx', '.ppt']:
                content = self._preview_office_file(normalized_path, 'pptx')
            elif file_ext == '.pdf':
                content = self._preview_office_file(normalized_path, 'pdf')
            # Handle text files
            elif is_text_file(normalized_path):
                content = self._preview_text_file(normalized_path)
            else:
                content = self._preview_binary_file(normalized_path)
            
            # Final check before displaying content
            if self.current_selected_file == file_path and content:
                self.preview_text.insert(tk.END, content)
                # Store content for AI
                if file_size > 1024 * 1024:  # 1MB
                    self.current_file_content = content[:5000] + "\n\n[Content truncated - large file]"
                else:
                    self.current_file_content = content
                
        except Exception as e:
            # Only show error if this is still the selected file
            if self.current_selected_file == file_path:
                error_msg = f"❌ Error previewing file: {str(e)}"
                self.preview_text.insert(tk.END, error_msg)
                self.current_file_content = None

    def _preview_office_file(self, file_path, file_type):
        """Preview office files with better error handling"""
        try:
            if file_type == 'docx':
                return self.office_reader.read_docx(file_path)
            elif file_type == 'xlsx':
                return self.office_reader.read_xlsx(file_path)
            elif file_type == 'pptx':
                return self.office_reader.read_pptx(file_path)
            elif file_type == 'pdf':
                return self.office_reader.read_pdf(file_path)
            else:
                return f"📄 {file_type.upper()} File\n\n⚠️ Unsupported office file format"
                    
        except Exception as e:
            return f"📄 {file_type.upper()} File\n\n❌ Error reading file: {str(e)}"

    def _preview_text_file(self, file_path):
        """Preview text files with better handling"""
        try:
            content, error = read_text_file(file_path)
            if content is not None:
                # Truncate very long content for display
                if len(content) > 50000:  # 50KB limit for display
                    return content[:50000] + "\n\n... [Content truncated for display]"
                return content
            else:
                return f"❌ Error reading text file: {error}"
                
        except Exception as e:
            return f"❌ Error reading text file: {str(e)}"

    def _preview_binary_file(self, file_path):
        """Preview binary files with file information"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            file_size = os.path.getsize(file_path)
            
            # Try to identify file type
            file_type_info = {
                '.exe': '⚙️ Windows Executable',
                '.dll': '🔧 Dynamic Link Library', 
                '.zip': '🗜️ ZIP Archive',
                '.rar': '📦 RAR Archive',
                '.7z': '🗜️ 7-Zip Archive',
                '.mp3': '🎵 MP3 Audio File',
                '.mp4': '🎬 MP4 Video File',
                '.avi': '📹 AVI Video File',
                '.mov': '🎬 QuickTime Video',
                '.wav': '🎼 WAV Audio File',
                '.flac': '🎼 FLAC Audio File (Lossless)',
            }
            
            file_description = file_type_info.get(file_ext, f'🔒 Binary File ({file_ext.upper()})')
            
            binary_info = f"""{file_description}

📊 File Size: {format_file_size(file_size)}
🏷️ Extension: {file_ext.upper()}

ℹ️ This is a binary file that cannot be displayed as text.

💡 Actions you can take:
  • Double-click to open with default application
  • Right-click for more options
  • Use file properties for detailed information
"""
            
            # For some file types, try to extract basic metadata
            if file_ext in ['.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac']:
                binary_info += f"\n🎵 Media file detected - use media player to view content"
            elif file_ext in ['.zip', '.rar', '.7z']:
                binary_info += f"\n📦 Archive file detected - extract to view contents"
            elif file_ext in ['.exe', '.msi']:
                binary_info += f"\n⚙️ Executable file - scan for viruses before running"
                
            return binary_info
            
        except Exception as e:
            return f"🔒 Binary file - cannot preview content\n\nError: {str(e)}"

    def _preview_image_file(self, file_path):
        """Preview image file in the image tab"""
        if not PIL_AVAILABLE:
            self.image_info_label.config(text="PIL not available for image preview")
            return
        
        try:
            # Load and display image
            self.original_image = Image.open(file_path)
            self.image_scale = 1.0
            self.image_rotation = 0
            
            # Update image info
            width, height = self.original_image.size
            self.image_info_label.config(
                text=f"{width}×{height} | {self.original_image.format} | {self.original_image.mode}"
            )
            
            # Fit image to canvas initially
            self._fit_image()
            
        except Exception as e:
            self.image_info_label.config(text=f"Error loading image: {str(e)}")
            # Show error in text tab too
            error_msg = f"🖼️ Image file detected but failed to load: {str(e)}"
            self.preview_text.insert(tk.END, error_msg)

    def _animate_3d_button_hover(self, button, entering):
        """Enhanced 3D button hover animation with shadow effects"""
        if not self.animation_active:
            self.animation_active = True
            
            if entering:
                # Simulate raising the button with subtle color shift
                current_bg = button.cget('bg')
                # Add slight highlight
                self.root.after(25, lambda: self._lighten_button_color(button, current_bg))
            else:
                # Return to normal state
                theme = get_theme(self.is_dark_mode)
                self.root.after(25, lambda: button.config(bg=theme.get('button_bg', '#e8e8e8')))
            
            self.root.after(100, lambda: setattr(self, 'animation_active', False))

    def _animate_3d_button_press(self, button):
        """Enhanced 3D button press animation with depth effect"""
        # Create pressed effect with color darkening
        original_bg = button.cget('bg')
        
        # Darken the button color to simulate depth
        self.root.after(25, lambda: button.config(bg='#a0a0a0'))
        self.root.after(75, lambda: button.config(bg=original_bg))

    def _lighten_button_color(self, button, base_color):
        """Lighten button color for 3D hover effect"""
        try:
            # Simple color lightening for 3D effect
            if base_color == '#e8e8e8':
                button.config(bg='#f0f0f0')
            elif 'button_hover' in str(base_color):
                button.config(bg='#e0f0e0')
        except:
            pass