import os
import csv
import requests
import streamlit as st
import pandas as pd
from io import StringIO
import time
import threading
import base64
from pathlib import Path
import tempfile
import zipfile
from PIL import Image

# Colors and styling constants
BACKGROUND_COLOR = "#000000"  # Black background
TEXT_COLOR = "#00FF00"  # Bright green text
ACCENT_COLOR = "#005500"  # Darker green for accents

# Apply custom CSS for Cyber Skulls theme
def apply_cyber_skulls_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #00FF00;
    }
    .stTextInput, .stSelectbox, .stFileUploader {
        color: #00FF00;
        border-color: #00FF00;
    }
    .stButton>button {
        color: #00FF00;
        background-color: #111111;
        border: 1px solid #00FF00;
        border-radius: 2px;
    }
    .stButton>button:hover {
        color: #00FF00;
        background-color: #005500;
        border: 1px solid #00FF00;
    }
    .stProgress>div>div {
        background-color: #00FF00;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00FF00 !important;
    }
    code {
        color: #00FF00 !important;
        background-color: #111111 !important;
    }
    .grid-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: 
            linear-gradient(#003300 1px, transparent 1px),
            linear-gradient(90deg, #003300 1px, transparent 1px);
        background-size: 40px 40px;
        z-index: -1;
        opacity: 0.3;
    }
    .cyber-box {
        border: 1px solid #00FF00;
        padding: 15px;
        margin: 10px 0px;
        background-color: rgba(0, 0, 0, 0.7);
        position: relative;
    }
    .cyber-box::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(#003300 1px, transparent 1px),
            linear-gradient(90deg, #003300 1px, transparent 1px);
        background-size: 20px 20px;
        z-index: -1;
        opacity: 0.2;
    }
    .cyber-header {
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .cyber-label {
        color: #00FF00;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        text-transform: uppercase;
    }
    .system-log {
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #00FF00;
        background-color: #111111;
        padding: 10px;
        height: 200px;
        overflow-y: auto;
        border: 1px solid #00FF00;
    }
    .folder-path {
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #00FF00;
        background-color: #111111;
        padding: 10px;
        border: 1px solid #00FF00;
        margin-top: 5px;
    }
    </style>
    <div class="grid-container"></div>
    """, unsafe_allow_html=True)

# Utility function to create a download link for a zip file
def create_download_link(zip_file_path, link_text="DOWNLOAD_FILES"):
    with open(zip_file_path, "rb") as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:application/zip;base64,{b64}" download="ipfs_downloads.zip" style="text-decoration:none;"><button style="color:#00FF00;background-color:#111111;border:1px solid #00FF00;padding:8px 16px;font-family:\'Courier New\',monospace;cursor:pointer;">{link_text}</button></a>'
    return href

# Function to create local version zip file
def create_local_version_zip():
    """Create a zip file containing the local GUI version and dependencies"""
    try:
        # Create a temporary zip file
        zip_filename = os.path.join(tempfile.gettempdir(), "cyber_skulls_local_version.zip")
        
        # Create README for local version
        local_readme_content = """# Cyber Skulls NFT Downloader - Local Version

## Quick Start (Windows)

**EASY WAY:** Double-click `run.bat` and it will handle everything automatically!

## Getting Your Collection Data

Before using this tool, you need to download your collection's CSV data:

**For ARC19 Collections:**
- Visit: https://www.wen.tools/download-arc19-collection-data
- Enter your collection ID
- Download the CSV file

**For ARC69 Collections:**
- Visit: https://www.wen.tools/download-arc69-collection-data
- Enter your collection ID  
- Download the CSV file

## Manual Installation

1. Make sure you have Python 3.7+ installed
2. Extract this ZIP file to a folder
3. Open a terminal/command prompt in the extracted folder
4. Install dependencies:
   ```
   pip install -r requirements_local.txt
   ```

## Usage

**Option 1 (Recommended for Windows):**
```
Double-click run.bat
```

**Option 2 (Manual):**
```
python download_ipfs_gui.py
```

## Features

- Desktop GUI application with Cyber Skulls theme
- Batch download of NFT images from IPFS
- Support for multiple CSV files
- Real-time progress tracking
- Customizable IPFS gateway
- Grid-line visual effects matching CyberSkulls aesthetic
- Includes Cyber Skulls logo

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- requests
- pillow

## CSV Format

Your CSV file should contain columns:
- name: NFT name
- unit-name: Unit name
- url: IPFS URL (ipfs://...)
- metadata_mime_type: (optional) MIME type for file extension

**Note:** The CSV files from wen.tools already have the correct format.

## Files Included

- **run.bat**: Easy launcher for Windows (double-click to start)
- download_ipfs_gui.py: Main GUI application
- logo.png: Cyber Skulls logo (if available)
- requirements_local.txt: Python dependencies
- README_LOCAL.md: This file

## Troubleshooting

- If `run.bat` doesn't work, make sure Python is installed and added to PATH
- If you get permission errors, run as Administrator
- For non-Windows systems, use the manual installation method
- Make sure you have downloaded your collection CSV from wen.tools first

© CYBER_SKULLS_NETWORK
"""
        
        # Create requirements for local version
        local_requirements = """requests>=2.25.0
pillow>=9.0.0"""
        
        # Create a run.bat file for Windows users
        run_bat_content = """@echo off
echo ========================================
echo   CYBER SKULLS NFT DOWNLOADER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [SYSTEM] Python found
echo [SYSTEM] Installing dependencies...
echo.

REM Install requirements
pip install -r requirements_local.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Dependencies installed
echo [SYSTEM] Starting Cyber Skulls NFT Downloader...
echo.

REM Run the GUI application
python download_ipfs_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo [SYSTEM] Application closed
pause
"""
        
        # Files to include in the zip (only essential files, with size checking)
        files_to_include = []
        total_size = 0
        
        # Check if GUI file exists and get its size
        gui_file = "download_ipfs_gui.py"
        if os.path.exists(gui_file):
            file_size = os.path.getsize(gui_file)
            if file_size < 50 * 1024 * 1024:  # Only include if less than 50MB
                files_to_include.append((gui_file, gui_file))
                total_size += file_size
        
        # Check for logo.png and include if reasonable size  
        logo_file = "logo.png"
        if os.path.exists(logo_file):
            logo_size = os.path.getsize(logo_file)
            logo_size_mb = logo_size / (1024 * 1024)
            # Include logo if it's less than 10MB and won't make total zip too large
            if logo_size < 10 * 1024 * 1024 and (total_size + logo_size) < 90 * 1024 * 1024:
                files_to_include.append((logo_file, logo_file))
                total_size += logo_size
                print(f"Including logo.png ({logo_size_mb:.1f} MB) in local version")
            else:
                print(f"Logo.png too large ({logo_size_mb:.1f} MB) - skipping to keep zip manageable")
        else:
            # Check for backup logo files
            backup_logos = ["cs GLOW.png"]
            for backup_logo in backup_logos:
                if os.path.exists(backup_logo):
                    backup_size = os.path.getsize(backup_logo)
                    if backup_size < 1 * 1024 * 1024 and (total_size + backup_size) < 90 * 1024 * 1024:  # Less than 1MB
                        files_to_include.append((backup_logo, backup_logo))
                        total_size += backup_size
                        print(f"Including backup logo {backup_logo} ({backup_size/1024:.0f} KB) in local version")
                        break
        
        # Create the zip file with only essential files
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add existing small files only
            for source_file, archive_name in files_to_include:
                zipf.write(source_file, archive_name)
            
            # Add README
            zipf.writestr("README_LOCAL.md", local_readme_content)
            
            # Add requirements
            zipf.writestr("requirements_local.txt", local_requirements)
            
            # Add run.bat file
            zipf.writestr("run.bat", run_bat_content)
        
        # Check final zip size
        if os.path.exists(zip_filename):
            zip_size = os.path.getsize(zip_filename)
            zip_size_mb = zip_size / (1024 * 1024)
            print(f"Created local version zip: {zip_size_mb:.1f} MB")
            
            # If zip is too large (>100MB), don't return it
            if zip_size > 100 * 1024 * 1024:
                print(f"Zip file too large ({zip_size_mb:.1f} MB) - removing")
                os.remove(zip_filename)
                return None
        
        return zip_filename
    except Exception as e:
        print(f"Error creating local version zip: {str(e)}")
        return None

# Function to create download link for local version
def create_local_download_link():
    """Create a download link for the local version"""
    zip_path = create_local_version_zip()
    if zip_path and os.path.exists(zip_path):
        with open(zip_path, "rb") as f:
            bytes_data = f.read()
            b64 = base64.b64encode(bytes_data).decode()
            href = f'<a href="data:application/zip;base64,{b64}" download="cyber_skulls_local_version.zip" style="text-decoration:none;"><button style="color:#00FF00;background-color:#111111;border:1px solid #00FF00;padding:8px 16px;font-family:\'Courier New\',monospace;cursor:pointer;">⬇ DOWNLOAD_LOCAL_VERSION</button></a>'
        return href
    return None

# Function to download an image from IPFS
def download_image(url, output_path, gateway_url, log_callback=None):
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
            if log_callback:
                log_callback(f"[WARNING] Skipping non-IPFS URL: {url}")
            return False
        
        # Download the image
        if log_callback:
            log_callback(f"[DOWNLOAD] Retrieving: {os.path.basename(output_path)}")
        
        response = requests.get(full_url, timeout=60)
        if response.status_code == 200:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            if log_callback:
                log_callback(f"[SUCCESS] Downloaded: {os.path.basename(output_path)}")
            return True
        else:
            if log_callback:
                log_callback(f"[ERROR] Failed to download {url}: HTTP {response.status_code}")
            return False
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error downloading {url}: {str(e)}")
        return False

# Process CSV data for downloading in batches
def process_csv_data_in_batches(df, output_dir, gateway_url, batch_size=50, 
                               progress_callback=None, log_callback=None):
    try:
        # Check if required columns exist
        required_columns = ["name", "unit-name", "url"]
        for col in required_columns:
            if col not in df.columns:
                if log_callback:
                    log_callback(f"[ERROR] CSV is missing required column: {col}")
                return 0, 0, []
        
        # Track success and failure counts
        success_count = 0
        fail_count = 0
        total_count = len(df)
        downloaded_files = []
        processed_count = 0
        
        if log_callback:
            log_callback(f"[INFO] Processing {total_count} items in batches of {batch_size}")
        
        # Process in batches
        for batch_start in range(0, total_count, batch_size):
            batch_end = min(batch_start + batch_size, total_count)
            batch = df.iloc[batch_start:batch_end]
            
            if log_callback:
                log_callback(f"[BATCH] Processing items {batch_start+1}-{batch_end} of {total_count}")
            
            # Process each row in the batch
            for _, row in batch.iterrows():
                processed_count += 1
                
                # Update progress based on processed count, not row index
                if progress_callback:
                    progress_callback(processed_count / total_count)
                
                name = row["name"].strip() if isinstance(row["name"], str) else str(row["name"])
                unit_name = row["unit-name"].strip() if isinstance(row["unit-name"], str) else str(row["unit-name"])
                url = row["url"].strip() if isinstance(row["url"], str) else str(row["url"])
                
                if not url or not name or not unit_name:
                    continue
                
                # Create a filename-safe version of the name
                safe_name = f"{name}_{unit_name}".replace("/", "_").replace("\\", "_")
                safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._- ")
                
                # Determine file extension based on mime type or default to .png
                mime_type = row.get("metadata_mime_type", "")
                if isinstance(mime_type, str):
                    mime_type = mime_type.strip()
                else:
                    mime_type = ""
                    
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
                success = download_image(url, output_path, gateway_url, log_callback)
                if success:
                    success_count += 1
                    downloaded_files.append(output_path)
                else:
                    fail_count += 1
            
            # Log batch completion with current stats
            if log_callback:
                log_callback(f"[BATCH_COMPLETE] Batch {batch_start//batch_size + 1} finished. Success: {success_count}, Failed: {fail_count}")
                log_callback(f"[SYSTEM] Files saved to local folder: {output_dir}")
            
            # Allow a short pause between batches to free up resources
            time.sleep(0.2)
        
        if log_callback:
            log_callback(f"[ALL_BATCHES_COMPLETE] All {total_count} items processed")
            
        return success_count, fail_count, downloaded_files
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error processing CSV: {str(e)}")
        return 0, 0, []

# Main application
def main():
    # Set page config
    st.set_page_config(
        page_title="Cyber Skulls NFT Downloader",
        page_icon="🔐",
        layout="wide",
    )
    
    # Apply custom theme
    apply_cyber_skulls_theme()
    
    # Set up the page header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<h1 class="cyber-header">■ CYBER_SKULLS_NFT_DOWNLOADER</h1>', unsafe_allow_html=True)
    with col2:
        # Try to load the logo
        try:
            # For online version, prefer the animated GIF logo
            logo_path = "logo.png"
            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                # Resize if too large to prevent browser issues
                if image.size[0] > 300 or image.size[1] > 300:
                    image.thumbnail((150, 150), Image.LANCZOS)
                st.image(image, width=150)
            else:
                # Fallback to PNG logo
                logo_path = "cs GLOW.png"
                if os.path.exists(logo_path):
                    image = Image.open(logo_path)
                    st.image(image, width=150)
        except Exception:
            st.text("[LOGO_NOT_FOUND]")
    
    # Local version download section
    st.markdown('<div class="cyber-box">', unsafe_allow_html=True)
    st.markdown('<h3 class="cyber-header">■ LOCAL_VERSION_AVAILABLE</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<p class="cyber-label">> DESKTOP_APPLICATION:</p>', unsafe_allow_html=True)
        # Create local download link
        local_download_link = create_local_download_link()
        if local_download_link:
            st.markdown(local_download_link, unsafe_allow_html=True)
            st.markdown('<p style="color:#888888;font-size:10px;font-family:Courier;">Lightweight version (~25KB)</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#FF0000;">LOCAL VERSION UNAVAILABLE</p>', unsafe_allow_html=True)
            st.markdown('<p style="color:#888888;font-size:10px;">Files too large or missing</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="cyber-label">> SOURCE_CODE:</p>', unsafe_allow_html=True)
        github_link = '<a href="https://github.com/YOUR_USERNAME/cyber-skulls-nft-downloader" target="_blank" style="text-decoration:none;"><button style="color:#00FF00;background-color:#111111;border:1px solid #00FF00;padding:8px 16px;font-family:\'Courier New\',monospace;cursor:pointer;">🔗 GITHUB_REPOSITORY</button></a>'
        st.markdown(github_link, unsafe_allow_html=True)
    
    with col3:
        st.markdown('<p class="cyber-label">> FEATURES_COMPARISON:</p>', unsafe_allow_html=True)
        with st.expander("📋 LOCAL vs WEB", expanded=False):
            st.markdown("""
            **Local Desktop App:**
            - ✅ Better performance
            - ✅ No file size limits  
            - ✅ Offline after download
            - ✅ Multiple CSV support
            
            **Web Version:**
            - ✅ No installation needed
            - ✅ Works on any device
            - ✅ Always up-to-date
            - ⚠️ File size limitations
            """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="cyber-box">', unsafe_allow_html=True)
    st.markdown('<h3 class="cyber-header">■ NETWORK_OPERATIONS</h3>', unsafe_allow_html=True)
    
    # CSV download instructions
    st.markdown('<p class="cyber-label">> GET_YOUR_COLLECTION_CSV:</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        arc19_link = '<a href="https://www.wen.tools/download-arc19-collection-data" target="_blank" style="text-decoration:none;"><button style="color:#00FF00;background-color:#111111;border:1px solid #00FF00;padding:6px 12px;font-family:\'Courier New\',monospace;cursor:pointer;font-size:12px;">📊 ARC19_COLLECTIONS</button></a>'
        st.markdown(arc19_link, unsafe_allow_html=True)
        
    with col2:
        arc69_link = '<a href="https://www.wen.tools/download-arc69-collection-data" target="_blank" style="text-decoration:none;"><button style="color:#00FF00;background-color:#111111;border:1px solid #00FF00;padding:6px 12px;font-family:\'Courier New\',monospace;cursor:pointer;font-size:12px;">📊 ARC69_COLLECTIONS</button></a>'
        st.markdown(arc69_link, unsafe_allow_html=True)
    
    st.markdown('<p style="color:#888888;font-size:11px;font-family:Courier;margin-top:5px;">Download your collection data from wen.tools before uploading here</p>', unsafe_allow_html=True)
    
    # IPFS Gateway setting
    st.markdown('<p class="cyber-label">> IPFS_GATEWAY:</p>', unsafe_allow_html=True)
    gateway_url = st.text_input("IPFS Gateway", value="https://ipfs.io/ipfs/", 
                               label_visibility="collapsed")
    if not gateway_url.endswith('/'):
        gateway_url += '/'
    
    # CSV file upload
    st.markdown('<p class="cyber-label">> SELECT_CSV_FILE:</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("CSV File", type=["csv"], label_visibility="collapsed")
    
    # Download mode selection
    st.markdown('<p class="cyber-label">> SELECT_DOWNLOAD_MODE:</p>', unsafe_allow_html=True)
    download_mode = st.radio(
        "Download Mode",
        ["Small Collection >200mb total (ZIP Download)", "Large Collection (Direct Folder)"],
        label_visibility="collapsed"
    )
    
    # Output folder selection for direct mode
    if download_mode == "Large Collection (Direct Folder)":
        st.markdown('<p class="cyber-label">> OUTPUT_FOLDER:</p>', unsafe_allow_html=True)
        output_folder = st.text_input("Output Folder", value=os.path.join(os.path.expanduser("~"), "Downloads", "IPFS_Downloads"), 
                                    label_visibility="collapsed")
        
        # Display the selected path
        st.markdown(f'<div class="folder-path">{output_folder}</div>', unsafe_allow_html=True)
        
        # Batch size setting
        st.markdown('<p class="cyber-label">> BATCH_SIZE:</p>', unsafe_allow_html=True)
        batch_size = st.slider("Batch Size", min_value=10, max_value=200, value=50, step=10, 
                              help="Number of images to process in each batch", 
                              label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize log list in session state if it doesn't exist
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'download_complete' not in st.session_state:
        st.session_state.download_complete = False
    if 'download_path' not in st.session_state:
        st.session_state.download_path = None
    
    # Create system log box
    st.markdown('<div class="cyber-box">', unsafe_allow_html=True)
    st.markdown('<h3 class="cyber-header">■ SYSTEM_LOG</h3>', unsafe_allow_html=True)
    log_placeholder = st.empty()
    
    # Display logs
    def update_logs():
        log_html = '<div class="system-log">'
        for log in st.session_state.logs:
            log_html += f"{log}<br>"
        log_html += '</div>'
        log_placeholder.markdown(log_html, unsafe_allow_html=True)
    
    update_logs()
    
    # Progress bar
    st.markdown('<h3 class="cyber-header">■ DOWNLOAD_STATUS</h3>', unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.markdown('<p class="cyber-label">SYSTEM_READY</p>', unsafe_allow_html=True)
    
    # Download button
    download_button = st.button("▶ INITIALIZE_DOWNLOAD")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download link area
    download_link_placeholder = st.empty()
    if st.session_state.download_complete and st.session_state.download_path and download_mode == "Small Collection >200mb total (ZIP Download)":
        download_link = create_download_link(st.session_state.download_path)
        download_link_placeholder.markdown(download_link, unsafe_allow_html=True)
    
    # Function to add log messages
    def add_log(message):
        st.session_state.logs.append(message)
        update_logs()
    
    # Function to handle the download process
    def process_download():
        try:
            # Reset session state
            st.session_state.logs = []
            st.session_state.download_complete = False
            st.session_state.download_path = None
            
            # Read CSV data
            csv_data = uploaded_file.getvalue().decode('utf-8')
            df = pd.read_csv(StringIO(csv_data))
            
            # Set up the output directory based on download mode
            if download_mode == "Small Collection >200mb total (ZIP Download)":
                # Create a temporary directory for downloads
                temp_dir = tempfile.mkdtemp()
                output_dir = temp_dir
                add_log(f"[SYSTEM] Using temporary directory for downloads")
            else:
                # Use the specified output folder
                output_dir = output_folder
                os.makedirs(output_dir, exist_ok=True)
                add_log(f"[SYSTEM] Saving files directly to: {output_dir}")
            
            # Log start of process
            add_log("[SYSTEM] Initializing download sequence...")
            total_items = len(df)
            add_log(f"[SYSTEM] Found {total_items} items to process")
            
            # Update status
            status_text.markdown('<p class="cyber-label">DOWNLOADING_IMAGES...</p>', unsafe_allow_html=True)
            
            # Define progress update function
            def update_progress(progress_value):
                progress_bar.progress(progress_value)
            
            # Process CSV and download images (with or without batches)
            if download_mode == "Small Collection >200mb total (ZIP Download)":
                # Process without batches for small collections
                success_count, fail_count, downloaded_files = process_csv_data_in_batches(
                    df, output_dir, gateway_url, 
                    batch_size=total_items,  # Use entire dataset as one batch
                    progress_callback=update_progress,
                    log_callback=add_log
                )
                
                # Check total size of downloaded files before creating zip
                total_size = 0
                for file_path in downloaded_files:
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
                
                # Convert to MB for logging
                total_size_mb = total_size / (1024 * 1024)
                add_log(f"[SIZE_CHECK] Total downloaded files: {total_size_mb:.1f} MB")
                
                # If total size exceeds 180MB (safety margin), switch to folder mode
                if total_size > 180 * 1024 * 1024:  # 180MB in bytes
                    add_log(f"[WARNING] Collection size ({total_size_mb:.1f} MB) exceeds safe download limit")
                    add_log(f"[SYSTEM] Switching to folder mode to prevent browser issues")
                    
                    # Move files to user downloads folder instead of creating zip
                    safe_output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "IPFS_Downloads_Large")
                    os.makedirs(safe_output_dir, exist_ok=True)
                    
                    # Move files to the safe directory
                    moved_count = 0
                    for file_path in downloaded_files:
                        if os.path.exists(file_path):
                            filename = os.path.basename(file_path)
                            new_path = os.path.join(safe_output_dir, filename)
                            try:
                                import shutil
                                shutil.move(file_path, new_path)
                                moved_count += 1
                            except Exception as e:
                                add_log(f"[ERROR] Failed to move {filename}: {str(e)}")
                    
                    add_log(f"[SYSTEM] Moved {moved_count} files to: {safe_output_dir}")
                    
                    # Display folder path instead of download link
                    folder_link = f'<div style="margin-top:20px;text-align:center;"><p class="cyber-label">COLLECTION TOO LARGE - FILES SAVED TO FOLDER:</p><div class="folder-path">{safe_output_dir}</div></div>'
                    download_link_placeholder.markdown(folder_link, unsafe_allow_html=True)
                    
                else:
                    # Safe to create zip file
                    add_log(f"[SYSTEM] Collection size is safe for ZIP download")
                    zip_filename = os.path.join(tempfile.gettempdir(), "ipfs_downloads.zip")
                    
                    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for file_path in downloaded_files:
                            if os.path.exists(file_path):
                                zipf.write(file_path, arcname=os.path.basename(file_path))
                    
                    # Check final zip size
                    if os.path.exists(zip_filename):
                        zip_size = os.path.getsize(zip_filename)
                        zip_size_mb = zip_size / (1024 * 1024)
                        add_log(f"[ZIP_CREATED] Zip file size: {zip_size_mb:.1f} MB")
                        
                        if zip_size > 190 * 1024 * 1024:  # Final safety check
                            add_log(f"[ERROR] Zip file too large for download ({zip_size_mb:.1f} MB)")
                            os.remove(zip_filename)
                            folder_link = f'<div style="margin-top:20px;text-align:center;"><p class="cyber-label">ZIP TOO LARGE - CHECK YOUR DOWNLOADS FOLDER</p></div>'
                            download_link_placeholder.markdown(folder_link, unsafe_allow_html=True)
                        else:
                            # Set session state for download
                            st.session_state.download_path = zip_filename
                            add_log(f"[SYSTEM] Created zip archive with {success_count} images")
                            
                            # Display download link for zip mode
                            download_link = create_download_link(st.session_state.download_path)
                            download_link_placeholder.markdown(download_link, unsafe_allow_html=True)
                
            else:
                # Process with batches for large collections
                success_count, fail_count, _ = process_csv_data_in_batches(
                    df, output_dir, gateway_url, 
                    batch_size=batch_size,
                    progress_callback=update_progress,
                    log_callback=add_log
                )
                
                # Add info about the output folder
                add_log(f"[SYSTEM] Saved {success_count} images to folder: {output_dir}")
                
                # Display folder path for direct mode
                add_log(f"[REPORT] Output location: {output_dir}")
                folder_link = f'<div style="margin-top:20px;text-align:center;"><p class="cyber-label">FILES SAVED TO FOLDER:</p><div class="folder-path">{output_dir}</div></div>'
                download_link_placeholder.markdown(folder_link, unsafe_allow_html=True)
            
            # Complete the progress
            progress_bar.progress(1.0)
            status_text.markdown('<p class="cyber-label">DOWNLOAD_COMPLETE</p>', unsafe_allow_html=True)
            
            # Add summary log
            add_log("\n[REPORT] Download Summary:")
            add_log(f"[REPORT] Images successfully downloaded: {success_count}")
            add_log(f"[REPORT] Images failed to download: {fail_count}")
            
            # Set download complete
            st.session_state.download_complete = True
            
        except Exception as e:
            add_log(f"[ERROR] Critical error during download: {str(e)}")
            status_text.markdown('<p class="cyber-label">SYSTEM_ERROR</p>', unsafe_allow_html=True)
    
    # Handle download button click
    if download_button:
        if uploaded_file is None:
            status_text.markdown('<p class="cyber-label">ERROR: NO_CSV_FILE_SELECTED</p>', unsafe_allow_html=True)
            add_log("[ERROR] Please select a CSV file")
        elif download_mode == "Large Collection (Direct Folder)" and not output_folder:
            status_text.markdown('<p class="cyber-label">ERROR: NO_OUTPUT_FOLDER_SELECTED</p>', unsafe_allow_html=True)
            add_log("[ERROR] Please specify an output folder")
        else:
            # Run download process
            process_download()
    
    # Footer
    st.markdown("""
    <div style="position: fixed; bottom: 0; right: 0; padding: 10px; font-family: 'Courier New', monospace; font-size: 12px; color: #00FF00;">
        © CYBER_SKULLS_NETWORK // SECURE_CONNECTION_ESTABLISHED
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 