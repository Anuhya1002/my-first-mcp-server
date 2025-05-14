from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
import uuid

app = FastAPI()
bugs: Dict[str, Dict] = {}

class BugReport(BaseModel):
    title: str
    description: str

class ResolveBugRequest(BaseModel):
    bug_id: str

@app.post("/report-bug")
def report_bug(data: BugReport) -> Dict:
    bug_id = str(uuid.uuid4())
    bugs[bug_id] = {
        "id": bug_id,
        "title": data.title,
        "description": data.description,
        "status": "open"
    }
    return {"message": "Bug reported", "id": bug_id}

@app.get("/bugs/open")
def list_open_bugs() -> List[Dict]:
    return [bug for bug in bugs.values() if bug["status"] == "open"]

@app.get("/bug/{bug_id}")
def get_bug(bug_id: str) -> Dict:
    return bugs.get(bug_id, {"error": "Bug not found"})

@app.post("/resolve-bug")
def resolve_bug(data: ResolveBugRequest) -> Dict:
    if data.bug_id in bugs:
        bugs[data.bug_id]["status"] = "resolved"
        return {"message": f"Bug {data.bug_id} resolved"}
    return {"error": "Bug ID not found"}
