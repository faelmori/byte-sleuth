#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test: Source Code with Bidirectional Unicode

This script simulates a source code file containing bidirectional override characters (e.g., U+202E),
which can be used in attacks to visually obfuscate code logic. ByteSleuth is used to detect and sanitize these issues.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from byte_sleuth.byte_sleuth import ByteSleuth

code_file = "test_code_with_bidi.py"

# Simulate a Python file with a bidirectional override character
with open(code_file, "w", encoding="utf-8") as f:
    f.write("print('Hello')\n# Normal comment\n# Dangerous: \u202Eelif True: pass\n")

print("Original code file content:")
with open(code_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

scanner = ByteSleuth(sanitize=True)
findings = scanner.scan_file(code_file)

print(f"\nFindings: {len(findings)} suspicious characters found.")
for cp, name, char in findings:
    print(f"  - U+{cp:04X} {name} ({repr(char)})")

print("\nSanitized code file content:")
with open(code_file, "r", encoding="utf-8") as f:
    print(repr(f.read()))

# Clean up
os.remove(code_file)
