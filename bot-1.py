import praw
import config
import time
import os
import sys

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    from tkinter.font import Font
    from PIL import Image, ImageTk
except ImportError as e:
    print("Error importing required modules:", e)
    sys.exit(1)

import threading

class RedditBotGUI:
    def __init__(self, root):
        self.running = False
        self.bot_thread = None
        self.reddit = None
        self.comments_replied = self.rep_com()
        
        self.background_image = None
        
        self.root = root
        self.root.title("Tilin Reddit Bot")
        self.root.geometry("800x600")
        
        self.configure_styles()
        self.setup_gui()
        self.log_message("Bot GUI initialized. Click 'Start Bot' to begin.")
        
    def configure_styles(self):
        self.COLORS = {
            'bg': '#2E3440',
            'fg': '#ECEFF4',
            'accent': '#88C0D0',
            'button': '#4C566A',
            'button_hover': '#5E81AC',
            'success': '#A3BE8C',
            'error': '#BF616A'
        }

        
        self.default_font = Font(family="Segoe UI", size=10)
        self.title_font = Font(family="Segoe UI", size=14, weight="bold")
        
        
        self.root.configure(bg=self.COLORS['bg'])
        
        
        style = ttk.Style()
        style.configure('TFrame', background=self.COLORS['bg'])
        style.configure('TLabel',
            background=self.COLORS['bg'],
            foreground=self.COLORS['fg'],
            font=self.default_font
        )
        style.configure('TButton',
            background=self.COLORS['button'],
            foreground=self.COLORS['fg'],
            padding=(20, 10),
            font=self.default_font
        )
        style.map('TButton',
            background=[('active', self.COLORS['button_hover'])]
        )
        
    def create_background(self, frame, image_path):
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Background image not found at {image_path}")
                
            # Load and resize image to fit frame
            image = Image.open(image_path)
            image = image.convert('RGBA')
            
            # Make overlay more transparent
            overlay = Image.new('RGBA', image.size, (46, 52, 64, 120))  # Reduced alpha value
            image = Image.alpha_composite(image, overlay)
            
            self.background_image = ImageTk.PhotoImage(image)
            
            canvas = tk.Canvas(
                frame,
                highlightthickness=0,
                bd=0,
            )
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # Create image on canvas
            canvas.create_image(0, 0, image=self.background_image, anchor='nw')
            
            return canvas
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            return frame
        
    def setup_gui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        
        title_label = ttk.Label(
            main_frame,
            text="Tilin Reddit Bot",
            font=self.title_font
        )
        title_label.pack(pady=(0, 20))
        
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Status: Ready",
            font=self.default_font
        )
        self.status_label.pack()
        
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=(0, 20))
        
        self.start_button = ttk.Button(
            control_frame,
            text="▶ Start Bot",
            command=self.start_bot
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            control_frame,
            text="⏹ Stop Bot",
            command=self.stop_bot,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Log Frame
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_label = ttk.Label(
            log_frame,
            text="Activity Log",
            font=self.default_font
        )
        log_label.pack(anchor=tk.W, pady=(0, 5))

        
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        # Add debug prints to verify paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "assets", "background.png")
        print(f"Looking for image at: {image_path}")
        print(f"File exists: {os.path.exists(image_path)}")
        
        # Fallback to solid color if image fails to load
        # Create transparent frame style before using it
        style = ttk.Style()
        style.configure('Transparent.TFrame', background='#2E3440')
        
        # Create container with style
        container = ttk.Frame(log_container, style='Transparent.TFrame')
        container.pack(fill=tk.BOTH, expand=True)
        
        # Replace the entire if os.path.exists(image_path) block with this:
        if os.path.exists(image_path):
            try:
                # Load and process image
                image = Image.open(image_path)
                image = image.convert('RGBA')
                
                # Create text widget directly
                self.log_area = scrolledtext.ScrolledText(
                    container,
                    height=15,
                    fg='#FFFFFF',
                    font=('Consolas', 11, 'bold'),
                    bd=0,
                    insertbackground='#FFFFFF',
                    selectbackground='#4C566A',
                    selectforeground='#FFFFFF',
                    relief=tk.FLAT,
                    highlightthickness=0
                )
                self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Create and store PhotoImage
                self.background_image = ImageTk.PhotoImage(image)
                
                # Configure text widget background
                self.log_area.configure(
                    bg='#2E3440',
                    insertbackground='white',
                )
                
                # Insert background image tag
                self.log_area.image_create('1.0', image=self.background_image)
                self.log_area.configure(state='disabled')  # Prevent editing background
                
                # Configure text display tag
                self.log_area.tag_configure('log_text', foreground='#FFFFFF', background='#2E3440')
                self.log_area.configure(state='normal')  # Allow text insertion again
                
            except Exception as e:
                print(f"Error setting up background: {e}")
                self.create_default_text_area(container)
        else:
            self.create_default_text_area(container)

    def create_default_text_area(self, container):
        """Fallback method to create default text area without background"""
        self.log_area = scrolledtext.ScrolledText(
            container,
            height=15,
            bg='#2E3440',
            fg='#FFFFFF',
            font=('Consolas', 11, 'bold'),
            bd=0,
            insertbackground='#FFFFFF',
            selectbackground='#4C566A',
            selectforeground='#FFFFFF',
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def bot_login(self):
        try:
            if not os.path.exists('config.py'):
                self.log_message("Error: config.py not found! Please copy config.example.py to config.py and fill in your credentials.")
                return None
                
            self.status_label.config(text="Status: Connecting to Reddit...")
            self.root.update()
            
            reddit = praw.Reddit(
                username=config.username,
                password=config.password,
                client_id=config.client_id,
                client_secret=config.client_secret,
                user_agent="El Tilin Reddit Bot v0.1"
            )
            
            # Verify credentials
            try:
                reddit.user.me()
            except:
                self.log_message("Error: Invalid Reddit credentials!")
                return None
                
            return reddit
            
        except Exception as e:
            self.log_message(f"Login Error: {str(e)}")
            self.status_label.config(text="Status: Login Failed!")
            return None
        
    def log_message(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n", 'log_text')
        self.log_area.see(tk.END)
        
    def rep_com(self):
        if not os.path.isfile("comments_replied.txt"):
            return []
        with open("comments_replied.txt", "r") as f:
            comments = f.read().split("\n")
            return list(filter(None, comments))

    def bot_loop(self):
        while self.running:
            try:
                for comment in self.reddit.subreddit("ToothpasteBoys").comments(limit=25):
                    if ("Ralsei" in comment.body or "Kris" in comment.body) and \
                       comment.id not in self.comments_replied and \
                       comment.author != self.reddit.user.me():
                        
                        self.log_message("Toothpaste boy detected")
                        comment.reply("💗")
                        self.log_message(f"Toothpaste boy showered with love {comment.id}")
                        
                        self.comments_replied.append(comment.id)
                        with open("comments_replied.txt", "a") as f:
                            f.write(comment.id + "\n")
                
                time.sleep(5)  
                
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                time.sleep(5)

    def start_bot(self):
        try:
            self.reddit = self.bot_login()
            if not self.reddit:
                return
                
            self.running = True
            self.bot_thread = threading.Thread(target=self.bot_loop)
            self.bot_thread.daemon = True  # Make thread close with main window
            self.bot_thread.start()
            
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Running")
            self.status_label.configure(foreground=self.COLORS['success'])
            self.log_message("Bot started!")
            
        except Exception as e:
            self.log_message(f"Start Error: {str(e)}")
            self.status_label.config(text="Status: Start Failed!")

    def stop_bot(self):
        self.status_label.config(text="Status: Stopping...")
        self.running = False
        if self.bot_thread:
            self.bot_thread.join(timeout=2.0)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Ready")
        self.status_label.configure(foreground=self.COLORS['fg'])
        self.log_message("Bot stopped!")

if __name__ == "__main__":
    print("Starting GUI application...")
    try:
        root = tk.Tk()
        print("Tkinter window created")
        app = RedditBotGUI(root)
        print("GUI initialized")
        root.protocol("WM_DELETE_WINDOW", root.quit)  
        print("Starting mainloop...")
        root.mainloop()
        print("Mainloop ended")
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)
