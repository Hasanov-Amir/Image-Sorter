const { dialog } = require('electron');
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('dialog', {
    openFolder: () => ipcRenderer.invoke('openFolder'),
})
