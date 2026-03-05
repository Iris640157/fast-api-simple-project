"""Minimal FastAPI app for testing PR review integration."""

from fastapi import FastAPI

app = FastAPI(title="PR System Test Project", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Hello from pr_system_test_project"}


@app.get("/health")
async def health():
    return {"status": "ok"}
