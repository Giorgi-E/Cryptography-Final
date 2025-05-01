import hashlib
import json
import sys
import os
#computes the different hashes for the selected file
def compute_hashes(file_path):
    hashes = {
        'sha256': hashlib.sha256(),
        'sha1': hashlib.sha1(),
        'md5': hashlib.md5()
    }

    try:
        #i the file is too big read in parts
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                for h in hashes.values():
                    h.update(chunk)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    return {name: h.hexdigest() for name, h in hashes.items()}
#saves the hashes to the json file
def save_hashes(file_path, hash_file='hashes.json'):
    hashes = compute_hashes(file_path)
    if hashes:
        with open(hash_file, 'w') as f:
            json.dump(hashes, f, indent=4)
#compares the file with previously saved hashes file
def check_integrity(file_path, hash_file='hashes.json'):
    current_hashes = compute_hashes(file_path)
    if not current_hashes:
        return
    #read the saved hashes file
    with open(hash_file, 'r') as f:
        original_hashes = json.load(f)

    #compare and save to passed boolean
    passed = True
    for algo in original_hashes:
        if original_hashes[algo] == current_hashes[algo]:
            print(f"  {algo.upper()}: PASS")
        else:
            print(f"  {algo.upper()}: FAIL")
            passed = False

if __name__ == "__main__":
    action, file_path = sys.argv[1], sys.argv[2]

    if action == "save":
        save_hashes(file_path)
    elif action == "check":
        check_integrity(file_path)
    else:
        print("error")
