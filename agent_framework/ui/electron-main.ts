import { app, BrowserWindow, ipcMain } from "electron";
import Store from "electron-store";

const store = new Store();

function createWindow() {
  const win = new BrowserWindow({
    width: 900,
    height: 700,
    webPreferences: { nodeIntegration: true, contextIsolation: false }
  });
  win.loadURL("http://localhost:3000");
}

app.whenReady().then(createWindow);

ipcMain.handle("get-config", () => store.get("config") || {});
ipcMain.handle("set-config", (_e, cfg) => {
  store.set("config", cfg);
}); 