import os
import json
import datetime
import sys

def update_manifest():
    # Path to MapsCreated directory
    directory = "MapsCreated"
    manifest_path = os.path.join(directory, "manifest.json")
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    # Get all HTML files in the directory
    html_files = [file for file in os.listdir(directory) if file.endswith(".html")]
    
    # Load existing manifest if it exists
    existing_files = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r") as f:
                manifest_data = json.load(f)
                # Create a lookup dictionary from existing files
                for file_entry in manifest_data.get("files", []):
                    if isinstance(file_entry, dict) and "filename" in file_entry and "added" in file_entry:
                        existing_files[file_entry["filename"]] = file_entry["added"]
        except json.JSONDecodeError:
            print("Error: Could not parse existing manifest.json. Creating a new one.")
    
    # Create new manifest entries
    now = datetime.datetime.now().isoformat(timespec='seconds')
    files_entries = []
    
    for filename in html_files:
        # If the file already exists in the manifest, keep its timestamp
        # Otherwise, set the current time as the added timestamp
        if filename in existing_files:
            added_time = existing_files[filename]
        else:
            added_time = now
            print(f"Adding new file: {filename}")
        
        files_entries.append({
            "filename": filename,
            "added": added_time
        })
    
    # Create manifest data
    manifest = {
        "files": files_entries
    }
    
    # Write to manifest.json
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Updated manifest.json with {len(files_entries)} files.")
    
    # If this is a new file, tell the user to commit the changes
    new_files = [f for f in html_files if f not in existing_files]
    if new_files:
        print("\nNew files detected! Don't forget to commit your changes:")
        print("git add MapsCreated/manifest.json")
        for f in new_files:
            print(f"git add MapsCreated/{f}")
        print('git commit -m "Add new mindmap files"')
        print("git push origin main")

if __name__ == "__main__":
    update_manifest()