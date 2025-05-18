#!/usr/bin/env python3
# -*- coding: utf-8 -*
# File: simple_scan.py

# Inserting the parent directory to the path
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importing the necessary modules
from src.byte_sleuth import ByteSleuth

# Creating a scanner with sanitization enabled
scanner = ByteSleuth(sanitize=True)

# Testing file scanning
file_path = "test_file.txt"
findings = scanner.scan_file(file_path, mode="all")
print(f"\n🔍 {file_path}: {len(findings)} suspicious characters found!")

# Testing directory scanning
test_dir = "test_scan"
os.makedirs(test_dir, exist_ok=True)
with open(os.path.join(test_dir, "example1.txt"), "w", encoding="utf-8") as f:
    f.write("Invisible char: \u200B\nAnother: \u202E")

scanner.scan_directory(test_dir, mode="all")
