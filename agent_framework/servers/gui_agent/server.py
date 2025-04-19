from fast_agent_mcp import ToolServer, tool
import pyautogui as gui
import time

app = ToolServer(title="GUI agent")

@app.tool(params={"script": {"type": "string"}}, summary="Run GUI script")
def run(script: str):
    locals_ = {
        "click": gui.click,
        "key": gui.press,
        "hotkey": gui.hotkey,
        "write": gui.write,
        "wait": time.sleep
    }
    for line in script.splitlines():
        eval(line, {}, locals_)
    return "ok"
