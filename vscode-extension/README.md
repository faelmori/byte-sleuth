# ByteSleuth VSCode Extension

This is a VSCode extension that adds a command to scan the currently open file for hidden or suspicious characters using the ByteSleuth Python package.

## Structure

```
vscode-extension/
  |- package.json
  |- extension.js
  |- README.md
```

---

## package.json (excerpt)

```
{
  "name": "bytesleuth-vscode",
  "displayName": "ByteSleuth Scanner",
  "description": "Scan open files for hidden/suspicious characters using ByteSleuth.",
  "version": "0.0.1",
  "engines": { "vscode": ">=1.60.0" },
  "activationEvents": [
    "onCommand:bytesleuth.scanCurrentFile"
  ],
  "main": "extension.js",
  "contributes": {
    "commands": [
      {
        "command": "bytesleuth.scanCurrentFile",
        "title": "ByteSleuth: Scan Current File"
      }
    ]
  },
  "categories": ["Other"]
}
```

---

## extension.js (excerpt)

```js
const vscode = require('vscode');
const cp = require('child_process');

function activate(context) {
    let disposable = vscode.commands.registerCommand('bytesleuth.scanCurrentFile', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file open to scan.');
            return;
        }
        const filePath = editor.document.fileName;
        // Adjust the Python/ByteSleuth path as needed
        const command = `python3 -m src.byte_sleuth "${filePath}"`;
        cp.exec(command, { cwd: vscode.workspace.rootPath }, (err, stdout, stderr) => {
            if (err) {
                vscode.window.showErrorMessage(stderr || err.message);
            } else {
                vscode.window.showInformationMessage(stdout || 'Scan complete.');
            }
        });
    });
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
```

---

## Usage
- Open a file in VSCode.
- Press `Ctrl+Shift+P` and search for `ByteSleuth: Scan Current File`.
- The result will be shown as a notification.
- **Tip:** You can customize the command in `extension.js` to use advanced flags, e.g. `-F` (fail on detect), `-s` (sanitize), or log removed characters.

### Example: Scan with fail-on-detect (exit code 1 if suspicious chars found)
```js
const command = `python3 byte_sleuth/byte_sleuth.py "${filePath}" -F`;
```

### Example: Log removed characters from PIPE
```bash
cat file.txt | python3 byte_sleuth/byte_sleuth.py -s -l removed_chars.log > sanitized.txt
```

---

## Automation & CI/CD
- Use the CLI with `-F` in pre-commit or CI to block code with hidden characters.
- The extension can be combined with automation for full coverage.

## Requirements
- Python 3 and ByteSleuth installed and available in your workspace.
- **The extension will automatically use the same Python interpreter selected in VSCode** (including virtualenv, conda, or workspace Python). This ensures compatibility with your project environment.
- Install ByteSleuth in the active Python environment:

```bash
pip install byte-sleuth
```

---
## How to use in your repository
- Place the `vscode-extension` folder at the root of your project.
- In VSCode, open the folder and run `npm install`.
- Press F5 to test the extension in development mode.
- To publish, follow the official [VSCode Marketplace guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension).

---

## Comparison with other tools

| Tool           | Unicode | ASCII Control | Sanitization | JSON Report | CLI/Automation | VSCode Integration |
|----------------|---------|--------------|--------------|-------------|----------------|-------------------|
| **ByteSleuth** |   ✔️    |      ✔️      |     ✔️       |     ✔️      |      ✔️        |        ✔️         |
| grep/sed       |   ❌    |      ✔️      |     ❌       |     ❌      |      ✔️        |        ❌         |
| ad-hoc scripts |   ❌    |      ✔️      |     ❌       |     ❌      |      ✔️        |        ❌         |

- **ByteSleuth** covers Unicode, ASCII, sanitizes, generates reports, and integrates easily with automation and VSCode.
- grep/sed are great for simple ASCII, but do not cover Unicode or sanitization.
- Ad-hoc scripts are fragile and hard to maintain.

---

> For questions or suggestions, open an issue in the main ByteSleuth repository!
