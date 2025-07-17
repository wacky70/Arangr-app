"""
AI Assistant - OpenAI API integration for file analysis and questions
"""

import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import threading

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIAssistant:
    """AI Assistant for file analysis and general questions"""
    
    def __init__(self):
        self.api_key = None
        self.client = None
        self.config_file = os.path.join(os.path.expanduser("~"), ".organizer_ai_config.json")
        self._load_api_key()
    
    def _load_api_key(self):
        """Load API key from encrypted config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = self._decrypt_key(config.get('api_key', ''))
                    if self.api_key and OPENAI_AVAILABLE:
                        self.client = openai.OpenAI(api_key=self.api_key)
        except Exception as e:
            print(f"Error loading API key: {e}")
    
    def _save_api_key(self, api_key):
        """Save API key to encrypted config file"""
        try:
            config = {'api_key': self._encrypt_key(api_key)}
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            self.api_key = api_key
            if OPENAI_AVAILABLE:
                self.client = openai.OpenAI(api_key=api_key)
            return True
        except Exception as e:
            print(f"Error saving API key: {e}")
            return False
    
    def _encrypt_key(self, key):
        """Simple encryption for API key storage"""
        # Basic encoding - in production, use proper encryption
        import base64
        return base64.b64encode(key.encode()).decode()
    
    def _decrypt_key(self, encrypted_key):
        """Simple decryption for API key retrieval"""
        try:
            import base64
            return base64.b64decode(encrypted_key.encode()).decode()
        except:
            return ""
    
    def setup_api_key(self, parent=None):
        """Setup or update OpenAI API key"""
        if not OPENAI_AVAILABLE:
            messagebox.showerror(
                "AI Assistant", 
                "OpenAI library not installed.\n\nInstall with: pip install openai"
            )
            return False
        
        # Create setup dialog
        dialog = tk.Toplevel(parent)
        dialog.title("AI Assistant Setup")
        dialog.geometry("500x300")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"500x300+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🤖 AI Assistant Setup", 
            font=('Segoe UI', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Instructions
        instructions = tk.Text(
            main_frame, 
            height=6, 
            wrap=tk.WORD, 
            font=('Segoe UI', 9),
            relief='flat',
            bg='#f8f9fa'
        )
        instructions.pack(fill=tk.X, pady=(0, 15))
        
        instructions.insert(tk.END, 
            "To use the AI Assistant feature, you need an OpenAI API key:\n\n"
            "1. Visit: https://platform.openai.com/api-keys\n"
            "2. Create an account or sign in\n"
            "3. Generate a new API key\n"
            "4. Paste your API key below\n\n"
            "Your API key will be stored securely on your local machine."
        )
        instructions.config(state=tk.DISABLED)
        
        # API Key input
        key_label = tk.Label(main_frame, text="OpenAI API Key:", font=('Segoe UI', 10, 'bold'))
        key_label.pack(anchor='w', pady=(10, 5))
        
        key_var = tk.StringVar(value=self.api_key or "")
        key_entry = tk.Entry(
            main_frame, 
            textvariable=key_var, 
            show="*", 
            font=('Consolas', 10),
            relief='flat',
            borderwidth=1,
            highlightthickness=1
        )
        key_entry.pack(fill=tk.X, ipady=5)
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def save_key():
            api_key = key_var.get().strip()
            if not api_key:
                messagebox.showerror("Error", "Please enter an API key")
                return
            
            if self._save_api_key(api_key):
                messagebox.showinfo("Success", "API key saved successfully!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to save API key")
        
        def test_key():
            api_key = key_var.get().strip()
            if not api_key:
                messagebox.showerror("Error", "Please enter an API key")
                return
            
            # Test the API key
            try:
                test_client = openai.OpenAI(api_key=api_key)
                response = test_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                messagebox.showinfo("Success", "API key is valid!")
            except Exception as e:
                messagebox.showerror("Error", f"API key test failed:\n{str(e)}")
        
        tk.Button(
            button_frame, 
            text="Test Key", 
            command=test_key,
            font=('Segoe UI', 9),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame, 
            text="Save", 
            command=save_key,
            font=('Segoe UI', 9, 'bold'),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy,
            font=('Segoe UI', 9),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT)
        
        return True
    
    def is_configured(self):
        """Check if AI assistant is properly configured"""
        return bool(self.api_key and self.client and OPENAI_AVAILABLE)
    
    def ask_question(self, question, file_content=None, file_name=None):
        """Ask AI a question, optionally about a specific file"""
        if not self.is_configured():
            return "❌ AI Assistant not configured. Please set up your OpenAI API key first."
        
        try:
            # Prepare the prompt
            if file_content and file_name:
                prompt = f"""I have a file named "{file_name}" with the following content:

```
{file_content[:4000]}  # Limit content to avoid token limits
```

Question: {question}

Please provide a helpful analysis or answer based on the file content."""
            else:
                prompt = question
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful file analysis assistant. Provide clear, concise, and useful responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error communicating with AI: {str(e)}"
    
    def analyze_file(self, file_path, file_content):
        """Provide automatic analysis of a file"""
        if not self.is_configured():
            return "❌ AI Assistant not configured."
        
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Prepare analysis prompt based on file type
        if file_ext in ['.py', '.js', '.html', '.css']:
            analysis_type = "code"
            prompt = f"Analyze this {file_ext} code file and provide insights about its structure, purpose, and any suggestions for improvement."
        elif file_ext in ['.txt', '.md']:
            analysis_type = "text"
            prompt = f"Analyze this text document and provide a summary of its content and key points."
        elif file_ext in ['.csv', '.xlsx']:
            analysis_type = "data"
            prompt = f"Analyze this data file and describe its structure and what insights can be gained from it."
        else:
            analysis_type = "general"
            prompt = f"Analyze this file and provide useful insights about its content and purpose."
        
        return self.ask_question(prompt, file_content, file_name)


class AIDialog:
    """Dialog for AI Assistant interactions"""
    
    def __init__(self, parent, ai_assistant, current_file=None, file_content=None):
        self.parent = parent
        self.ai_assistant = ai_assistant
        self.current_file = current_file
        self.file_content = file_content
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🤖 AI Assistant")
        self.dialog.geometry("700x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"700x500+{x}+{y}")
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the AI dialog UI"""
        main_frame = tk.Frame(self.dialog, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            header_frame, 
            text="🤖 AI Assistant", 
            font=('Segoe UI', 16, 'bold')
        )
        title_label.pack(side=tk.LEFT)
        
        if self.current_file:
            file_label = tk.Label(
                header_frame, 
                text=f"📄 {os.path.basename(self.current_file)}", 
                font=('Segoe UI', 10),
                fg='#666666'
            )
            file_label.pack(side=tk.RIGHT)
        
        # Chat area
        chat_frame = tk.Frame(main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.chat_text = tk.Text(
            chat_frame, 
            wrap=tk.WORD, 
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=1,
            highlightthickness=1,
            padx=10,
            pady=10
        )
        
        chat_scroll = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=chat_scroll.set)
        
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Input area
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, text="Ask a question:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        entry_frame = tk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.question_var = tk.StringVar()
        self.question_entry = tk.Entry(
            entry_frame, 
            textvariable=self.question_var,
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=1,
            highlightthickness=1
        )
        self.question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.question_entry.bind('<Return>', self._ask_question)
        
        ask_button = tk.Button(
            entry_frame, 
            text="Ask", 
            command=self._ask_question,
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=5
        )
        ask_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Quick actions
        action_frame = tk.Frame(main_frame)
        action_frame.pack(fill=tk.X)
        
        if self.current_file and self.file_content:
            tk.Button(
                action_frame, 
                text="📊 Analyze File", 
                command=self._analyze_file,
                font=('Segoe UI', 9),
                padx=15,
                pady=3
            ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            action_frame, 
            text="🔧 Setup API Key", 
            command=lambda: self.ai_assistant.setup_api_key(self.dialog),
            font=('Segoe UI', 9),
            padx=15,
            pady=3
        ).pack(side=tk.LEFT)
        
        tk.Button(
            action_frame, 
            text="Close", 
            command=self.dialog.destroy,
            font=('Segoe UI', 9),
            padx=15,
            pady=3
        ).pack(side=tk.RIGHT)
        
        # Initial message
        if not self.ai_assistant.is_configured():
            self._add_message("system", "⚠️ AI Assistant not configured. Click 'Setup API Key' to get started.")
        else:
            self._add_message("system", "🤖 AI Assistant ready! Ask me anything about your files or general questions.")
        
        self.question_entry.focus()
    
    def _add_message(self, sender, message):
        """Add a message to the chat"""
        self.chat_text.config(state=tk.NORMAL)
        
        if sender == "user":
            self.chat_text.insert(tk.END, f"👤 You: {message}\n\n")
        elif sender == "ai":
            self.chat_text.insert(tk.END, f"🤖 AI: {message}\n\n")
        else:
            self.chat_text.insert(tk.END, f"{message}\n\n")
        
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
    
    def _ask_question(self, event=None):
        """Ask AI a question"""
        question = self.question_var.get().strip()
        if not question:
            return
        
        self.question_var.set("")
        self._add_message("user", question)
        
        # Show thinking message
        self.chat_text.config(state=tk.NORMAL)
        thinking_start = self.chat_text.index(tk.END)
        self.chat_text.insert(tk.END, "🤖 AI: Thinking...\n\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
        # Ask AI in background thread
        def get_response():
            response = self.ai_assistant.ask_question(
                question, 
                self.file_content, 
                self.current_file
            )
            
            # Update UI in main thread
            self.dialog.after(0, lambda: self._update_response(thinking_start, response))
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def _analyze_file(self):
        """Analyze the current file"""
        if not self.current_file or not self.file_content:
            return
        
        self._add_message("user", f"Analyze file: {os.path.basename(self.current_file)}")
        
        # Show thinking message
        self.chat_text.config(state=tk.NORMAL)
        thinking_start = self.chat_text.index(tk.END)
        self.chat_text.insert(tk.END, "🤖 AI: Analyzing file...\n\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
        # Analyze in background thread
        def analyze():
            response = self.ai_assistant.analyze_file(self.current_file, self.file_content)
            self.dialog.after(0, lambda: self._update_response(thinking_start, response))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def _update_response(self, thinking_start, response):
        """Update the AI response, replacing the thinking message"""
        self.chat_text.config(state=tk.NORMAL)
        
        # Delete the thinking message
        self.chat_text.delete(thinking_start, tk.END)
        
        # Add the actual response
        self.chat_text.insert(tk.END, f"🤖 AI: {response}\n\n")
        
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
