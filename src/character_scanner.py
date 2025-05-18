import os
import unicodedata
import argparse
import logging

class CharacterScanner:
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

    def __init__(self, sanitize=False, log_file="scanner.log"):
        """Inicializa o scanner com opção de sanitização automática e logging."""
        self.sanitize = sanitize
        logging.basicConfig(
            filename=log_file, filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

    def detect_ascii_chars(self, text):
        """Detecta caracteres ASCII de controle."""
        findings = []
        for char in text:
            cp = ord(char)
            if cp in self.ASCII_CONTROL_NAMES:
                findings.append((cp, self.ASCII_CONTROL_NAMES[cp], char))
        logging.info(f"Detectados {len(findings)} caracteres ASCII suspeitos.")
        return findings

    def detect_unicode_chars(self, text):
        """Detecta caracteres Unicode suspeitos."""
        findings = []
        for char in text:
            cp = ord(char)
            if cp in self.UNICODE_SUSPICIOUS_CODEPOINTS:
                name = unicodedata.name(char, "UNKNOWN CHARACTER")
                findings.append((cp, name, char))
        logging.info(f"Detectados {len(findings)} caracteres Unicode suspeitos.")
        return findings

    def detect_all_chars(self, text):
        """Detecta ASCII e Unicode na mesma execução."""
        findings = self.detect_ascii_chars(text) + self.detect_unicode_chars(text)
        logging.info(f"Total de {len(findings)} caracteres suspeitos detectados.")
        return findings

    def scan_file(self, file_path, mode="all"):
        """Escaneia um arquivo e registra os caracteres suspeitos encontrados."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Erro ao ler arquivo {file_path}: {e}")
            return []

        if mode == "ascii":
            findings = self.detect_ascii_chars(content)
        elif mode == "unicode":
            findings = self.detect_unicode_chars(content)
        else:
            findings = self.detect_all_chars(content)

        if self.sanitize:
            content = self.sanitize_text(content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Sanitização aplicada em {file_path}")

        return findings

    def sanitize_text(self, text):
        """Remove caracteres suspeitos."""
        sanitized_text = ''.join(char for char in text if ord(char) not in self.ASCII_CONTROL_NAMES and ord(char) not in self.UNICODE_SUSPICIOUS_CODEPOINTS)
        logging.info("Sanitização concluída.")
        return sanitized_text

    def scan_directory(self, directory_path, mode="all"):
        """Escaneia todos os arquivos dentro de um diretório."""
        if not os.path.isdir(directory_path):
            logging.error(f"Diretório inválido: {directory_path}")
            return

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                findings = self.scan_file(file_path, mode)
                logging.info(f"🔍 {file_path}: {len(findings)} caracteres suspeitos encontrados.")

# CLI aprimorada
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner de caracteres suspeitos (Unicode & ASCII)")
    parser.add_argument("target", help="Arquivo ou diretório a ser escaneado")
    parser.add_argument("-m", "--mode", choices=["ascii", "unicode", "all"], default="all",
                        help="Modo de varredura: 'ascii' para ASCII, 'unicode' para Unicode, 'all' para ambos")
    parser.add_argument("-s", "--sanitize", action="store_true", help="Ativar correção automática")
    parser.add_argument("-l", "--log", default="scanner.log", help="Arquivo de log")
    args = parser.parse_args()

    scanner = CharacterScanner(sanitize=args.sanitize, log_file=args.log)

    if os.path.isdir(args.target):
        scanner.scan_directory(args.target, args.mode)
    elif os.path.isfile(args.target):
        findings = scanner.scan_file(args.target, args.mode)
        print(f"🔍 {args.target}: {len(findings)} caracteres suspeitos encontrados!")
    else:
        print("Erro: Caminho inválido. Forneça um arquivo ou diretório existente.")
        exit(1)

    print("Escaneamento concluído.")
    logging.info("Escaneamento concluído.")
    print("Verifique o arquivo de log para detalhes.")
    logging.info("Verifique o arquivo de log para detalhes.")
    exit(0)
# Fim do código