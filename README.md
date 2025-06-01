# Cyber Skulls NFT Downloader

🔗 **Live App:** [https://cs-nft-downloader.streamlit.app](https://cs-nft-downloader.streamlit.app)

🔗 **GitHub Repository:** [https://github.com/theonetwoone/CS_NFT_DOWNLOADER](https://github.com/theonetwoone/CS_NFT_DOWNLOADER)

A comprehensive tool for downloading and preserving IPFS-hosted NFT images from Algorand collections before unpinning, featuring a cyberpunk-themed interface inspired by Cyber Skulls.

## 🚀 Quick Start

### Web Version (Recommended)
Visit the live Streamlit app (link above) - no installation required!

### Local Desktop Version
Download the local GUI version directly from the web app or clone this repository.

## 📊 Getting Collection Data

Before using this tool, download your collection's CSV data:

- **ARC19 Collections:** [wen.tools ARC19 data](https://www.wen.tools/download-arc19-collection-data)
- **ARC69 Collections:** [wen.tools ARC69 data](https://www.wen.tools/download-arc69-collection-data)

## 🎨 Features

- **Web Version:** Streamlit-based with intelligent size management
- **Desktop Version:** tkinter GUI with full feature set
- **CLI Version:** Lightweight command-line tool
- **Cyber Skulls Theme:** Authentic cyberpunk aesthetic with grid effects
- **Smart Download Management:** Automatic ZIP/folder mode switching
- **Batch Processing:** Configurable batch sizes for large collections
- **IPFS Gateway Support:** Configurable IPFS gateway settings

## 🛠️ Installation

### Web Version
No installation needed - use the live app link above.

### Local Installation
```bash
git clone https://github.com/theonetwoone/CS_NFT_DOWNLOADER.git
cd CS_NFT_DOWNLOADER
pip install -r requirements.txt
```

### Usage
```bash
# Streamlit Web App
streamlit run download_ipfs_streamlit.py

# Desktop GUI
python download_ipfs_gui.py

# Command Line
python download_ipfs_images.py
```

## 📁 File Structure

- `download_ipfs_streamlit.py` - Web version with intelligent size management
- `download_ipfs_gui.py` - Desktop GUI with full Cyber Skulls theme
- `download_ipfs_images.py` - CLI version for basic usage
- `requirements.txt` - Python dependencies
- `logo.png` - Cyber Skulls logo
- `test collections/` - Sample collection data for testing

## ⚡ Technical Features

- Automatic fallback from ZIP to folder mode for large collections (>200MB)
- Batch processing system for memory efficiency
- Real-time progress tracking and logging
- Cross-platform filename sanitization
- MIME type detection for proper file extensions
- Error handling and retry logic

## 🎯 CSV Format

Your CSV should contain:
- `name` - NFT name
- `unit-name` - Unit name  
- `url` - IPFS URL (ipfs://...)
- `metadata_mime_type` - (optional) MIME type

**Note:** Files from wen.tools already have the correct format.

## 🌐 Deployment

This app is deployed on Streamlit Cloud. To deploy your own version:

1. Fork this repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository and `download_ipfs_streamlit.py`

## 📝 License

© CYBER_SKULLS_NETWORK

---

**⚠️ Important:** This tool is designed for preserving your own NFT collections before IPFS unpinning. Always respect copyright and ownership rights.

## Requirements

The following Python packages are required:
- requests
- tkinter (normally included in standard Python installation)
- pillow (for logo display)

Install the necessary packages with:
```
pip install -r requirements.txt
```

## Usage

Run the application from the command line with:

```
python download_ipfs_gui.py
```

### User Interface

The application has a cyberpunk-styled interface with the following features:

1. **CSV Files**: Click "BROWSE" to choose one or more CSV files containing NFT data.
2. **Output Folder**: Click "BROWSE" to specify where the downloaded images should be saved.
3. **IPFS Gateway**: You can specify a different IPFS gateway if the default gateway doesn't work.
4. **Start Download**: Click to begin the download process.
5. **Progress Indicator**: Shows the download progress.
6. **System Log**: Displays detailed information about the download process.

### CSV File Requirements

The CSV files must contain the following columns:
- `name`: The NFT name
- `unit-name`: The NFT unit name (used in the filename along with the name)
- `url`: IPFS URL to the image (must start with "ipfs://")

## IPFS Gateway

By default, the application uses "https://ipfs.io/ipfs/" as the IPFS gateway. You can specify a different gateway in the interface.

Some other public IPFS gateways you can try if there are problems:
- https://dweb.link/ipfs/
- https://gateway.pinata.cloud/ipfs/
- https://cloudflare-ipfs.com/ipfs/
- https://gateway.ipfs.io/ipfs/

## Troubleshooting

If the application can't download some images, you can try:

1. Check your internet connection
2. Try a different IPFS gateway
3. Check if the IPFS content is still available (it may already be unpinned)
4. Look in the log area for detailed error messages

## Future Development

This application handles the download part. To re-mint these NFTs as ARC-19 with a stable, free IPFS provider, additional functionality needs to be developed. 