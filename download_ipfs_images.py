import os
import csv
import requests
import argparse
from pathlib import Path

# Configure IPFS gateway
IPFS_GATEWAY = "https://ipfs.io/ipfs/"

def download_image(url, output_path, gateway_url):
    """Download an image from IPFS URL and save it to the specified path."""
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
            print(f"Skipping non-IPFS URL: {url}")
            return False
        
        # Download the image
        print(f"Downloading from: {full_url}")
        response = requests.get(full_url, timeout=30)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {output_path}")
            return True
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def process_csv_file(csv_file, output_dir, gateway_url):
    """Process a CSV file to download images and save them with name_unit-name format."""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Track success and failure counts
    success_count = 0
    fail_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Check if the required columns exist
        required_columns = ["name", "unit-name", "url"]
        if not all(col in reader.fieldnames for col in required_columns):
            missing = [col for col in required_columns if col not in reader.fieldnames]
            print(f"Error: CSV file {csv_file} is missing required columns: {', '.join(missing)}")
            return 0, 0
        
        # Process each row
        for row in reader:
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
            success = download_image(url, output_path, gateway_url)
            if success:
                success_count += 1
            else:
                fail_count += 1
    
    print(f"Processed {csv_file}:")
    print(f"  Success: {success_count}")
    print(f"  Failed: {fail_count}")
    return success_count, fail_count

def main():
    parser = argparse.ArgumentParser(description="Download NFT images from IPFS URLs in CSV files")
    parser.add_argument("csv_files", nargs="+", help="CSV file(s) containing NFT data")
    parser.add_argument("--output", "-o", default="downloaded_images", help="Output directory for downloaded images")
    parser.add_argument("--gateway", "-g", default=IPFS_GATEWAY, help="IPFS gateway URL")
    
    args = parser.parse_args()
    
    # Get the gateway URL
    gateway_url = args.gateway
    
    # Create the output directory
    output_dir = args.output
    
    # Process each CSV file
    total_success = 0
    total_fail = 0
    for csv_file in args.csv_files:
        if not os.path.exists(csv_file):
            print(f"Error: CSV file {csv_file} not found")
            continue
            
        print(f"Processing {csv_file}...")
        success, fail = process_csv_file(csv_file, output_dir, gateway_url)
        total_success += success
        total_fail += fail
    
    print("\nSummary:")
    print(f"Total images successfully downloaded: {total_success}")
    print(f"Total images failed to download: {total_fail}")
    print(f"Images saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main() 