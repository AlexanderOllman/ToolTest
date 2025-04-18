#!/usr/bin/env python
"""
Setup script for Agent Framework
Initializes configuration and creates required directories
"""
import json, os, pathlib, shutil
from dotenv import load_dotenv
from config import CONFIG_PATH, DEFAULTS, update_config

def main():
    print("Setting up Agent Framework...")
    
    # Load environment variables from .env file if it exists
    env_file = pathlib.Path(".env")
    if not env_file.exists():
        if pathlib.Path(".env.example").exists():
            print("Creating .env file from example...")
            shutil.copy(".env.example", ".env")
        else:
            print("No .env file found, creating empty one...")
            env_file.write_text("")
    
    load_dotenv()
    
    # Create config with environment variables
    config = DEFAULTS.copy()
    
    # Update endpoints from environment if set
    if os.getenv("OAUTH_SERVICE_PORT"):
        config["endpoints"]["oauth_service"] = f"http://localhost:{os.getenv('OAUTH_SERVICE_PORT')}"
    if os.getenv("TASK_EXECUTOR_PORT"):
        config["endpoints"]["task_executor"] = f"http://localhost:{os.getenv('TASK_EXECUTOR_PORT')}"
    if os.getenv("MCP_SERVERS_PORT"):
        config["endpoints"]["mcp_servers_base"] = f"http://localhost:{os.getenv('MCP_SERVERS_PORT')}"
    
    # Use API keys from environment if available
    if os.getenv("OPENAI_API_KEY"):
        config["chat"]["api_key"] = os.getenv("OPENAI_API_KEY")
        # Don't reference vault if we're using env var
        config["chat"]["api_key_ref"] = None
    
    if os.getenv("VOYAGEAI_API_KEY"):
        config["embed"]["api_key"] = os.getenv("VOYAGEAI_API_KEY")
        config["embed"]["api_key_ref"] = None
    
    # Create data directories
    data_dir = pathlib.Path("data/faiss_index")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Update config file
    update_config(config)
    print(f"Configuration saved to {CONFIG_PATH}")
    
    print("Setup complete! You can now start the application.")

if __name__ == "__main__":
    main() 