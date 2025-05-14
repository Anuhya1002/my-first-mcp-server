from mcp.server.fastmcp import FastMCP
from typing import List, Dict
import uuid

# Create the MCP server
mcp = FastMCP("ClickUpBugSolver")

# Simulated in-memory bug database
bugs: Dict[str, Dict] = {}

# Mock data for testing
def populate_mock_bugs():
    mock_bugs = [
        {
            "title": "Login button not working",
            "description": "When clicked, nothing happens. No API call seen in console.",
            "status": "open"
        },
        {
            "title": "404 on user profile page",
            "description": "Navigating to /user/123 gives a 404 even though the user exists.",
            "status": "open"
        },
                {
            "title": "Login button not working",
            "description": "When clicked, nothing happens. No API call seen in console.",
            "status": "open"
        },
        {
            "title": "404 on user profile page",
            "description": "Navigating to /user/123 gives a 404 even though the user exists.",
            "status": "open"
        },
    ]
    for bug in mock_bugs:
        bug_id = str(uuid.uuid4())
        bugs[bug_id] = {
            "id": bug_id,
            **bug
        }

# Call this to populate initial data
populate_mock_bugs()

# Add a bug report
@mcp.tool()
def report_bug(title: str, description: str) -> str:
    """Report a new bug"""
    bug_id = str(uuid.uuid4())
    bugs[bug_id] = {
        "id": bug_id,
        "title": title,
        "description": description,
        "status": "open"
    }
    return f"Bug reported with ID: {bug_id}"

# Get list of all open bugs
@mcp.resource("bugs://open")
def list_open_bugs() -> List[Dict]:
    """List all open bugs"""
    return [bug for bug in bugs.values() if bug["status"] == "open"]

# Get details of a specific bug by ID
@mcp.resource("bug://{bug_id}")
def get_bug_details(bug_id: str) -> Dict:
    """Get details of a bug"""
    return bugs.get(bug_id, {"error": "Bug not found"})

# Mark a bug as solved
@mcp.tool()
def resolve_bug(bug_id: str) -> str:
    """Resolve a bug by ID"""
    if bug_id in bugs:
        bugs[bug_id]["status"] = "resolved"
        return f"Bug {bug_id} marked as resolved"
    return "Bug ID not found"
