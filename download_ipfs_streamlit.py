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
def download_image(url, output_path, gateway_url, log_callback=None, is_cloud_env=False):
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
        
        # Download the image with cloud-specific timeout
        if log_callback:
            log_callback(f"[DOWNLOAD] Retrieving: {os.path.basename(output_path)}")
        
        # Use shorter timeout for cloud environments to avoid hanging
        timeout = 30 if is_cloud_env else 60
        
        response = requests.get(full_url, timeout=timeout)
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
    except requests.exceptions.Timeout:
        if log_callback:
            log_callback(f"[TIMEOUT] Download timeout for {url}")
        return False
    except requests.exceptions.RequestException as e:
        if log_callback:
            log_callback(f"[ERROR] Network error downloading {url}: {str(e)}")
        return False
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error downloading {url}: {str(e)}")
        return False

# Process CSV data for downloading in batches
def process_csv_data_in_batches(df, output_dir, gateway_url, batch_size=50, 
                               progress_callback=None, log_callback=None, is_cloud_env=False):
    try:
        # Check if required columns exist
        required_columns = ["name", "unit-name", "url"]
        for col in required_columns:
            if col not in df.columns:
                if log_callback:
                    log_callback(f"[ERROR] CSV is missing required column: {col}")
                return 0, 0, [], []
        
        # Adjust batch size for cloud environments
        if is_cloud_env:
            # Use smaller batches in cloud to avoid timeouts
            batch_size = min(batch_size, 15)
            if log_callback:
                log_callback(f"[CLOUD] Adjusted batch size to {batch_size} for cloud environment")
        
        # Track success and failure counts
        success_count = 0
        fail_count = 0
        total_count = len(df)
        downloaded_files = []
        file_data_list = []  # Store file data in memory for ZIP creation
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
                
                filename = f"{safe_name}{extension}"
                output_path = os.path.join(output_dir, filename)
                
                # Download the image and store in memory for web apps
                file_data = download_image_to_memory(url, gateway_url, log_callback, is_cloud_env)
                if file_data:
                    success_count += 1
                    downloaded_files.append(output_path)
                    file_data_list.append((filename, file_data))
                    if log_callback:
                        log_callback(f"[SUCCESS] Downloaded: {filename}")
                else:
                    fail_count += 1
                    if is_cloud_env and fail_count > 5:
                        if log_callback:
                            log_callback(f"[CLOUD_WARNING] Multiple failures detected. This may be due to cloud resource limits.")
            
            # Log batch completion with current stats
            if log_callback:
                log_callback(f"[BATCH_COMPLETE] Batch {batch_start//batch_size + 1} finished. Success: {success_count}, Failed: {fail_count}")
            
            # Allow a longer pause between batches in cloud environment
            pause_time = 1.0 if is_cloud_env else 0.2
            time.sleep(pause_time)
        
        if log_callback:
            log_callback(f"[ALL_BATCHES_COMPLETE] All {total_count} items processed")
            
        return success_count, fail_count, downloaded_files, file_data_list
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error processing CSV: {str(e)}")
        return 0, 0, [], []

# Function to download an image to memory instead of disk
def download_image_to_memory(url, gateway_url, log_callback=None, is_cloud_env=False):
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
            return None
        
        # Download the image with cloud-specific timeout
        if log_callback:
            log_callback(f"[DOWNLOAD] Retrieving: {url.split('/')[-1] if '/' in url else url}")
        
        # Use shorter timeout for cloud environments to avoid hanging
        timeout = 30 if is_cloud_env else 60
        
        response = requests.get(full_url, timeout=timeout)
        if response.status_code == 200:
            return response.content
        else:
            if log_callback:
                log_callback(f"[ERROR] Failed to download {url}: HTTP {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        if log_callback:
            log_callback(f"[TIMEOUT] Download timeout for {url}")
        return None
    except requests.exceptions.RequestException as e:
        if log_callback:
            log_callback(f"[ERROR] Network error downloading {url}: {str(e)}")
        return None
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error downloading {url}: {str(e)}")
        return None

# Function to create multiple ZIP files from file data
def create_multiple_zips(file_data_list, max_size_mb=80, log_callback=None):
    """Create multiple ZIP files if the total size exceeds the limit"""
    zip_files = []
    current_zip_files = []
    current_size = 0
    max_size_bytes = max_size_mb * 1024 * 1024
    zip_counter = 1
    
    if log_callback:
        log_callback(f"[ZIP] Creating ZIP files with max size {max_size_mb}MB each")
    
    try:
        for i, (filename, file_data) in enumerate(file_data_list):
            file_size = len(file_data)
            
            # If adding this file would exceed the limit, create a new ZIP
            if current_size + file_size > max_size_bytes and current_zip_files:
                # Create ZIP for current batch
                if log_callback:
                    log_callback(f"[ZIP] Creating part {zip_counter} with {len(current_zip_files)} files...")
                
                zip_path = create_zip_from_data(current_zip_files, f"ipfs_downloads_part_{zip_counter}.zip")
                if zip_path:
                    zip_files.append((zip_path, f"Part {zip_counter}"))
                    if log_callback:
                        log_callback(f"[ZIP] Created part {zip_counter}: {current_size / (1024*1024):.1f}MB")
                
                # Clear memory by removing processed files
                current_zip_files = []
                current_size = 0
                zip_counter += 1
                
                # Force garbage collection to free memory
                import gc
                gc.collect()
            
            # Add file to current batch
            current_zip_files.append((filename, file_data))
            current_size += file_size
            
            # Progress logging for large collections
            if i % 20 == 0 and log_callback:
                log_callback(f"[ZIP] Processed {i+1}/{len(file_data_list)} files for ZIP creation")
        
        # Create final ZIP if there are remaining files
        if current_zip_files:
            if log_callback:
                log_callback(f"[ZIP] Creating final part {zip_counter} with {len(current_zip_files)} files...")
            
            zip_path = create_zip_from_data(current_zip_files, f"ipfs_downloads_part_{zip_counter}.zip")
            if zip_path:
                zip_files.append((zip_path, f"Part {zip_counter}"))
                if log_callback:
                    log_callback(f"[ZIP] Created part {zip_counter}: {current_size / (1024*1024):.1f}MB")
        
        return zip_files
        
    except MemoryError:
        if log_callback:
            log_callback(f"[ERROR] Out of memory while creating ZIP files. Try smaller batches or use local version.")
        return zip_files  # Return what we have so far
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error creating ZIP files: {str(e)}")
        return zip_files  # Return what we have so far

# Function to create a ZIP file from file data in memory
def create_zip_from_data(file_data_list, zip_name):
    """Create a ZIP file from a list of (filename, data) tuples"""
    try:
        zip_path = os.path.join(tempfile.gettempdir(), zip_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename, file_data in file_data_list:
                zipf.writestr(filename, file_data)
        
        return zip_path
    except Exception as e:
        print(f"Error creating ZIP {zip_name}: {str(e)}")
        return None

# Function to create download buttons for multiple ZIPs
def create_multiple_download_buttons(zip_files):
    """Create download buttons for multiple ZIP files"""
    if not zip_files:
        return ""
    
    html_content = '<div style="margin-top:20px;">'
    html_content += '<p class="cyber-label">⬇ DOWNLOAD_YOUR_FILES:</p>'
    
    for i, (zip_path, part_name) in enumerate(zip_files):
        if os.path.exists(zip_path):
            # Get file size for display
            file_size = os.path.getsize(zip_path) / (1024 * 1024)  # Convert to MB
            
            with open(zip_path, "rb") as f:
                bytes_data = f.read()
                b64 = base64.b64encode(bytes_data).decode()
                download_name = f"cyber_skulls_{part_name.lower().replace(' ', '_')}.zip"
                
                button_html = f'''
                <div style="margin:10px 0;">
                    <a href="data:application/zip;base64,{b64}" download="{download_name}" style="text-decoration:none;">
                        <button style="color:#00FF00;background-color:#111111;border:1px solid #00FF00;padding:10px 20px;font-family:'Courier New',monospace;cursor:pointer;width:300px;text-align:left;">
                            📦 {part_name} ({file_size:.1f} MB)
                        </button>
                    </a>
                </div>
                '''
                html_content += button_html
    
    html_content += '</div>'
    return html_content

# Function to detect if running on Streamlit Cloud
def is_running_on_streamlit_cloud():
    """Detect if the app is running on Streamlit Cloud"""
    try:
        # Check for common Streamlit Cloud environment indicators
        import os
        # Streamlit Cloud typically runs on Linux with specific environment variables
        if os.environ.get('STREAMLIT_SERVER_HEADLESS') == 'true':
            return True
        # Check for typical Streamlit Cloud paths
        if '/home/appuser' in os.path.expanduser("~"):
            return True
        # Check hostname patterns common in cloud environments
        import socket
        hostname = socket.gethostname()
        if any(cloud_indicator in hostname.lower() for cloud_indicator in ['streamlit', 'cloud', 'heroku', 'render']):
            return True
    except:
        pass
    return False

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
    
    # Detect environment
    is_cloud = is_running_on_streamlit_cloud()
    
    # Set up the page header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<h1 class="cyber-header">■ CYBER_SKULLS_NFT_DOWNLOADER</h1>', unsafe_allow_html=True)
        if is_cloud:
            st.markdown('<p style="color:#888888;font-size:12px;font-family:Courier;">🌐 RUNNING_ON_STREAMLIT_CLOUD</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#888888;font-size:12px;font-family:Courier;">💻 RUNNING_LOCALLY</p>', unsafe_allow_html=True)
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
    
    # Local version download section (only show on cloud)
    if is_cloud:
        st.markdown('<div class="cyber-box">', unsafe_allow_html=True)
        st.markdown('<h3 class="cyber-header">■ LOCAL_VERSION_AVAILABLE</h3>', unsafe_allow_html=True)
        st.info("💡 **Better Performance:** Download the desktop version for unlimited file sizes and faster processing!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown('<p class="cyber-label">> DESKTOP_APPLICATION:</p>', unsafe_allow_html=True)
            # Create local download link
            local_download_link = create_local_download_link()
            if local_download_link:
                st.markdown(local_download_link, unsafe_allow_html=True)
                st.markdown('<p style="color:#888888;font-size:10px;font-family:Courier;">No size limits • Faster downloads</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#FF0000;">LOCAL VERSION UNAVAILABLE</p>', unsafe_allow_html=True)
                st.markdown('<p style="color:#888888;font-size:10px;">Files too large or missing</p>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<p class="cyber-label">> SOURCE_CODE:</p>', unsafe_allow_html=True)
            github_link = '<a href="https://github.com/theonetwoone/CS_NFT_DOWNLOADER" target="_blank" style="text-decoration:none;"><button style="color:#00FF00;background-color:#111111;border:1px solid #00FF00;padding:8px 16px;font-family:\'Courier New\',monospace;cursor:pointer;">🔗 GITHUB_REPOSITORY</button></a>'
            st.markdown(github_link, unsafe_allow_html=True)
        
        with col3:
            st.markdown('<p class="cyber-label">> FEATURES_COMPARISON:</p>', unsafe_allow_html=True)
            with st.expander("📋 LOCAL vs CLOUD", expanded=False):
                st.markdown("""
                **Local Desktop App:**
                - ✅ No file size limits  
                - ✅ Direct folder access
                - ✅ Faster downloads
                - ✅ Works offline
                
                **Cloud Version:**
                - ✅ No installation needed
                - ✅ Works on any device
                - ✅ Always up-to-date
                - ⚠️ 200MB limit per download
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
    gateway_url = st.text_input("IPFS Gateway URL", value="https://ipfs.io/ipfs/", 
                               label_visibility="collapsed")
    if not gateway_url.endswith('/'):
        gateway_url += '/'
    
    # CSV file upload
    st.markdown('<p class="cyber-label">> SELECT_CSV_FILE:</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], label_visibility="collapsed")
    
    # Preview CSV and estimate size
    if uploaded_file is not None:
        try:
            # Read CSV for preview
            csv_data = uploaded_file.getvalue().decode('utf-8')
            df_preview = pd.read_csv(StringIO(csv_data))
            
            # Show basic stats
            st.markdown('<div class="cyber-box">', unsafe_allow_html=True)
            st.markdown('<h3 class="cyber-header">■ COLLECTION_ANALYSIS</h3>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown(f'<p class="cyber-label">TOTAL_ITEMS: {len(df_preview)}</p>', unsafe_allow_html=True)
            with col2:
                # Estimate average file size (typical NFT images are 200KB-2MB)
                avg_size_mb = 0.8  # Conservative estimate: 800KB average
                estimated_size = len(df_preview) * avg_size_mb
                st.markdown(f'<p class="cyber-label">ESTIMATED_SIZE: ~{estimated_size:.0f}MB</p>', unsafe_allow_html=True)
            with col3:
                estimated_zips = max(1, int(estimated_size / 80) + (1 if estimated_size % 80 > 0 else 0))
                st.markdown(f'<p class="cyber-label">ESTIMATED_ZIPS: {estimated_zips}</p>', unsafe_allow_html=True)
            
            # Size warnings
            if is_cloud:
                if estimated_size > 800:
                    st.error(f"🚨 **Collection Too Large:** {estimated_size:.0f}MB estimated size exceeds cloud limit (~800MB). Consider using the local desktop version.")
                elif estimated_size > 400:
                    st.warning(f"⚠️ **Large Collection:** {estimated_size:.0f}MB estimated. May cause timeouts or memory issues on cloud.")
                elif estimated_size > 200:
                    st.info(f"ℹ️ **Medium Collection:** {estimated_size:.0f}MB estimated. Should process fine but may take time.")
            
            # Show preview of first few rows
            if st.checkbox("👁️ PREVIEW_DATA", help="Show first 5 rows of your CSV"):
                st.markdown('<p class="cyber-label">CSV_PREVIEW:</p>', unsafe_allow_html=True)
                preview_df = df_preview.head().copy()
                # Truncate long URLs for display
                if 'url' in preview_df.columns:
                    preview_df['url'] = preview_df['url'].apply(lambda x: str(x)[:50] + '...' if len(str(x)) > 50 else str(x))
                st.dataframe(preview_df, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            uploaded_file = None
    
    # Download mode selection
    st.markdown('<p class="cyber-label">> SELECT_DOWNLOAD_MODE:</p>', unsafe_allow_html=True)
    
    if is_cloud:
        # On cloud, explain the new approach with limitations
        st.info("🌐 **Streamlit Cloud Mode:** Files are processed in memory and packaged as ZIP downloads. Large collections are split into multiple ZIP files (≤80MB each).")
        st.warning("⚠️ **Cloud Limitations:**\n- Maximum ~800MB total collection size\n- Memory constraints may cause failures\n- Processing timeout after ~10 minutes")
        download_mode = st.radio(
            "Processing Mode",
            ["Standard Processing (Recommended)", "Small Batches (Slower but more stable)"],
            help="Standard mode processes all files together. Small batches mode is more stable for unreliable connections.",
            label_visibility="collapsed"
        )
    else:
        # Local mode - show simpler options
        st.info("💻 **Local Mode:** Better performance and no size limits.")
        download_mode = st.radio(
            "Processing Mode",
            ["Standard Processing (Recommended)", "Small Batches (Slower but more stable)"],
            help="Standard mode is faster. Small batches mode is better for very large collections or unstable connections.",
            label_visibility="collapsed"
        )
    
    # Batch size setting (only for batch mode)
    if "Small Batches" in download_mode:
        st.markdown('<p class="cyber-label">> BATCH_SIZE:</p>', unsafe_allow_html=True)
        if is_cloud:
            max_batch = 15  # Smaller batches for cloud
            default_batch = 10
        else:
            max_batch = 50
            default_batch = 20
        batch_size = st.slider("Items per Batch", min_value=5, max_value=max_batch, value=default_batch, step=5, 
                              help="Number of images to process in each batch", 
                              label_visibility="collapsed")
    else:
        batch_size = 1000  # Large batch for standard processing
    
    # Initialize log list in session state if it doesn't exist
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'download_complete' not in st.session_state:
        st.session_state.download_complete = False
    if 'download_path' not in st.session_state:
        st.session_state.download_path = None
    if 'zip_files' not in st.session_state:
        st.session_state.zip_files = []
    
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
    
    # Download link area - show multiple download buttons if available
    download_link_placeholder = st.empty()
    if st.session_state.download_complete and st.session_state.zip_files:
        download_html = create_multiple_download_buttons(st.session_state.zip_files)
        download_link_placeholder.markdown(download_html, unsafe_allow_html=True)
    
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
            st.session_state.zip_files = []
            
            # Read CSV data
            csv_data = uploaded_file.getvalue().decode('utf-8')
            df = pd.read_csv(StringIO(csv_data))
            
            # Set up the output directory based on download mode
            temp_dir = tempfile.mkdtemp()
            output_dir = temp_dir
            add_log(f"[SYSTEM] Processing files in memory for download")
            
            # Log start of process
            add_log("[SYSTEM] Initializing download sequence...")
            total_items = len(df)
            add_log(f"[SYSTEM] Found {total_items} items to process")
            
            # Early size check and warning
            estimated_size = total_items * 0.8  # 800KB average estimate
            if is_cloud and estimated_size > 800:
                add_log(f"[WARNING] Estimated size ({estimated_size:.0f}MB) may exceed cloud limits")
                add_log(f"[WARNING] Processing anyway but may fail due to memory constraints")
            
            # Update status
            status_text.markdown('<p class="cyber-label">DOWNLOADING_IMAGES...</p>', unsafe_allow_html=True)
            
            # Define progress update function
            def update_progress(progress_value):
                progress_bar.progress(progress_value)
            
            # Process CSV and download images to memory
            success_count, fail_count, downloaded_files, file_data_list = process_csv_data_in_batches(
                df, output_dir, gateway_url, 
                batch_size=batch_size if "Small Batches" in download_mode else total_items,
                progress_callback=update_progress,
                log_callback=add_log,
                is_cloud_env=is_cloud
            )
            
            if not file_data_list:
                add_log("[ERROR] No files were successfully downloaded")
                status_text.markdown('<p class="cyber-label">DOWNLOAD_FAILED</p>', unsafe_allow_html=True)
                return
            
            # Calculate total size and memory check
            total_size = sum(len(data) for _, data in file_data_list)
            total_size_mb = total_size / (1024 * 1024)
            add_log(f"[SIZE_CHECK] Total downloaded files: {total_size_mb:.1f} MB")
            
            # Memory warning for cloud
            if is_cloud and total_size_mb > 600:
                add_log(f"[MEMORY_WARNING] Large dataset in memory ({total_size_mb:.1f}MB)")
                add_log(f"[MEMORY_WARNING] ZIP creation may fail due to memory limits")
            
            # Determine how to package the files
            if total_size_mb <= 80:
                # Single ZIP file
                add_log(f"[ZIP] Creating single ZIP file ({total_size_mb:.1f} MB)")
                zip_path = create_zip_from_data(file_data_list, "cyber_skulls_collection.zip")
                if zip_path:
                    st.session_state.zip_files = [(zip_path, "Complete Collection")]
                    add_log(f"[SUCCESS] Created ZIP file with {success_count} images")
                else:
                    add_log(f"[ERROR] Failed to create ZIP file - possibly too large for memory")
                    status_text.markdown('<p class="cyber-label">ZIP_CREATION_FAILED</p>', unsafe_allow_html=True)
                    return
            else:
                # Multiple ZIP files
                add_log(f"[ZIP] Collection too large for single download, creating multiple ZIP files")
                
                # Clear some memory before creating ZIPs
                import gc
                gc.collect()
                
                zip_files = create_multiple_zips(file_data_list, max_size_mb=80, log_callback=add_log)
                st.session_state.zip_files = zip_files
                
                if zip_files:
                    add_log(f"[SUCCESS] Created {len(zip_files)} ZIP files with {success_count} images total")
                else:
                    add_log(f"[ERROR] Failed to create any ZIP files - likely memory exhaustion")
                    add_log(f"[SUGGESTION] Try using smaller batches or the local desktop version")
                    status_text.markdown('<p class="cyber-label">MEMORY_EXHAUSTED</p>', unsafe_allow_html=True)
                    return
            
            # Display download buttons
            if st.session_state.zip_files:
                download_html = create_multiple_download_buttons(st.session_state.zip_files)
                download_link_placeholder.markdown(download_html, unsafe_allow_html=True)
            
            # Complete the progress
            progress_bar.progress(1.0)
            status_text.markdown('<p class="cyber-label">DOWNLOAD_COMPLETE</p>', unsafe_allow_html=True)
            
            # Add summary log
            add_log("\n[REPORT] Download Summary:")
            add_log(f"[REPORT] Images successfully downloaded: {success_count}")
            add_log(f"[REPORT] Images failed to download: {fail_count}")
            if st.session_state.zip_files:
                add_log(f"[REPORT] ZIP files created: {len(st.session_state.zip_files)}")
                add_log(f"[REPORT] Click the download buttons above to get your files")
            
            # Set download complete
            st.session_state.download_complete = True
            
        except MemoryError:
            add_log(f"[CRITICAL] Out of memory! Collection too large for cloud processing")
            add_log(f"[SOLUTION] Use the local desktop version for large collections")
            status_text.markdown('<p class="cyber-label">MEMORY_ERROR</p>', unsafe_allow_html=True)
        except Exception as e:
            add_log(f"[ERROR] Critical error during download: {str(e)}")
            status_text.markdown('<p class="cyber-label">SYSTEM_ERROR</p>', unsafe_allow_html=True)
    
    # Handle download button click
    if download_button:
        if uploaded_file is None:
            status_text.markdown('<p class="cyber-label">ERROR: NO_CSV_FILE_SELECTED</p>', unsafe_allow_html=True)
            add_log("[ERROR] Please select a CSV file")
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