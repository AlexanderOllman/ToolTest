from fastmcp import MCPServer, tool
import pyautogui as gui, time

app = MCPServer(title="GUI agent")

@app.tool(params={"script": {"type": "string"}}, summary="Run GUI script")
def run(script: str):
    locals_ = {"click": gui.click, "key": gui.press, "hotkey": gui.hotkey,
               "write": gui.write, "wait": time.sleep}
    for line in script.splitlines():
        eval(line, {}, locals_)
    return "ok" 