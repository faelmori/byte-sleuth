const vscode = require('vscode');
const cp = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

async function getPythonPath() {
    // Tenta pegar o Python do VSCode (settings ou extensão Python)
    // 1. VSCode Python extension (>=2021): usa API se disponível
    // 2. Fallback: settings.json (python.pythonPath)
    // 3. Fallback: 'python3'
    try {
        // VSCode Python extension API
        const pythonExt = vscode.extensions.getExtension('ms-python.python');
        if (pythonExt) {
            if (!pythonExt.isActive) {
                await pythonExt.activate();
            }
            if (pythonExt.exports && pythonExt.exports.settings) {
                const execCommand = pythonExt.exports.settings.getExecutionDetails().execCommand;
                if (execCommand && execCommand.length > 0) {
                    return execCommand.join(' ');
                }
            }
        }
    } catch (e) {
        // ignore
    }
    // VSCode user/workspace settings
    const config = vscode.workspace.getConfiguration('python');
    const pythonPath = config.get('pythonPath');
    if (pythonPath) {
        return pythonPath;
    }
    // Fallback
    return 'python3';
}

function activate(context) {
    let disposable = vscode.commands.registerCommand('bytesleuth.scanCurrentFile', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file open to scan.');
            return;
        }
        const filePath = editor.document.fileName;
        const tmpDir = os.tmpdir();
        const reportPath = path.join(tmpDir, `bytesleuth_report_${Date.now()}.json`);
        const pythonCmd = await getPythonPath();
        const command = `${pythonCmd} -m byte_sleuth "${filePath}" -v -r "${reportPath}"`;
        const outputChannel = vscode.window.createOutputChannel('ByteSleuth');
        outputChannel.clear();
        outputChannel.show(true);
        outputChannel.appendLine(`Running: ${command}`);
        cp.exec(command, (err, stdout, stderr) => {
            if (stderr) {
                outputChannel.appendLine('[stderr] ' + stderr);
            }
            if (stdout) {
                outputChannel.appendLine('[stdout] ' + stdout);
            }
            if (err && err.code !== 0) {
                outputChannel.appendLine(`[ERROR] ${err.message}`);
                vscode.window.showErrorMessage('ByteSleuth scan failed. See Output for details.');
            }
            fs.readFile(reportPath, 'utf8', (readErr, data) => {
                if (readErr) {
                    outputChannel.appendLine(`[ERROR] Failed to read report: ${readErr.message}`);
                    vscode.window.showErrorMessage('Failed to read ByteSleuth report.');
                } else {
                    outputChannel.appendLine('\n=== ByteSleuth Report ===\n');
                    outputChannel.appendLine(data);
                    outputChannel.appendLine('\n=========================');
                }
                fs.unlink(reportPath, (rmErr) => {
                    if (rmErr) {
                        outputChannel.appendLine(`[WARN] Failed to remove temp report: ${rmErr.message}`);
                    }
                });
            });
        });
    });
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
