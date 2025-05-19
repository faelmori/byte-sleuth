![ByteSleuth_Banner](docs/assets/top_banner_a.png)

# 🕵️‍♂️ **ByteSleuth** — The Ghost Hunter for Hidden Characters  

> "Elementary, my dear dev. The ghosts of hidden characters won't escape this audit!"  
> — **CharlockHolmes**, the detective inside ByteSleuth  

ByteSleuth is a **powerful Unicode & ASCII character scanner** designed to detect obfuscation, invisible threats, and suspicious bytes lurking in text or code. Whether you're hunting down **ghost characters** or analyzing **unexpected encoding issues**, ByteSleuth ensures a **clean and transparent result**.

---

## 🚀 **Key Features**
✅ Detects **ASCII control characters** (e.g., `NUL`, `BEL`, `ESC`)  
✅ Flags **Unicode invisibles** and **directional controls** (e.g., `U+200B`, `U+202E`)  
✅ Optionally **sanitizes** input by removing hidden/malicious characters  
✅ Works seamlessly with **files** and **directories**  
✅ Supports **logging** for audit trails  
✅ Can be **embedded in existing workflows**  

---

## 🔧 **CLI Usage**

```bash
python byte_sleuth.py <target> [-m MODE] [-s] [-l LOG_FILE]
```

### **CLI Arguments**
| Argument | Description |
|----------|------------|
| `target` | File or directory to scan |
| `-m`, `--mode` | Scan **only ASCII**, **only Unicode**, or **both** (`all`) |
| `-s`, `--sanitize` | Automatically **remove suspicious characters** |
| `-l`, `--log` | Log file to write results (default: `scanner.log`) |

### **CLI Example**
```bash
python byte_sleuth.py suspicious.txt -m all -s
```
> Scans `suspicious.txt` for **both ASCII & Unicode anomalies**, removes them, and logs results.

---

## 📦 **Using ByteSleuth in Your Python Projects**

Since **ByteSleuth** is modular, you can easily integrate it into any **existing application**.  

### **Installing ByteSleuth**
Once published to PyPI, you can install it via:  
```bash
pip install byte-sleuth
```

### **Basic Usage in Python**
```python
from byte_sleuth import CharacterScanner

scanner = CharacterScanner(sanitize=True)
findings = scanner.scan_file("example.txt", mode="all")

for cp, name, char in findings:
    print(f"⚠️ Suspicious Character: {name} (U+{cp:04X}) → {repr(char)}")
```
> This scans `"example.txt"` for hidden characters and removes them if needed.

---

## 🔁 **Embedding ByteSleuth in Workflows**
ByteSleuth can be **used beyond basic scans**, making it a perfect fit for **automation and security audits**:

- **🛠️ Pre-commit hook** — Block commits containing obfuscated characters.
- **🔍 CI/CD pipelines** — Ensure clean and readable source code before deployment.
- **📜 Log analysis** — Detect and clean malformed logs with invisible characters.

### **Example: Pre-commit Hook**
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: byte-sleuth-scan
      name: ByteSleuth Unicode & ASCII Scanner
      entry: python byte_sleuth.py src/ -m all -s
      language: system
      pass_filenames: false
```

---

## 🧠 **Why Use ByteSleuth?**
Some characters are **invisible but dangerous**—causing confusion in **source code, configs, or documents**.  
Common attack vectors include:

🔹 **Zero-width spaces** used for code obfuscation  
🔹 **Bidirectional override characters** affecting text visibility  
🔹 **Hidden ASCII control codes** that alter behavior unexpectedly  
🔹 **Formatting trickery** affecting debugging & diffs  

ByteSleuth gives you a **detective's magnifying glass** to **expose them all**. 🔍

---

## 🚀 **Roadmap**
✔️ **Expand sanitization methods**  
✔️ **Improve CLI interactivity**  
✔️ **Output JSON reports**  
🟡 **VSCode Extension** *(planned)*  
🟡 **Interactive CLI with `rich` or `curses` UI** *(planned)*  

---

## 🕵️‍♂️ **Honorary Agent: CharlockHolmes**
> When **Unicode hides**... he **seeks**.  
> When **ASCII misbehaves**... he **strikes**.  
> Because **no character escapes**... the **ByteSleuth**.  

---

## 📄 **License**
MIT — *Feel free to sleuth away!*
