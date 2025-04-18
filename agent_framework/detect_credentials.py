import httpx, sys, json
from config import get_config

# Use config endpoint if no arg provided, otherwise use the provided endpoint
if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    # Extract host from config
    config = get_config()
    mcp_url = config["endpoints"]["mcp_servers_base"]
    host = mcp_url.replace("http://", "")

spec = httpx.get(f"http://{host}/docs").json()
print("🔒 requires auth" if spec.get("components", {}).get("securitySchemes") else "🆓 open") 