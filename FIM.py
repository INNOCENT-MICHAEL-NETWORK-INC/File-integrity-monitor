import os
import hashlib
import time
import argparse
import keyboard

def generate_line_hash(line):
    """Generate SHA-256 hash of a line"""
    return hashlib.sha256(line.encode()).hexdigest()

def monitor_files(rootdir):
    """Monitor all files in a directory tree"""
    print(f'started integrity monitor on {rootdir}')
    all_filenames = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            all_filenames.append(os.path.join(dirpath, filename))
    line_hashes = {filename: {} for filename in all_filenames}
    
    while True:
        print("listening....")
        time.sleep(5) # Wait for 5 seconds before checking again
        if keyboard.is_pressed("q"):  # Check if "q" key is pressed
            print("Stopping monitoring...")
            break
        for filename in all_filenames:
            with open(filename, "r") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                line_hash = generate_line_hash(line)
                if i not in line_hashes[filename]:
                    line_hashes[filename][i] = line_hash
                elif line_hashes[filename][i] != line_hash:
                    print(f"Line {i+1} of file '{filename}' has been modified:")
                    print(line)
                    line_hashes[filename][i] = line_hash
            
def main():
    # Create an argparse parser to accept command line arguments
    parser = argparse.ArgumentParser(description='Monitor all files in a directory tree for changes')
    parser.add_argument('rootdir', help='Example: Python FIM.py /Downloads')
    args = parser.parse_args()

    # Start monitoring files
    monitor_files(args.rootdir)

if __name__ == "__main__":
    main()
