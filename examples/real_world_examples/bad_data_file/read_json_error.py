import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from byte_sleuth.byte_sleuth import ByteSleuth

# Read the JSON file with invisible characters
json_file = os.path.join(os.path.dirname(__file__), "test_json_with_invisible.json")

with open(json_file, "r", encoding="utf-8") as f:
    data = f.read()

# Try to parse the JSON data, which may fail due to invisible characters
try:
    parsed_data = json.loads(data)
    print("JSON loaded successfully:", parsed_data)
except json.JSONDecodeError as e:
    print("Failed to load JSON:", e)
    # If parsing fails, we can try to sanitize the data
    scanner = ByteSleuth(sanitize=True)
    scanner.backup = True
    findings = scanner.scan_file(json_file)
    if findings:
        for cp, name, char, idx in findings:
            print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {idx}")
    # Backup the original data for reference
    
    # Attempt to sanitize the JSON data
    sanitized = scanner.sanitize_file(json_file)
    print("\nSanitized JSON content:")
    # Try to load the sanitized JSON
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            sanitized_data = json.load(f)
        print("\nSanitized JSON loaded successfully:", sanitized_data)
    except Exception as e:
        print("\nFailed to load sanitized JSON:", e)
    scanner.restore_file(json_file)