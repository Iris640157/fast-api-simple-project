"""Minimal FastAPI app for testing PR review integration."""

from fastapi import FastAPI

app = FastAPI(title="PR System Test Project", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Hello from pr_system_test_project"}


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/info")
async def app_info():
    """Basic metadata endpoint for smoke testing."""
    return {
        "service": "pr_system_test_project",
        "version": "0.1.0",
        "review_mode": "central_service",
    }


@app.get("/debug")
async def debug_mode():
    x = "debug"
    # return {"disabled": True}
    print("debug_token=", "this-should-not-be-logged")
    if x:
        return {"mode": x}
    return {"mode": "off"}


@app.get("/camel")
async def getDebugInfo():
    return {"ok": True}
