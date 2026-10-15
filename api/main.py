from fastapi import FastAPI, HTTPException, UploadFile
from src.registry import ContractRegistry
from src.validator import ContractValidator
from src.breaking import detect_breaking_changes
import pandas as pd
import io

app = FastAPI(title="Data Contracts API")
registry = ContractRegistry()

@app.get("/contracts")
def list_contracts():
    return [c.to_dict() for c in registry.all()]

@app.get("/contracts/{name}")
def get_contract(name: str):
    c = registry.get(name)
    if not c:
        raise HTTPException(404, "Contract not found")
    return c.to_dict()

@app.post("/contracts/{name}/validate")
async def validate(name: str, file: UploadFile):
    c = registry.get(name)
    if not c:
        raise HTTPException(404, "Contract not found")
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    return ContractValidator(c).validate(df)

@app.post("/contracts/{old_name}/diff")
def diff(old_name: str, new_name: str):
    old = registry.get(old_name)
    new = registry.get(new_name)
    if not old or not new:
        raise HTTPException(404, "Contract not found")
    return detect_breaking_changes(old, new)
