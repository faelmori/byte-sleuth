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
        // Ajuste o caminho do Python/ByteSleuth conforme necessário
        const command = `python3 -m src.byte_sleuth "${filePath}" -v`;
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
