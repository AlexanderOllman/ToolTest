"""Dynamic runtime configuration for LLM & embedding models."""
from __future__ import annotations
import json, pathlib, os
from credential_vault import load, save

CONFIG_PATH = pathlib.Path.home() / ".agent_framework_config.json"
DEFAULTS = {
    "chat": {
        "model": "gpt-4o-mini",
        "base_url": "https://api.openai.com/v1",
        "api_key_ref": "openai"  # key stored in vault under this service name
    },
    "embed": {
        "model": "voyage-3-lite",
        "base_url": None,
        "api_key_ref": None
    },
    "endpoints": {
        "oauth_service": "http://localhost:9300",
        "task_executor": "http://localhost:8001",
        "mcp_servers_base": "http://localhost:8000"
    }
}

def _read() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    CONFIG_PATH.write_text(json.dumps(DEFAULTS, indent=2))
    return DEFAULTS.copy()

def get_config() -> dict:
    cfg = _read()
    for section in ("chat", "embed"):
        ref = cfg[section].get("api_key_ref")
        if ref and "api_key" not in cfg[section]:
            cred = load(ref)
            if cred:
                cfg[section]["api_key"] = cred["api_key"]
    
    # Ensure all sections exist
    for key in DEFAULTS:
        if key not in cfg:
            cfg[key] = DEFAULTS[key]
    
    return cfg

def update_config(new_cfg: dict):
    cfg = _read()
    # Deep merge to handle nested dicts
    for section, values in new_cfg.items():
        if section not in cfg:
            cfg[section] = {}
        if isinstance(values, dict):
            for k, v in values.items():
                cfg[section][k] = v
        else:
            cfg[section] = values
            
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
    return cfg 