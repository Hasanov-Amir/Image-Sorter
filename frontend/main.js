const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const path = require('node:path');

const createWindow = () => {
    const win = new BrowserWindow({
        width: 1600,
        height: 900,
        // frame: false,
        // titleBarStyle: 'hidden',
        autoHideMenuBar: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            nodeIntegration: false,
            devTools: true
        }
    });
    win.loadFile('index.html');
};

const getPath = () => {
    return dialog.showOpenDialogSync({properties: ['openDirectory']})
}

app.whenReady().then(() => {
    ipcMain.handle('openFolder', () => getPath())
    createWindow();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
