from fast_agent_mcp import FastAgent, orchestrator
from planner_agent import plan
import faiss, json, numpy as np, subprocess, socketio, asyncio
from config import get_config

config = get_config()
endpoints = config["endpoints"]

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)  # mount in uvicorn alongside oauth_service if desired

index = faiss.read_index("data/faiss_index/tools.faiss")
payloads = json.load(open("data/faiss_index/payloads.json"))

EMBED_DIM = 2048

embed_cfg = config["embed"]
if embed_cfg["model"] == "voyage-3-lite":
    from voyageai import Client as EClient
    eclient = EClient()
    def embed_one(text):
        return np.array(eclient.embed([text], model="voyage-3-lite").embeddings[0]).astype("float32")
else:
    from openai import OpenAI
    oclient = OpenAI(api_key=embed_cfg.get("api_key"), base_url=embed_cfg.get("base_url"))
    model_name = embed_cfg["model"]
    def embed_one(text):
        return np.array(oclient.embeddings.create(model=model_name, input=text).data[0].embedding).astype("float32")

def find_tool(desc: str):
    v = embed_one(desc)
    D, I = index.search(np.array([v]), 1)
    if D[0][0] < 1e6:  # arbitrary threshold
        return payloads[I[0][0]]["tool"]
    return None

def llm_generate_gui_script(desc: str) -> str:
    from openai import OpenAI
    cfg = config["chat"]
    c = OpenAI(api_key=cfg.get("api_key"), base_url=cfg.get("base_url"))
    prompt = f"Convert this instruction into PyAutoGUI pseudo-script, minimal lines: {desc}"
    resp = c.chat.completions.create(model=cfg["model"], messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content.strip()

@orchestrator(name="backend_executor")
async def run_query(query: str):
    p = plan(query)
    for t in p.tasks:
        await sio.emit("task_event", {"taskId": t.id, "status": "start", "message": t.description})
        tool = find_tool(t.description)
        if not tool:
            tool = "gui-agent"
            t.params = {"script": llm_generate_gui_script(t.description)}
        
        # Use the base URL from config
        mcp_base_url = endpoints["mcp_servers_base"]
        agent = FastAgent(name=tool, endpoint=f"{mcp_base_url}/{tool}")
        
        try:
            res = agent(**t.params)
            await sio.emit("task_event", {"taskId": t.id, "status": "done", "message": str(res)})
        except Exception as e:
            await sio.emit("task_event", {"taskId": t.id, "status": "error", "message": str(e)}) 