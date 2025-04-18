from fastapi import FastAPI, HTTPException
from credential_vault import save, load
from config import get_config, update_config

app = FastAPI(title="OAuth & Config Service")

@app.post("/token/{provider}")
def store(provider: str, token: dict):
    save(provider, token)
    return {"status": "stored"}

@app.get("/token/{provider}")
def fetch(provider: str):
    tok = load(provider)
    if not tok:
        raise HTTPException(404, "Missing")
    return tok

@app.get("/config")
def read_cfg():
    return get_config()

@app.post("/config")
def write_cfg(cfg: dict):
    update_config(cfg)
    return {"status": "updated"} 