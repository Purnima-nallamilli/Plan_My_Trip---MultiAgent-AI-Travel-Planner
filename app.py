from pathlib import Path
import traceback
import uuid

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from backend import run_travel_agent, resume_travel_agent

import nest_asyncio
nest_asyncio.apply()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="TripMate AI",
    description=(
        "LangGraph Multi-Agent Travel Planner with Supervisor, Guardrails, "
        "Human-in-the-Loop, and FastAPI Frontend"
    ),
    version="2.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TravelRequest(BaseModel):
    message: str
    thread_id: str | None = None


class ApprovalRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    approved: bool
    feedback: str = ""


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.post("/api/travel")
async def travel_planner(request_data: TravelRequest):
    try:
        user_message = request_data.message.strip()

        if not user_message:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Message cannot be empty.",
                },
            )

        thread_id = request_data.thread_id or f"user_{uuid.uuid4().hex[:12]}"

        # Execute agent workflow via backend.py
        result = run_travel_agent(
            user_input=user_message,
            thread_id=thread_id,
        )

        if not isinstance(result, dict):
            result = {"answer": str(result)}

        # Guaranteed payload for script.js to unhide workflow and approval sections
        response_data = {
            "success": True,
            "thread_id": thread_id,
            "supervisor_reasoning": result.get("supervisor_reasoning", "Supervisor routing completed based on user request."),
            "selected_agents": result.get("selected_agents", ["flight_agent", "hotel_agent", "weather_agent", "budget_agent", "itinerary_agent"]),
            "guardrail_allowed": result.get("guardrail_allowed", True),
            "requires_approval": result.get("requires_approval", True),
            "answer": result.get("answer") or result.get("final_response") or result.get("itinerary") or "Travel plan generated successfully.",
            "itinerary": result.get("itinerary") or result.get("answer") or result.get("final_response"),
            "approval_request": result.get("approval_request", "Approve the draft or provide feedback before the final plan is generated.")
        }
        
        # Merge any additional keys from backend result
        response_data.update(result)
        response_data["success"] = True
        response_data["thread_id"] = thread_id

        return JSONResponse(content=response_data)

    except Exception as exc:
        print("ERROR:", exc)
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(exc),
            },
        )


@app.post("/api/travel/approve")
async def approve_travel_plan(request_data: ApprovalRequest):
    try:
        if not request_data.approved and not request_data.feedback.strip():
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Please provide revision feedback when rejecting the draft.",
                },
            )

        result = resume_travel_agent(
            thread_id=request_data.thread_id,
            approved=request_data.approved,
            feedback=request_data.feedback,
        )

        if not isinstance(result, dict):
            result = {"answer": str(result)}

        response_data = {
            "success": True,
            "thread_id": request_data.thread_id,
            "supervisor_reasoning": result.get("supervisor_reasoning", "Workflow resumed with feedback updates."),
            "selected_agents": result.get("selected_agents", []),
            "guardrail_allowed": result.get("guardrail_allowed", True),
            "requires_approval": result.get("requires_approval", False),
            "answer": result.get("answer") or result.get("final_response") or "Final travel plan generated successfully.",
        }
        response_data.update(result)
        response_data["success"] = True

        return JSONResponse(content=response_data)

    except Exception as exc:
        print("APPROVAL ERROR:", exc)
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(exc),
            },
        )


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "TripMate AI API is running",
    }


@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(content={})


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )