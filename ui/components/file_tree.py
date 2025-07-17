"""
File Tree Component
"""

import tkinter as tk
from tkinter import ttk
import os

from core.file_operations import FileOperations


class FileTreeComponent:
    """File tree widget component"""
    
    def __init__(self, parent, on_select=None, on_double_click=None):
        self.parent = parent
        self.on_select_callback = on_select
        self.on_double_click_callback = on_double_click
        self.current_directory = None
        
        self._create_widgets()
        self._bind_events()
    
    def _create_widgets(self):
        """Create the tree widget with hierarchical support"""
        # Container frame
        self.container = tk.Frame(self.parent)
        self.container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(8, 15))
        
        # Configure enhanced tree style with hierarchy support
        style = ttk.Style()
        style.configure("Enhanced.Treeview", 
                       font=('Segoe UI', 10),
                       rowheight=32,  # Taller rows for better hierarchy
                       borderwidth=0,
                       relief='flat',
                       fieldbackground='white')
        style.configure("Enhanced.Treeview.Heading", 
                       font=('Segoe UI', 11, 'bold'), 
                       padding=(10, 10),
                       borderwidth=0,
                       relief='flat')
        
        # Enhanced selection and hierarchy colors
        style.map("Enhanced.Treeview",
                 background=[('selected', '#0078d4'), ('focus', '#e8f4fd')],
                 foreground=[('selected', 'white')])
        
        # Create tree with hierarchical features
        self.tree = ttk.Treeview(
            self.container,
            columns=('size', 'modified', 'type'),
            show='tree headings',
            style="Enhanced.Treeview"
        )
        
        # Configure columns with better spacing
        self.tree.heading('#0', text='📁 Name', anchor='w')
        self.tree.heading('size', text='📊 Size', anchor='center')
        self.tree.heading('modified', text='📅 Modified', anchor='center')
        self.tree.heading('type', text='🏷️ Type', anchor='center')
        
        self.tree.column('#0', width=350, minwidth=250)  # Wider for hierarchy
        self.tree.column('size', width=90, minwidth=80, anchor='center')
        self.tree.column('modified', width=140, minwidth=120, anchor='center')
        self.tree.column('type', width=120, minwidth=100, anchor='center')
        
        # Enhanced scrollbars
        v_scroll = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self.container, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )
        
        # Pack components with hierarchy support
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add hierarchy visual enhancements
        self._setup_hierarchy_features()
    
    def _setup_hierarchy_features(self):
        """Setup hierarchical tree features"""
        # Enable folder expansion
        self.tree.bind('<<TreeviewOpen>>', self._on_folder_expand)
        self.tree.bind('<<TreeviewClose>>', self._on_folder_collapse)
        
        # Add hover effects for better visual feedback
        self.tree.bind('<Motion>', self._on_tree_motion)
        self.tree.bind('<Leave>', self._on_tree_leave)
        
        # Configure hierarchy tags
        self.tree.tag_configure('folder', foreground='#0066cc')
        self.tree.tag_configure('file', foreground='#333333')
        self.tree.tag_configure('hover', background='#f0f8ff')
        self.tree.tag_configure('large_file', foreground='#cc6600')
        self.tree.tag_configure('hidden', foreground='#999999')

    def populate_with_hierarchy(self, directory_path, show_hidden=False):
        """Populate tree with hierarchical folder structure"""
        self.current_directory = directory_path
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            folders, files, error = self._get_directory_contents(directory_path, show_hidden)
            
            if error:
                return 0, 0, error
            
            # Add folders first with hierarchy support
            folder_items = []
            for folder in folders:
                item_id = self._add_hierarchical_item(folder, is_folder=True)
                if item_id:
                    folder_items.append(item_id)
                    # Pre-populate expandable folders
                    self._add_folder_placeholder(item_id, folder)
            
            # Add files with enhanced icons
            for file in files:
                self._add_hierarchical_item(file, is_folder=False)
            
            return len(folders), len(files), None
            
        except Exception as e:
            return 0, 0, str(e)

    def _add_hierarchical_item(self, item_name, is_folder=False, parent=''):
        """Add item with hierarchical support and enhanced visuals"""
        item_path = os.path.join(self.current_directory, item_name)
        
        try:
            # Get enhanced file info
            file_info = self._get_enhanced_file_info(item_path, is_folder)
            
            if not file_info:
                return None
            
            # Create display text with better visual hierarchy
            if is_folder:
                display_text = f"{file_info['icon']}  {item_name}"
                values = ('--', file_info['modified_formatted'], file_info['type'])
                tags = ('folder',)
                
                # Check if folder has many items for visual cue
                try:
                    item_count = len(os.listdir(item_path))
                    if item_count > 50:
                        display_text += f" ({item_count} items)"
                except:
                    pass
            else:
                display_text = f"  {file_info['icon']}  {item_name}"  # Indent files
                values = (file_info['size_formatted'], file_info['modified_formatted'], file_info['type'])
                
                # Add tags based on file characteristics
                tags = ['file']
                if file_info['size'] > 100 * 1024 * 1024:  # > 100MB
                    tags.append('large_file')
                if item_name.startswith('.'):
                    tags.append('hidden')
            
            # Insert item with hierarchy support
            item_id = self.tree.insert(
                parent, 'end', 
                text=display_text, 
                values=values,
                tags=tags,
                open=False  # Folders start collapsed
            )
            
            return item_id
            
        except Exception as e:
            print(f"Error adding hierarchical item {item_name}: {e}")
            return None

    def _add_folder_placeholder(self, folder_item_id, folder_name):
        """Add placeholder for expandable folders"""
        folder_path = os.path.join(self.current_directory, folder_name)
        
        try:
            # Check if folder has contents
            contents = os.listdir(folder_path)
            if contents:
                # Add a placeholder that will be replaced when expanded
                self.tree.insert(folder_item_id, 'end', text='Loading...', values=('', '', ''))
        except (PermissionError, OSError):
            # Add indicator for inaccessible folders
            self.tree.insert(folder_item_id, 'end', text='🔒 Access Denied', values=('', '', ''))

    def _on_folder_expand(self, event):
        """Handle folder expansion with dynamic loading"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return
        
        # Get folder path
        folder_name = self._extract_item_name(self.tree.item(item, 'text'))
        folder_path = os.path.join(self.current_directory, folder_name)
        
        # Remove placeholder
        children = self.tree.get_children(item)
        for child in children:
            self.tree.delete(child)
        
        # Load actual contents
        try:
            contents = os.listdir(folder_path)
            folders = [f for f in contents if os.path.isdir(os.path.join(folder_path, f))]
            files = [f for f in contents if os.path.isfile(os.path.join(folder_path, f))]
            
            # Sort and add items
            folders.sort(key=str.lower)
            files.sort(key=str.lower)
            
            # Temporarily change current directory context
            old_dir = self.current_directory
            self.current_directory = folder_path
            
            # Add folders and files
            for folder in folders[:20]:  # Limit for performance
                child_id = self._add_hierarchical_item(folder, is_folder=True, parent=item)
                if child_id:
                    self._add_folder_placeholder(child_id, folder)
            
            for file in files[:50]:  # Limit for performance
                self._add_hierarchical_item(file, is_folder=False, parent=item)
            
            # Show truncation message if needed
            total_hidden = len(folders) + len(files) - 70
            if total_hidden > 0:
                self.tree.insert(item, 'end', 
                               text=f"... and {total_hidden} more items", 
                               values=('', '', ''),
                               tags=('hidden',))
            
            # Restore directory context
            self.current_directory = old_dir
            
        except (PermissionError, OSError) as e:
            self.tree.insert(item, 'end', 
                           text=f"🔒 Error: {str(e)}", 
                           values=('', '', ''),
                           tags=('hidden',))

    def _on_folder_collapse(self, event):
        """Handle folder collapse"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return
        
        # Remove all children and add placeholder back
        children = self.tree.get_children(item)
        for child in children:
            self.tree.delete(child)
        
        # Add placeholder back
        folder_name = self._extract_item_name(self.tree.item(item, 'text'))
        self._add_folder_placeholder(item, folder_name)

    def _on_tree_motion(self, event):
        """Handle mouse motion over tree for hover effects"""
        item = self.tree.identify_row(event.y)
        
        # Remove old hover
        for tagged_item in self.tree.tag_has('hover'):
            tags = list(self.tree.item(tagged_item, 'tags'))
            if 'hover' in tags:
                tags.remove('hover')
            self.tree.item(tagged_item, tags=tags)
        
        # Add new hover
        if item:
            tags = list(self.tree.item(item, 'tags'))
            tags.append('hover')
            self.tree.item(item, tags=tags)

    def _on_tree_leave(self, event):
        """Handle mouse leaving tree"""
        # Remove all hover effects
        for tagged_item in self.tree.tag_has('hover'):
            tags = list(self.tree.item(tagged_item, 'tags'))
            if 'hover' in tags:
                tags.remove('hover')
            self.tree.item(tagged_item, tags=tags)

    def _get_enhanced_file_info(self, file_path, is_folder):
        """Get enhanced file information with better details"""
        try:
            stat = os.stat(file_path)
            
            from utils.file_utils import get_file_icon, format_file_size, get_file_type_description
            from datetime import datetime
            
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'size_formatted': format_file_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'modified_formatted': datetime.fromtimestamp(stat.st_mtime).strftime('%m/%d %H:%M'),
                'icon': get_file_icon(file_path),
                'type': get_file_type_description(file_path),
                'is_folder': is_folder
            }
        except Exception as e:
            print(f"Error getting file info for {file_path}: {e}")
            return None

    def populate(self, directory_path):
        """Populate tree with directory contents"""
        self.current_directory = directory_path
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        folders, files, error = FileOperations.list_directory(directory_path)
        
        if error:
            return 0, 0, error
        
        # Add folders
        for folder in folders:
            self._add_item(folder, is_folder=True)
        
        # Add files
        for file in files:
            self._add_item(file, is_folder=False)
        
        return len(folders), len(files), None
    
    def _add_item(self, item_name, is_folder=False):
        """Add an item to the tree"""
        item_path = os.path.join(self.current_directory, item_name)
        file_info = FileOperations.get_file_info(item_path)
        
        if file_info:
            display_text = f"{file_info['icon']} {item_name}"
            
            if is_folder:
                values = ('--', file_info['modified_formatted'])
            else:
                values = (file_info['size_formatted'], file_info['modified_formatted'])
            
            self.tree.insert('', 'end', text=display_text, values=values)
    
    def _on_select(self, event):
        """Handle item selection"""
        selection = self.tree.selection()
        if selection and self.on_select_callback:
            item = self.tree.item(selection[0])
            item_name = self._extract_item_name(item['text'])
            item_path = os.path.join(self.current_directory, item_name)
            self.on_select_callback(item_path)
    
    def _on_double_click(self, event):
        """Handle item double-click"""
        selection = self.tree.selection()
        if selection and self.on_double_click_callback:
            item = self.tree.item(selection[0])
            item_name = self._extract_item_name(item['text'])
            item_path = os.path.join(self.current_directory, item_name)
            self.on_double_click_callback(item_path)
    
    def _extract_item_name(self, display_text):
        """Extract actual item name from display text"""
        # Remove icon and get the name
        parts = display_text.split(' ', 1)
        return parts[1] if len(parts) > 1 else display_text
    
    def get_widget(self):
        """Get the tree widget for styling"""
        return self.tree

    def _bind_events(self):
        """Bind tree events"""
        self.tree.bind('<Button-1>', self._on_select)
        self.tree.bind('<Double-1>', self._on_double_click)

    def _get_directory_contents(self, directory_path, show_hidden=False):
        """Get directory contents with error handling"""
        try:
            items = os.listdir(directory_path)
            folders = []
            files = []
            
            for item in items:
                if not show_hidden and item.startswith('.'):
                    continue
                    
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    folders.append(item)
                else:
                    files.append(item)
            
            folders.sort(key=str.lower)
            files.sort(key=str.lower)
            
            return folders, files, None
            
        except (PermissionError, OSError) as e:
            return [], [], str(e)

    def _animate_3d_button_hover(self, button, entering):
        """Enhanced 3D button hover animation with shadow effects"""
        if not hasattr(self, 'animation_active'):
            self.animation_active = False
            
        if not self.animation_active:
            self.animation_active = True
            
            if entering:
                # Simulate raising the button with subtle color shift
                current_bg = button.cget('bg')
                # Add slight highlight
                self.parent.after(25, lambda: self._lighten_button_color(button, current_bg))
            else:
                # Return to normal state
                from config.themes import get_theme
                theme = get_theme(False)  # Default to light theme
                self.parent.after(25, lambda: button.config(bg=theme.get('button_bg', '#e8e8e8')))
            
            self.parent.after(100, lambda: setattr(self, 'animation_active', False))

    def _animate_3d_button_press(self, button):
        """Enhanced 3D button press animation with depth effect"""
        # Create pressed effect with color darkening
        original_bg = button.cget('bg')
        
        # Darken the button color to simulate depth
        self.parent.after(25, lambda: button.config(bg='#a0a0a0'))
        self.parent.after(75, lambda: button.config(bg=original_bg))

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
