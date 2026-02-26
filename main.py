from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_skip_header(request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.get("/execute")
def execute(q: str = Query(None)):
    
    if q is None:
        return JSONResponse(
            content={"message": "Ready. Use ?q=your question"},
            headers={"ngrok-skip-browser-warning": "true"}
        )

    match = re.search(r'ticket\s+(\d+)', q, re.IGNORECASE)
    if match:
        return JSONResponse(
            content={"name": "get_ticket_status", "arguments": json.dumps({"ticket_id": int(match.group(1))})},
            headers={"ngrok-skip-browser-warning": "true"}
        )

    match = re.search(r'meeting\s+on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(Room\s+\S+)', q, re.IGNORECASE)
    if match:
        return JSONResponse(
            content={"name": "schedule_meeting", "arguments": json.dumps({"date": match.group(1), "time": match.group(2), "meeting_room": match.group(3).rstrip('.')})},
            headers={"ngrok-skip-browser-warning": "true"}
        )

    match = re.search(r'expense\s+balance\s+for\s+employee\s+(\d+)', q, re.IGNORECASE)
    if match:
        return JSONResponse(
            content={"name": "get_expense_balance", "arguments": json.dumps({"employee_id": int(match.group(1))})},
            headers={"ngrok-skip-browser-warning": "true"}
        )

    match = re.search(r'performance\s+bonus\s+for\s+employee\s+(\d+)\s+for\s+(\d{4})', q, re.IGNORECASE)
    if match:
        return JSONResponse(
            content={"name": "calculate_performance_bonus", "arguments": json.dumps({"employee_id": int(match.group(1)), "current_year": int(match.group(2))})},
            headers={"ngrok-skip-browser-warning": "true"}
        )

    match = re.search(r'office\s+issue\s+(\d+)\s+for\s+(?:the\s+)?(\w+)\s+department', q, re.IGNORECASE)
    if match:
        return JSONResponse(
            content={"name": "report_office_issue", "arguments": json.dumps({"issue_code": int(match.group(1)), "department": match.group(2)})},
            headers={"ngrok-skip-browser-warning": "true"}
        )

    return JSONResponse(
        content={"error": "Query not recognized"},
        headers={"ngrok-skip-browser-warning": "true"}
    )
