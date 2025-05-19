#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test: SQL Injection with Hidden Characters

This script simulates a scenario where a SQL injection payload is obfuscated using invisible Unicode characters.
The ByteSleuth package is used to detect and sanitize these hidden threats before they reach the database layer.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.byte_sleuth import ByteSleuth

# Simulate a user input with a hidden zero-width space in the SQL injection payload
payload = "admin'\u200B OR 1=1 --"

# Write the payload to a test file
test_file = "test_sql_injection_payload.txt"
with open(test_file, "w", encoding="utf-8") as f:
    f.write(f"username={payload}\n")

print("Original payload (with hidden char):")
with open(test_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

# Scan and sanitize the file
scanner = ByteSleuth(sanitize=True)
findings = scanner.scan_file(test_file)

print(f"\nFindings: {len(findings)} suspicious characters found.")
for cp, name, char in findings:
    print(f"  - U+{cp:04X} {name} ({repr(char)})")

print("\nSanitized payload:")
with open(test_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

# Clean up
os.remove(test_file)
