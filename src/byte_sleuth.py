"""
byte_sleuth.py
A utility for scanning text streams, files, and directories for suspicious ASCII control and Unicode characters, with optional sanitization and backup features.

This module provides the ByteSleuth class, which can be used as a library, via CLI, or as a filter in shell pipelines to detect and optionally remove control characters from text. It is designed for international use and follows Python packaging best practices.
"""
import os
import unicodedata
import argparse
import logging
import json
import sys
import hashlib
from concurrent.futures import ProcessPoolExecutor

class ByteSleuth:
    """
    Scans text streams, files, and directories for suspicious ASCII control and Unicode characters.
    Optionally sanitizes files or streams by removing these characters.
    Supports concurrent scanning of files in directories for improved performance.
    """
    ASCII_CONTROL_NAMES = {i: unicodedata.name(chr(i), f"ASCII {i}") for i in range(32)}
    ASCII_CONTROL_NAMES[127] = "DEL (Delete)"

    # List of suspicious/invisible Unicode codepoints (expandable)
    UNICODE_SUSPICIOUS_CODEPOINTS = set([
        0x00AD,  # SOFT HYPHEN
        0x034F,  # COMBINING GRAPHEME JOINER
        0x061C,  # ARABIC LETTER MARK
        0x115F, 0x1160,  # HANGUL FILLER
        0x17B4, 0x17B5,  # KHMER VOWEL INHERENT
        0x180B, 0x180C, 0x180D, 0x180E,  # MONGOLIAN FREE VARIATION SELECTOR
        0x200B, 0x200C, 0x200D, 0x200E, 0x200F,  # ZERO WIDTH, LRM, RLM
        0x202A, 0x202B, 0x202C, 0x202D, 0x202E,  # BIDI overrides
        0x2060, 0x2061, 0x2062, 0x2063, 0x2064, 0x2066, 0x2067, 0x2068, 0x2069, 0x206A, 0x206B, 0x206C, 0x206D, 0x206E, 0x206F,  # INVISIBLE CONTROLS
        0xFEFF,  # ZERO WIDTH NO-BREAK SPACE
        0xFFF9, 0xFFFA, 0xFFFB,  # INTERLINEAR ANNOTATION
        0x1D173, 0x1D174, 0x1D175, 0x1D176, 0x1D177, 0x1D178, 0x1D179, 0x1D17A,  # MUSICAL INVISIBLE
    ])

    def __init__(self, sanitize=False, backup=True, log_file="scanner.log", verbose=False, debug=False, quiet=False, sanitize_only=False):
        """
        Initialize the scanner with optional sanitization and backup.
        Args:
            sanitize (bool): If True, automatically remove suspicious characters.
            backup (bool): If True, create a backup before modifying files (not used in PIPE mode).
            log_file (str): Path to the log file.
        """
        self.sanitize = sanitize
        self.backup = backup
        self.verbose = verbose
        self.debug = debug
        self.quiet = quiet
        self.sanitize_only = sanitize_only
        logging.basicConfig(
            filename=log_file, filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.DEBUG if debug else logging.INFO
        )

    def detect_suspicious_chars(self, text):
        """
        Detect ASCII control and suspicious Unicode characters in the text.
        Args:
            text (str): The text to scan.
        Returns:
            list: List of tuples (codepoint, name, character, position) for each suspicious character found.
        """
        findings = []
        for idx, char in enumerate(text):
            cp = ord(char)
            # ASCII control (0-31, 127)
            if (0 <= cp < 32) or cp == 127:
                name = self.ASCII_CONTROL_NAMES.get(cp, unicodedata.name(char, "UNKNOWN"))
                findings.append((cp, name, char, idx))
            # Unicode suspicious/invisible
            elif cp in self.UNICODE_SUSPICIOUS_CODEPOINTS:
                name = unicodedata.name(char, "UNKNOWN")
                findings.append((cp, name, char, idx))
        return findings

    def sanitize_text(self, text):
        """
        Remove suspicious characters while preserving formatting.
        Args:
            text (str): The text to sanitize.
        Returns:
            str: Sanitized text.
        """
        return ''.join(
            char if not (
                (0 <= ord(char) < 32) or ord(char) == 127 or ord(char) in self.UNICODE_SUSPICIOUS_CODEPOINTS
            ) else ''
            for char in text
        )

    def process_stdin(self):
        """
        Sanitize input from PIPE in real-time, line by line.
        Reads from sys.stdin and writes sanitized output to stdout.
        """
        for line in sys.stdin:
            sanitized_line = self.sanitize_text(line)
            print(sanitized_line, end="")

    def file_hash(self, file_path):
        """
        Calculate the SHA256 hash of a file.
        Args:
            file_path (str): Path to the file.
        Returns:
            str: SHA256 hex digest, or None if file not found.
        """
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Could not hash {file_path}: {e}")
            return None

    def scan_file(self, file_path):
        """
        Scan a file and optionally sanitize it. Handles backup and sanitize-only modes.
        Args:
            file_path (str): Path to the file to scan.
        Returns:
            list: List of suspicious characters found.
        """
        pre_hash = self.file_hash(file_path)
        if self.verbose:
            print(f"[INFO] Pre-scan hash for {file_path}: {pre_hash}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            if not self.quiet:
                print(f"Error reading {file_path}: {e}")
            return []

        if self.sanitize_only:
            if self.backup:
                self.backup_file(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.sanitize_text(content))
            post_hash = self.file_hash(file_path)
            if self.verbose:
                print(f"[INFO] Post-sanitize hash for {file_path}: {post_hash}")
            if not self.quiet:
                print(f"Sanitization complete for {file_path} (sanitize-only mode).")
            return []

        findings = self.detect_suspicious_chars(content)

        if not findings:
            logging.info(f"No suspicious characters found in {file_path}. ✅")
            if not self.quiet:
                print(f"✅ {file_path} is clean!")
            return []

        if self.sanitize:
            if self.backup:
                self.backup_file(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.sanitize_text(content))
            post_hash = self.file_hash(file_path)
            if self.verbose:
                print(f"[INFO] Post-sanitize hash for {file_path}: {post_hash}")
            if not self.quiet:
                print(f"Sanitization complete for {file_path}.")

        if self.verbose or self.debug:
            for cp, name, char, idx in findings:
                print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {idx}")
        return findings

    def scan_directory(self, directory_path):
        """
        Scan all files in a directory using parallel processing for performance.
        Args:
            directory_path (str): Path to the directory to scan.
        Returns:
            dict: Mapping of file names to findings (for reporting).
        """
        if not os.path.isdir(directory_path):
            logging.error(f"Invalid directory: {directory_path}")
            if not self.quiet:
                print(f"Invalid directory: {directory_path}")
            return {}

        files = [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]
        if not self.quiet:
            print(f"🔍 Scanning {len(files)} files in parallel...")

        cpu_count = os.cpu_count() or 1
        max_workers = min(4, max(1, cpu_count // 2))
        results = {}
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            scan_results = list(executor.map(self.scan_file, files))
        for file_path, findings in zip(files, scan_results):
            if findings:
                results[file_path] = findings
        return results

    def report(self, results, output_path=None):
        """
        Print or save a JSON report of suspicious character findings.
        Args:
            results (dict): Mapping of file paths to findings.
            output_path (str or None): If given, write report to this file; else print to stdout.
        """
        report_data = {}
        for file_path, findings in results.items():
            report_data[file_path] = [
                {"codepoint": cp, "name": name, "char": repr(char)} for cp, name, char in findings
            ]
        report_json = json.dumps(report_data, indent=4, ensure_ascii=False)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_json)
            print(f"\n📄 Report written to {output_path}")
        else:
            print("\n=== Suspicious Character Report ===")
            print(report_json)
    

    def backup_file(self, file_path):
        """
        Create a backup of the file before sanitization.
        Args:
            file_path (str): Path to the file to back up.
        """
        if self.backup:
            backup_path = f"{file_path}.bak"
            with open(file_path, 'r', encoding='utf-8') as original_file:
                with open(backup_path, 'w', encoding='utf-8') as backup_file:
                    backup_file.write(original_file.read())
            logging.info(f"Backup created: {backup_path}")
            print(f"Backup created: {backup_path}")
        else:
            logging.warning("Backup feature is disabled. No backup created.")
            print("Backup feature is disabled. No backup created.")

    def restore_file(self, file_path):
        """
        Restore the original file from the backup.
        Args:
            file_path (str): Path to the file to restore.
        """
        backup_path = f"{file_path}.bak"
        if os.path.exists(backup_path):
            with open(backup_path, 'r', encoding='utf-8') as backup_file:
                with open(file_path, 'w', encoding='utf-8') as original_file:
                    original_file.write(backup_file.read())
            os.remove(backup_path)
            logging.info(f"File restored from backup: {file_path}")
            print(f"File restored from backup: {file_path}")
        else:
            logging.warning("No backup found. Cannot restore.")
            print("No backup found. Cannot restore.")
        return True
    
# CLI usage
# This section allows the script to be run from the command line with arguments.
# It uses argparse to handle command-line arguments and options.
# It provides options for sanitization, logging, and reporting.
# The script can scan files or directories, and it can also read from standard input (PIPE).
# This is a simple command-line interface (CLI) for the ByteSleuth class.
# It allows users to scan files or directories for suspicious characters, with options for sanitization and logging.
# The script can be run directly from the command line, and it supports both file and directory scanning.
# It also provides options for sanitization and logging, and can read from standard input (PIPE).
# This section is executed when the script is run directly.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suspicious character scanner (Unicode & ASCII)")
    parser.add_argument("target", nargs="?", help="File or directory to scan (or use PIPE input)")
    parser.add_argument("-s", "--sanitize", action="store_true", help="Enable automatic sanitization")
    parser.add_argument("-l", "--log", default="scanner.log", help="Log file path")
    parser.add_argument("-r", "--report", nargs="?", default="", help="Print JSON report to stdout or save to file if a path is provided.")
    parser.add_argument("-f", "--no-backup", action="store_true", default=False, help="Disable backup creation")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output except errors")
    parser.add_argument("-S", "--sanitize-only", action="store_true", help="Only sanitize the input, do not scan")
    parser.add_argument("-F", "--fail-on-detect", action="store_true", help="Exit with code 1 if suspicious characters are found")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s 1.0", help="Show version and exit")
    args = parser.parse_args()

    backup = not args.no_backup
    scanner = ByteSleuth(
        sanitize=args.sanitize,
        backup=backup,
        log_file=args.log,
        verbose=args.verbose,
        debug=args.debug,
        quiet=args.quiet,
        sanitize_only=args.sanitize_only
    )

    suspicious_found = False
    if args.target:
        if os.path.isdir(args.target):
            results = scanner.scan_directory(args.target)
            if args.report:
                output_path = args.report if isinstance(args.report, str) and args.report else None
                scanner.report(results, output_path=output_path)
            # Always print findings summary for VSCode/CLI
            if results:
                print("\n=== Suspicious Character Report ===")
                for file_path, findings in results.items():
                    print(f"\nFile: {file_path}")
                    for cp, name, char, idx in findings:
                        print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {idx}")
                suspicious_found = True
            else:
                print("\n✅ All files in the directory are clean!")
        elif os.path.isfile(args.target):
            findings = scanner.scan_file(args.target)
            if args.report:
                output_path = args.report if isinstance(args.report, str) and args.report else None
                scanner.report({args.target: findings}, output_path=output_path)
            # Always print findings summary for VSCode/CLI
            if findings:
                print("\n=== Suspicious Character Report ===")
                print(f"File: {args.target}")
                for cp, name, char, idx in findings:
                    print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {idx}")
                suspicious_found = True
            else:
                print(f"\n✅ {args.target} is clean!")
        else:
            if not args.quiet:
                print("Error: Invalid path. Provide an existing file or directory.")
            exit(1)
    else:
        if not args.quiet:
            print("⏳ Reading from PIPE...")
        scanner.process_stdin()

    if not args.quiet:
        print("\n✅ Scan finished! Check the log for details.")
    logging.info("✅ Scan finished! Check the log for details.")
    if args.fail_on_detect and suspicious_found:
        exit(1)
    exit(0)


# Note: The script can be run from the command line with various options.
# Usage examples:
# python byte_sleuth.py /path/to/file.txt -s -l my_log.log
# python byte_sleuth.py /path/to/directory
# cat file.txt | python byte_sleuth.py -s > sanitized.txt