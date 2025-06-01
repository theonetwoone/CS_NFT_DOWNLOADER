# CyberSkulls NFT Collection Image Downloader (GUI)

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