#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example 1: Basic file and directory scan with ByteSleuth

This example demonstrates how to use ByteSleuth to scan a file and a directory for suspicious characters,
with automatic sanitization enabled.
"""
# Inserting the parent directory to the path
import os
from byte_sleuth import ByteSleuth

# Create a scanner with sanitization enabled
detector = ByteSleuth(sanitize=True)

# Scan a single file
file_path = "./test_file.txt"
findings = detector.scan_file(file_path)
print(f"\n🔍 {file_path}: {len(findings)} suspicious characters found!")

# Scan a directory (create a test file if needed)
test_dir = "test_scan"
os.makedirs(test_dir, exist_ok=True)
with open(os.path.join(test_dir, "example1.txt"), "w", encoding="utf-8") as f:
    f.write("Invisible char: \u200B\nAnother: \u202E")

detector.scan_directory(test_dir)
