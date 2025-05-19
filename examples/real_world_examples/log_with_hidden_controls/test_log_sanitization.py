#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test: Log File with Hidden Control Characters

This script simulates a log file containing hidden ASCII control characters (e.g., NUL, BEL, etc.)
that could disrupt log parsing, monitoring, or security tools. ByteSleuth is used to detect and sanitize these issues.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.byte_sleuth import ByteSleuth

log_file = "test_log_with_controls.log"

# Simulate a log entry with hidden control characters
with open(log_file, "w", encoding="utf-8") as f:
    f.write("[INFO] User login\x00\x07\n[ERROR] Invalid password\x1B\n")

print("Original log file content:")
with open(log_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

scanner = ByteSleuth(sanitize=True)
findings = scanner.scan_file(log_file)

print(f"\nFindings: {len(findings)} suspicious characters found.")
for cp, name, char in findings:
    print(f"  - U+{cp:04X} {name} ({repr(char)})")

print("\nSanitized log file content:")
with open(log_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

# Clean up
os.remove(log_file)
