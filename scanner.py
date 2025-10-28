# This is a utility file for file scanning.
import os
import magic  # This is from the 'python-magic' library
import hashlib
import datetime


def get_file_hash(file_path):
    """Calculates the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read the file in chunks to avoid memory issues with large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating hash: {e}")
        return f"Error: {e}"


def get_file_metadata(file_path):
    """Gets file size and timestamps."""
    try:
        stats = os.stat(file_path)
        
        # Format size to be human-readable
        size_bytes = stats.st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} Bytes"
        elif size_bytes < 1024**2:
            size_str = f"{size_bytes/1024:.2f} KB"
        elif size_bytes < 1024**3:
            size_str = f"{size_bytes/(1024**2):.2f} MB"
        else:
            size_str = f"{size_bytes/(1024**3):.2f} GB"
            
        creation_time = datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modified_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "size": size_str,
            "creation_time": creation_time,
            "modified_time": modified_time
        }
    except Exception as e:
        print(f"Error getting metadata: {e}")
        return {
            "size": "Error",
            "creation_time": "Error",
            "modified_time": "Error"
        }


def verify_file_type(file_path):
    """
    Checks the true file type and gathers all metadata.
    
    Args:
        file_path (str): The full path to the file to check.

    Returns:
        dict: A dictionary containing all file information.
    """
    print(f"Scanning file: {file_path}")
    
    # 1. Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return {"error": "File not found"}

    try:
        # 2. Get the file extension from the name
        original_extension = os.path.splitext(file_path)[1].lower()

        # 3. Use python-magic to detect the MIME type
        detected_mime = magic.from_file(file_path, mime=True)
        description = magic.from_file(file_path)

        # 4. Get metadata (size, timestamps)
        metadata = get_file_metadata(file_path)
        
        # 5. Get file hash
        file_hash = get_file_hash(file_path)

        print(f"  > Original Extension: {original_extension}")
        print(f"  > Detected MIME Type: {detected_mime}")
        print(f"  > Detected Description: {description}")
        print(f"  > Hash (SHA256): {file_hash}")
        print(f"  > Metadata: {metadata}")

        # Combine all info into one dictionary
        final_result = {
            "extension": original_extension,
            "detected_mime": detected_mime,
            "description": description,
            "hash_sha256": file_hash
        }
        final_result.update(metadata) # Add size, creation_time, modified_time
        
        return final_result

    except Exception as e:
        print(f"Error during file scan: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # You can run this file directly to test it
    
    print("Running a simple test...")
    
    # Test 1: Create a real .txt file
    try:
        with open("test_file.txt", "w") as f:
            f.write("This is a real text file.")
        print(verify_file_type("test_file.txt"))
        os.remove("test_file.txt")

    except Exception as e:
        print(f"Test setup failed. Do you have 'python-magic-bin' installed? Error: {e}")
        # Clean up in case of failure
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

