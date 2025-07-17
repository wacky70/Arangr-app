# 🎯 Arangr Application

A professional file explorer application with animated 3D logo, dual themes, comprehensive file preview, and AI-powered assistance capabilities.

## ✨ Key Features

### 🎨 **Enhanced Visual Design**
- **3D Animated Logo** - Professional ARANGR banner with Monokai theming
- **Dual Theme System** - Seamless light/dark mode with Monokai color scheme
- **Responsive UI** - Clean, modern interface with smooth animations
- **Professional Typography** - Segoe UI fonts with enhanced readability

### 📄 **Comprehensive File Preview**
- **Office Documents** - Word (.docx), Excel (.xlsx), PowerPoint (.pptx)
- **PDF Support** - Text extraction and page navigation
- **Image Viewing** - Full-featured viewer with zoom, rotate, and fit controls
- **Text Files** - Syntax highlighting for 50+ programming languages
- **Binary Files** - Intelligent file type detection and metadata display

### 🤖 **AI Assistant Integration**
- **OpenAI GPT Integration** - Analyze files and answer questions
- **File Analysis** - Automatic code review and document summarization
- **Context-Aware** - Uses current file content for relevant responses
- **Secure Storage** - Encrypted API key storage on local machine

### 🚀 **Advanced File Management**
- **Enhanced File Tree** - Hierarchical navigation with content-aware icons
- **Live Search** - Real-time filtering with visual feedback
- **Smart Icons** - Content-based folder icons (images, code, media)
- **Performance Optimized** - Asynchronous loading and caching

## 🎨 Logo & Theming

### **3D ARANGR Banner**
- **Professional Design** - Rounded corners with 3D beveled effects
- **Monokai Integration** - Uses authentic Monokai color palette
- **Dynamic Sizing** - 250×60 banner format for optimal visibility
- **Theme Adaptive** - Automatically adjusts to light/dark mode

### **Monokai Theme System**
```
Dark Mode Colors:
  Background: #272822 (Monokai background)
  Text: #F8F8F2 (Monokai foreground)
  Accent: #66D9EF (Monokai cyan)
  Highlight: #FD971F (Monokai orange)
  Success: #A6E22E (Monokai green)
  Error: #F92672 (Monokai pink)
```

## 🚀 Quick Start

### **Installation**
```bash
# Core dependencies (required)
pip install Pillow

# Full feature set (recommended)
pip install -r requirements.txt
```

### **Running the Application**
```bash
# Windows (recommended)
run.bat

# Cross-platform
python main.py

# Full setup with dependency management
arangr.bat
```

### **AI Assistant Setup**
1. Get OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. Click "🤖 Ask AI" → "🔧 Setup API Key"
3. Enter your API key (stored securely locally)
4. Start analyzing files with AI assistance

## 📁 Project Structure

```
ARANGR/
├── main.py                 # 🚀 Application entry point
├── run.bat                 # 🖥️ Windows quick launcher
├── arangr.bat             # 🔧 Complete setup manager
├── logo.png               # 🎨 Your custom logo (auto-resized to 250×60)
├── requirements.txt        # 📦 Python dependencies
│
├── ui/                     # 🎨 User Interface Components
│   ├── main_window.py      # Main application window
│   ├── animated_logo.py    # 3D ARANGR banner with animations
│   └── components/         # Reusable UI components
│       ├── file_tree.py    # Enhanced hierarchical file tree
│       └── file_preview.py # Multi-format file preview system
│
├── core/                   # ⚙️ Core Application Logic
│   ├── office_reader.py    # Microsoft Office file processing
│   ├── ai_assistant.py     # OpenAI GPT integration
│   └── file_operations.py  # Advanced file management
│
├── utils/                  # 🔧 Utility Functions
│   └── file_utils.py       # File type detection and processing
│
└── config/                 # ⚙️ Configuration & Settings
    ├── themes.py           # Monokai theme definitions
    └── settings.py         # Application settings
```

## 🔧 Technical Features

### **Enhanced File Processing**
- **Smart Detection** - Automatic file type recognition for 100+ formats
- **Performance Caching** - LRU cache for icons, sizes, and metadata
- **Encoding Detection** - UTF-8, Latin-1, CP1252 support with fallbacks
- **Large File Handling** - Streaming for files >10MB with progress indicators

### **Advanced UI Components**
- **Hierarchical Tree View** - Expandable folders with lazy loading
- **Tabbed Preview System** - Text, Image, and Properties tabs
- **Responsive Design** - Adapts to different screen sizes
- **Keyboard Navigation** - Full keyboard shortcuts support

### **AI Integration Details**
- **GPT-3.5 Turbo** - Latest OpenAI model for analysis
- **Context Limits** - Smart content truncation for API efficiency
- **Error Handling** - Graceful fallbacks for API issues
- **Privacy First** - All processing respects user data privacy

## 📊 Supported File Types

### **📄 Documents**
- **Microsoft Office**: .docx, .xlsx, .pptx (full content extraction)
- **PDF**: Text extraction, page navigation, metadata
- **Text**: .txt, .md, .rtf with encoding detection
- **Code**: 50+ languages with syntax recognition

### **🖼️ Images**
- **Common**: .jpg, .png, .gif, .bmp, .svg
- **Professional**: .tiff, .webp, .ico
- **RAW**: .raw, .cr2, .nef, .dng (metadata only)
- **Modern**: .heic, .heif, .avif, .jxl

### **🎵 Media**
- **Audio**: .mp3, .wav, .flac, .aac, .ogg
- **Video**: .mp4, .avi, .mov, .mkv, .webm
- **Metadata**: Duration, resolution, codec information

### **📦 Archive**
- **Common**: .zip, .rar, .7z, .tar
- **Compressed**: .gz, .bz2, .xz
- **Disk Images**: .dmg, .iso

## 🛠️ Dependencies

### **Core (Required)**
```
Python >= 3.7
tkinter (bundled with Python)
Pillow >= 9.0.0 (image processing)
```

### **Office Support (Optional)**
```
python-docx >= 0.8.11 (Word documents)
openpyxl >= 3.0.9 (Excel spreadsheets)
python-pptx >= 0.6.21 (PowerPoint presentations)
PyPDF2 >= 3.0.1 (PDF documents)
```

### **AI Assistant (Optional)**
```
openai >= 1.0.0 (GPT integration)
```

### **Enhanced Features (Optional)**
```
chardet >= 4.0.0 (encoding detection)
```

## 🚀 Performance Features

- **Asynchronous Loading** - Non-blocking file operations
- **Smart Caching** - LRU cache for frequently accessed data
- **Lazy Loading** - Load content only when needed
- **Progress Indicators** - Visual feedback for long operations
- **Memory Management** - Efficient handling of large files

## 🔒 Security Features

- **Local Storage** - All data stays on your machine
- **Encrypted Config** - API keys stored with base64 encoding
- **Permission Checks** - Respects file system permissions
- **Safe Preview** - Sandboxed file content display

## 🌟 Recent Updates

### **Version 7.0.0 - Enhanced Professional Edition**
- ✅ **3D ARANGR Banner** - Professional logo with Monokai theming
- ✅ **AI Assistant Integration** - OpenAI GPT for file analysis
- ✅ **Enhanced File Preview** - Multi-tab system with zoom controls
- ✅ **Performance Optimization** - Async loading and smart caching
- ✅ **Monokai Theme System** - Complete dark/light mode integration
- ✅ **Hierarchical File Tree** - Expandable folders with content icons
- ✅ **Advanced File Support** - 100+ file types with metadata
- ✅ **Professional UI** - Modern design with smooth animations

---

**Version**: 7.0.0 (Enhanced Professional Edition)  
**Platform**: Windows, macOS, Linux  
**License**: MIT  
**Requirements**: Python 3.7+

*Professional file organization with AI assistance! 🎯📁🤖*
