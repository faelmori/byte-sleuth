import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.byte_sleuth import ByteSleuth

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
    scanner.backup_file(json_file)
    findings = scanner.scan_file(json_file)
    if findings:
        for cp, name, char in findings:
            print(f"  - U+{cp:04X} {name} ({repr(char)})")
    # Backup the original data for reference
    
    # Attempt to sanitize the JSON data
    sanitized_data = scanner.sanitize_text(data)
    print("\nSanitized JSON content:")
    print(repr(sanitized_data))
    # Try to load the sanitized JSON
    try:
        parsed_data = json.loads(sanitized_data)
        print("Sanitized JSON loaded successfully:", parsed_data)
    except json.JSONDecodeError as e:
        print("Failed to load sanitized JSON:", e)

    # Clean up
    del scanner
    # Restore the original file
    with open(json_file, "w", encoding="utf-8") as f:
        f.write(data)
    print("\nOriginal JSON file restored.")
    # Clean up
    os.remove(json_file+".bak")
    