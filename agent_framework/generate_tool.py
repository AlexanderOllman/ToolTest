import openai, pathlib, subprocess, sys, uuid
from config import get_config

cfg = get_config()["chat"]
client = openai.OpenAI(api_key=cfg.get("api_key"), base_url=cfg.get("base_url"))

prompt = f"Generate a FastMCP server exposing a tool that can: {sys.argv[1]}"". Return only code."
code = client.chat.completions.create(model=cfg["model"], messages=[{"role": "user", "content": prompt}]).choices[0].message.content.strip("```python\n").strip("```")
name = f"tool_{uuid.uuid4().hex[:6]}"
root = pathlib.Path("servers") / name
root.mkdir(parents=True)
(root/"server.py").write_text(code)
subprocess.check_call(["python", "add_mcp_server.py", str(root)])
print("Added", name) 