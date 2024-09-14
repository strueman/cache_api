from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import secrets
import configparser
import os

app = FastAPI()
cache: Dict[str, Dict[str, Any]] = {}

# Load or generate API key
config = configparser.ConfigParser()
config_file = 'settings.cfg'

if os.path.exists(config_file):
    config.read(config_file)
    API_KEY = config.get('cache_api', 'API_KEY', fallback=None)
    
if not API_KEY:
    API_KEY = secrets.token_urlsafe(32)
    config['Security'] = {'API_KEY': API_KEY}
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print(f"New API Key generated and saved to {config_file}")

print(f"API Key: {API_KEY}")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

class Variable(BaseModel):
    process: str
    name: str
    value: Any

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate credentials")

@app.post("/set")
def set_variable(variable: Variable, api_key: str = Depends(get_api_key)):
    if variable.process not in cache:
        cache[variable.process] = {}
    cache[variable.process][variable.name] = variable.value
    return {"success": True}

@app.get("/get/{process}/{name}")
def get_variable(process: str, name: str, api_key: str = Depends(get_api_key)):
    if process not in cache or name not in cache[process]:
        raise HTTPException(status_code=404, detail="Variable not found")
    return {"process": process, "name": name, "value": cache[process][name]}

@app.get("/list/{process}")
def list_variables(process: str, api_key: str = Depends(get_api_key)):
    if process not in cache:
        return {"process": process, "variables": []}
    return {"process": process, "variables": list(cache[process].keys())}

@app.delete("/clear/{process}")
def clear_process(process: str, api_key: str = Depends(get_api_key)):
    if process in cache:
        cache[process].clear()
        return {"success": True, "message": f"All variables for process '{process}' have been cleared"}
    return {"success": False, "message": f"Process '{process}' not found"}

@app.delete("/clear_all")
def clear_all(api_key: str = Depends(get_api_key)):
    cache.clear()
    return {"success": True, "message": "All variables across all processes have been cleared"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
