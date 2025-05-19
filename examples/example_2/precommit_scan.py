#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example 2: Pre-commit style scan and reporting with ByteSleuth

This example demonstrates how to use ByteSleuth to scan all files in a source directory (e.g., a codebase)
and print a summary report, without sanitizing files. This is useful for CI/CD, pre-commit hooks, or audits.
"""
import os
from byte_sleuth import ByteSleuth

# Directory to scan (simulate a codebase or data folder)
source_dir = "../../examples/test_scan"

# Create a scanner (no sanitization, just detection)
scanner = ByteSleuth(sanitize=False)

# Collect results for all files in the directory
def collect_results(directory):
    results = {}
    for fname in os.listdir(directory):
        fpath = os.path.join(directory, fname)
        if os.path.isfile(fpath):
            findings = scanner.scan_file(fpath)
            if findings:
                results[fname] = findings
    return results

results = collect_results(source_dir)

# Print a summary report
if results:
    print("\n=== Suspicious Character Report ===")
    for fname, findings in results.items():
        print(f"\nFile: {fname}")
        for cp, name, char in findings:
            print(f"  - U+{cp:04X} {name} ({repr(char)})")
else:
    print("\n✅ All files in the directory are clean!")
