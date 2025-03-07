import os
import json

# Path to MapsCreated directory
directory = "MapsCreated"

# Get all HTML files in the directory
html_files = [file for file in os.listdir(directory) if file.endswith(".html")]

# Create manifest data
manifest = {
    "files": html_files
}

# Write to manifest.json
with open(os.path.join(directory, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Updated manifest.json with {len(html_files)} files.")