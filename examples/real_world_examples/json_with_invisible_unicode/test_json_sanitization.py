#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test: JSON Data with Invisible Unicode

This script simulates a JSON file containing invisible Unicode characters in keys or values,
which can cause parsing errors or data integrity issues. ByteSleuth is used to detect and sanitize these issues.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import json
from src.byte_sleuth import ByteSleuth

json_file = "test_json_with_invisible.json"

# Simulate a JSON with a zero-width space in a key and value
bad_json = '{"na\u200Bme": "Jo\u200Bhn Doe", "age": 30}'
with open(json_file, "w", encoding="utf-8") as f:
    f.write(bad_json)

print("Original JSON content:")
with open(json_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

scanner = ByteSleuth(sanitize=True)
findings = scanner.scan_file(json_file)

print(f"\nFindings: {len(findings)} suspicious characters found.")
for cp, name, char in findings:
    print(f"  - U+{cp:04X} {name} ({repr(char)})")

print("\nSanitized JSON content:")
with open(json_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

# Try to load the sanitized JSON
try:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("\nJSON loaded successfully:", data)
except Exception as e:
    print("\nFailed to load JSON:", e)

# Clean up
os.remove(json_file)
