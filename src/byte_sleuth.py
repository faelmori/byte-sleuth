"""
byte_sleuth.py
A utility for scanning files and directories for suspicious ASCII control and Unicode characters, with optional sanitization and backup features.

This module provides the ByteSleuth class, which can be used as a library or via CLI to detect and optionally remove control characters from text files. It is designed for international use and follows Python packaging best practices.
"""
import os
import unicodedata
import argparse
import logging

class ByteSleuth:
    """
    Scans files and directories for suspicious ASCII control and Unicode characters.
    Optionally sanitizes files by removing these characters, with backup support.
    """
    ASCII_CONTROL_NAMES = {
        0: "NUL (Null)", 1: "SOH (Start of Heading)", 2: "STX (Start of Text)",
        3: "ETX (End of Text)", 4: "EOT (End of Transmission)", 5: "ENQ (Enquiry)",
        6: "ACK (Acknowledge)", 7: "BEL (Bell)", 8: "BS (Backspace)", 9: "HT (Horizontal Tab)",
        10: "LF (Line Feed)", 11: "VT (Vertical Tab)", 12: "FF (Form Feed)", 13: "CR (Carriage Return)",
        14: "SO (Shift Out)", 15: "SI (Shift In)", 16: "DLE (Data Link Escape)", 17: "DC1 (Device Control 1)",
        18: "DC2 (Device Control 2)", 19: "DC3 (Device Control 3)", 20: "DC4 (Device Control 4)",
        21: "NAK (Negative Acknowledge)", 22: "SYN (Synchronous Idle)", 23: "ETB (End of Transmission Block)",
        24: "CAN (Cancel)", 25: "EM (End of Medium)", 26: "SUB (Substitute)", 27: "ESC (Escape)",
        28: "FS (File Separator)", 29: "GS (Group Separator)", 30: "RS (Record Separator)",
        31: "US (Unit Separator)", 127: "DEL (Delete)"
    }

    UNICODE_SUSPICIOUS_CODEPOINTS = [
        0x00AD, 0x200B, 0x200E, 0x200F, 0x2060, 0xFEFF, 0x202E
    ]

    def __init__(self, sanitize=False, backup=True, log_file="scanner.log"):
        """
        Initialize the scanner with optional sanitization and backup.
        Args:
            sanitize (bool): If True, automatically remove suspicious characters.
            backup (bool): If True, create a backup before modifying files.
            log_file (str): Path to the log file.
        """
        self.sanitize = sanitize
        self.backup = backup
        logging.basicConfig(
            filename=log_file, filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

    def detect_ascii_chars(self, text):
        """
        Detect ASCII control characters in the given text.
        Args:
            text (str): The text to scan.
        Returns:
            list: Tuples of (codepoint, name, character) for each match.
        """
        return [(ord(char), self.ASCII_CONTROL_NAMES[ord(char)], char)
                for char in text if ord(char) in self.ASCII_CONTROL_NAMES]

    def detect_unicode_chars(self, text):
        """
        Detect suspicious Unicode characters in the given text.
        Args:
            text (str): The text to scan.
        Returns:
            list: Tuples of (codepoint, name, character) for each match.
        """
        return [(ord(char), unicodedata.name(char, "UNKNOWN CHARACTER"), char)
                for char in text if ord(char) in self.UNICODE_SUSPICIOUS_CODEPOINTS]

    def detect_all_chars(self, text):
        """
        Detect both ASCII control and suspicious Unicode characters in the text.
        Args:
            text (str): The text to scan.
        Returns:
            list: Combined list of suspicious characters.
        """
        return self.detect_ascii_chars(text) + self.detect_unicode_chars(text)

    def backup_file(self, file_path):
        """
        Create a backup before overwriting the original file.
        Args:
            file_path (str): Path to the file to backup.
        Returns:
            str: Path to the backup file.
        """
        backup_path = file_path + ".bak"
        if not os.path.exists(backup_path):
            os.rename(file_path, backup_path)
            logging.info(f"Backup created: {backup_path}")
        return backup_path

    def sanitize_text(self, text):
        """
        Remove suspicious characters while preserving original formatting.
        Args:
            text (str): The text to sanitize.
        Returns:
            str: Sanitized text.
        """
        sanitized_text = ''.join(
            char if ord(char) not in self.ASCII_CONTROL_NAMES and ord(char) not in self.UNICODE_SUSPICIOUS_CODEPOINTS
            else '' for char in text
        )
        logging.info("Sanitization completed.")
        return sanitized_text

    def scan_file(self, file_path, mode="all"):
        """
        Scan a file and optionally sanitize it.
        Args:
            file_path (str): Path to the file to scan.
            mode (str): Scan mode: 'ascii', 'unicode', or 'all'.
        Returns:
            list: List of suspicious characters found.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            return []

        findings = {
            "ascii": self.detect_ascii_chars(content),
            "unicode": self.detect_unicode_chars(content),
            "all": self.detect_all_chars(content)
        }[mode]

        if self.sanitize:
            if self.backup:
                self.backup_file(file_path)
            sanitized_content = self.sanitize_text(content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sanitized_content)

        logging.info(f"Scan completed → {file_path}: {len(findings)} suspicious characters found.")
        return findings

    def scan_directory(self, directory_path, mode="all"):
        """
        Scan all files in a directory.
        Args:
            directory_path (str): Path to the directory to scan.
            mode (str): Scan mode: 'ascii', 'unicode', or 'all'.
        """
        if not os.path.isdir(directory_path):
            logging.error(f"Invalid directory: {directory_path}")
            return

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                findings = self.scan_file(file_path, mode)
                logging.info(f"📄 {file_path}: {len(findings)} suspicious characters found.")

# Enhanced CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suspicious character scanner (Unicode & ASCII)")
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("-m", "--mode", choices=["ascii", "unicode", "all"], default="all",
                        help="Scan mode: 'ascii' for ASCII, 'unicode' for Unicode, 'all' for both")
    parser.add_argument("-s", "--sanitize", action="store_true", help="Enable automatic sanitization")
    parser.add_argument("--no-backup", action="store_true", help="Sanitize WITHOUT backup")
    parser.add_argument("-l", "--log", default="scanner.log", help="Log file path")
    args = parser.parse_args()

    scanner = ByteSleuth(sanitize=args.sanitize, backup=not args.no_backup, log_file=args.log)

    if os.path.isdir(args.target):
        scanner.scan_directory(args.target, args.mode)
    elif os.path.isfile(args.target):
        findings = scanner.scan_file(args.target, args.mode)
        print(f"🔍 {args.target}: {len(findings)} suspicious characters found!")
    else:
        print("Error: Invalid path. Please provide an existing file or directory.")
        exit(1)

    logging.info("✅ Scan finished! Check the log for details.")
    print("\n✅ Scan finished! Check the log for details.")
    exit(0)

# Usage examples:
# python byte_sleuth.py /path/to/file.txt -m all -s --no-backup -l my_log.log
# python byte_sleuth.py /path/to/directory -m ascii
# python byte_sleuth.py /path/to/file.txt -m unicode
# python byte_sleuth.py /path/to/directory -m all -s
# python byte_sleuth.py /path/to/file.txt -m all --no-backup