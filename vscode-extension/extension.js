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
        const reportPath = 'bytesleuth_report.json';
        // Ajuste o caminho do Python/ByteSleuth conforme necessário
        const command = `python3 -m src.byte_sleuth "${filePath}" -v -r "${reportPath}"`;
        // Execute the command
        // Use the path to the Python interpreter and the ByteSleuth module
        cp.exec(command, (err, stdout, stderr) => {
            if (err && err.code !== 0) {
                vscode.window.showErrorMessage(stderr || err.message);
                return;
            }
            if (stderr) {
                vscode.window.showErrorMessage(stderr);
                return;
            }
            if (stdout) {
                vscode.window.showInformationMessage(stdout);
            }
            // Open the report file in a new editor tab
            vscode.workspace.openTextDocument(reportPath).then(doc => {
                vscode.window.showTextDocument(doc);
            }, err => {
                vscode.window.showErrorMessage('Failed to open report: ' + err.message);
            });
            // Remove the report file after opening
            cp.exec(`rm "${reportPath}"`, (err) => {
                if (err) {
                    console.error('Failed to remove report file:', err);
                }
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
