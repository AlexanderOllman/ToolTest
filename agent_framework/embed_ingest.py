import json, os, httpx, faiss, numpy as np
from config import get_config
from tqdm import tqdm

cfg = get_config()["embed"]

if cfg["model"] == "voyage-3-lite":
    from voyageai import Client as EmbedClient
    eclient = EmbedClient()
    def embed(texts):
        return eclient.embed(texts, model="voyage-3-lite").embeddings
else:
    from openai import OpenAI
    eclient = OpenAI(api_key=cfg.get("api_key"), base_url=cfg.get("base_url"))
    model_name = cfg["model"]
    def embed(texts):
        return [eclient.embeddings.create(model=model_name, input=t).data[0].embedding for t in texts]

INDEX_DIR = "data/faiss_index"
DIM = 2048
index = faiss.IndexFlatL2(DIM)

def ingest():
    mcpo = json.load(open("mcpo.json"))
    payloads, embeds = [], []
    for name, cfg in mcpo["mcpServers"].items():
        host = cfg.get("hostname", "localhost:8000")
        spec = httpx.get(f"http://{host}/docs").json()
        for path, ops in spec["paths"].items():
            for m, meta in ops.items():
                text = f"{m.upper()} {path} {meta.get('summary','')}"[:4096]
                embeds.append(embed([text])[0])
                payloads.append({"tool": name, "text": text})
    vecs = np.array(embeds).astype("float32")
    index.add(vecs)
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, f"{INDEX_DIR}/tools.faiss")
    json.dump(payloads, open(f"{INDEX_DIR}/payloads.json", "w"))

if __name__ == "__main__":
    ingest() 