import os
import csv
import requests
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from pathlib import Path
import threading
import queue
from PIL import Image, ImageTk

# Colors and styling constants
BACKGROUND_COLOR = "#000000"  # Black background
TEXT_COLOR = "#00FF00"  # Bright green text
ACCENT_COLOR = "#005500"  # Darker green for accents
FONT_FAMILY = "Courier"  # Terminal-like font

class CyberSkullsTheme:
    """Custom theme for the Cyber Skulls application"""
    
    @staticmethod
    def setup_theme():
        """Set up the custom theme for ttk widgets"""
        style = ttk.Style()
        
        # Configure the theme
        style.theme_create("cyberskulls", parent="alt", settings={
            "TFrame": {
                "configure": {"background": BACKGROUND_COLOR}
            },
            "TLabel": {
                "configure": {"background": BACKGROUND_COLOR, "foreground": TEXT_COLOR, "font": (FONT_FAMILY, 10)}
            },
            "TButton": {
                "configure": {"background": BACKGROUND_COLOR, "foreground": TEXT_COLOR, 
                             "borderwidth": 1, "relief": "raised", "font": (FONT_FAMILY, 10)},
                "map": {"background": [("active", ACCENT_COLOR)],
                       "foreground": [("active", TEXT_COLOR)]}
            },
            "TLabelframe": {
                "configure": {"background": BACKGROUND_COLOR, "foreground": TEXT_COLOR, 
                             "borderwidth": 1, "relief": "solid"}
            },
            "TLabelframe.Label": {
                "configure": {"background": BACKGROUND_COLOR, "foreground": TEXT_COLOR, 
                             "font": (FONT_FAMILY, 10, "bold")}
            },
            "TProgressbar": {
                "configure": {"background": TEXT_COLOR, "troughcolor": BACKGROUND_COLOR, 
                              "borderwidth": 1, "thickness": 20}
            },
            "TEntry": {
                "configure": {"background": BACKGROUND_COLOR, "foreground": TEXT_COLOR, 
                             "fieldbackground": "#111111", "insertbackground": TEXT_COLOR,
                             "font": (FONT_FAMILY, 10)}
            }
        })
        
        # Set the theme
        style.theme_use("cyberskulls")
        
        return style

class CyberSkullsDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Skulls NFT Downloader")
        self.root.geometry("900x700")
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Create a canvas for grid lines (must be created before other widgets)
        self.grid_canvas = tk.Canvas(self.root, bg=BACKGROUND_COLOR, 
                                   highlightthickness=0, bd=0)
        self.grid_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Set up the theme
        self.style = CyberSkullsTheme.setup_theme()
        
        # Default IPFS gateway
        self.ipfs_gateway = "https://ipfs.io/ipfs/"
        
        # Create a queue for log messages
        self.log_queue = queue.Queue()
        
        # Track selected files and output directory
        self.csv_files = []
        self.output_dir = ""
        
        # Load logo if it exists
        self.logo_image = None
        self.try_load_logo()
        
        # Create UI elements
        self.create_widgets()
        
        # Start log consumer
        self.consume_logs()
        
        # Add grid line effect
        self.create_grid_effect()
    
    def try_load_logo(self):
        """Try to load the logo image if it exists"""
        # First try the provided cs GLOW.png file
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        
        try:
            img = Image.open(logo_path)
            # Resize to appropriate dimensions
            img = img.resize((150, 150), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Could not load logo: {e}")
    
    def create_grid_effect(self):
        """Create a grid line effect in the background"""
        # Draw horizontal and vertical grid lines
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Function to update grid lines when window size changes
        def update_grid_lines(event=None):
            self.grid_canvas.delete("grid")
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # Draw horizontal lines
            for y in range(0, height, 40):
                self.grid_canvas.create_line(0, y, width, y, fill="#003300", 
                                           tags="grid", dash=(1, 5))
            
            # Draw vertical lines
            for x in range(0, width, 40):
                self.grid_canvas.create_line(x, 0, x, height, fill="#003300", 
                                           tags="grid", dash=(1, 5))
        
        # Bind resize event to update grid lines
        self.root.bind("<Configure>", update_grid_lines)
        
        # Initial drawing of grid lines
        self.root.update()
        update_grid_lines()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and logo frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add system ID in corner
        sys_id = ttk.Label(main_frame, text="[SYS.1]", foreground=TEXT_COLOR, font=(FONT_FAMILY, 8))
        sys_id.place(relx=1.0, rely=0, anchor="ne")
        
        # Add header
        header_label = ttk.Label(header_frame, text="■ CYBER_SKULLS_NFT_DOWNLOADER", 
                                font=(FONT_FAMILY, 18, "bold"))
        header_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add logo if it exists
        if self.logo_image:
            logo_label = ttk.Label(header_frame, image=self.logo_image, background=BACKGROUND_COLOR)
            logo_label.pack(side=tk.RIGHT, padx=5)
        
        # Terminal-style separator
        separator = ttk.Frame(main_frame, height=2, style="TSeparator")
        separator.pack(fill=tk.X, pady=5)
        
        # File operations frame with border
        file_ops_frame = ttk.LabelFrame(main_frame, text="■ NETWORK_OPERATIONS", padding="10")
        file_ops_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # File selection frame
        file_frame = ttk.Frame(file_ops_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        # CSV file selection
        csv_label = ttk.Label(file_frame, text="> SELECT_CSV_FILES:", 
                             font=(FONT_FAMILY, 10, "bold"))
        csv_label.pack(side=tk.LEFT, padx=(0, 10))
        
        csv_button = ttk.Button(file_frame, text="BROWSE", command=self.select_csv_files)
        csv_button.pack(side=tk.LEFT, padx=5)
        
        self.csv_label = ttk.Label(file_frame, text="NO_FILES_SELECTED")
        self.csv_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Output directory frame
        output_frame = ttk.Frame(file_ops_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        # Output directory selection
        output_label = ttk.Label(output_frame, text="> OUTPUT_LOCATION:", 
                                font=(FONT_FAMILY, 10, "bold"))
        output_label.pack(side=tk.LEFT, padx=(0, 10))
        
        output_button = ttk.Button(output_frame, text="BROWSE", command=self.select_output_dir)
        output_button.pack(side=tk.LEFT, padx=5)
        
        self.output_label = ttk.Label(output_frame, text="NO_DIRECTORY_SELECTED")
        self.output_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # IPFS Gateway frame
        gateway_frame = ttk.Frame(file_ops_frame)
        gateway_frame.pack(fill=tk.X, pady=5)
        
        gateway_label = ttk.Label(gateway_frame, text="> IPFS_GATEWAY:", 
                                 font=(FONT_FAMILY, 10, "bold"))
        gateway_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.gateway_var = tk.StringVar(value=self.ipfs_gateway)
        gateway_entry = tk.Entry(gateway_frame, textvariable=self.gateway_var, width=40,
                                bg="#111111", fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                font=(FONT_FAMILY, 10))
        gateway_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Action buttons in new frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=15)
        
        self.download_button = ttk.Button(action_frame, text="▶ INITIALIZE_DOWNLOAD", 
                                         command=self.start_download)
        self.download_button.pack(side=tk.RIGHT, padx=5)
        
        # Progress frame with border
        progress_frame = ttk.LabelFrame(main_frame, text="■ DOWNLOAD_STATUS", padding="10")
        progress_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="SYSTEM_READY")
        self.status_label.pack(anchor=tk.W, pady=2)
        
        # Log display with border
        log_frame = ttk.LabelFrame(main_frame, text="■ SYSTEM_LOG", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        # Create a custom scrolled text with the right styling
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD, 
                               bg="#111111", fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                               font=(FONT_FAMILY, 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        self.log_text.config(state=tk.DISABLED)
        
        # Add a footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=5)
        
        footer_text = ttk.Label(footer_frame, 
                              text="© CYBER_SKULLS_NETWORK // SECURE_CONNECTION_ESTABLISHED",
                              font=(FONT_FAMILY, 8))
        footer_text.pack(side=tk.RIGHT)
        
    def select_csv_files(self):
        """Open file dialog to select CSV files"""
        filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        filenames = filedialog.askopenfilenames(
            title="Select CSV Files",
            filetypes=filetypes
        )
        
        if filenames:
            self.csv_files = list(filenames)
            if len(self.csv_files) == 1:
                self.csv_label.config(text=os.path.basename(self.csv_files[0]))
            else:
                self.csv_label.config(text=f"{len(self.csv_files)} files selected")
            self.log(f"[SYSTEM] Selected {len(self.csv_files)} CSV files")
    
    def select_output_dir(self):
        """Open directory dialog to select output directory"""
        directory = filedialog.askdirectory(
            title="Select Output Folder"
        )
        
        if directory:
            self.output_dir = directory
            self.output_label.config(text=self.output_dir)
            self.log(f"[SYSTEM] Output folder set to: {self.output_dir}")
    
    def download_image(self, url, output_path, gateway_url):
        """Download an image from IPFS URL and save it to the specified path"""
        try:
            # Parse IPFS URL to extract CID
            if url.startswith("ipfs://"):
                # Extract the CID and handle any fragment identifier
                path = url[7:]  # Remove 'ipfs://' prefix
                
                # Handle fragment identifiers (like #i at the end)
                if '#' in path:
                    path = path.split("#")[0]
                
                # Create full gateway URL
                full_url = f"{gateway_url}{path}"
            else:
                self.log(f"[WARNING] Skipping non-IPFS URL: {url}")
                return False
            
            # Download the image
            self.log(f"[DOWNLOAD] Retrieving: {os.path.basename(output_path)}")
            response = requests.get(full_url, timeout=30)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                self.log(f"[SUCCESS] Downloaded: {os.path.basename(output_path)}")
                return True
            else:
                self.log(f"[ERROR] Failed to download {url}: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log(f"[ERROR] Error downloading {url}: {str(e)}")
            return False
    
    def process_csv_file(self, csv_file, output_dir, gateway_url):
        """Process a CSV file to download images"""
        try:
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Track success and failure counts
            success_count = 0
            fail_count = 0
            total_count = 0
            
            # First, count total rows for progress
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for _ in reader:
                    total_count += 1
            
            if total_count == 0:
                self.log(f"[WARNING] CSV file {os.path.basename(csv_file)} is empty or has invalid formatting")
                return 0, 0
            
            # Now process each row
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Check if the required columns exist
                required_columns = ["name", "unit-name", "url"]
                if not all(col in reader.fieldnames for col in required_columns):
                    missing = [col for col in required_columns if col not in reader.fieldnames]
                    self.log(f"[ERROR] CSV file {os.path.basename(csv_file)} is missing required columns: {', '.join(missing)}")
                    return 0, 0
                
                # Process each row
                current_row = 0
                for row in reader:
                    current_row += 1
                    
                    # Update progress
                    progress = int((current_row / total_count) * 100)
                    self.update_progress(progress, f"PROCESSING: {os.path.basename(csv_file)} [{current_row}/{total_count}]")
                    
                    name = row["name"].strip()
                    unit_name = row["unit-name"].strip()
                    url = row["url"].strip()
                    
                    if not url or not name or not unit_name:
                        continue
                    
                    # Create a filename-safe version of the name
                    safe_name = f"{name}_{unit_name}".replace("/", "_").replace("\\", "_")
                    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._- ")
                    
                    # Determine file extension based on mime type or default to .png
                    mime_type = row.get("metadata_mime_type", "").strip()
                    extension = ".png"  # Default extension
                    if mime_type:
                        if "jpeg" in mime_type or "jpg" in mime_type:
                            extension = ".jpg"
                        elif "png" in mime_type:
                            extension = ".png"
                        elif "gif" in mime_type:
                            extension = ".gif"
                    
                    output_path = os.path.join(output_dir, f"{safe_name}{extension}")
                    
                    # Download the image
                    success = self.download_image(url, output_path, gateway_url)
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
            
            return success_count, fail_count
        except Exception as e:
            self.log(f"[ERROR] Error processing {os.path.basename(csv_file)}: {str(e)}")
            return 0, 0
    
    def download_thread(self):
        """Background thread for downloading images"""
        try:
            gateway_url = self.gateway_var.get()
            if not gateway_url.endswith('/'):
                gateway_url += '/'
            
            self.log("[SYSTEM] Initializing download sequence...")
            self.update_progress(0, "PREPARING_DOWNLOAD...")
            
            # Process each CSV file
            total_success = 0
            total_fail = 0
            
            for i, csv_file in enumerate(self.csv_files):
                self.log(f"[SYSTEM] Processing file {i+1}/{len(self.csv_files)}: {os.path.basename(csv_file)}...")
                success, fail = self.process_csv_file(csv_file, self.output_dir, gateway_url)
                total_success += success
                total_fail += fail
            
            self.log("\n[REPORT] Download Summary:")
            self.log(f"[REPORT] Images successfully downloaded: {total_success}")
            self.log(f"[REPORT] Images failed to download: {total_fail}")
            self.log(f"[REPORT] Images saved to: {os.path.abspath(self.output_dir)}")
            
            self.update_progress(100, "DOWNLOAD_COMPLETE")
            messagebox.showinfo("Download Complete", f"Download operation complete!\n\nSuccessful: {total_success}\nFailed: {total_fail}")
        except Exception as e:
            self.log(f"[ERROR] Critical error during download: {str(e)}")
            messagebox.showerror("System Error", f"A critical error occurred during download: {str(e)}")
        finally:
            # Enable the download button again
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
    
    def start_download(self):
        """Start the download process in a background thread"""
        if not self.csv_files:
            messagebox.showwarning("Input Error", "Please select at least one CSV file")
            return
        
        if not self.output_dir:
            messagebox.showwarning("Input Error", "Please select an output folder")
            return
        
        # Disable the download button to prevent multiple clicks
        self.download_button.config(state=tk.DISABLED)
        
        # Clear the log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Start the download thread
        threading.Thread(target=self.download_thread, daemon=True).start()
    
    def log(self, message):
        """Add a message to the log queue"""
        self.log_queue.put(message)
    
    def consume_logs(self):
        """Consume messages from the log queue and update the UI"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, f"{message}\n")
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)
        except queue.Empty:
            # No more messages in the queue, schedule the next check
            self.root.after(100, self.consume_logs)
    
    def update_progress(self, value, status_text):
        """Update the progress bar and status label"""
        self.root.after(0, lambda: self.progress_var.set(value))
        self.root.after(0, lambda: self.status_label.config(text=status_text))

def main():
    root = tk.Tk()
    app = CyberSkullsDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 