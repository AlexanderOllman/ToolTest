from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
import json, os
from config import get_config

cfg = get_config()["chat"]
client = OpenAI(api_key=cfg.get("api_key"), base_url=cfg.get("base_url"))
MODEL = cfg["model"]

class Task(BaseModel):
    id: int
    description: str
    tool_hint: str | None = None
    params: dict = Field(default_factory=dict)

class Plan(BaseModel):
    tasks: list[Task]

def plan(query: str) -> Plan:
    system = "You are a planner that ONLY returns JSON matching the Plan schema."
    function = {"name": "return_plan", "parameters": Plan.model_json_schema()}
    chat = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": query}],
        functions=[function],
        function_call={"name": "return_plan"}
    )
    try:
        return Plan.model_validate(json.loads(chat.choices[0].message.function_call.arguments))
    except ValidationError as e:
        raise RuntimeError(f"Planner invalid JSON: {e}") 