import json, subprocess, sys, os, time, pathlib, git
from test_tool import smoke_test
from embed_ingest import ingest
from config import get_config

config = get_config()
endpoints = config["endpoints"]

REPO = sys.argv[1]
DEST = pathlib.Path("servers") / REPO.split("/")[-1]
print("Cloning", REPO)
git.Repo.clone_from(REPO, DEST, depth=1)
run_cmd = ["uv", "run", "--directory", str(DEST), f"server.py"]
proc = subprocess.Popen(run_cmd)
print("Starting server for health check…")
time.sleep(3)

# Extract host and port from config
mcp_url = endpoints["mcp_servers_base"]
mcp_host = mcp_url.replace("http://", "")

try:
    smoke_test(mcp_host)
except Exception as e:
    proc.terminate(); raise
with open("mcpo.json") as f:
    mcpo = json.load(f)
mcpo["mcpServers"][DEST.name] = {"command": "uv", "args": run_cmd[2:]}
json.dump(mcpo, open("mcpo.json", "w"), indent=2)
proc.terminate()
ingest()
print("✓ added", DEST.name) 